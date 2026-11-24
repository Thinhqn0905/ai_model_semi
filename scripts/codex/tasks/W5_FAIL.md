# W5_FAIL — Failure injection + FMEA v2 (WP09.3)   [mentor M06 M11]
Account: .codex-C. Effort: medium.
Owner files: src/regenate/safety/failures.py, tests/test_failures.py, runs/fail_v1/**, reports/safety/failure_injection.md,
  reports/safety/fmea_v2.md
Read: AGENTS.md, docs/system_spec.md (1, 3, 6), src/regenate/simulation/replay.py (Replay API: events sensor_loss,
  mes_disconnect, delay; approve gate; max_solve_s fallback), src/regenate/optimization/rolling.py (Replanner(inst, mode,
  flex, time_limit)), src/regenate/simulation/bus_twin.py (check_plan), src/regenate/evaluation/oracle_campaign.py
  (load, score). Do not edit those modules.

## Contract
Scenario runner on 3 bench_v1 S3 instances (n=10, seed 0) with Replanner mode "P0", flex 0.25, time_limit 10:
| Failure | Injection | Expected behaviour (assert) |
| forecast wrong | replanner whose predictions are scaled x1.5 | plan still executed without overlap / deadline check reported |
| sensor loss | event sensor_loss on a station | obs marks stale; logged |
| MES disconnect | mes_disconnect 2 h | no replan accepted in window, plan kept |
| AFE saturation | ElecParams(P_afe_max small) | ledger afe_violation_steps > 0 -> plan flagged rejected by validator |
| bus overvoltage | synchronous burst plan into check_plan | rejected |
| test delay | delay event on a running-next job | job starts later, others re-planned, no frozen change |
| engineer reject | approve = lambda *_: False | realised == initial plan order |
| solver timeout | replanner sleeping > max_solve_s | fallback logged, plan kept |
| replanner exception | raises | fallback logged |
Each row writes runs/fail_v1/<case>.json (decision log, realised plan summary, ledger totals) and the report table
(expected vs observed, PASS/FAIL, boundary SIM_ASSUMED_PROFILE; proves simulation logic only).
fmea_v2.md: update slide-16 FMEA (S/O/D/RPN) with ReGenATE-specific modes, link each to the test above, remove
"speed change" as a mitigation (not a ReGenATE decision).
Gate: `python -m pytest -q tests/test_failures.py` all failure cases pass (use small time limits; total < 10 min).
