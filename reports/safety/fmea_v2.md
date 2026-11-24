# FMEA v2

Boundary: **SIM_ASSUMED_PROFILE**. S/O/D scores below are provisional engineering judgments, not measured failure rates; RPN = S × O × D. Reassess with site data and protection engineering. Tests demonstrate simulation behavior only.

| Failure mode | Effect | Mitigation | S | O | D | RPN | Test |
|---|---|---|---:|---:|---:|---:|---|
| Wrong forecast | Late tests or poor energy matching | Deadline check and engineer review | 8 | 5 | 4 | 160 | [forecast](../../runs/fail_v1/forecast_wrong.json) |
| Lost sensor | Stale state | Mark stale and review | 7 | 4 | 4 | 112 | [sensor](../../runs/fail_v1/sensor_loss.json) |
| MES disconnected | Commands unavailable | Keep existing plan | 7 | 4 | 3 | 84 | [MES](../../runs/fail_v1/mes_disconnect.json) |
| AFE saturated | Electrical limit exceeded | Reject on ledger flag; independent hardware protection | 9 | 3 | 3 | 81 | [AFE](../../runs/fail_v1/afe_saturation.json) |
| Bus overvoltage | Equipment damage | Twin screening and independent protection | 10 | 3 | 3 | 90 | [bus](../../runs/fail_v1/bus_overvoltage.json) |
| Test delayed | Schedule disruption | Replan queued jobs; freeze running jobs | 7 | 4 | 3 | 84 | [delay](../../runs/fail_v1/test_delay.json) |
| Engineer rejects | Plan not authorised | Keep initial order | 5 | 3 | 2 | 30 | [approval](../../runs/fail_v1/engineer_reject.json) |
| Solver timeout | Stale schedule | Keep existing plan and log fallback | 6 | 4 | 3 | 72 | [timeout](../../runs/fail_v1/solver_timeout.json) |
| Replanner exception | No new schedule | Keep existing plan and log fallback | 6 | 3 | 3 | 54 | [exception](../../runs/fail_v1/replanner_exception.json) |

Screening and independent hardware protection require integration and validation before deployment.
