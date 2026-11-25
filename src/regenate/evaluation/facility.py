"""Run 4 WP-G/I/J — test cell(s) inside a measured facility load (DS07) and monthly billed demand.
  python -m regenate.evaluation.facility --proc /content/ds05_proc --ds07 /content/ds07_raw/Data_list.zip \
      --runs /content/ai_runs/run3/v2_diag /content/ai_runs/run3/v2_e1_peak --facilities Forge_2 --months 2019-03 --out OUT
Counterfactual (D013/D015): DS07 is measured WHOLE-facility load; a simulated DS06 cell is ADDED behind the same meter
(P_meter = P_facility + P_cell_net, export of the cell nets 1:1 against facility load). DS07 and DS06 are not synchronised.
Monthly workload: consecutive non-overlapping blocks of `block_h`, each block = one held-out DS06 instance drawn with a fixed seed
(same draw for every method); cell traces of energy-only methods come from saved schedules; billing-aware methods re-solve each
block with the facility background of that block (ORACLE-BILL: true cycles + true background, one-shot).
Billed demand: max over aligned `interval_min` windows of the mean meter power; a window counts only with >= 80 % minute coverage.
"""
import argparse, io, json, re, zipfile
from pathlib import Path
import numpy as np
import pandas as pd

SLOT_MIN = 15
TOPO = {"B0": "B0", "B1": "B1", "B1-OPT": "B1", "B1p": "B1p", "B1p-OPT": "B1p"}   # others: shared DC


def topo_of(method):
    return TOPO.get(method.split("@")[0], "DC")


def load_ds07(zip_path, name):
    """1-min facility kW on a complete minute grid (missing rows -> NaN, never interpolated)."""
    with zipfile.ZipFile(zip_path) as z:
        d = pd.read_csv(io.BytesIO(z.read(f"Data_list/Factories/{name}.csv")))
    t = pd.to_datetime(d.iloc[:, 0], format="%Y-%m-%d %H:%M"); v = pd.to_numeric(d.iloc[:, 1], errors="coerce")
    s = pd.Series(v.values, index=t).groupby(level=0).mean()
    return s.reindex(pd.date_range(s.index.min().floor("D"), s.index.max().ceil("D") - pd.Timedelta(minutes=1), freq="min"))


def billed_demand(p_1min, interval_min=30, min_cov=0.8, md_window=None):
    """(kW, window start) max aligned-window mean; windows with < min_cov valid minutes are excluded.
    md_window = (weekdays, h0, h1): only intervals starting on those weekdays (0=Mon) within [h0, h1) h count, e.g. TNB RP4 MV:
    'Maximum Demand which occurs during Off-Peak period will not be charged', peak = Mon-Fri 14:00-22:00 (mytnb.com.my/tariff)."""
    g = p_1min.groupby(p_1min.index.floor(f"{interval_min}min"))
    m, c = g.mean(), g.count() / interval_min
    m = m[c >= min_cov]
    if md_window is not None:
        m = m[window_mask(m.index, md_window)]
    return (float(m.max()), m.idxmax()) if len(m) else (np.nan, None)


def cell_net_slots(inst, sch, prm, topo="DC"):
    """Per-slot cell AC net power (import - export, kW) from a saved schedule, TRUE traces, same ledger as the campaigns."""
    from regenate.data.bench_v2 import render_traces
    from regenate.electrical.ledger import ledger
    assign = dict(zip(sch.job_id.astype(int), sch.station.astype(int)))
    starts = dict(zip(sch.job_id.astype(int), sch.start_h.astype(float)))
    L = ledger(*render_traces(inst, assign, starts, inst["dt_h"], truth=True), inst["dt_h"], topo, prm)
    return L["p_import"] - L["p_export"]


def to_minutes(slots, slot_min=SLOT_MIN):
    return np.repeat(np.asarray(slots, float), slot_min)


def month_blocks(month, block_h):
    t0 = pd.Timestamp(month + "-01"); t1 = t0 + pd.offsets.MonthBegin(1)
    n = int((t1 - t0) / pd.Timedelta(hours=block_h))
    return [t0 + pd.Timedelta(hours=block_h * i) for i in range(n)]


