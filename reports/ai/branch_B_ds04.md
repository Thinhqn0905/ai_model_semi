# Forecast benchmark

LOCAL_RUN; source observations MEASURED; forecasts and metrics DERIVED. DS04 manufacturing machines are not semiconductor test cells. Company A uses 5-minute and B 1-minute bins, stored split, exact future slot, and uncorrected extreme values. Features are four completed power bins; other DS04 baseline features are excluded for common model input.

NMAE uses the training-target p99 absolute power, not rated power. One fixed configuration per model; no hyperparameter selection. M0 persistence point uses last observation, with training residual quantiles. Only the three directly predicted quantiles are calibrated.

| dataset | horizon | model | nmae | skill_vs_persistence | coverage80 |
| --- | --- | --- | --- | --- | --- |
| A | 1 | M0 | 0.0245 | 0.0 | 0.9905 |
| A | 1 | M1 | 0.0215 | 0.1208 | 0.8538 |
| A | 1 | M2 | 0.0169 | 0.3106 | 0.8378 |
| A | 1 | M3 | 0.018 | 0.2659 | 0.8718 |
| A | 1 | M4 | 0.0178 | 0.273 | 0.8721 |
| A | 1 | M5 | 0.0151 | 0.3855 | 0.9566 |
| A | 1 | M6 | 0.0203 | 0.1709 | 0.8146 |
| A | 6 | M0 | 0.0223 | 0.0 | 0.9807 |
| A | 6 | M1 | 0.0232 | -0.041 | 0.8794 |
| A | 6 | M2 | 0.0216 | 0.029 | 0.8584 |
| A | 6 | M3 | 0.0225 | -0.0128 | 0.8677 |
| A | 6 | M4 | 0.022 | 0.0108 | 0.8941 |
| A | 6 | M5 | 0.0202 | 0.0908 | 0.8813 |
| A | 6 | M6 | 0.0224 | -0.0084 | 0.8625 |
| A | 12 | M0 | 0.0254 | 0.0 | 0.9749 |
| A | 12 | M1 | 0.0261 | -0.0293 | 0.8797 |
| A | 12 | M2 | 0.0246 | 0.0298 | 0.8476 |
| A | 12 | M3 | 0.0253 | 0.005 | 0.9011 |
| A | 12 | M4 | 0.0252 | 0.0072 | 0.8846 |
| A | 12 | M5 | 0.0229 | 0.1004 | 0.8992 |
| A | 12 | M6 | 0.0251 | 0.0114 | 0.8069 |
| B | 1 | M0 | 0.0124 | 0.0 | 0.8074 |
| B | 1 | M1 | 0.0134 | -0.082 | 0.8091 |
| B | 1 | M2 | 0.0129 | -0.0436 | 0.7885 |
| B | 1 | M3 | 0.0134 | -0.0803 | 0.7999 |
| B | 1 | M4 | 0.0135 | -0.0949 | 0.7959 |
| B | 1 | M5 | 0.0151 | -0.2182 | 0.9106 |
| B | 1 | M6 | 0.012 | 0.0282 | 0.8817 |
| B | 6 | M0 | 0.0226 | -0.0 | 0.8093 |
| B | 6 | M1 | 0.026 | -0.1467 | 0.8151 |
| B | 6 | M2 | 0.0266 | -0.1761 | 0.7832 |
| B | 6 | M3 | 0.0268 | -0.1855 | 0.8011 |
| B | 6 | M4 | 0.0264 | -0.1658 | 0.8065 |
| B | 6 | M5 | 0.0238 | -0.0524 | 0.8884 |
| B | 6 | M6 | 0.022 | 0.0301 | 0.8825 |
| B | 12 | M0 | 0.0287 | 0.0 | 0.8011 |
| B | 12 | M1 | 0.0339 | -0.1837 | 0.8061 |
| B | 12 | M2 | 0.0345 | -0.2049 | 0.7723 |
| B | 12 | M3 | 0.0346 | -0.206 | 0.7876 |
| B | 12 | M4 | 0.0342 | -0.1946 | 0.7931 |
| B | 12 | M5 | 0.0293 | -0.021 | 0.8671 |
| B | 12 | M6 | 0.0281 | 0.0188 | 0.8458 |
