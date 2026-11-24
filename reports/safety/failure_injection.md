# Failure injection

Boundary: **SIM_ASSUMED_PROFILE**; bench_v1 S3 uses assumed station and recipe profiles. These checks demonstrate simulation logic only, not site safety or hardware protection. Results and decision logs are in [runs/fail_v1](../../runs/fail_v1/). The pytest gate determines pass or fail; inspect each case JSON for observed results and deadline violations.

| Failure | Expected observation | Observed (retry) | Evidence |
|---|---|---|---|
| Forecast wrong | Executed without overlap; deadlines reported | PASS | [forecast_wrong](../../runs/fail_v1/forecast_wrong.json) |
| Sensor loss | Stale observation and event logged | PASS | [sensor_loss](../../runs/fail_v1/sensor_loss.json) |
| MES disconnect | No accepted replan in disconnect window | PASS | [mes_disconnect](../../runs/fail_v1/mes_disconnect.json) |
| AFE saturation | Ledger violation rejects candidate at approval gate | PASS | [afe_saturation](../../runs/fail_v1/afe_saturation.json) |
| Bus overvoltage | Twin rejects synchronous burst | PASS | [bus_overvoltage](../../runs/fail_v1/bus_overvoltage.json) |
| Test delay | Delayed start, another queued job changed, frozen plan unchanged | PASS | [test_delay](../../runs/fail_v1/test_delay.json) |
| Engineer reject | Initial station order maintained | PASS | [engineer_reject](../../runs/fail_v1/engineer_reject.json) |
| Solver timeout | Fallback logged, plan kept | PASS | [solver_timeout](../../runs/fail_v1/solver_timeout.json) |
| Replanner exception | Fallback logged, plan kept | PASS | [replanner_exception](../../runs/fail_v1/replanner_exception.json) |

AFE screening uses the replay approval callback for the injected case. Twin screening is a separate assumed burst, not a hardware protection test. Solver timeout is detected after the callable returns.

Gate: [run 3 output](../../runs/fail_v1/pytest_run3.log) passed. The timeout injection sleeps 2 s with a 0.5 s limit. The `deadline_violations` field includes AFE violation steps because `score` combines both; consult `afe_violation_steps` separately.
