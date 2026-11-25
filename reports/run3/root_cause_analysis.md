# Run 3 WP-A — Why AI did not improve downstream energy (root-cause analysis)

Mentor references: M09 (strong baselines + Oracle), M12 (AI incremental benefit), M13 (paired statistics), M14 (AI predicts,
optimizer decides). Source of the requirement: `Instruction/Mentor_Feedback.md` (AI-necessity rule: if the optimizer alone is
almost as good, recommend the simpler solution).

## 1. Objective and hypothesis
Run 2 found P1-P4 (AI forecasts for running jobs) 0.2-0.3 % worse than P0 although the forecasters beat the recipe baseline
(Branch C skill 0.3-0.7). Hypotheses: (H1) the forecasts are not good enough; (H2) the way forecasts enter the scheduler loses
the information; (H3) the physical/information headroom is intrinsically small; (H4) the one-shot ORACLE is not a matched
upper bound for a rolling policy.

## 2. Dataset and provenance
DS06 (bench v2): stations replay MEASURED DS05 test-split cycles (Loughborough second-life battery sweat test, CC BY 4.0,
doi:10.17028/rd.lboro.28732490.v2); scaling (25 modules/station), windows and 8 stations ASSUMED -> boundary **SIM_DATA_PROFILE**.
Colab runtime (8 CPU), code commit `2420de0`, Drive `MyDrive/semiexpo/ai_runs/run3/v2_diag/results.csv`, seeds 0-99,
flex 0.25, time limit 20 s, 10 jobs/instance. Local DS05 rebuild from `DS5.zip` gave the same 14,755 valid cycles / 2 errors
as the Colab build (`runs/ds05_local_build.log`).

## 3. Configuration (information decomposition, same rolling MILP for every row)
| Method | Running jobs | Queued jobs |
|---|---|---|
| P0 | recipe (previous cycle) | recipe |
| TR_RUN | TRUE profile | recipe |
| TR_Q | recipe | TRUE profile |
| TR_ALL (rolling oracle) | TRUE | TRUE |
| P1*..P4* | Run 2 integration (3-horizon interpolation / warped recipe) fed PERFECT forecasts | recipe |
Diagnostic variants are not deployable (they read the future); they measure where the headroom is.

## 4. Reproducibility check (Run 2 vs Run 3, same seeds)
Mean net kWh per instance: P0 8.446 (Run 2 8.45), B1p-OPT 9.446 (9.45), ORACLE 8.352 (8.35), B1 11.524 (11.52).
Kill test B1p-OPT -> ORACLE 1.094 kWh [1.037, 1.148], 100/100 (Run 2: identical). All 200 one-shot MILPs (B1p-OPT, ORACLE)
returned status optimal with mip_gap 0 -> these are certified optima, not incumbents. 0 constraint violations.

## 5. Results (paired vs P0, positive = better than P0, 95 % bootstrap CI, n = 100)
| Method | kWh saved vs P0 | share of headroom | wins | peak kW vs P0 | wins |
|---|---|---|---|---|---|
| TR_ALL (rolling oracle) | +0.094 [+0.077, +0.112] | 1.00 | 94 | +1.12 [+0.59, +1.65] | 66 |
| ORACLE (one-shot) | +0.094 [+0.077, +0.112] | 1.00 | 94 | +1.14 [+0.57, +1.72] | 65 |
| TR_Q (perfect queued info) | +0.049 [+0.035, +0.064] | 0.52 | 74 | +0.82 [+0.31, +1.36] | 61 |
| TR_RUN (perfect running info) | +0.024 [+0.013, +0.037] | 0.26 | 59 | +0.16 [-0.25, +0.57] | 32 |
| P1* (perfect power, Run 2 integration) | -0.005 [-0.017, +0.007] | -0.05 | 31 | -0.52 [-1.11, +0.05] | 29 |
| P2* (perfect duration, warped recipe) | +0.000 [-0.009, +0.009] | 0.00 | 30 | -0.02 [-0.36, +0.33] | 23 |
| P3* / P4* (perfect joint) | -0.009 [-0.022, +0.003] | -0.10 | 32 | -0.27 [-0.86, +0.32] | 30 |
TR_ALL vs ORACLE: difference exactly 0 on all 100 instances. Mean tardiness: P0 0.188 h, TR_RUN 0.174 h, TR_Q/TR_ALL/ORACLE 0.140 h.

## 6. Interpretation (status per hypothesis)
- **H4 rejected.** Rolling re-planning with perfect information reaches the one-shot ORACLE exactly, so the P0 -> ORACLE gap
  (0.094 kWh, 1.1 %) is pure information value; the rolling policy itself loses nothing.
- **H3 confirmed (partly).** The total information headroom is small: 0.094 kWh/instance = 1.1 % of P0 energy, vs 1.094 kWh for
  the shared-DC topology + scheduling itself. Energy savings of ReGenATE are carried by topology + optimisation, not by forecasting.
- **H2 confirmed for the Run 2 design.** With PERFECT forecasts, the Run 2 integration captures 0 % (P2*) or loses (P1*, P3*, P4*)
  of the available running-job headroom (TR_RUN = 26 %). Main defects: (a) power is known only at 3 horizons (15 min, 1 h, 4 h)
  and linearly interpolated between them, which smears phase transitions; (b) beyond 4 h the elapsed-time-indexed recipe is kept,
  so the tail is misaligned with the phases; (c) a perfect remaining duration applied by uniform time-warping of the recipe shape
  moves every transition, which is not how these cycles deviate (AI14: transitions are mostly at recipe times; deviations are
  concentrated in a few phases). The Run 2 negative AI result is therefore an integration failure, NOT evidence that the
  forecasting models are useless.
- **H1 not the bottleneck** for P1-P4: even perfect inputs do not help through that integration.
- **Largest AI opportunity is queued jobs (52 %)**: forecasting the next cycle of a module before it starts. Run 2 never used AI
  for queued jobs (no telemetry before start). Run 3 tests a cycle-level model (`cycle_model.py`, variants PQ/PQ5) for this.

## 7. Limitations
DS05 battery modules are not semiconductor DUTs; station scaling and time windows are assumed; flex 0.25 only in this campaign;
the decomposition shares are means of small differences (CIs above). One seed set (0-99).

## 8. Status and next action
Root cause: **identified** (integration + small intrinsic headroom; queued-job information is the main lever). Next: P5/P5s
(phase-aligned running-job trajectory), PQ/PQ5 (cycle-level queued-job forecast with AI18 gate) on the same 100 instances;
decision rule unchanged: AI is adopted only if P beats P0 with a paired CI excluding 0.
