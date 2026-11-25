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

## Product configuration: P0 + E1 limits + peak level (`v2_e1_peak`, same 50 instances)
Peak level on top of E1 (paired vs E1 energy-only): ORACLE -0.224 kW [0.055, 0.500] at +0.0002 kWh; P0 -0.301 kW [-0.029, +0.679]
(n.s.) at -0.003 kWh (n.s.). Peak vs B1p-OPT (optimised in-rack, 14.32 kW mean): P0 -3.67 kW [2.51, 4.78] (-25.6 %), wins 40/50.
P0 tardiness 0.235 h vs 0.174 h for one-shot methods (rolling P0 is not given the true durations); FIFO B2 has 3 AFE-shortfall
violations in 50 instances, all optimised plans 0.

## Run 4 WP-E joint AFE / bus sizing inside the MILP (Colab runtime 3; Drive `ai_runs/run4_rt3/`, `sizing_summary.csv`)
Same 30 DS06 instances (seeds 0-29), E1 step 10 kW, peak level on; (20, 32) = the E1 reference run. Violations = deadline misses +
AFE-shortfall slots in the ledger (for FIFO B2 the AFE cap also removes imported energy, so its kWh is not comparable when violated).
| AFE kW | bus kW | ORACLE solved | ORACLE peak kW | P0 violations | P0 peak kW | B2 violations |
|---|---|---|---|---|---|---|
| 10 | 32 | 27/30 (3 infeasible at the TT stage) | 7.87 | 15 | 8.85 | 66 |
| 15 | 32 | 30/30 | 8.62 | 1 | 10.04 | 16 |
| 15 | 24 | 30/30 | 8.62 | 1 | 10.07 | 16 |
| 20 | 16 | 30/30 | 8.59 | 0 | 10.19 | 0 |
| 20 | 24 | 30/30 | 8.81 | 0 | 10.23 | 0 |
| 20 | 32 | 30/30 | 8.81 | 0 | 10.23 | 0 |
| 30 | 32 | 30/30 | 8.81 | 0 | 10.23 | 0 |
Energy is unchanged across feasible configurations (ORACLE 8.43 kWh, P0 8.53 kWh per instance). Reading: for this 48 kW-rated cell
the coordinated plans need ~15-20 kW of AFE (FIFO B2 fails below 20 kW); bus throughput >= 16 kW never binds after local reuse; a 10 kW
AFE makes 10 % of workloads infeasible. Feasibility target (>= 90 % within the envelope) met for AFE >= 15 kW (100 %) and borderline at
10 kW (90 %). AFE sizing changes hardware cost (not included in FIN-B, which assumes existing infrastructure). Simulation only.
