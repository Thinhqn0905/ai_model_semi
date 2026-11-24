# Bus stability KPI for rolling schedules

Boundary: **SIM_ASSUMED_PROFILE**. This checks simulation logic only; it is not hardware safety or measured performance. Synthetic S3 job phases and station ratings are assumed. True simulated powers are rendered from saved schedules. Residual source and sink exclude local self-use and auxiliary AC power. B1p-OPT is screened hypothetically on a shared bus; its actual topology has separate buses.

The B2 ledger peak imports exceed the default 20 kW AFE rating, indicating a sizing mismatch and motivating peak reduction. In the twin, steady-state AFE capacity must at least cover the net DC demand; transient excursions can occur even below that limit. Ledger import is AC-side and includes conversion and auxiliary effects, while the twin uses DC residuals; this is a sizing proxy, not a calibrated hardware requirement. AFE dynamics, droop, ramps and link limits can still cause excursions even with sufficient nominal capacity.

Each instance uses the same AFE cap across methods: default 20 kW, 1.2 times its B2 ledger peak import, or fixed 60 kW. All other twin defaults and boundary-window limitations are in [bus_twin.md](bus_twin.md). Integration stops immediately at the first undervoltage, so later events and energy are unobserved. Chopper energy covers simulated windows only. The negative control synchronizes every station at its assumed rated regenerative power with zero sink. Oracle schedules may be feasible time-limit incumbents.

## default

| Method | Evaluated / expected | Approved | v_min V (min / median / max) | v_max V (min / median / max) | i_peak A (min / median / max) | Chopper kWh (min / median / max) | Violation events by kind |
|---|---:|---:|---|---|---|---|---|
| B2 | 18 / 18 | 0/18 (0.0%) | 379.8 / 379.8 / 380 | 400 / 400 / 402.4 | 38.3 / 56.21 / 80.59 | 0 / 0 / 0 | overcurrent: 5, undervoltage: 18 |
| B1p-OPT | 18 / 18 | 0/18 (0.0%) | 379.8 / 379.9 / 380 | 400.9 / 404.3 / 408.3 | 50.74 / 65.75 / 86.93 | 0 / 0 / 0 | overcurrent: 6, undervoltage: 18 |
| P0 | 18 / 18 | 0/18 (0.0%) | 379.8 / 379.9 / 380 | 400 / 400.6 / 402.4 | 54.08 / 65.36 / 75.13 | 0 / 0 / 0 | undervoltage: 18 |
| P | 18 / 18 | 0/18 (0.0%) | 379.8 / 379.9 / 380 | 400 / 400 / 402.4 | 68.8 / 83.02 / 89.05 | 0 / 0 / 0 | overcurrent: 17, undervoltage: 18 |
| ORACLE | 18 / 18 | 0/18 (0.0%) | 379.8 / 379.9 / 380 | 400 / 400.5 / 402.1 | 54.56 / 66.21 / 78.99 | 0 / 0 / 0 | undervoltage: 18 |
| uncoordinated burst | 18 / 18 | 0/18 (0.0%) | 400 / 400 / 400 | 1533 / 1533 / 1533 | 103.5 / 103.5 / 103.5 | 0.01609 / 0.01609 / 0.01609 | overcurrent: 18, overvoltage: 18 |

## 1.2x B2 peak

