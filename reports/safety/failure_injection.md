# Failure injection

Boundary: **SIM_ASSUMED_PROFILE**; bench_v1 S3 uses assumed station and recipe profiles. These checks demonstrate simulation logic only, not site safety or hardware protection. Results and decision logs are in [runs/fail_v1](../../runs/fail_v1/). The pytest gate determines pass or fail; inspect each case JSON for observed results and deadline violations.

| Failure | Expected observation | Evidence |
|---|---|---|
| Forecast wrong | Executed without overlap; deadlines reported | [forecast_wrong](../../runs/fail_v1/forecast_wrong.json) |
| Sensor loss | Stale observation and event logged | [sensor_loss](../../runs/fail_v1/sensor_loss.json) |
| MES disconnect | No accepted replan in disconnect window | [mes_disconnect](../../runs/fail_v1/mes_disconnect.json) |
| AFE saturation | Ledger violation flagged for rejection | [afe_saturation](../../runs/fail_v1/afe_saturation.json) |
| Bus overvoltage | Twin rejects synchronous burst | [bus_overvoltage](../../runs/fail_v1/bus_overvoltage.json) |
| Test delay | Delayed start, replanning and frozen jobs | [test_delay](../../runs/fail_v1/test_delay.json) |
| Engineer reject | Initial station order maintained | [engineer_reject](../../runs/fail_v1/engineer_reject.json) |
| Solver timeout | Fallback logged, plan kept | [solver_timeout](../../runs/fail_v1/solver_timeout.json) |
| Replanner exception | Fallback logged, plan kept | [replanner_exception](../../runs/fail_v1/replanner_exception.json) |

AFE screening is evaluated after replay; it is not integrated into Replay's approval gate. Twin screening is a separate assumed burst, not a hardware protection test. Solver timeout is detected after the callable returns.

Gate review: `pytest_retry.log` reports the test passed, but this does **not** establish the complete contract. The AFE case computes a rejection flag from the ledger after execution; it does not invoke an integrated validator. The delay case records accepted replans and checks no overlap, but does not assert that another queued job changed or independently verify frozen proposals. The `deadline_violations` field includes AFE violation steps because `score` combines both; consult `afe_violation_steps` separately. The expected/observed links above therefore describe available artifacts, not verified PASS for every contract assertion.
