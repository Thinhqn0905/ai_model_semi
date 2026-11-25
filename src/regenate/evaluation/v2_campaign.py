"""DS06 / bench v2 campaign: full ladder + AI ablation on stations replaying measured DS05 cycles.
  python -m regenate.evaluation.v2_campaign --proc /content/ds05_proc --models runs/ai/ds05/ai_models.joblib \
         --out runs/v2_ladder --seeds 0 1 2 ... --n_jobs 10 --split test
Every method is scored by the same ledger on the TRUE traces; P0..P4 share the same rolling MILP, period, time limit.
"""
import argparse, json, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import pandas as pd
from regenate.data.bench_v2 import load_proc, make_instance, fifo, job_profile
from regenate.electrical.ledger import ElecParams
from regenate.evaluation.oracle_campaign import execute, score
from regenate.optimization.milp import Job, solve, assign_stations
from regenate.optimization.rolling import Replanner
from regenate.simulation.replay import Replay

FIFO_M = {"B0": "B0", "B1": "B1", "B1p": "B1p", "B2": "DC"}
ONESHOT = {"B1-OPT": ("B1", "truth"), "B1p-OPT": ("B1p", "truth"), "B3": ("DC", "nominal"), "ORACLE": ("DC", "truth")}
ROLLING = ("P0", "P1", "P2", "P3", "P4")
DIAG = ("P5", "P5s", "PQ", "PQ5", "P1*", "P2*", "P3*", "P4*", "TR_RUN", "TR_Q", "TR_ALL")   # Run 3 information decomposition (no model needed)


def milp_jobs(inst, which, flex, fifo_starts, sl):
    out = []
    for r in inst["jobs"].itertuples():
        pi, pr, ax = job_profile(inst, r.job_id, sl, which)
        dur_h = len(pi) * sl
        rel = int(np.ceil(r.release_h / sl - 1e-9))
        lat = int(np.floor(min(r.deadline_h - dur_h, r.release_h + flex * r.max_shift_h) / sl + 1e-9))
        lat = max(rel, lat, int(np.ceil(fifo_starts[r.job_id] / sl - 1e-9)))
        out.append(Job(rel, lat, r.due_h / sl, pi, pr, ax))
    return out


def run_one(inst, engine, flex=0.25, time_limit=20.0, prm=None, methods=None, peak_stage=False, cycle_pred=None):
    from regenate.forecasting.ai_engine import make_profile_fn
    prm = prm or ElecParams(); sl = inst["dt_h"]; S = len(inst["stations"])
    methods = methods or (list(FIFO_M) + list(ONESHOT) + list(ROLLING))
    rows, schs = [], []
    fa, fs = fifo(inst)
    for m in methods:
        t0 = time.time(); extra = {}
        if m in FIFO_M:
            topo, assign, starts = FIFO_M[m], fa, fs
        elif m in ONESHOT:
            topo, which = ONESHOT[m]
            jobs = milp_jobs(inst, which, flex, fs, sl)
            K = max(j.latest + j.dur for j in jobs) + 1
            res = solve(jobs, S, K, topo, prm, sl, time_limit=time_limit, peak_stage=peak_stage and topo == "DC")
            if not res.starts:
                rows.append(dict(method=m, status=res.status)); continue
            ids = list(inst["jobs"].job_id)
            stn = assign_stations(res.starts, [j.dur for j in jobs], S)
            assign = dict(zip(ids, stn)); planned = {i: t * sl for i, t in zip(ids, res.starts)}
            starts = execute(inst, assign, planned); extra = dict(status=res.status, mip_gap=res.mip_gap)
        else:
            if m in ROLLING[1:] and engine is None:
                continue
            topo = "DC"
            rp = Replanner(inst, m, sl, prm, flex, time_limit, profile_fn=make_profile_fn(inst, m, engine, sl, cycle_pred=cycle_pred), peak_stage=peak_stage)
            real, log = Replay(inst, {j: (fa[j], fs[j]) for j in fa}, rp, period_h=sl, max_solve_s=3 * time_limit).run()
            assign = {j: v[0] for j, v in real.items()}; starts = {j: v[1] for j, v in real.items()}
            extra = dict(n_replans=int((log.event == "replan").sum()),
                         n_rejected=int(((log.event == "replan") & ~log.accepted).sum()), status="rolling")
        r, s = score(inst, m, topo, assign, starts, sl, prm, time.time() - t0)
        rows.append(dict(r, **extra)); schs += s
    meta = dict(instance_id=inst["instance_id"], n_jobs=len(inst["jobs"]), n_stations=S, flex=flex, peak_stage=peak_stage,
                use_cases="|".join(sorted(inst["jobs"].use_case.unique())), boundary=inst["meta"]["boundary"])
    return [dict(meta, **r) for r in rows], [dict(instance_id=inst["instance_id"], **s) for s in schs]


_G = {}


def _init(proc, models, kw):
    _G["cyc"], _G["arrs"] = load_proc(proc)
    _G["eng"] = None
    if models:
        from regenate.forecasting.ai_engine import AIEngine
        _G["eng"] = AIEngine.load(models)
    _G["kw"] = kw
    _G["cpred"] = None
    if kw.get("cycle_pred"):
        _G["cpred"] = pd.read_parquet(kw["cycle_pred"]).set_index("cycle_file")[["r_dur", "r_ech", "r_eds"]].to_dict("index")


def _task(seed):
    kw = _G["kw"]
    inst = make_instance(_G["cyc"], _G["arrs"], seed, n_jobs=kw["n_jobs"], n_stations=kw["n_stations"], split=kw["split"])
    return run_one(inst, _G["eng"], kw["flex"], kw["time_limit"], prm=ElecParams(**kw["prm"]), methods=kw["methods"], peak_stage=kw["peak"], cycle_pred=_G["cpred"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--proc", required=True); ap.add_argument("--models", default=None); ap.add_argument("--out", required=True)
    ap.add_argument("--seeds", type=int, nargs="+", default=list(range(20))); ap.add_argument("--n_jobs", type=int, default=10)
    ap.add_argument("--n_stations", type=int, default=8); ap.add_argument("--split", default="test")
    ap.add_argument("--flex", type=float, default=0.25); ap.add_argument("--time_limit", type=float, default=20.0)
    ap.add_argument("--workers", type=int, default=4); ap.add_argument("--peak", action="store_true")
    ap.add_argument("--prm", default="{}", help='JSON ElecParams overrides, e.g. {"P_afe_max":15}')
    ap.add_argument("--cycle_pred", default=None, help="cycle_model.py cycle_pred.parquet (variants PQ, PQ5)")
    ap.add_argument("--methods", nargs="+", default=None, help="subset; default all FIFO/one-shot/P0..P4; DIAG names allowed")
    a = ap.parse_args()
    kw = dict(n_jobs=a.n_jobs, n_stations=a.n_stations, split=a.split, flex=a.flex, time_limit=a.time_limit, peak=a.peak, methods=a.methods, prm=json.loads(a.prm), cycle_pred=a.cycle_pred)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True); rows, schs = [], []
    with ProcessPoolExecutor(a.workers, initializer=_init, initargs=(a.proc, a.models, kw)) as ex:
        for k, (r, s) in enumerate(ex.map(_task, a.seeds), 1):
            rows += r; schs += s
            pd.DataFrame(rows).to_csv(out / "results.csv", index=False); print(f"{k}/{len(a.seeds)}", flush=True)
    pd.DataFrame(schs).to_parquet(out / "schedules.parquet", index=False)
    (out / "manifest.json").write_text(json.dumps(dict(args=vars(a)), indent=1))


if __name__ == "__main__":
    main()