def draw_instances(ids, n, seed):
    return list(np.random.default_rng(seed).choice(sorted(ids), size=n, replace=True))


def place(blocks, traces_min, index):
    """Sum block traces (1-min arrays starting at each block start) onto a minute index; raises on overlap of a block with the next."""
    out = pd.Series(0.0, index=index)
    for t, tr in zip(blocks, traces_min):
        i = index.get_indexer([t])[0]
        if i < 0:
            continue
        out.iloc[i:i + len(tr)] += tr[:max(0, len(index) - i)]
    return out


def solve_bill_block(inst, bg_slots, prm, time_limit=10.0, interval_slots=2, floor=0.0, e_tol=1e-4):
    """ORACLE-BILL for one block: one-shot DC MILP on TRUE profiles, lexicographic TT -> energy -> billed demand of (bg + cell)."""
    from regenate.evaluation.v2_campaign import milp_jobs
    from regenate.data.bench_v2 import fifo
    from regenate.optimization.milp import solve, assign_stations
    from regenate.evaluation.oracle_campaign import execute
    sl = inst["dt_h"]; S = len(inst["stations"]); _, fs = fifo(inst)
    jobs = milp_jobs(inst, "truth", 0.25, fs, sl)
    K = max(j.latest + j.dur for j in jobs) + 1
    bg = np.r_[bg_slots, np.zeros(max(0, K - len(bg_slots)))][:K]
    res = solve(jobs, S, K, "DC", prm, sl, time_limit=time_limit, peak_stage=True, peak_bg=np.nan_to_num(bg),
                peak_floor=floor, peak_avg_slots=interval_slots, e_tol=e_tol)
    if not res.starts:
        return None
    ids = list(inst["jobs"].job_id); stn = assign_stations(res.starts, [j.dur for j in jobs], S)
    assign = dict(zip(ids, stn)); starts = execute(inst, assign, {i: t * sl for i, t in zip(ids, res.starts)})
    return pd.DataFrame(dict(job_id=list(starts), station=[assign[j] for j in starts], start_h=[starts[j] for j in starts]))


_AI = dict(pred=None, factory=None)     # learned facility-load predictor (forecasting/facility_load.py), set in main()


def bg_forecast(bg15, t, n, kind):
    """Causal background forecast (kW per 15-min slot) for n slots from time t, using only data before t.
    oracle = true future (headroom only); persist = last valid slot; hist = mean of the same weekday/time over the previous 4 weeks."""
    idx = pd.date_range(t, periods=n, freq=f"{SLOT_MIN}min")
    if kind == "oracle":
        return bg15.reindex(idx).values
    past = bg15[:t - pd.Timedelta(minutes=1)].dropna()
    if kind == "persist":
        return np.full(n, past.iloc[-1] if len(past) else np.nan)
    if kind == "ai":                                   # learned forecaster for the first 60 slots, 'hist' beyond its horizon
        f = bg_forecast(bg15, t, n, "hist")
        m = min(n, 60); f[:m] = _AI["pred"].predict(_AI["factory"], t, m)
        return f
    if kind == "hist":
        lags = [bg15.reindex(idx - pd.Timedelta(weeks=w)).values for w in (1, 2, 3, 4)]
        f = np.nanmean(np.vstack(lags), axis=0) if len(lags) else np.full(n, np.nan)
        return np.where(np.isnan(f), past.iloc[-1] if len(past) else 0.0, f)
    raise ValueError(kind)


def window_mask(index, mdw):
    if mdw is None:
        return np.ones(len(index), bool)
    hr = index.hour + index.minute / 60
    mask = index.weekday.isin(mdw[0]) & (hr >= mdw[1]) & (hr < mdw[2])
    if len(mdw) > 3:
        mask &= ~np.isin(index.date, list(mdw[3]))
    return np.asarray(mask)


