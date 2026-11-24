"""WP05 oracle campaign (E04 negative control, E05 oracle AC/in-rack/DC, E06 flexibility sweep).

Every plan is scored the same way: executed with TRUE durations (station order kept, a job waits for
its station), rendered by regenate.data.generator.render(truth=True) and passed to the shared ledger.
  python -m regenate.evaluation.oracle_campaign --out runs/oracle_v1 --n 10 --seeds 0 1 --flex 0 0.25 1
"""
import argparse, hashlib, json, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import pandas as pd
from regenate.data.generator import fifo_schedule, render, _phase_steps
from regenate.electrical.ledger import ledger, ElecParams
from regenate.optimization.milp import Job, solve, assign_stations

BENCH = Path("data/generated/bench_v1")
FIFO_METHODS = {"B0": "B0", "B1": "B1", "B1p": "B1p", "B2": "DC"}
OPT_METHODS = {"B1-OPT": ("B1", True), "B1p-OPT": ("B1p", True), "ORACLE": ("DC", True), "B3": ("DC", False)}


def load(iid):
    d = BENCH / iid
    return dict(instance_id=iid, jobs=pd.read_parquet(d / "jobs.parquet"),
                stations=pd.read_parquet(d / "stations.parquet"), recipe=pd.read_parquet(d / "recipes.parquet"),
                dt_h=float(json.loads((BENCH / "manifest.json").read_text())["config"]["dt_h"]))


def slot_profile(inst, j, slot_h, truth):
    one = dict(inst, jobs=inst["jobs"].iloc[[j]])
    jid = int(one["jobs"].job_id.iloc[0])
    p_in, p_rec, aux = render(one, {jid: 0}, {jid: 0.0}, slot_h, truth=truth)
    return p_in[0], p_rec[0], aux[0]


def milp_jobs(inst, slot_h, truth, flex, fifo_start):
    out = []
    for j, r in enumerate(inst["jobs"].itertuples()):
        p_in, p_rec, aux = slot_profile(inst, j, slot_h, truth)
        dur = len(p_in)
        rel = int(np.ceil(r.release_h / slot_h - 1e-9))
        lat_dead = int(np.floor((r.deadline_h - (r.dur_true_h if truth else r.dur_nom_h)) / slot_h + 1e-9))
        lat_flex = int(np.floor((r.release_h + flex * r.max_shift_h) / slot_h + 1e-9))
        lat = max(rel, min(lat_dead, max(lat_flex, int(np.ceil(fifo_start[int(r.job_id)] / slot_h)))))
        out.append(Job(rel, lat, r.due_h / slot_h, p_in, p_rec, aux))
    return out


