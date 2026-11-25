# Run 3 WP-E1 — Electrical limits inside the optimizer (instead of post-scheduling rejection only)

Mentor references: M04 (losses/accounting), M06 (bus stability, independent protection), M11 (hard production constraints).
Boundary: **SIM_DATA_PROFILE** (DS06: measured DS05 cycle shapes; station scaling, windows, bus/AFE parameters ASSUMED);
the twin is a simulation screen, not hardware qualification. Independent hardware protection remains mandatory.

## Implementation
`src/regenate/optimization/milp.py` (DC topology), parameters in `ElecParams`:
- `P_afe_max` (existing): central AFE import cap per slot.
- `P_bus_max` (new): total residual DC sink and total residual DC source per slot <= cap (proxy of the twin's link-current
  check I = max(sum source, sum sink)/V).
- `dP_step_max` (new): |net residual DC demand(k) - net(k-1)| <= cap (proxy of the AFE transient at slot boundaries).
Exactness: brute-force equality tests with binding caps (`tests/test_milp.py::test_bus_limits_match_bruteforce`).
Screening tool: `src/regenate/simulation/screen_v2.py` (TRUE traces, residual after local self-use, `bus_twin.check_plan`,
default TwinParams: 400 V, 380-420 V, 0.04 F, AFE 20 kW, 80 A link).

## Campaign
DS06 seeds 0-49 (test-split cycles), flex 0.25, 20 s limit, Colab, limits `{"P_afe_max": 20, "P_bus_max": 32, "dP_step_max": 10}`
(32 kW = 80 A x 400 V; 10 kW step ASSUMED). Sources: `MyDrive/semiexpo/ai_runs/run3/v2_e1/results.csv`, unlimited reference
`v2_diag` (same 50 instances), screening `screen_e1.csv`. All one-shot MILPs optimal.

## Results
Cost of the limits (limited minus unlimited, same instances, paired 95 % CI):
| Method | energy change kWh | peak change kW |
|---|---|---|
| ORACLE | +0.0021 [+0.0006, +0.0043] | -0.76 |
| P0 | +0.0028 [-0.0069, +0.0127] (n.s.) | -0.55 |
| B1p-OPT (in-rack; caps do not apply) | 0 | 0 |
Mean P0 tardiness unchanged (0.250 h both). Kill test with limits: B1p-OPT -> ORACLE 1.092 kWh [1.018, 1.167], 50/50;
B1p-OPT -> P0 0.982 kWh [0.902, 1.064], 50/50. FIFO B2 has 0.06 AFE-shortfall violations per instance (ledger) under the 20 kW cap.

Twin approval (50 instances per cell):
| Method | unlimited MILP | with E1 limits | rejection causes (unlimited) |
|---|---|---|---|
| B2 (FIFO shared DC) | 94 % | 94 % (no optimisation) | 3 overcurrent+UV |
| B1p-OPT (hypothetical on a shared bus) | 92 % | 92 % | 3 overcurrent+UV, 1 UV |
| ORACLE | 98 % | **100 %** | 1 overcurrent+UV |
| P0 | 100 % | 100 % | - |
Mean max slot step of net residual demand: ORACLE 8.5 -> 7.6 kW, P0 11.2 -> 10.2 kW; peak residual sink 13.6 -> 13.0 kW (ORACLE).

## Interpretation
- With measured-cycle stations (~6 kW each, 8 stations) the 20 kW AFE / 80 A link of the screen is adequate for coordinated
  plans; the Run 2 rejection rates (bench_v1, assumed S3 profiles) were a sizing artefact of those larger assumed powers
  (reports/safety/bus_stability_kpi.md). Uncoordinated FIFO and in-rack plans still fail 6-8 % of instances.
- Putting the limits inside the MILP costs ~0.002 kWh (0.03 %) and removes the remaining ORACLE rejection while lowering peak:
  feasibility-by-construction is cheap. Status **PASS (simulation level)** for "integrate physical feasibility into the
  optimizer"; hardware/bus qualification **NOT_VERIFIED**.

## Limitations
dP_step_max = 10 kW is an assumed proxy, not derived from a measured AFE bandwidth; the twin uses boundary windows (+-2 s) and
lumped parameters; DS05 module powers are scaled (25 modules/station); n = 50.
