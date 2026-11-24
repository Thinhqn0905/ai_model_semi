"""Deterministic synthetic benchmark. All physical mappings are assumed."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from regenate.data.ds01 import SOURCE, load_instance, to_frames
from regenate.data.recipes import recipes
from regenate.electrical.ledger import ledger, ElecParams

def generate(ds, scenario, seed, cfg):
    nst = int(cfg["n_stations"])
    if nst not in (4, 8, 16, 32): raise ValueError("unsupported station count")
    key = f"{ds['instance_id']}|{scenario}|{seed}"
    rng = np.random.default_rng(int.from_bytes(hashlib.sha256(key.encode()).digest()[:8], "big"))
    src,_ = to_frames(ds)
    unit = float(cfg["unit_h"])
    dur = src.p_stage3_u.map(lambda values: float(np.mean(values))).to_numpy() * unit
    delay = rng.exponential(float(cfg["release_delay_mean_h"]), len(src))
    jobs = pd.DataFrame(dict(job_id=src.job_id, size=src['size'], recipe_id=scenario, release_h=delay, due_h=src.due_u * unit, deadline_h=np.maximum(src.due_u * unit, delay + dur) + float(cfg["max_shift_h"]), dur_nom_h=dur, dur_true_h=dur * (1 + np.clip(rng.normal(0, cfg["sigma_dur"], len(src)), -.5, .5)), kappa_true=np.clip(rng.normal(1,.05,len(src)),.8,1.2), eligible_stations=[list(range(nst)) for _ in range(len(src))], max_shift_h=cfg["max_shift_h"]))
    horizon = max(float(jobs.due_h.max()), float(jobs.dur_true_h.sum()))
    stations=[]
    for s in range(nst):
        windows=[]
        for day in range(int(np.ceil(horizon / 24))):
            if rng.random() < cfg["downtime_probability_per_day"]:
                start=day*24+rng.uniform(0,24); windows.append([start,start+rng.exponential(cfg["downtime_mean_h"])])
        stations.append(dict(station_id=s,p_rated_kw=float(cfg["p_rated_kw"]),downtime_json=json.dumps(windows, separators=(",",":"))))
    return dict(instance_id=key.replace("|","_"),jobs=jobs,stations=pd.DataFrame(stations),recipe=recipes(scenario,cfg["aux_kw"],cfg["cycle_scale"]),dt_h=float(cfg["dt_h"]))

def _phase_steps(recipe, duration, step):
    if step <= 0 or duration <= 0:
        raise ValueError("step and duration must be positive")
    fractions = recipe.dur_frac.to_numpy(dtype=float)
    active = np.flatnonzero(fractions > 0)
    total = max(len(active), int(np.ceil(duration / step - 1e-12)))
    # Constrained largest remainder, with a minimum of one step per active phase.
    ideal = fractions[active] / fractions[active].sum() * total
    counts = np.maximum(1, np.floor(ideal).astype(int))
    while counts.sum() > total:
        candidates = np.flatnonzero(counts > 1)
        i = candidates[np.argmin(ideal[candidates] - counts[candidates])]
        counts[i] -= 1
    while counts.sum() < total:
        i = np.argmax(ideal - counts)
        counts[i] += 1
    result = np.zeros(len(fractions), dtype=int)
    result[active] = counts
    return result


def fifo_schedule(inst):
    jobs=inst["jobs"]; stations=inst["stations"]; dt=inst["dt_h"]
    free={int(s):0.0 for s in stations.station_id}; assignment={}; starts={}
    for j in jobs.sort_values(["release_h","job_id"]).itertuples(index=False):
        duration=_phase_steps(inst["recipe"], j.dur_true_h, dt).sum()*dt
        candidates=[]
        for s in j.eligible_stations:
            start=np.ceil(max(float(j.release_h),free[int(s)])/dt-1e-12)*dt
            for a,b in sorted(json.loads(stations.loc[stations.station_id == s,"downtime_json"].iloc[0])):
                if start < b and start + duration > a: start=np.ceil(b/dt-1e-12)*dt
            candidates.append((start,int(s)))
        start,s=min(candidates); assignment[int(j.job_id)]=s; starts[int(j.job_id)]=start; free[s]=start+duration
    return assignment, starts


def job_slot_profile(inst, job, slot_h):
    """Nominal planner profile, averaged over whole slots; report mixed source/sink slots."""
    if slot_h <= 0: raise ValueError("slot_h must be positive")
    duration=float(job["dur_nom_h"] if isinstance(job, (dict, pd.Series)) else job.dur_nom_h)
    station=inst["stations"].iloc[0]; rated=float(station.p_rated_kw)
    n=int(np.ceil(duration/slot_h-1e-12)); out=np.zeros((3,n)); pos=0.0
    for ph in inst["recipe"].itertuples():
        end=pos+ph.dur_frac*n*slot_h
        for t in range(max(0,int(np.floor(pos/slot_h))), min(n,int(np.ceil(end/slot_h)))):
            overlap=max(0.,min(end,(t+1)*slot_h)-max(pos,t*slot_h))/slot_h
            out[:,t] += overlap*np.array([rated*ph.p_in_frac,rated*ph.p_rec_frac,ph.p_aux_kw])
        pos=end
    return {"p_in":out[0], "p_rec":out[1], "p_aux":out[2], "mixed_slots":(out[0]>1e-12)&(out[1]>1e-12)}


def render(inst, assign, starts_h, dt_h, truth=True):
    if "traces" in inst:                     # lead: bench v2 (DS06) jobs replay measured DS05 cycles
        from regenate.data.bench_v2 import render_traces
        return render_traces(inst, assign, starts_h, dt_h, truth)
    if dt_h <= 0: raise ValueError("dt_h must be positive")
    jobs=inst["jobs"]; stations=inst["stations"]; recipe=inst["recipe"]
    profiles=[]; end=0
    for j in jobs.itertuples():
        start=float(starts_h[int(j.job_id)])/dt_h
        if not np.isclose(start,round(start),rtol=0,atol=1e-9): raise ValueError("job start must be on render grid")
        start=int(round(start)); counts=_phase_steps(recipe,float(j.dur_true_h if truth else j.dur_nom_h),dt_h)
        profiles.append((j,start,counts)); end=max(end,start+sum(counts))
    arrays=[np.zeros((len(stations),end)) for _ in range(3)]; occupied=np.zeros((len(stations),end),dtype=bool)
    for j,start,counts in profiles:
        s=int(assign[int(j.job_id)]); k=float(j.kappa_true if truth else 1); rated=float(stations.loc[stations.station_id==s,"p_rated_kw"].iloc[0]); pos=start
        for ph,steps in zip(recipe.itertuples(),counts):
            stop=pos+steps
            if np.any(occupied[s,pos:stop]): raise ValueError("overlapping jobs")
            occupied[s,pos:stop]=True
            for arr,power in zip(arrays,(rated*k*ph.p_in_frac,rated*k*ph.p_rec_frac,ph.p_aux_kw)): arr[s,pos:stop]=power
            pos=stop
    return tuple(arrays)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--config",required=True); args=parser.parse_args(); cfg=yaml.safe_load(Path(args.config).read_text()); out=Path("data/generated/bench_v1"); out.mkdir(parents=True,exist_ok=True)
    manifest={"boundary":"SIM_ASSUMED_PROFILE", "config":cfg,"splits":{"train":[],"val":[],"test":[]},"provenance":{"jobs":"DS01 synthetic sizes and due dates; mean p_stage3_u across DS01 ovens times unit_h ASSUMED; other fields ASSUMED", "stations":"ASSUMED", "recipes":"ASSUMED and DERIVED(DS03 EDC); processed sequence ratio is not closed-cycle efficiency"},"instances":[]}
    shares={s:[] for s in cfg["scenarios"]}
    for path in sorted(SOURCE.glob("n*_tau*_r*.json")):
        ds=load_instance(path)
        if ds["n"] not in cfg["n"] or ds["tau"] not in cfg["tau"] or ds["replicate"] not in cfg["reps"]: continue
        for scenario in cfg["scenarios"]:
            for seed in cfg["seeds"]:
                inst=generate(ds,scenario,seed,cfg); target=out/inst["instance_id"]; target.mkdir(parents=True,exist_ok=True)
                inst["jobs"].to_parquet(target/"jobs.parquet",index=False); inst["stations"].to_parquet(target/"stations.parquet",index=False); inst["recipe"].to_parquet(target/"recipes.parquet",index=False)
                manifest["instances"].append(inst["instance_id"])
                a,t=fifo_schedule(inst); p=render(inst,a,t,cfg["dt_h"]); result=ledger(*p,cfg["dt_h"],topology="DC"); rec=p[1].sum()*cfg["dt_h"]*ElecParams().eta_rl_dc; shares[scenario].append((rec-result["self_use_kwh"])/rec if rec else 0.)
    if not manifest["instances"]: raise RuntimeError("No DS01 instances matched")
    ordered=sorted(manifest["instances"],key=lambda x: hashlib.sha256(x.encode()).digest())
    n=len(ordered); a=int(n*.6); b=int(n*.8)
    if a == 0 or b == a or b == n: raise ValueError("too few instances for nonempty splits")
    manifest["splits"]={"train":ordered[:a],"val":ordered[a:b],"test":ordered[b:]}
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    report=Path("reports/data/bench_v1_report.md"); report.parent.mkdir(parents=True,exist_ok=True)
    lines=["# Benchmark generator report", "", "Boundary: SIM_ASSUMED_PROFILE. DS01 abstract stage-3 duration and due dates mapped using ASSUMED unit_h; synthetic station power, phase power, station availability and events. DS03 EDC timing and observed sequence energy ratio are DERIVED; endpoints may differ in SOC, so ratio is not a closed-cycle efficiency. The DS03 transformer-side ratio is used as an assumed DUT-level proxy, not a measured DUT efficiency.", "", "FIFO residual-source share = (r - u)/r, where r = p_rec * eta_rl_dc and u = min(p_in / eta_sup_dc, r), summed over stations and steps. Ledger self_use supplies u. Phase lengths use constrained largest-remainder rounding to max(ceil(duration / dt), number of nonzero phases) steps, with at least one step per nonzero phase (short jobs are extended to make this feasible); starts are on the step grid. Scheduler slots use nominal whole-slot duration and report mixed charge/discharge slots.", "", "| Scenario | Runs | Mean share |", "|---|---:|---:|"]
    for s,x in shares.items(): lines.append(f"| {s} | {len(x)} | {np.mean(x):.6f} |")
    lines += ["", "Command: python -m regenate.data.generator --config configs/bench_v1.yaml", "Output: data/generated/bench_v1/manifest.json", "Recipe phase durations are synthetic rescaling of the first DS03 EDC sequence; the zero-duration rest is assumed because no rest was observed."]
    report.write_text("\n".join(lines)+"\n",encoding="utf-8"); print(f"SIM_ASSUMED_PROFILE: {len(manifest['instances'])} instances; {out / 'manifest.json'}")

if __name__ == "__main__": main()
