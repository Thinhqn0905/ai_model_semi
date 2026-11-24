# ReGenATE AI plan v1 (lead) — follows the user's AI plan 2026-11-25, adjusted by D001/D002

## Role of AI (mentor p1, p6, Q2c, Q3b)
AI predicts; the constrained MILP decides. Three outputs per station: Model A source/sink power trajectory
(two channels, never net), Model B remaining duration / station-available time (never changes qualified stress time),
Model C P10/P50/P90 for both (quantile heads, calibrated). Value is judged only downstream: dE_AI = E_P0 - E_P with
paired CI on the same realised workload, same optimizer, constraints, horizon and compute budget (AI-G08/G09).

## Branches (separate train/test per domain, shared framework `regenate.forecasting.framework`)
| Branch | Data | Task | Status |
|---|---|---|---|
| A | DS02 SHIFT2DC LVDC | bus / infeed power multi-step | worker default (W5_AIFW) |
| B | DS04 SME | machine power, cycle time | worker default (W5_AIFW) |
| C | DS05 Lboro second-life battery sweat test (Chroma 17020, CC BY 4.0, doi 10.17028/rd.lboro.28732490.v2) | charge/discharge power, phase duration, energy matching | lead, Colab |
| D | DS06 = ReGenATE bench v2 (S3 stations driven by DS05 cycles) | multi-station source/sink + remaining duration + quantiles -> scheduler | lead |
DS01 = scheduling context, DS03 = physics (efficiency curves), not trained on.

## Why bench v2 (D002)
bench_v1 deviations are i.i.d. -> no model can beat nominal. Bench v2 replays REAL DS05 cycles as station jobs:
duration/power variation then comes from real battery state (SoH, temperature, use-case recipe), partly observable
from M2 telemetry and history (previous cycles of the same cell). No synthetic structure is added to favour AI.
Features allowed at decision time: recipe/use case, cell history (previous cycles' capacity, duration, energy, IR proxy),
elapsed telemetry of the running cycle. Never: the future of the current cycle.

## Models (equal tuning budget, val only)
AI00 recipe nominal, AI01 persistence / last-cycle, AI02 per-recipe median, AI03 linear, AI04 RF, AI05 XGBoost,
AI06 LightGBM, AI10 quantile LightGBM, AI09 TCN (GPU, Colab T4/L4), AI11 physics-informed residual
(P_hat = P_physics(recipe, DS03 efficiency, cell capacity estimate) + learned residual, then projection to limits).

## Ablation with the same rolling MILP (regenate.optimization.rolling)
P0 nominal | P1 power AI | P2 duration AI | P3 joint | P4 joint + quantile-robust (P90 duration for station availability,
P50 power) | P5 physics-informed | ORACLE. Final "P" chosen on validation instances only.

## Gates AI-G01..G10 as in the user plan; fail -> recommend optimisation-only (mentor p6).

## Splits
DS05: by cell (battery) and by time — test cells never seen in training; within-cell chronological for history features.
Bench v2 instances: built only from test-split cells for the final ladder.
