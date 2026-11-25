# Failure injection v2

Boundary: **SIM_ASSUMED_PROFILE**. One synthetic bench-v2 instance uses generated DS05-like cycles; this is a simulation check, not evidence of hardware or site safety. The FIFO DC comparison uses the same instance and electrical parameters.

| Failure | Expected | Observed | Result | Evidence |
|---|---|---|---|---|
| Solver timeout | Keep accepted plan; all jobs run without overlap; log failure | Injected TimeoutError; plan retained, all jobs ran without overlap, event logged | PASS | [JSON](../../runs/run3/fail/solver_timeout.json) |
| Invalid AI / exception | Nominal recipe fallback; same schedule as P0 | Both fallback profiles and realized schedules matched P0 | PASS | [JSON](../../runs/run3/fail/ai_invalid.json) |
| NaN power | Reject invalid prediction | Inconsistent validity flag with NaN powers returned the finite nominal profile | PASS | [JSON](../../runs/run3/fail/ai_nan.json) |
| Engineer rejects all | Execute initial FIFO; match FIFO DC KPIs | Initial plan executed and recorded numeric ledger outputs matched FIFO DC | PASS | [JSON](../../runs/run3/fail/engineer_reject_all.json) |

R3_FAIL originally found that a stub marking NaN powers valid could pass nonfinite values through. The lead fixed the profile fallback; this rerun confirms the nominal profile is returned ([ai_engine.py:196](../../src/regenate/forecasting/ai_engine.py#L196)).

In the inspected simulation paths, AI supplies a scheduling forecast, not protection or voltage-stress control; approval is an external callback ([replay.py:108](../../src/regenate/simulation/replay.py#L108)). The nominal recipe is used for fallback and execution duration comes from the instance's true duration ([replay.py:29](../../src/regenate/simulation/replay.py#L29), [replay.py:120](../../src/regenate/simulation/replay.py#L120)); AI does not alter the actual recipe or test duration in these paths. This is not a claim about external deployments.

Pytest gate: PASS, `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_fail2 tests/test_failures.py`; [run output](../../runs/run3/fail/pytest_fail2_run2.log). Boundary: SIM_ASSUMED_PROFILE.
