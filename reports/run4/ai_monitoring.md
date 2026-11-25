# Run 4 cycle monitoring

Boundary: PENDING_COLAB. DS05 completed-cycle summaries are unlabelled; natural scores and top flagged cycles are for engineer review and cannot establish accuracy or fault detection. The monitor is advisory only, and never replaces independent protection. Do not claim predictive maintenance, downtime reduction, or avoided failures.

Models fit on training cycles; thresholds are selected on validation cycles only. Each score uses the completed cycle and prior history within the same use case. The conditional quantile models use the Run 3 cycle-model lag features and log-ratio targets; P10 and P90 are independently fitted quantile regressions, and the score is distance outside their band. Statistical scores include previous-cycle recipe deviation, rolling quantiles, MAD, EWMA, Shewhart and CUSUM. Isolation Forest and one-class SVM are fitted on training summaries. Inference time includes sequential history calculations and batch model scoring; it is a local throughput estimate, not a real-time guarantee.

Controlled held-out stress tests separately apply duration x1.3, charge energy x1.2, RTE x0.9 and missing rest. They are labelled SYNTHETIC_INJECTED, never real faults. Report precision, recall, F1, PR-AUC and detection at each method's validation-selected threshold, with test normal false alarms per 1,000 cycles and per operating hour. Injected and normal examples are paired counterfactuals; their prevalence and the resulting precision/PR-AUC are artificial. Thresholds target a common validation false-alarm rate; achieved test rates can differ. No threshold is calibrated to an equipment protection limit.

PENDING_COLAB: natural score distributions, top cycles and features; synthetic metrics and achieved false-alarm rates; per-cycle inference time. Run `python -m regenate.forecasting.monitor --proc DIR --out DIR` and retain the output directory and manifest as evidence.

## Results (lead, Colab run of `python -m regenate.forecasting.monitor`, Drive `MyDrive/semiexpo/ai_runs/run4/monitor/`)
Boundary: natural scores on MEASURED DS05 cycles (no fault labels); detection metrics on SYNTHETIC_INJECTED perturbations of held-out
test cycles (never real faults); thresholds from val. 2,210 normal test cycles.
- Synthetic duration x1.3 at val-chosen thresholds: recall 0.01-0.29, precision ~0.50 for every method (recipe limits 0.08 / PR-AUC 0.67,
  quantile 0.04 / 0.72, CQR residual 0.08 / 0.66, CUSUM 0.29 at 286 false alarms per 1,000 normal cycles, Isolation Forest 0.05 / 0.50,
  One-Class SVM 0.05 / 0.50). Learned detectors are not better than the statistical baselines.
- Natural scores are dominated by structurally different cycles (FFR one-direction cycles, EFR 137 h cycle): top-ranked cycles are
  listed in natural_top.csv for engineer review only.
Verdict: **FAIL** for automatic anomaly detection at a usable false-alarm rate (the val-chosen thresholds flag ~4-8 % of normal cycles
while catching <= 9 % of injected deviations, except CUSUM). Kept only as an advisory "far from recipe" flag (the AI18 gate itself
already marks cycles whose predicted duration deviates); no predictive-maintenance claim.