def capacity(inst, K, slot_h):
    cap = np.full(K, len(inst["stations"]), float)
    for w in inst["stations"].downtime_json:            # shortcut: downtime as cell capacity
        for a, b in json.loads(w):
            cap[int(a // slot_h):int(np.ceil(b / slot_h))] -= 1
    return np.maximum(cap, 0)


def true_dur(inst, jid):
    """Realised duration on the render grid (phase steps of the generator), hours."""
    dt = inst["dt_h"]; d = float(inst["jobs"].set_index("job_id").loc[jid, "dur_true_h"])
    return int(sum(_phase_steps(inst["recipe"], d, dt))) * dt


def execute(inst, assign, planned):
    """Run a plan with true durations: keep each station's order, wait while the station is busy."""
    dt = inst["dt_h"]; starts = {}
    for s in set(assign.values()):
        free = 0.0
        for jid in sorted([j for j in assign if assign[j] == s], key=lambda j: planned[j]):
            st = max(planned[jid], free); st = round(np.ceil(st / dt - 1e-9) * dt, 9)
            starts[jid] = st; free = st + true_dur(inst, jid)
    return starts


def score(inst, method, topo, assign, starts, dt_h, prm, solve_s=0.0, gap=0.0):
    J = inst["jobs"].set_index("job_id")
    end = {j: starts[j] + true_dur(inst, j) for j in starts}
    tt = sum(max(0.0, end[j] - J.loc[j, "due_h"]) for j in end)
    viol = sum(end[j] > J.loc[j, "deadline_h"] + 1e-9 for j in end)
    L = ledger(*render(inst, assign, starts, dt_h, truth=True), dt_h, topo, prm)
    row = dict(method=method, topology=topo, TT_h=tt, makespan_h=max(end.values()), completed_jobs=len(end),
               violations=int(viol + L["afe_violation_steps"]), solve_s=solve_s, mip_gap=gap,
               **{k: L[k] for k in ("import_kwh", "export_kwh", "net_kwh", "peak_import_kw", "direct_reuse_kwh",
                                    "self_use_kwh", "recoverable_kwh", "dump_kwh", "loss_kwh")})
    sch = [dict(method=method, job_id=j, station=assign[j], start_h=starts[j], end_h=end[j]) for j in starts]
    return row, sch


def set_bench(path):
    global BENCH
    BENCH = Path(path)


def run_instance(args):
    iid, flex, slot_h, prm_kw, time_limit = args[:5]
    if len(args) > 5:
        set_bench(args[5])                       # worker processes do not inherit the global
    inst = load(iid); prm = ElecParams(**prm_kw); S = len(inst["stations"])
    rows, schs = [], []
    fa, fs = fifo_schedule(inst)
    for m, topo in FIFO_METHODS.items():
        r, s = score(inst, m, topo, fa, fs, slot_h, prm); rows.append(r); schs += s
    for m, (topo, truth) in OPT_METHODS.items():
        jobs = milp_jobs(inst, slot_h, truth, flex, fs)
        K = max(j.latest + j.dur for j in jobs) + 1
        t0 = time.time()
        res = solve(jobs, S, K, topo, prm, slot_h, cap=capacity(inst, K, slot_h), time_limit=time_limit)
        dt = time.time() - t0
        if not res.starts:
            rows.append(dict(method=m, topology=topo, status=res.status, solve_s=dt)); continue
        stn = assign_stations(res.starts, [j.dur for j in jobs], S)
        ids = [int(x) for x in inst["jobs"].job_id]
        assign = dict(zip(ids, stn)); planned = {i: t * slot_h for i, t in zip(ids, res.starts)}
        starts = execute(inst, assign, planned)
        r, s = score(inst, m, topo, assign, starts, slot_h, prm, dt, res.mip_gap)
        r["milp_net_kwh"] = res.net_kwh; r["status"] = res.status
        rows.append(r); schs += s
    meta = dict(instance_id=iid, scenario=iid.split("_")[3], n_jobs=len(inst["jobs"]), n_stations=S,
                seed=int(iid.split("_")[-1]), flex=flex, boundary="SIM_ASSUMED_PROFILE")
    return [dict(meta, **r) for r in rows], [dict(instance_id=iid, flex=flex, **s) for s in schs]


def code_hash():
    h = hashlib.sha256()
    for p in sorted(Path("src/regenate").rglob("*.py")):
        h.update(p.read_bytes())
    return h.hexdigest()[:16]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="runs/oracle_v1"); ap.add_argument("--n", type=int, nargs="+", default=[10])
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1]); ap.add_argument("--scenarios", nargs="+", default=["S1", "S2", "S3"])
    ap.add_argument("--flex", type=float, nargs="+", default=[0.0, 0.25, 1.0]); ap.add_argument("--slot_h", type=float, default=0.25)
    ap.add_argument("--time_limit", type=float, default=60.0); ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--P_link_max", type=float, default=float("inf"))
    ap.add_argument("--bench", default=str(BENCH), help="generated benchmark folder")
    ap.add_argument("--prm", default="{}", help='JSON overrides of ElecParams, e.g. {"eta_afe_imp":0.95}')
    a = ap.parse_args()
    set_bench(a.bench)
    man = json.loads((BENCH / "manifest.json").read_text())
    ids = [i for i in man["instances"] if int(i[1:4]) in a.n and int(i.split("_")[-1]) in a.seeds and i.split("_")[3] in a.scenarios]
    split = {i: s for s, lst in man["splits"].items() for i in lst}
    prm_kw = dict(P_link_max=a.P_link_max, **json.loads(a.prm))
    tasks = [(i, f, a.slot_h, prm_kw, a.time_limit, str(BENCH)) for f in a.flex for i in ids]
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    rows, schs = [], []
    with ProcessPoolExecutor(a.workers) as ex:
        for k, (r, s) in enumerate(ex.map(run_instance, tasks), 1):
            rows += r; schs += s
            if k % 10 == 0 or k == len(tasks):
                print(f"{k}/{len(tasks)} done", flush=True)
                df = pd.DataFrame(rows); df["split"] = df.instance_id.map(split)
                df.to_csv(out / "results.csv", index=False)
    pd.DataFrame(schs).to_parquet(out / "schedules.parquet", index=False)
    (out / "manifest.json").write_text(json.dumps(dict(args=vars(a), code_sha256_16=code_hash(), n_tasks=len(tasks),
                                                        bench=str(BENCH), boundary="SIM_ASSUMED_PROFILE"), indent=2, default=str))


if __name__ == "__main__":
    main()