| Method | Evaluated / expected | Approved | v_min V (min / median / max) | v_max V (min / median / max) | i_peak A (min / median / max) | Chopper kWh (min / median / max) | Violation events by kind |
|---|---:|---:|---|---|---|---|---|
| B2 | 18 / 18 | 0/18 (0.0%) | 379.8 / 379.9 / 380 | 400 / 400.9 / 412.6 | 77.05 / 92.88 / 109.2 | 0 / 0 / 0 | overcurrent: 44, undervoltage: 18 |
| B1p-OPT | 18 / 18 | 0/18 (0.0%) | 379.8 / 380 / 384.4 | 400.9 / 408.3 / 413.8 | 66.93 / 96.79 / 106.4 | 0 / 0 / 0 | overcurrent: 54, undervoltage: 12 |
| P0 | 18 / 18 | 5/18 (27.8%) | 380 / 382.7 / 387.1 | 400.5 / 405.3 / 408.4 | 63.1 / 81.64 / 99.58 | 0 / 0 / 0 | overcurrent: 32, undervoltage: 1 |
| P | 18 / 18 | 0/18 (0.0%) | 379.9 / 380 / 380.7 | 400 / 400 / 413 | 92.61 / 107.6 / 111.8 | 0 / 0 / 0 | overcurrent: 32, undervoltage: 14 |
| ORACLE | 18 / 18 | 7/18 (38.9%) | 380 / 383.4 / 386.6 | 400.4 / 402.7 / 405.9 | 62.81 / 82.14 / 112.8 | 0 / 0 / 0 | overcurrent: 17, undervoltage: 5 |
| uncoordinated burst | 18 / 18 | 0/18 (0.0%) | 400 / 400 / 400 | 419.3 / 419.3 / 419.3 | 111.3 / 111.3 / 111.3 | 0.01056 / 0.01056 / 0.01056 | overcurrent: 18 |

## fixed 60 kW

| Method | Evaluated / expected | Approved | v_min V (min / median / max) | v_max V (min / median / max) | i_peak A (min / median / max) | Chopper kWh (min / median / max) | Violation events by kind |
|---|---:|---:|---|---|---|---|---|
| B2 | 18 / 18 | 0/18 (0.0%) | 379.8 / 379.9 / 380 | 400 / 400.9 / 412.6 | 77.05 / 92.88 / 109.2 | 0 / 0 / 0 | overcurrent: 44, undervoltage: 18 |
| B1p-OPT | 18 / 18 | 0/18 (0.0%) | 379.8 / 380 / 384.4 | 400.9 / 408.3 / 413.8 | 66.93 / 96.79 / 106.4 | 0 / 0 / 0 | overcurrent: 54, undervoltage: 12 |
| P0 | 18 / 18 | 5/18 (27.8%) | 380 / 382.7 / 387.1 | 400.5 / 405.3 / 408.4 | 63.1 / 81.64 / 99.58 | 0 / 0 / 0 | overcurrent: 32, undervoltage: 1 |
| P | 18 / 18 | 0/18 (0.0%) | 379.9 / 380 / 380.7 | 400 / 400 / 413 | 92.61 / 107.6 / 111.8 | 0 / 0 / 0 | overcurrent: 32, undervoltage: 14 |
| ORACLE | 18 / 18 | 7/18 (38.9%) | 380 / 383.4 / 386.6 | 400.4 / 402.7 / 405.9 | 62.81 / 82.14 / 112.8 | 0 / 0 / 0 | overcurrent: 17, undervoltage: 5 |
| uncoordinated burst | 18 / 18 | 0/18 (0.0%) | 400 / 400 / 400 | 419.3 / 419.3 / 419.3 | 111.3 / 111.3 / 111.3 | 0.01056 / 0.01056 / 0.01056 | overcurrent: 18 |

## Failures and rejected plans

