"""DS06 = ReGenATE bench v2: test-cell instances whose station jobs REPLAY measured DS05 cycles (D002).

Each job = one DS05 cycle (60-s bins). p_in = charge power at the module terminals (station is a sink), p_rec = discharge
power (station is a source; the regenerative cycler takes it back). Shapes, durations, energies: MEASURED (DS05).
Scaling to a station: `modules_per_station` modules in parallel (ASSUMED, default 25 -> ~6 kW peak like bench_v1).
What a planner knows before a job starts (P0 "recipe"): the PREVIOUS cycle of the same module (same use case) — the real
repeat of the test recipe. Release / due / deadline / shift window: ASSUMED (stated in the manifest).
"""
import json
import numpy as np
import pandas as pd

TRACE_DT_H = 1 / 60


def load_proc(proc):
    from pathlib import Path
    from regenate.forecasting.ds05_bench import order_cycles, cycle_arrays
    cyc = order_cycles(pd.read_parquet(Path(proc) / "ds05_cycles.parquet"))
    arrs = {}
    for p in sorted((Path(proc) / "ds05_traces").glob("*.parquet")):
        arrs.update(cycle_arrays(pd.read_parquet(p)))
    return cyc, arrs


def make_instance(cyc, arrs, seed, n_jobs=10, n_stations=8, split="test", modules_per_station=25.0,
                  max_dur_h=12.0, release_span_h=4.0, slack_h=(2.0, 8.0), deadline_extra_h=12.0, max_shift_h=4.0,
                  dt_h=0.25, use_cases=None):
    rng = np.random.default_rng(seed)
    c = cyc[(cyc.split == split) & (cyc.dur_h <= max_dur_h) & (cyc.dur_h > 0.5)].copy()
    c["prev_file"] = cyc.groupby("use_case").cycle_file.shift(1).reindex(c.index)
    c = c[c.prev_file.notna() & c.cycle_file.isin(arrs) & c.prev_file.isin(arrs)]
    if use_cases:
        c = c[c.use_case.isin(use_cases)]
    pick = c.sample(n_jobs, random_state=int(rng.integers(1 << 31)))
    traces, nominal, telem, rows = {}, {}, {}, []
    k = modules_per_station
    for jid, r in enumerate(pick.itertuples()):
        ch, ds = arrs[r.cycle_file][:2]; pch, pds = arrs[r.prev_file][:2]
        traces[jid] = (ch * k, ds * k); nominal[jid] = (pch * k, pds * k)
        telem[jid] = tuple(arrs[r.cycle_file][2:4])            # module V and ambient T (M2/M3 telemetry)
        rel = float(np.round(rng.uniform(0, release_span_h) / dt_h) * dt_h)
        dur_nom = len(pch) * TRACE_DT_H
        due = rel + dur_nom + rng.uniform(*slack_h)
        rows.append(dict(job_id=jid, cycle_file=r.cycle_file, prev_file=r.prev_file, use_case=r.use_case, recipe_id=r.use_case,
                         release_h=rel, due_h=due, deadline_h=due + deadline_extra_h, dur_true_h=len(ch) * TRACE_DT_H,
                         dur_nom_h=dur_nom, max_shift_h=max_shift_h, eligible_stations=list(range(n_stations))))
    jobs = pd.DataFrame(rows)
    stations = pd.DataFrame(dict(station_id=range(n_stations), p_rated_kw=float(k * 0.24), downtime_json="[]"))
    return dict(instance_id=f"v2_{split}_n{n_jobs}_s{seed}", jobs=jobs, stations=stations, dt_h=dt_h,
                trace_dt_h=TRACE_DT_H, traces=traces, nominal=nominal, telem=telem,
                meta=dict(modules_per_station=k, boundary="SIM_DATA_PROFILE(DS05 MEASURED shapes; scaling+timing ASSUMED)"))


def _bin(a, step):
    """Average a 1-min array into bins of `step` samples (last partial bin padded with its own mean)."""
    n = int(np.ceil(len(a) / step))
    out = np.zeros(n)
    for i in range(n):
        out[i] = a[i * step:(i + 1) * step].mean()
    return out


def job_profile(inst, jid, dt_h, which="truth"):
    """(p_in, p_rec, p_aux) of one job on a dt_h grid; which = truth | nominal."""
    src = inst["traces" if which == "truth" else "nominal"][jid]
    step = int(round(dt_h / inst["trace_dt_h"]))
    pi, pr = _bin(src[0], step), _bin(src[1], step)
    return pi, pr, np.zeros_like(pi)


def render_traces(inst, assign, starts_h, dt_h, truth=True):
    profs = {j: job_profile(inst, j, dt_h, "truth" if truth else "nominal") for j in starts_h}
    S = len(inst["stations"])
    end = max(int(round(starts_h[j] / dt_h)) + len(profs[j][0]) for j in starts_h)
    out = [np.zeros((S, end)) for _ in range(3)]
    for j, t in starts_h.items():
        k = t / dt_h
        if not np.isclose(k, round(k), atol=1e-9):
            raise ValueError("job start must be on render grid")
        k = int(round(k)); s = int(assign[j])
        for a, p in zip(out, profs[j]):
            a[s, k:k + len(p)] += p
    return tuple(out)


def fifo(inst):
    dt = inst["dt_h"]; free = {int(s): 0.0 for s in inst["stations"].station_id}; assign, starts = {}, {}
    from regenate.evaluation.oracle_campaign import true_dur
    for j in inst["jobs"].sort_values(["release_h", "job_id"]).itertuples():
        s = min(free, key=lambda s: (max(free[s], j.release_h), s))
        st = np.ceil(max(free[s], j.release_h) / dt - 1e-9) * dt
        assign[j.job_id] = s; starts[j.job_id] = st; free[s] = st + true_dur(inst, j.job_id)
    return assign, starts
