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


def billed_demand(p_1min, interval_min=30, min_cov=0.8):
    """(kW, window start) max aligned-window mean; windows with < min_cov valid minutes are excluded."""
    g = p_1min.groupby(p_1min.index.floor(f"{interval_min}min"))
    m, c = g.mean(), g.count() / interval_min
    m = m[c >= min_cov]
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


def solve_bill_block(inst, bg_slots, prm, time_limit=10.0, interval_slots=2, floor=0.0):
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
                peak_floor=floor, peak_avg_slots=interval_slots)
    if not res.starts:
        return None
    ids = list(inst["jobs"].job_id); stn = assign_stations(res.starts, [j.dur for j in jobs], S)
    assign = dict(zip(ids, stn)); starts = execute(inst, assign, {i: t * sl for i, t in zip(ids, res.starts)})
    return pd.DataFrame(dict(job_id=list(starts), station=[assign[j] for j in starts], start_h=[starts[j] for j in starts]))


def main():
    from regenate.data.bench_v2 import load_proc, make_instance
    from regenate.electrical.ledger import ElecParams
    ap = argparse.ArgumentParser()
    ap.add_argument("--proc", required=True); ap.add_argument("--ds07", required=True); ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--facilities", nargs="+", required=True); ap.add_argument("--months", nargs="+", required=True)
    ap.add_argument("--block_h", type=float, default=0.0, help="0 = smallest whole hour >= longest cell trace")
    ap.add_argument("--n_cells", type=int, default=1); ap.add_argument("--interval_min", type=int, default=30)
    ap.add_argument("--seed", type=int, default=0); ap.add_argument("--methods", nargs="+", default=None); ap.add_argument("--bill", action="store_true", help="also ORACLE-BILL re-solve")
    ap.add_argument("--prm", default='{"P_afe_max": 20, "P_bus_max": 32, "dP_step_max": 10}'); ap.add_argument("--out", required=True)
    a = ap.parse_args(); prm = ElecParams(**json.loads(a.prm)); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
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
    for fac in a.facilities:
        bg_all = load_ds07(a.ds07, fac)
        for month in a.months:
            blocks = month_blocks(month, block_h); idx = bg_all[month].index; bg = bg_all[month]
            md0, t0 = billed_demand(bg, a.interval_min)
            draws = [draw_instances(ids, len(blocks), a.seed + 1000 * c) for c in range(a.n_cells)]
            cand = {m: [[traces[(i, m)] for i in dr] for dr in draws] for m in methods}
            if a.bill:
                bgs = bg.resample(f"{SLOT_MIN}min").mean().ffill()
                cand["ORACLE-BILL"] = []
                for dr in draws:
                    tr = []
                    for t, i in zip(blocks, dr):
                        s_ = solve_bill_block(insts[i], bgs[t:t + pd.Timedelta(hours=block_h)].values, prm, floor=md0,
                                              interval_slots=a.interval_min // SLOT_MIN)
                        tr.append(to_minutes(cell_net_slots(insts[i], s_, prm)) if s_ is not None else traces[(i, "ORACLE@v2_e1_peak")] if (i, "ORACLE@v2_e1_peak") in traces else traces[(i, "ORACLE")])
                    cand["ORACLE-BILL"].append(tr)
            for m, per_cell in cand.items():
                cell = sum(place(blocks, tr, idx) for tr in per_cell)
                md, tmd = billed_demand(bg + cell, a.interval_min)
                rows.append(dict(facility=fac, month=month, method=m, n_cells=a.n_cells, block_h=block_h, n_blocks=len(blocks),
                                 md_bg_kw=md0, md_kw=md, md_increment_kw=md - md0, md_time=str(tmd), bg_md_time=str(t0),
                                 cell_kwh=float(cell.sum() / 60), cell_peak_kw=float(cell.max()),
                                 coverage=float(bg.notna().mean()), boundary="SIM_DATA_PROFILE cell + MEASURED DS07 facility (not synchronised)"))
            pd.DataFrame(rows).to_csv(out / "facility_md.csv", index=False); print(fac, month, flush=True)
    (out / "manifest.json").write_text(json.dumps(dict(args=vars(a), block_h=block_h, n_instances=len(ids), methods=methods), indent=1))


if __name__ == "__main__":
    main()