- n010_tau02_r00_S3_0 / B2 / default: rejected (undervoltage).
- n010_tau02_r00_S3_0 / B2 / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau02_r00_S3_0 / B2 / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau02_r00_S3_0 / B1p-OPT / default: rejected (undervoltage).
- n010_tau02_r00_S3_0 / B1p-OPT / 1.2x B2 peak: rejected (undervoltage).
- n010_tau02_r00_S3_0 / B1p-OPT / fixed 60 kW: rejected (undervoltage).
- n010_tau02_r00_S3_0 / P0 / default: rejected (undervoltage).
- n010_tau02_r00_S3_0 / P / default: rejected (undervoltage).
- n010_tau02_r00_S3_0 / P / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau02_r00_S3_0 / P / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau02_r00_S3_0 / ORACLE / default: rejected (undervoltage).
- n010_tau02_r00_S3_0 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau02_r00_S3_0 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r00_S3_0 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r00_S3_1 / B2 / default: rejected (undervoltage).
- n010_tau02_r00_S3_1 / B2 / 1.2x B2 peak: rejected (undervoltage).
- n010_tau02_r00_S3_1 / B2 / fixed 60 kW: rejected (undervoltage).
- n010_tau02_r00_S3_1 / B1p-OPT / default: rejected (undervoltage).
- n010_tau02_r00_S3_1 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r00_S3_1 / B1p-OPT / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r00_S3_1 / P0 / default: rejected (undervoltage).
- n010_tau02_r00_S3_1 / P0 / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r00_S3_1 / P0 / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r00_S3_1 / P / default: rejected (undervoltage).
- n010_tau02_r00_S3_1 / P / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau02_r00_S3_1 / P / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau02_r00_S3_1 / ORACLE / default: rejected (undervoltage).
- n010_tau02_r00_S3_1 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau02_r00_S3_1 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r00_S3_1 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r01_S3_0 / B2 / default: rejected (overcurrent, undervoltage).
- n010_tau02_r01_S3_0 / B2 / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau02_r01_S3_0 / B2 / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau02_r01_S3_0 / B1p-OPT / default: rejected (overcurrent, undervoltage).
- n010_tau02_r01_S3_0 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau02_r01_S3_0 / B1p-OPT / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau02_r01_S3_0 / P0 / default: rejected (undervoltage).
- n010_tau02_r01_S3_0 / P0 / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r01_S3_0 / P0 / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r01_S3_0 / P / default: rejected (undervoltage).
- n010_tau02_r01_S3_0 / P / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau02_r01_S3_0 / P / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau02_r01_S3_0 / ORACLE / default: rejected (undervoltage).
- n010_tau02_r01_S3_0 / ORACLE / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r01_S3_0 / ORACLE / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r01_S3_0 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau02_r01_S3_0 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r01_S3_0 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r01_S3_1 / B2 / default: rejected (undervoltage).
- n010_tau02_r01_S3_1 / B2 / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau02_r01_S3_1 / B2 / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau02_r01_S3_1 / B1p-OPT / default: rejected (undervoltage).
- n010_tau02_r01_S3_1 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau02_r01_S3_1 / B1p-OPT / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau02_r01_S3_1 / P0 / default: rejected (undervoltage).
- n010_tau02_r01_S3_1 / P0 / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r01_S3_1 / P0 / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r01_S3_1 / P / default: rejected (undervoltage).
- n010_tau02_r01_S3_1 / P / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r01_S3_1 / P / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r01_S3_1 / ORACLE / default: rejected (undervoltage).
- n010_tau02_r01_S3_1 / ORACLE / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r01_S3_1 / ORACLE / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r01_S3_1 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau02_r01_S3_1 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r01_S3_1 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r02_S3_0 / B2 / default: rejected (undervoltage).
- n010_tau02_r02_S3_0 / B2 / 1.2x B2 peak: rejected (undervoltage).
- n010_tau02_r02_S3_0 / B2 / fixed 60 kW: rejected (undervoltage).
- n010_tau02_r02_S3_0 / B1p-OPT / default: rejected (undervoltage).
- n010_tau02_r02_S3_0 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau02_r02_S3_0 / B1p-OPT / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau02_r02_S3_0 / P0 / default: rejected (undervoltage).
- n010_tau02_r02_S3_0 / P0 / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r02_S3_0 / P0 / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r02_S3_0 / P / default: rejected (overcurrent, undervoltage).
- n010_tau02_r02_S3_0 / P / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau02_r02_S3_0 / P / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau02_r02_S3_0 / ORACLE / default: rejected (undervoltage).
- n010_tau02_r02_S3_0 / ORACLE / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau02_r02_S3_0 / ORACLE / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau02_r02_S3_0 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau02_r02_S3_0 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r02_S3_0 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r02_S3_1 / B2 / default: rejected (undervoltage).
- n010_tau02_r02_S3_1 / B2 / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau02_r02_S3_1 / B2 / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau02_r02_S3_1 / B1p-OPT / default: rejected (undervoltage).
- n010_tau02_r02_S3_1 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r02_S3_1 / B1p-OPT / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r02_S3_1 / P0 / default: rejected (undervoltage).
- n010_tau02_r02_S3_1 / P0 / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r02_S3_1 / P0 / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r02_S3_1 / P / default: rejected (overcurrent, undervoltage).
- n010_tau02_r02_S3_1 / P / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau02_r02_S3_1 / P / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau02_r02_S3_1 / ORACLE / default: rejected (undervoltage).
- n010_tau02_r02_S3_1 / ORACLE / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r02_S3_1 / ORACLE / fixed 60 kW: rejected (overcurrent).
- n010_tau02_r02_S3_1 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau02_r02_S3_1 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau02_r02_S3_1 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau05_r00_S3_0 / B2 / default: rejected (undervoltage).
- n010_tau05_r00_S3_0 / B2 / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau05_r00_S3_0 / B2 / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau05_r00_S3_0 / B1p-OPT / default: rejected (undervoltage).
- n010_tau05_r00_S3_0 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau05_r00_S3_0 / B1p-OPT / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau05_r00_S3_0 / P0 / default: rejected (undervoltage).
- n010_tau05_r00_S3_0 / P / default: rejected (overcurrent, undervoltage).
- n010_tau05_r00_S3_0 / P / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau05_r00_S3_0 / P / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau05_r00_S3_0 / ORACLE / default: rejected (undervoltage).
- n010_tau05_r00_S3_0 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau05_r00_S3_0 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau05_r00_S3_0 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau05_r00_S3_1 / B2 / default: rejected (undervoltage).
- n010_tau05_r00_S3_1 / B2 / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau05_r00_S3_1 / B2 / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau05_r00_S3_1 / B1p-OPT / default: rejected (undervoltage).
- n010_tau05_r00_S3_1 / B1p-OPT / 1.2x B2 peak: rejected (undervoltage).
- n010_tau05_r00_S3_1 / B1p-OPT / fixed 60 kW: rejected (undervoltage).
- n010_tau05_r00_S3_1 / P0 / default: rejected (undervoltage).
- n010_tau05_r00_S3_1 / P / default: rejected (undervoltage).
- n010_tau05_r00_S3_1 / P / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau05_r00_S3_1 / P / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau05_r00_S3_1 / ORACLE / default: rejected (undervoltage).
- n010_tau05_r00_S3_1 / ORACLE / 1.2x B2 peak: rejected (overcurrent).
- n010_tau05_r00_S3_1 / ORACLE / fixed 60 kW: rejected (overcurrent).
- n010_tau05_r00_S3_1 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau05_r00_S3_1 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau05_r00_S3_1 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau05_r01_S3_0 / B2 / default: rejected (undervoltage).
- n010_tau05_r01_S3_0 / B2 / 1.2x B2 peak: rejected (undervoltage).
- n010_tau05_r01_S3_0 / B2 / fixed 60 kW: rejected (undervoltage).
- n010_tau05_r01_S3_0 / B1p-OPT / default: rejected (undervoltage).
- n010_tau05_r01_S3_0 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau05_r01_S3_0 / B1p-OPT / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau05_r01_S3_0 / P0 / default: rejected (undervoltage).
- n010_tau05_r01_S3_0 / P0 / 1.2x B2 peak: rejected (overcurrent).
- n010_tau05_r01_S3_0 / P0 / fixed 60 kW: rejected (overcurrent).
- n010_tau05_r01_S3_0 / P / default: rejected (overcurrent, undervoltage).
- n010_tau05_r01_S3_0 / P / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau05_r01_S3_0 / P / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau05_r01_S3_0 / ORACLE / default: rejected (undervoltage).
- n010_tau05_r01_S3_0 / ORACLE / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau05_r01_S3_0 / ORACLE / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau05_r01_S3_0 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau05_r01_S3_0 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau05_r01_S3_0 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau05_r01_S3_1 / B2 / default: rejected (undervoltage).
- n010_tau05_r01_S3_1 / B2 / 1.2x B2 peak: rejected (undervoltage).
- n010_tau05_r01_S3_1 / B2 / fixed 60 kW: rejected (undervoltage).
- n010_tau05_r01_S3_1 / B1p-OPT / default: rejected (undervoltage).
- n010_tau05_r01_S3_1 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent).
- n010_tau05_r01_S3_1 / B1p-OPT / fixed 60 kW: rejected (overcurrent).
- n010_tau05_r01_S3_1 / P0 / default: rejected (undervoltage).
- n010_tau05_r01_S3_1 / P0 / 1.2x B2 peak: rejected (undervoltage).
- n010_tau05_r01_S3_1 / P0 / fixed 60 kW: rejected (undervoltage).
- n010_tau05_r01_S3_1 / P / default: rejected (overcurrent, undervoltage).
- n010_tau05_r01_S3_1 / P / 1.2x B2 peak: rejected (overcurrent).
- n010_tau05_r01_S3_1 / P / fixed 60 kW: rejected (overcurrent).
- n010_tau05_r01_S3_1 / ORACLE / default: rejected (undervoltage).
- n010_tau05_r01_S3_1 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau05_r01_S3_1 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau05_r01_S3_1 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau05_r02_S3_0 / B2 / default: rejected (overcurrent, undervoltage).
- n010_tau05_r02_S3_0 / B2 / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau05_r02_S3_0 / B2 / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau05_r02_S3_0 / B1p-OPT / default: rejected (undervoltage).
- n010_tau05_r02_S3_0 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau05_r02_S3_0 / B1p-OPT / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau05_r02_S3_0 / P0 / default: rejected (undervoltage).
- n010_tau05_r02_S3_0 / P0 / 1.2x B2 peak: rejected (overcurrent).
- n010_tau05_r02_S3_0 / P0 / fixed 60 kW: rejected (overcurrent).
- n010_tau05_r02_S3_0 / P / default: rejected (overcurrent, undervoltage).
- n010_tau05_r02_S3_0 / P / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau05_r02_S3_0 / P / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau05_r02_S3_0 / ORACLE / default: rejected (undervoltage).
- n010_tau05_r02_S3_0 / ORACLE / 1.2x B2 peak: rejected (overcurrent).
- n010_tau05_r02_S3_0 / ORACLE / fixed 60 kW: rejected (overcurrent).
- n010_tau05_r02_S3_0 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau05_r02_S3_0 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau05_r02_S3_0 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau05_r02_S3_1 / B2 / default: rejected (undervoltage).
- n010_tau05_r02_S3_1 / B2 / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau05_r02_S3_1 / B2 / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau05_r02_S3_1 / B1p-OPT / default: rejected (undervoltage).
- n010_tau05_r02_S3_1 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent).
- n010_tau05_r02_S3_1 / B1p-OPT / fixed 60 kW: rejected (overcurrent).
- n010_tau05_r02_S3_1 / P0 / default: rejected (undervoltage).
- n010_tau05_r02_S3_1 / P / default: rejected (undervoltage).
- n010_tau05_r02_S3_1 / P / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau05_r02_S3_1 / P / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau05_r02_S3_1 / ORACLE / default: rejected (undervoltage).
- n010_tau05_r02_S3_1 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau05_r02_S3_1 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau05_r02_S3_1 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r00_S3_0 / B2 / default: rejected (undervoltage).
- n010_tau08_r00_S3_0 / B2 / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r00_S3_0 / B2 / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r00_S3_0 / B1p-OPT / default: rejected (overcurrent, undervoltage).
- n010_tau08_r00_S3_0 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r00_S3_0 / B1p-OPT / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r00_S3_0 / P0 / default: rejected (undervoltage).
- n010_tau08_r00_S3_0 / P0 / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r00_S3_0 / P0 / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r00_S3_0 / P / default: rejected (overcurrent, undervoltage).
- n010_tau08_r00_S3_0 / P / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r00_S3_0 / P / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r00_S3_0 / ORACLE / default: rejected (undervoltage).
- n010_tau08_r00_S3_0 / ORACLE / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r00_S3_0 / ORACLE / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r00_S3_0 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau08_r00_S3_0 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r00_S3_0 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r00_S3_1 / B2 / default: rejected (undervoltage).
- n010_tau08_r00_S3_1 / B2 / 1.2x B2 peak: rejected (undervoltage).
- n010_tau08_r00_S3_1 / B2 / fixed 60 kW: rejected (undervoltage).
- n010_tau08_r00_S3_1 / B1p-OPT / default: rejected (undervoltage).
- n010_tau08_r00_S3_1 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r00_S3_1 / B1p-OPT / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r00_S3_1 / P0 / default: rejected (undervoltage).
- n010_tau08_r00_S3_1 / P0 / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r00_S3_1 / P0 / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r00_S3_1 / P / default: rejected (overcurrent, undervoltage).
- n010_tau08_r00_S3_1 / P / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r00_S3_1 / P / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r00_S3_1 / ORACLE / default: rejected (undervoltage).
- n010_tau08_r00_S3_1 / ORACLE / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r00_S3_1 / ORACLE / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r00_S3_1 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau08_r00_S3_1 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r00_S3_1 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r01_S3_0 / B2 / default: rejected (undervoltage).
- n010_tau08_r01_S3_0 / B2 / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r01_S3_0 / B2 / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r01_S3_0 / B1p-OPT / default: rejected (overcurrent, undervoltage).
- n010_tau08_r01_S3_0 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r01_S3_0 / B1p-OPT / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r01_S3_0 / P0 / default: rejected (undervoltage).
- n010_tau08_r01_S3_0 / P0 / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r01_S3_0 / P0 / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r01_S3_0 / P / default: rejected (overcurrent, undervoltage).
- n010_tau08_r01_S3_0 / P / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r01_S3_0 / P / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r01_S3_0 / ORACLE / default: rejected (undervoltage).
- n010_tau08_r01_S3_0 / ORACLE / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r01_S3_0 / ORACLE / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r01_S3_0 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau08_r01_S3_0 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r01_S3_0 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r01_S3_1 / B2 / default: rejected (undervoltage).
- n010_tau08_r01_S3_1 / B2 / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r01_S3_1 / B2 / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r01_S3_1 / B1p-OPT / default: rejected (undervoltage).
- n010_tau08_r01_S3_1 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r01_S3_1 / B1p-OPT / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r01_S3_1 / P0 / default: rejected (undervoltage).
- n010_tau08_r01_S3_1 / P0 / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r01_S3_1 / P0 / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r01_S3_1 / P / default: rejected (overcurrent, undervoltage).
- n010_tau08_r01_S3_1 / P / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r01_S3_1 / P / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r01_S3_1 / ORACLE / default: rejected (undervoltage).
- n010_tau08_r01_S3_1 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau08_r01_S3_1 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r01_S3_1 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r02_S3_0 / B2 / default: rejected (undervoltage).
- n010_tau08_r02_S3_0 / B2 / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r02_S3_0 / B2 / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r02_S3_0 / B1p-OPT / default: rejected (undervoltage).
- n010_tau08_r02_S3_0 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r02_S3_0 / B1p-OPT / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r02_S3_0 / P0 / default: rejected (undervoltage).
- n010_tau08_r02_S3_0 / P / default: rejected (overcurrent, undervoltage).
- n010_tau08_r02_S3_0 / P / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r02_S3_0 / P / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r02_S3_0 / ORACLE / default: rejected (undervoltage).
- n010_tau08_r02_S3_0 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau08_r02_S3_0 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r02_S3_0 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r02_S3_1 / B2 / default: rejected (undervoltage).
- n010_tau08_r02_S3_1 / B2 / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r02_S3_1 / B2 / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r02_S3_1 / B1p-OPT / default: rejected (undervoltage).
- n010_tau08_r02_S3_1 / B1p-OPT / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r02_S3_1 / B1p-OPT / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r02_S3_1 / P0 / default: rejected (undervoltage).
- n010_tau08_r02_S3_1 / P0 / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r02_S3_1 / P0 / fixed 60 kW: rejected (overcurrent).
- n010_tau08_r02_S3_1 / P / default: rejected (overcurrent, undervoltage).
- n010_tau08_r02_S3_1 / P / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r02_S3_1 / P / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r02_S3_1 / ORACLE / default: rejected (undervoltage).
- n010_tau08_r02_S3_1 / ORACLE / 1.2x B2 peak: rejected (overcurrent, undervoltage).
- n010_tau08_r02_S3_1 / ORACLE / fixed 60 kW: rejected (overcurrent, undervoltage).
- n010_tau08_r02_S3_1 / uncoordinated burst / default: rejected (overcurrent, overvoltage).
- n010_tau08_r02_S3_1 / uncoordinated burst / 1.2x B2 peak: rejected (overcurrent).
- n010_tau08_r02_S3_1 / uncoordinated burst / fixed 60 kW: rejected (overcurrent).

Command: `python runs/twin_check/run.py`
Evidence: [results_run2.json](../../runs/twin_check/results_run2.json) and [run2.log](../../runs/twin_check/run2.log).