def run_p0bill_block(inst, prm, bg15, t_block, kind, floor, mdw, interval_slots=2, time_limit=20.0, e_tol=0.02):
    """Causal P0-BILL on one block: rolling P0 (recipe profiles) whose peak level minimises billed demand of (forecast bg + cell),
    floor = billed demand reached in the month before the block; off-window intervals never bind."""
    from regenate.data.bench_v2 import fifo
    from regenate.forecasting.ai_engine import make_profile_fn
    from regenate.optimization.rolling import Replanner
    from regenate.simulation.replay import Replay
    sl = inst["dt_h"]

    def bill_fn(t0_h, K, slot_h):
        t = t_block + pd.Timedelta(hours=float(t0_h))
        f = bg_forecast(bg15, t, K, kind); idx = pd.date_range(t, periods=K, freq=f"{SLOT_MIN}min")
        f = np.where(window_mask(idx, mdw), np.nan_to_num(f), -1e6)
        phase = int((t.minute % (interval_slots * SLOT_MIN)) // SLOT_MIN)
        return dict(peak_bg=f, peak_floor=floor, peak_avg_slots=interval_slots, peak_phase=phase, e_tol=e_tol)

    fa, fs = fifo(inst)
    rp = Replanner(inst, "P0", sl, prm, 0.25, time_limit, profile_fn=make_profile_fn(inst, "P0", None, sl), peak_stage=True, bill_fn=bill_fn)
    real, _ = Replay(inst, {j: (fa[j], fs[j]) for j in fa}, rp, period_h=sl, max_solve_s=3 * time_limit).run()
    return pd.DataFrame(dict(job_id=list(real), station=[v[0] for v in real.values()], start_h=[v[1] for v in real.values()]))


def main():
    from regenate.data.bench_v2 import load_proc, make_instance
    from regenate.electrical.ledger import ElecParams
    ap = argparse.ArgumentParser()
    ap.add_argument("--proc", required=True); ap.add_argument("--ds07", required=True); ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--facilities", nargs="+", required=True); ap.add_argument("--months", nargs="+", required=True)
    ap.add_argument("--block_h", type=float, default=0.0, help="0 = smallest whole hour >= longest cell trace")
    ap.add_argument("--n_cells", type=int, default=1); ap.add_argument("--interval_min", type=int, default=30)
    ap.add_argument("--md_window", default="", help='e.g. "0,1,2,3,4:14:22" = Mon-Fri 14-22 h (TNB RP4 MV peak); empty = all hours')
    ap.add_argument("--holidays", choices=["none", "MY"], default="none")
    ap.add_argument("--seed", type=int, default=0); ap.add_argument("--methods", nargs="+", default=None); ap.add_argument("--bill", action="store_true", help="also ORACLE-BILL re-solve")
    ap.add_argument("--p0bill", nargs="*", default=[], help="causal P0-BILL with background forecast kinds: oracle persist hist")
    ap.add_argument("--p0bill_etol", type=float, default=0.02)
    ap.add_argument("--load_model", default=None, help="facility_predictor.joblib for P0-BILL kind 'ai'")
    ap.add_argument("--bill_etol", type=float, nargs="+", default=[1e-4], help="energy tolerance of the billing level (sweep)")
    ap.add_argument("--prm", default='{"P_afe_max": 20, "P_bus_max": 32, "dP_step_max": 10}'); ap.add_argument("--out", required=True)
    a = ap.parse_args(); prm = ElecParams(**json.loads(a.prm)); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    holiday_dates = set()
    if a.holidays == "MY":
        from regenate.economics.billing import my_public_holidays
        for year in {int(month[:4]) for month in a.months}:
            holiday_dates.update(my_public_holidays(year))
    mdw = None
    if a.md_window:
        d_, h0, h1 = a.md_window.split(":"); mdw = ([int(x) for x in d_.split(",")], float(h0), float(h1))
        if holiday_dates:
            mdw += (holiday_dates,)
    cyc, arrs = load_proc(a.proc)
    sch = {}
    for d in a.runs:                                                    # method label = run dir tag + method
        s = pd.read_parquet(Path(d) / "schedules.parquet"); tag = Path(d).name
        for (iid, m), g in s.groupby(["instance_id", "method"]):
            sch[(iid, m if tag == "v2_diag" else f"{m}@{tag}")] = g
    methods = sorted({m for _, m in sch if not a.methods or m in a.methods})
    ids = sorted({i for i, m in sch if all((i, mm) in sch for mm in methods)})
    insts = {i: make_instance(cyc, arrs, int(i.rsplit("s", 1)[1]), n_jobs=10, n_stations=8, split="test") for i in ids}
    traces = {(i, m): to_minutes(cell_net_slots(insts[i], sch[(i, m)], prm, topo_of(m))) for i in ids for m in methods}
    block_h = a.block_h or float(np.ceil(max(len(v) for v in traces.values()) / 60))
    rows = []
    if "ai" in a.p0bill:
        import joblib
        _AI["pred"] = joblib.load(a.load_model)
    for fac in a.facilities:
        bg_all = load_ds07(a.ds07, fac); _AI["factory"] = fac
        for month in a.months:
            blocks = month_blocks(month, block_h); idx = bg_all[month].index; bg = bg_all[month]
            md0, t0 = billed_demand(bg, a.interval_min, md_window=mdw)
            draws = [draw_instances(ids, len(blocks), a.seed + 1000 * c) for c in range(a.n_cells)]
            cand = {m: [[traces[(i, m)] for i in dr] for dr in draws] for m in methods}
            if a.bill:
                bgs = bg.resample(f"{SLOT_MIN}min").mean().ffill()
                if mdw is not None:                                   # off-window intervals are never billed -> never bind
                    bgs = bgs.where(window_mask(bgs.index, mdw), -1e6)
                for et in a.bill_etol:
                    key = "ORACLE-BILL" if et == 1e-4 else f"ORACLE-BILL@etol{et:g}"; cand[key] = []
                    for dr in draws:
                        tr = []
                        for t, i in zip(blocks, dr):
                            s_ = solve_bill_block(insts[i], bgs[t:t + pd.Timedelta(hours=block_h)].values, prm, floor=md0,
                                                  interval_slots=a.interval_min // SLOT_MIN, e_tol=et)
                            fb = (i, "ORACLE@v2_e1_peak") if (i, "ORACLE@v2_e1_peak") in traces else (i, "ORACLE")
                            tr.append(to_minutes(cell_net_slots(insts[i], s_, prm)) if s_ is not None else traces[fb])
                        cand[key].append(tr)
            if a.p0bill:
                bg15 = bg_all.resample(f"{SLOT_MIN}min").mean()               # whole record: forecasts look back across months
                for kind in a.p0bill:
                    key = f"P0-BILL:{kind}@etol{a.p0bill_etol:g}"; cand[key] = []
                    for dr in draws:
                        tr, so_far = [], pd.Series(0.0, index=idx)
                        for t, i in zip(blocks, dr):
                            past = (bg + so_far)[:t - pd.Timedelta(minutes=1)]
                            fl = billed_demand(past, a.interval_min, md_window=mdw)[0] if len(past) else 0.0
                            s_ = run_p0bill_block(insts[i], prm, bg15, t, kind, 0.0 if np.isnan(fl) else fl, mdw,
                                                  a.interval_min // SLOT_MIN, e_tol=a.p0bill_etol)
                            x = to_minutes(cell_net_slots(insts[i], s_, prm)); tr.append(x)
                            so_far = so_far.add(place([t], [x], idx), fill_value=0.0)
                        cand[key].append(tr)
            for m, per_cell in cand.items():
                cell = sum(place(blocks, tr, idx) for tr in per_cell)
                md, tmd = billed_demand(bg + cell, a.interval_min, md_window=mdw)
                rows.append(dict(facility=fac, month=month, method=m, md_window=a.md_window or "all", n_cells=a.n_cells, block_h=block_h, n_blocks=len(blocks),
                                 md_bg_kw=md0, md_kw=md, md_increment_kw=md - md0, md_time=str(tmd), bg_md_time=str(t0),
                                 cell_kwh=float(cell.sum() / 60), cell_peak_kw=float(cell.max()),
                                 coverage=float(bg.notna().mean()), boundary="SIM_DATA_PROFILE cell + MEASURED DS07 facility (not synchronised)"))
            pd.DataFrame(rows).to_csv(out / "facility_md.csv", index=False); print(fac, month, flush=True)
    (out / "manifest.json").write_text(json.dumps(dict(args=vars(a), block_h=block_h, n_instances=len(ids), methods=methods,
                                                        holidays=sorted(d.isoformat() for d in holiday_dates)), indent=1))


if __name__ == "__main__":
    main()
