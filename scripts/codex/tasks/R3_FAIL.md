# R3_FAIL — Run 3 failure injection v2: solver timeout, invalid AI prediction fallback, DS06 path (mentor M05, M06, M11, M14)
Account: default. Effort: medium.
Owner files: src/regenate/safety/failures.py, tests/test_failures.py, runs/run3/fail/**, reports/run3/failure_injection_v2.md
Read: AGENTS.md, docs/run3_plan.md, reports/safety/failure_injection.md, src/regenate/safety/failures.py, tests/test_failures.py,
  src/regenate/simulation/replay.py, src/regenate/optimization/rolling.py, src/regenate/forecasting/ai_engine.py (make_profile_fn,
  AIEngine.predict -> prediction_valid), tests/test_v2_campaign.py (synth() + StubEngine show how to build a bench-v2 instance
  without real data). Do not edit replay/rolling/ai_engine (lead owns them); add cases in failures.py only.
Contract (keep all existing cases and their outputs; new outputs go to runs/run3/fail/):
1. solver_timeout: Replanner with time_limit tiny (e.g. 1e-3 s) or a replanner that raises -> Replay keeps the previous accepted
   plan / fallback, no overlap, every job still runs, event logged.
2. ai_invalid: a stub engine returning prediction_valid=False and one raising an exception -> make_profile_fn returns the nominal
   recipe (AI-G10 fallback); the schedule equals the P0 schedule on the same synthetic bench-v2 instance.
3. ai_nan: stub engine returning NaN powers -> rejected as invalid (if not rejected, report it as an ISSUE with file:line; do not fix
   ai_engine yourself).
4. engineer_reject_all: engineer gate rejects every replan -> initial FIFO plan executes; KPIs equal FIFO DC (B2) on that instance.
5. Report table: failure, expected, observed, PASS/FAIL, evidence json; state that AI never controls protection, voltage stress,
   recipe or test duration (inspect the code paths and cite them).
Boundary SIM_ASSUMED_PROFILE (synthetic). Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_fail2 tests/test_failures.py`
passes and runs/run3/fail/*.json exist for the 4 new cases. Keep CPU light: synthetic instances, time limits <= 5 s.

## Run 2 (lead)
The NaN ISSUE you found is fixed by the lead in src/regenate/forecasting/ai_engine.py (non-finite power or remaining duration -> nominal recipe). Re-run only your ai_nan case, update its JSON and the report row (keep the history: found by R3_FAIL, fixed by lead), then the gate. Keep CPU light.
