# W3_REPLAY — SimPy replay environment for rolling-horizon control   [WP07 / WP11 shadow emulator, mentor M05 M11 M14]
Account: default. Effort: medium.
Owner files: src/regenate/simulation/replay.py, tests/test_replay.py, reports/product/replay.md
Read: AGENTS.md, docs/system_spec.md (3, 6, 10), src/regenate/data/generator.py (load/render/fifo API),
  src/regenate/evaluation/oracle_campaign.py (functions `load`, `execute`, `score` — reuse, do not copy),
  src/regenate/optimization/milp.py (Job/solve signature only).

## Contract
A discrete-event shadow-mode emulator; it executes, it does not optimise.
- `Replay(inst, initial_plan, replanner=None, period_h=0.25, approve=None, seed=0)`:
  * plan = {job_id: (station, planned_start_h)}; jobs start at max(planned_start, release, station free,
    station back from downtime); true duration from inst (never revealed to the replanner before the job ends).
  * every `period_h` it builds an observation: t_h, jobs done / running (station, start_h, elapsed_h, observed
    partial power trace so far at dt_h from render(truth=True) up to t), queued jobs (release, due, deadline,
    dur_nom_h, recipe), station availability known now; calls `replanner(obs) -> new plan for NOT-started jobs`
    (running / done jobs are frozen: any change to them is rejected and logged).
  * engineer gate: `approve(old_plan, new_plan, obs) -> bool` (default approve-all); rejected -> keep old plan;
    failures (replanner exception, timeout `max_solve_s`, infeasible plan) -> keep the last valid plan (fallback),
    log the reason.
  * events: station downtime from stations.downtime_json; optional injected events list
    [(t_h, kind, payload)] for kinds `sensor_loss` (obs marks the station stale), `mes_disconnect`
    (no replan during window), `delay` (job start delayed).
- Output: final realised {job_id: (station, start_h)} usable by oracle_campaign.score(), and a decision log
  DataFrame (t_h, event, accepted, reason, solve_s).
Gate: `python -m pytest -q tests/test_replay.py`: with replanner=None the replay of a FIFO plan equals
oracle_campaign.execute() on the same instance; frozen-job modification is rejected; replanner exception ->
fallback keeps the previous plan; engineer reject keeps old plan; downtime respected (no job overlaps a downtime
window on its station); determinism by seed.
