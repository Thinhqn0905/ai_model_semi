# W2_GEN — Unified ReGenATE benchmark generator   [WP04, mentor M02 M07 M08 M13]
Account: default. Effort: medium.
Owner files: src/regenate/data/generator.py, src/regenate/data/recipes.py, configs/bench_v1.yaml,
  tests/test_generator.py, reports/data/bench_v1_report.md, data/generated/bench_v1/**
Read: AGENTS.md, docs/system_spec.md (all), docs/decisions.md (D001), src/regenate/electrical/ledger.py
  (interface only), src/regenate/data/ds01.py (interface), reports/data/ds01_report.md,
  reports/data/ds03_report.md (EDC section). Do not edit other modules.

## Contract
Scenarios (recipes.py, every number carries provenance ASSUMED / DERIVED(DS03 EDC) / DATASHEET):
- S1 converter burn-in (negative control): stress phase p_in = rated*load, p_rec = eta_dut*p_in,
  eta_dut in [0.85, 0.95]; ramp-up/ramp-down phases with p_rec = 0; chamber p_aux.
- S2 dynamic converter load: load steps per recipe (e.g. 25/50/75/100 % cycles), p_rec = eta_dut(load)*p_in.
- S3 energy-storage / bidirectional cycling: phases charge (p_in > 0, p_rec = 0), discharge (p_in = 0,
  p_rec > 0), rest; phase lengths and round-trip efficiency derived from DS03 EDC cycles (DERIVED),
  with a config switch to scale them. No phase pattern without a stated basis.
- recipes table: recipe_id, scenario, phase_idx, kind, dur_frac, p_in_frac, p_rec_frac, p_aux_kw, provenance.

Instances (generator.py), deterministic from (ds01 instance id, scenario, seed):
- Jobs from a DS01 instance: n jobs, sizes, due dates; burn-in duration = p_stage3_u * unit_h where
  `unit_h` is a config parameter (ASSUMED, default 1.0, swept later) — report the mapping as ASSUMED.
- Columns: job_id, recipe_id, release_h, due_h (soft, tardiness), deadline_h (hard), dur_nom_h,
  dur_true_h (= dur_nom * (1+eps), eps ~ N(0, sigma_dur) clipped), kappa_true (power multiplier),
  eligible_stations (list), max_shift_h (allowed start window).
- Stations: N in {4, 8, 16, 32}, identical rated power p_rated_kw (config), one job per station at a time.
- Operational events: random station downtime windows (prob per day, mean length) and release delays.
- Splits: instance-level train/val/test lists (60/20/20 by seed hash), written to manifest.json.
- `render(inst, assign, starts_h, dt_h, truth=True) -> (p_in, p_rec, p_aux)` arrays (S, K) for
  regenate.electrical.ledger; truth=False uses nominal duration and kappa=1 (what a planner knows).
  Jobs are never interrupted; durations and recipes never changed by the renderer.
- `fifo_schedule(inst)` reference schedule: release order, earliest free eligible station, no shift.
- CLI: `python -m regenate.data.generator --config configs/bench_v1.yaml` writes
  data/generated/bench_v1/<instance_id>/{jobs,stations}.parquet + manifest.json (+ provenance per column group).
  bench_v1 config: DS01 n in {10, 20}, tau {0.2, 0.5, 0.8}, reps 0..2, scenarios S1, S2, S3,
  N = 8 stations, sigma_dur 0.10, 5 seeds.

## Gate
`python -m pytest -q tests/test_generator.py`: determinism (same seed -> identical files), physics
(S1/S2: p_rec <= p_in every step; S3: never p_in > 0 and p_rec > 0 at the same station and step),
render energy = sum over phases (tolerance 1e-9), FIFO schedule respects release, eligibility,
one-job-per-station, no interruption; and a smoke that ledger(render(fifo)) runs for all four topologies
and ELEC-09 holds for S1 (DC == B1p). Report bench_v1_report.md with residual-source share per scenario
under FIFO: (recoverable - self_use)/recoverable from the DC ledger, label SIM_ASSUMED_PROFILE.

## Run 2 (lead 2026-11-24) — fix the two failures, keep everything else
1. Phase quantisation: every phase length is rounded to an integer number of render steps (>= 1 step,
   largest-remainder rounding so the total job duration in steps is preserved); a job's start is always on
   the step grid. Then S3 can never have p_in > 0 and p_rec > 0 in the same step. Record the rounding rule.
   Durations used by the MILP are in scheduler slots: provide `job_slot_profile(inst, job, slot_h)` that
   returns per-slot mean p_in, p_rec, p_aux with the job duration ceil-ed to whole slots, plus a flag if a
   slot mixes charge and discharge (allowed at slot level, reported as `mixed_slots`).
2. Splits: assign by sorting instances on a stable hash and cutting 60/20/20 so no split is empty;
   test asserts all three non-empty and disjoint.
3. Residual-source share in the report: use the DC-side definition (r - u)/r with r = p_rec*eta_rl_dc,
   u = min(p_in/eta_sup_dc, r) from the ledger outputs, so S1 should be 0.
Gate unchanged.
