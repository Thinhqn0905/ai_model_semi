# Raw-result binding manifest (lead, 2026-11-25; full JSON on Drive `MyDrive/semiexpo/ai_runs/drive_manifest.json`)
Computed on Colab runtime 2 from the Drive files themselves (sha256 = first 16 hex). All files are SIM_DATA_PROFILE (DS06) unless noted;
facility files = SIM cell + MEASURED DS07. Use this table to replace NOT_VERIFIED raw-result bindings in the reports.

## DS06 campaign files (status of one-shot MILPs, mean tardiness, violation counts)
| Drive path | sha256 | n inst | one-shot status | TT_h (one-shot / P0) | violations |
|---|---|---|---|---|---|
| ai_runs/v2_flex025_n100.csv (Run 2 ladder) | 5a97158f145ea3b5 | 100 | all optimal, gap 0; B3: 99 optimal + 1 infeasible (TT stage) | 0.14 / P0 0.188, B3 0.271, P1-P4 0.187-0.202 | 0 all |
| ai_runs/v2_flex1/results.csv (flex 1.0) | 43b3f53afd3a6284 | 26 | **ORACLE 17/26 and B3 18/26 time-limit INCUMBENTS (gap > 0)**; rest optimal | 0.061 / P0 0.405 | 0 |
| ai_runs/v2_peak/results.csv | f1d8b3aa4fedd61f | 50 | all optimal | 0.174 / P0 0.240, B3 0.318 | 0 |
| ai_runs/run3/v2_diag/results.csv | 4a8d6b74b0c8a154 | 100 | all optimal, gap 0 | 0.14 / P0 0.188, TR_RUN 0.174, TR_Q/TR_ALL 0.14 | 0 |
| ai_runs/run3/v2_p5 / v2_pq_gated / v2_pq_ungated / v2_pqd / v2_pqstar | 08e1bf44 / 9a345636 / 17331443 / 42be5793 / 0b3e7234 | 100 each | rolling only | P0 0.188 in every file (identical P0) | 0 |
| ai_runs/run3/v2_e1/results.csv (E1 limits) | 6fec39385077a926 | 50 | all optimal | 0.174 / P0 0.250 | B2 3 (AFE shortfall) |
| ai_runs/run3/v2_e1_peak/results.csv | 6f56722501fa8770 | 50 (seeds 0-49) | all optimal | 0.174 / P0 0.235 | B2 3 |
| ai_runs/run4_rt2/v2_e1_peak_b/results.csv | 6b7b13b2c0f59075 | 50 (seeds 50-99) | all optimal | 0.105 / P0 0.125 | B2 10, P0 1 |
| ai_runs/run4_rt2/v2_e1_peak100/results.csv (merged default engine) | 57cd90452ba6e187 | 100 | all optimal | 0.14 / P0 0.18 | B2 13, P0 1 |
| ai_runs/run4/v2_wpc_gated / v2_wpc_ungated (WP-C) | f346ca242945923d / 176ec98bfbe7f7a0 | 100 | rolling | P0 0.180, PQd 0.175 / 0.189, PQd* 0.142 | P0 1, PQd 2 |
| ai_runs/run4_rt3/v2_size_afe10_bus32 | ad65c2b5dcde9508 | 30 | ORACLE 27 optimal + **3 infeasible** | 0.121-0.135 / P0 0.174 | B2 66, P0 15 |
| ai_runs/run4_rt3/v2_size_afe15_bus32 / _bus24 | 915b2959 / 97cb62c0 | 30 | all optimal | 0.121 / 0.174 | B2 16, P0 1 |
| ai_runs/run4_rt3/v2_size_afe20_bus16 / _bus24, afe30_bus32 | 9b253122 / 49e7062767 / b0b1fe62 | 30 | all optimal | 0.121 / 0.174 | 0 |

## Facility files (70 = 10 factories x 7 months unless noted)
| Drive path | sha256 | rows | facility-months |
|---|---|---|---|
| run4/fac_grid (General rule, 1 cell) | 6e669d46a861fe54 | 420 | 70 |
| run4/fac_grid_tnb (ToU rule, 1 cell) | dd3ded7dbdac9347 | 420 | 70 |
| run4/fac_grid_tnb_3cells, fac_tou_5cells, fac_tou_10cells | 74177c2a / 53e74ab0 / 055b9ff9 | 350 each | 70 |
| run4/fac_gen_3cells, _5cells, _10cells | 7455a70f / 1263d44d / 7d0bf4f6 | 350 each | 70 |
| run4/fac_grid_tnb_ai (PQd at facility) | e601af37042b5ddf | 280 | 70 |
| run4_rt2/fac_gen_1cell_n100, fac_tou_1cell_n100 | f015fa19 / 7c1c86d6 | 350 each | 70 |
| run4_rt2/fac_tou_hol_1cells, _5cells | b07c5178 / 4442b193 | 140 each | 70 |
| run4/fac_p0bill_{Forge_1,Forge_2,Metal_1,Metal_3,Paper,Steel_1} | 3f97864b / f9b5e7b8 / 443e386b / 40072 0c6 / 469be4dd / fb2731dd | 8-10 each | 2 each (12 total) |
| run4/fac_p0bill5_{Forge_2,Metal_1} | f427310b / 150ec779 | 4 each | 1 each |
| run4/fin_fac_{gen,tou}_fx{0.21,0.24}/clustered_summary.csv | cea2e596 / 4371d9b7 / cc7cf179 / f8d9ed54 | 16 each | - |

## Reconciliation facts (replace NOT_VERIFIED with these)
- Solver: every DS06 one-shot MILP is optimal with gap 0 EXCEPT (a) flex 1.0 run: ORACLE 17/26 and B3 18/26 are time-limited incumbents ->
  the "-13.3 % at flex 1.0" result is a lower bound on the oracle saving, not a certified optimum; (b) B3 1 infeasible in the Run 2 ladder (n=99);
  (c) AFE 10 kW: ORACLE 3/30 infeasible.
- Tardiness: rolling P0 always has higher mean tardiness than one-shot methods (they know true durations): 0.18-0.25 h vs 0.105-0.174 h. Energy
  comparisons P0 vs one-shot are therefore not at equal production; equal-TT subsets are reported where stated (e.g. lex() tables in reports).
- Violations: FIFO B2 under the 20 kW AFE cap 13/100 instances (E1 default engine), P0-E1-Peak 1/100, optimised one-shot 0; PQd 2/100.
- Baselines are matched by instance_id within each file; across files P0 is identical (diag vs p5/pq*/pqd P0 rows identical).
