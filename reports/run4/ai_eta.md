# Run 4: station availability and cycle ETA

Boundary: PENDING_COLAB. DS05 measured battery-cycling data is a proxy, not semiconductor-site evidence.

Train on the existing chronological per-module split; choose EWMA alpha and AI18 gates on validation only. T1 predicts cycle duration from earlier cycles; T2 predicts remaining minutes from observations before each 15-minute decision point starting at minute 60. Calibrate quantile intervals on validation using split CQR. True duration is used only for outcomes, abnormal-cycle labels and progress reporting. Accuracy does not establish production, energy, throughput or scheduling improvement. Report uncertainty and drift; interval coverage is not a guarantee.

| Task | Use case | Model | MAE / RMSE | Skill vs previous | Pinball | Coverage / width | Median APE | Latency |
|---|---|---|---|---|---|---|---|---|
| T1 / T2 | PENDING_COLAB | PENDING_COLAB | PENDING_COLAB | PENDING_COLAB | PENDING_COLAB | PENDING_COLAB | PENDING_COLAB | PENDING_COLAB |

Fill from metrics_T1.csv and metrics_T2.csv; include normal/abnormal subsets and T2 progress bins, sample counts and limitations. Do not infer site performance or production improvement from forecasting accuracy.

## Results (lead, Colab run of `python -m regenate.forecasting.eta`, commit ba44c54; Drive `MyDrive/semiexpo/ai_runs/run4/eta/`)
Boundary: LOCAL_RUN on MEASURED DS05 cycles, held-out test split (unchanged Run 2/3 split), selection/calibration on val.
Units: minutes. Skill = 1 - MAE/MAE(previous cycle). "abnormal" = |log(true dur / previous dur)| > log 1.5 (reporting only).

T1 — total duration before the cycle starts (n = 2,210 test cycles)
| Model | MAE | skill | coverage80 | predict ms |
|---|---|---|---|---|
| previous cycle (recipe) | 290.7 | 0 | - | 0 |
| median of last 5 | 293.6 | -0.01 | - | 0 |
| EWMA | 269.3 | +0.07 | - | 0 |
| ridge / RF / XGBoost / LightGBM (point, raw target) | 950 / 552 / 1,307 / 589 | -2.27 / -0.90 / -3.50 / -1.03 | - | <0.03 |
| quantile LightGBM P50 (+CQR) | 188.5 | +0.35 | 0.710 -> **0.780** | 0.033 |
| **AI18 gated (Run 3 model)** | **116.5** | **+0.60** (reproduces Run 3 0.599) | - | 0.012 |
Normal cycles: previous 7.9, AI18 10.2 (slightly worse), QLGBM-CQR 78.2 (coverage 0.85); abnormal: previous 2,240, AI18 849,
QLGBM 949 (coverage 0.29). Per use case AI18 skill: Day Ahead 0.51, EFR 0.65, TOU 0.66, PV 0.41, PV-TOU -0.08, FFR 0.
Reading: the gain is concentrated in abnormal (long) cycles; on normal cycles the recipe is already almost exact and the gate keeps
it (small loss 7.9 -> 10.2 min). Point tree models on the raw duration target are far worse than the recipe (they do not anchor on
the previous cycle); only ratio-to-recipe models (AI18, quantile LGBM) beat it.

T2 — remaining duration during a cycle (decision points every 15 min from minute 60; n = 24,141)
| Model | MAE all | skill | 0-25 % | 25-50 % | 50-75 % | 75-100 % | coverage80 | width80 |
|---|---|---|---|---|---|---|---|---|
| previous cycle | 154.4 | 0 | 428.1 | 184.6 | 114.2 | 70.8 | - | - |
| **random forest** | **62.0** | **+0.60** | 109.6 (+0.74) | 58.3 (+0.68) | 46.3 (+0.59) | 63.1 (+0.11) | - | - |
| quantile LightGBM P50 + CQR | 99.6 | +0.36 | 178.7 | 89.9 | 86.9 | 90.9 (-0.29) | **0.756** | 338 |
Normal cycles: RF 32.9 vs 47.3 (skill 0.30); abnormal: RF 226.9 vs 760.3 (0.70). Latency: RF 0.009 ms, QLGBM 0.036 ms per sample.
Calibration: remaining-duration P10-P90 coverage stays below nominal (0.756 after CQR; 0.71 in the last quarter of a cycle), the
same under-coverage seen in Run 2 (0.755) -> P90 remaining duration must not be used as a guaranteed bound.

## Gates
G06 (AI operational value): **PASS for ETA accuracy** — two learned tasks beat strong non-AI baselines on held-out measured data
(T1 AI18 +0.60, T2 RF +0.60). Calibration: T1 PASS (0.78 ~ 0.80), T2 PARTIAL (0.756). Production benefit: not implied by accuracy;
see the WP-C downstream test (reports/run4/ai_production_planning.md).

## Optional deep learning: TCN on GPU (T2 remaining duration) — `ai_runs/run4/eta_tcn/`
Tesla T4, 30 epochs, 1,006 s training, lookback 240 min, same samples/split as eta.py T2. MAE 104.1 min (skill 0.33 vs previous cycle)
vs random forest 62.0 (0.60); by progress 0-25 % 240.6 (0.44), 25-50 % 110.4 (0.40), 50-75 % 81.8 (0.28), 75-100 % 71.6 (-0.01).
P10-P90 coverage 0.702 -> 0.767 after CQR (closer to nominal than QLGBM 0.756). Inference 0.16 ms/sample GPU, 0.19 ms CPU.
Verdict: deep temporal model NOT justified for accuracy (worse than RF); its calibrated interval is marginally better. RF stays the
remaining-duration model; AI18 gated stays the before-start model.
