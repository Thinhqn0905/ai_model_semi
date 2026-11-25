# Run 4: station availability and cycle ETA

Boundary: PENDING_COLAB. DS05 measured battery-cycling data is a proxy, not semiconductor-site evidence.

Train on the existing chronological per-module split; choose EWMA alpha and AI18 gates on validation only. T1 predicts cycle duration from earlier cycles; T2 predicts remaining minutes from observations before each 15-minute decision point starting at minute 60. Calibrate quantile intervals on validation using split CQR. True duration is used only for outcomes, abnormal-cycle labels and progress reporting. Accuracy does not establish production, energy, throughput or scheduling improvement. Report uncertainty and drift; interval coverage is not a guarantee.

| Task | Use case | Model | MAE / RMSE | Skill vs previous | Pinball | Coverage / width | Median APE | Latency |
|---|---|---|---|---|---|---|---|---|
| T1 / T2 | PENDING_COLAB | PENDING_COLAB | PENDING_COLAB | PENDING_COLAB | PENDING_COLAB | PENDING_COLAB | PENDING_COLAB | PENDING_COLAB |

Fill from metrics_T1.csv and metrics_T2.csv; include normal/abnormal subsets and T2 progress bins, sample counts and limitations. Do not infer site performance or production improvement from forecasting accuracy.
