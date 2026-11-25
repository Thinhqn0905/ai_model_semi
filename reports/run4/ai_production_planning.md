# Run 4 WP-C — AI-assisted production planning (learned ETA in the scheduler) (D010; mentor M11, M12, M14)

Question: can the learned next-cycle duration (Run 3 AI18 gated model, T1 skill 0.60 on test, reports/run4/ai_eta.md) capture the
tardiness value that PERFECT duration information has (Run 3 PQd*: +0.048 h/instance)?
Boundary: SIM_DATA_PROFILE (DS06, held-out DS05 test cycles; scaling/windows ASSUMED). Default engine D006: rolling P0 + E1 limits
(AFE 20 kW, bus 32 kW, step 10 kW) + peak level; flex 0.25; 20 s per stage; n = 100 paired instances, seeds 0-99.
Same realised workloads, constraints, objective hierarchy (TT -> energy -> peak), solver budget and re-plan triggers for all rows;
the ONLY difference is the duration used for queued jobs. AI never changes recipes or required stress durations (it only changes
the planner's expectation of when a station becomes free).
Source: Drive `MyDrive/semiexpo/ai_runs/run4/v2_wpc_gated/results.csv` (P0, PQd = P-ETA-S, PQd* = ORACLE-T); ungated P-ETA in
`v2_wpc_ungated` (pending at time of writing). P-ETA-Q (P90 duration) not run: T1 P10-P90 coverage is 0.78 overall but 0.29 on the
abnormal cycles where the model acts, so a P90 bound would not be trustworthy (ai_eta.md).

## Results (mean per instance; paired 95 % CI vs P0, + = better than P0)
| | P0-E1-Peak | P-ETA-S (gated AI) | ORACLE-T (true duration) |
|---|---|---|---|
| total tardiness h | 0.1804 | 0.1750 | 0.1415 |
| TT saved vs P0 | - | +0.0054 [0.0000, +0.0158] (2 better / 0 worse, d = 0.11) | +0.0389 [+0.0101, +0.0744] (9 / 1, d = 0.23) |
| makespan h | 9.700 | 9.745 | 9.745 |
| net kWh | 8.4465 | 8.4739 | 8.4682 |
| kWh vs P0 | - | -0.0274 [-0.0437, -0.0123] | -0.0217 [-0.0366, -0.0078] |
| equal-TT kWh vs P0 | - | -0.0298 [-0.0462, -0.0152] (n=98) | -0.0214 [-0.0372, -0.0070] (n=90) |
| peak kW | 10.716 | 11.140 | 11.127 |
| peak vs P0 | - | -0.42 [-0.87, -0.01] | -0.41 [-0.93, +0.10] |
| violation count (all instances) | 1 | 2 | 0 |

Ungated P-ETA (same engine, `v2_wpc_ungated`, n = 100): TT saved -0.0083 h [-0.0317, +0.0113] (n.s.), kWh -0.051 [-0.080, -0.023]
(worse) -> the ungated model is worse than the gated one, as in Run 3.

## Verdict
- **P-ETA-S FAILS the WP-C acceptance**: it realises ~14 % of the perfect-duration tardiness value (0.0054 of 0.0389 h) and pays for
  it with significantly higher energy and peak. Not adopted for automatic scheduling (D010).
- On the default engine even PERFECT durations trade energy (+0.022 kWh) for tardiness (-0.039 h); on the energy-only engine (Run 3)
  they did not. A site that values throughput could accept that trade; it is a policy choice, not an AI result.
- Kept as an ETA ADVISORY service (station-available-time display, T1/T2 accuracy in ai_eta.md); no production benefit claimed.
