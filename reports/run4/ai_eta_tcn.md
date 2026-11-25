# T2 temporal convolution: PENDING_COLAB

Boundary: NOT_VERIFIED_INPUT_DATA until the Colab DS05 run is inspected. DS05 battery cycling is a proxy, not semiconductor-site evidence.

Use the ETA T2 chronological split and identical decision keys. Four past-only minute-bin channels are zero-padded at cycle start; the ETA T2 features and use-case indicators accompany the causal temporal convolution. Train quantile heads on log1p remaining minutes with pinball loss, validation early stopping and a fixed seed; convert to minutes and calibrate intervals using validation CQR. True duration is used only for targets, reporting progress and abnormal labels. GPU mixed precision is enabled when requested. The manifest records runtime and CPU/GPU inference timings, including input loading.

Run on Colab: `python -m regenate.forecasting.eta_tcn --proc DIR --out DIR --device cuda --lookback 240 --epochs 30`. Compare matched rows of `metrics_tcn.csv` against RF and quantile LightGBM in the corresponding ETA `metrics_T2.csv`, including progress and normal/abnormal subsets. Verify sample keys and inputs before interpreting differences.

| Model | MAE | Skill vs previous | Coverage80 | Boundary |
|---|---|---|---|---|
| RF | 62.0 min | 0.60 | Not applicable | LOCAL_RUN, measured DS05 held-out test; reports/run4/ai_eta.md |
| Quantile LightGBM + CQR | 99.6 min | 0.36 | 0.756 | LOCAL_RUN, measured DS05 held-out test; reports/run4/ai_eta.md |
| TCN / TCN + CQR | PENDING_COLAB | PENDING_COLAB | PENDING_COLAB | NOT_VERIFIED |

The baseline values above are prior reported results, not a verified matched comparison with this run. Forecast accuracy and interval coverage do not establish energy or production benefit; coverage is not a guarantee.
