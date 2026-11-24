# Forecast benchmark

LOCAL_RUN; source observations MEASURED; forecasts and metrics DERIVED. DS04 manufacturing machines are not semiconductor test cells. Company A uses 5-minute and B 1-minute bins, stored split, exact future slot, and uncorrected extreme values. Features match ds04_bench: four completed power bins, rolling mean and standard deviation, hour, asset and status.

NMAE uses the training-target p99 absolute power, not rated power. Two candidate configurations per model selected by validation MAE; M0 and M1 repeat their deterministic configuration. M0 persistence point uses last observation, with training residual quantiles. Calibration uses nine quantiles; TCN intermediate quantiles are linearly interpolated between its three heads.

| dataset | horizon | model | nmae | skill_vs_persistence | coverage80 |
| --- | --- | --- | --- | --- | --- |
| A | 1 | M0 | 0.0245 | 0.0 | 0.9905 |
| A | 1 | M1 | 0.0254 | -0.0371 | 0.8576 |
| A | 1 | M2 | 0.0162 | 0.3374 | 0.8396 |
| A | 1 | M3 | 0.0174 | 0.2889 | 0.8455 |
| A | 1 | M4 | 0.0165 | 0.3248 | 0.8422 |
| A | 1 | M5 | 0.014 | 0.4275 | 0.9704 |
| A | 1 | M6 | 0.0221 | 0.0965 | 0.914 |
| A | 6 | M0 | 0.0223 | 0.0 | 0.9807 |
| A | 6 | M1 | 0.0305 | -0.3717 | 0.848 |
| A | 6 | M2 | 0.0223 | -0.0012 | 0.8388 |
| A | 6 | M3 | 0.0221 | 0.0062 | 0.8435 |
| A | 6 | M4 | 0.0219 | 0.017 | 0.8411 |
| A | 6 | M5 | 0.019 | 0.1444 | 0.9213 |
| A | 6 | M6 | 0.0236 | -0.06 | 0.8699 |
| A | 12 | M0 | 0.0254 | 0.0 | 0.9749 |
| A | 12 | M1 | 0.0335 | -0.3174 | 0.8426 |
| A | 12 | M2 | 0.027 | -0.0616 | 0.837 |
| A | 12 | M3 | 0.0266 | -0.0468 | 0.849 |
| A | 12 | M4 | 0.0258 | -0.0155 | 0.8444 |
| A | 12 | M5 | 0.0215 | 0.1552 | 0.9062 |
| A | 12 | M6 | 0.025 | 0.0175 | 0.3959 |
| B | 1 | M0 | 0.0124 | 0.0 | 0.8074 |
| B | 1 | M1 | 0.0155 | -0.2525 | 0.8147 |
| B | 1 | M2 | 0.0128 | -0.0344 | 0.7898 |
| B | 1 | M3 | 0.0132 | -0.0638 | 0.8011 |
| B | 1 | M4 | 0.013 | -0.0473 | 0.7988 |
| B | 1 | M5 | 0.0125 | -0.0083 | 0.9103 |
| B | 1 | M6 | 0.0124 | -0.0055 | 0.8774 |
| B | 6 | M0 | 0.0226 | -0.0 | 0.8093 |
| B | 6 | M1 | 0.0316 | -0.3959 | 0.8134 |
| B | 6 | M2 | 0.0257 | -0.1344 | 0.793 |
| B | 6 | M3 | 0.0257 | -0.1333 | 0.8107 |
| B | 6 | M4 | 0.0256 | -0.1297 | 0.8191 |
| B | 6 | M5 | 0.0217 | 0.0412 | 0.89 |
| B | 6 | M6 | 0.0226 | -0.0 | 0.8653 |
| B | 12 | M0 | 0.0287 | 0.0 | 0.8011 |
| B | 12 | M1 | 0.0399 | -0.3931 | 0.7994 |
| B | 12 | M2 | 0.0341 | -0.1883 | 0.7837 |
| B | 12 | M3 | 0.0342 | -0.1924 | 0.809 |
| B | 12 | M4 | 0.0339 | -0.1835 | 0.799 |
| B | 12 | M5 | 0.0278 | 0.0302 | 0.8825 |
| B | 12 | M6 | 0.0287 | -0.0025 | 0.8563 |
