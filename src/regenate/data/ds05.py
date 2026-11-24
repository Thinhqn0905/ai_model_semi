"""DS05 — Loughborough "Long-Term Sweat Testing Data for Second-Life Batteries" (Chroma 17020 cycler).
CC BY 4.0, doi:10.17028/rd.lboro.28732490.v2. Six use cases (TOU, PV, PV-TOU, EFR, FFR, Day Ahead), one repurposed
EV module (2 cells in series, ~8 V) per use case, cycles stored as CSV inside "Sweat Test Data.zip".

Streams every cycle CSV straight from the zip (no extraction) and writes
  ds05_traces/<use_case>.parquet : use_case, period, cycle_file, t_s (Cumulative_Time), p_charge_w, p_discharge_w,
                                   v, i, v_cell1, v_cell2, t_amb_c   (mean over `step_s` bins; MEASURED)
  ds05_cycles.parquet            : one row per cycle file (energies, durations, voltages, temperature; DERIVED)
Sign: POWER > 0 = charging (station is a SINK), POWER < 0 = discharging (station is a SOURCE, energy returned).
  python -m regenate.data.ds05 --zip "/content/ds05_raw/Sweat Test Data.zip" --out /content/ds05_proc --workers 8
"""
import argparse, io, os, re, zipfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import pandas as pd

USECOLS = ["POWER", "CURRENT", "VOLTAGE", "STEP_MODE", "STATUS_IDX", "Cumulative_Time", "REAL_TIME",
           "Cell1", "Cell2", "Ambient Temperature"]


def cycle_no(name):
    m = re.search(r"Cycle_(\d+)\.csv$", name)
    return int(m.group(1)) if m else -1


def parse_cycle(raw, step_s=60.0):
    """(trace bins DataFrame, summary dict) for one cycle CSV given as bytes."""
    df = pd.read_csv(io.BytesIO(raw), usecols=lambda c: c in USECOLS, low_memory=False)
    df = df.dropna(subset=["Cumulative_Time", "POWER"]).sort_values("Cumulative_Time")
    t = df["Cumulative_Time"].to_numpy(float); p = df["POWER"].to_numpy(float)
    if len(t) < 2:
        return None, None
    dt = np.diff(t, append=t[-1]); dt = np.clip(dt, 0, 60.0)       # gaps > 60 s are not integrated (logging pauses)
    e_ch = float(np.sum(np.clip(p, 0, None) * dt) / 3.6e6)          # kWh
    e_dis = float(np.sum(np.clip(-p, 0, None) * dt) / 3.6e6)
    ch, dis = p > 1.0, p < -1.0                                      # >1 W threshold = active
    summ = dict(t0_s=t[0], t1_s=t[-1], dur_h=(t[-1] - t[0]) / 3600, e_charge_kwh=e_ch, e_discharge_kwh=e_dis,
                h_charge=float(dt[ch].sum() / 3600), h_discharge=float(dt[dis].sum() / 3600),
                h_rest=float(dt[~ch & ~dis].sum() / 3600), p_charge_max_w=float(p.max()), p_discharge_max_w=float(-p.min()),
                v_min=float(df["VOLTAGE"].min()), v_max=float(df["VOLTAGE"].max()),
                i_abs_max=float(df["CURRENT"].abs().max()), n_rows=len(df), median_dt_s=float(np.median(np.diff(t))))
    for c, k in (("Ambient Temperature", "t_amb_mean_c"), ("Cell1", "v_cell1_mean"), ("Cell2", "v_cell2_mean")):
        summ[k] = float(df[c].mean()) if c in df else np.nan
    summ["rte"] = e_dis / e_ch if e_ch > 0 else np.nan
    df["p_charge_w"] = np.clip(p, 0, None); df["p_discharge_w"] = np.clip(-p, 0, None)
    df["bin"] = np.floor((t - t[0]) / step_s).astype(int)
    agg = {"Cumulative_Time": "first", "p_charge_w": "mean", "p_discharge_w": "mean", "VOLTAGE": "mean", "CURRENT": "mean"}
    for c in ("Cell1", "Cell2", "Ambient Temperature"):
        if c in df:
            agg[c] = "mean"
    tr = df.groupby("bin").agg(agg).reset_index(drop=True).rename(columns={
        "Cumulative_Time": "t_s", "VOLTAGE": "v", "CURRENT": "i", "Cell1": "v_cell1", "Cell2": "v_cell2",
        "Ambient Temperature": "t_amb_c"})
    return tr, summ


def _work(args):
    zpath, names, step_s = args
    z = zipfile.ZipFile(zpath); traces, rows = [], []
    for n in names:
        parts = n.split("/")
        uc, period = parts[0], "/".join(parts[1:-1])
        try:
            tr, s = parse_cycle(z.read(n), step_s)
        except Exception as e:                                       # keep the failure, never drop silently
            rows.append(dict(use_case=uc, period=period, cycle_file=n, error=f"{type(e).__name__}: {e}")); continue
        if s is None:
            rows.append(dict(use_case=uc, period=period, cycle_file=n, error="empty")); continue
        rows.append(dict(use_case=uc, period=period, cycle_file=n, cycle_no=cycle_no(n), error="", **s))
        traces.append(tr.assign(use_case=uc, period=period, cycle_file=n))
    return (pd.concat(traces, ignore_index=True) if traces else pd.DataFrame()), rows


def build(zpath, out, workers=8, step_s=60.0, limit=None):
    out = Path(out); (out / "ds05_traces").mkdir(parents=True, exist_ok=True)
    names = sorted(i.filename for i in zipfile.ZipFile(zpath).infolist() if i.filename.endswith(".csv"))
    if limit:
        names = names[::max(1, len(names) // limit)][:limit]
    by_uc = {}
    for n in names:
        by_uc.setdefault(n.split("/")[0], []).append(n)
    rows = []
    for uc, lst in by_uc.items():
        chunks = [lst[k:k + 25] for k in range(0, len(lst), 25)]
        parts = []
        with ProcessPoolExecutor(workers) as ex:
            for tr, r in ex.map(_work, [(zpath, c, step_s) for c in chunks]):
                parts.append(tr); rows += r
        tr = pd.concat([p for p in parts if len(p)], ignore_index=True)
        tr.to_parquet(out / "ds05_traces" / f"{uc.replace(' ', '_')}.parquet", index=False)
        print(uc, len(lst), "cycles ->", len(tr), "trace rows", flush=True)
    cyc = pd.DataFrame(rows)
    cyc["provenance"] = "DERIVED(MEASURED DS05)"
    cyc.to_parquet(out / "ds05_cycles.parquet", index=False)
    print("cycles", len(cyc), "errors", int((cyc.error != "").sum()))
    return cyc


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=os.cpu_count()); ap.add_argument("--step_s", type=float, default=60.0)
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    build(a.zip, a.out, a.workers, a.step_s, a.limit)
