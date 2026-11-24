# Rolling ladder

Boundary: SIM_ASSUMED_PROFILE; bench_v1 synthetic assumed power profiles. D002: i.i.d. uncertainty makes P vs P0 a control, not an AI claim.

Net M0 kWh, import peak, matching ratio, tardiness and makespan are means over available instances; violations include AFE violation steps. Bus voltage excursions are not simulated.

| Method | n | net kWh | peak kW | matching ratio | TT h | makespan h | completed | violations |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B0 | 36 | 350.7 | 60.31 | 0 | 0.03472 | 11.56 | 10 | 0 |
| B1 | 36 | 107.8 | 36.94 | 0 | 0.03472 | 11.56 | 10 | 0 |
| B1-OPT | 36 | 107.8 | 30.4 | 0 | 0 | 13.57 | 10 | 0 |
| B1p | 36 | 93.91 | 35.82 | 0 | 0.03472 | 11.56 | 10 | 0 |
| B1p-OPT | 36 | 93.91 | 28.84 | 0 | 0 | 13.55 | 10 | 0 |
| B2 | 36 | 92.02 | 35.8 | 0.298 | 0.03472 | 11.56 | 10 | 0 |
| B3 | 36 | 91.33 | 25.42 | 0.407 | 0.03472 | 13.81 | 10 | 0 |
| P0 | 36 | 91.32 | 25.06 | 0.4073 | 0.05556 | 14.58 | 10 | 0 |
| P | 36 | 91.78 | 30.82 | 0.3371 | 0.05556 | 12.54 | 10 | 0 |
| ORACLE | 36 | 91.17 | 25.28 | 0.4316 | 0 | 13.88 | 10 | 0 |

## Equal tardiness

| Comparison | n | mean kWh | 95% paired bootstrap CI |
|---|---:|---:|---:|
| B1 -> B0 (regen hardware) | 36 | 242.9 | [214, 271.2] |
| B2 vs B1 (shared DC, same FIFO) | 36 | 15.78 | [13.27, 18.23] |
| B3 vs B2 (static optimisation) | 34 | 0.6263 | [0.3627, 0.9162] |
| P0 vs B3 (rolling adaptation) | 34 | 0.003694 | [-0.05567, 0.07159] |
| P vs P0 (AI forecast, dE_AI) | 32 | -0.426 | [-0.6032, -0.2575] |
| P vs B1-OPT | 35 | 16.25 | [13.78, 18.63] |
| P vs B1p-OPT (kill test) | 35 | 2.099 | [1.385, 2.834] |
| ORACLE vs P (oracle gap) | 35 | 0.5596 | [0.3605, 0.7716] |
| ORACLE vs B1p-OPT (ceiling of shared DC) | 36 | 2.736 | [1.839, 3.646] |
| B1 minus B1-OPT | 34 | 1.254e-15 | [-8.359e-15, 1.129e-14] |
| B1 minus B1p | 36 | 13.89 | [10.75, 16.93] |
| B1 minus B1p-OPT | 34 | 14.42 | [11.22, 17.51] |
| B1 minus B2 | 36 | 15.78 | [13.27, 18.23] |
| B1 minus B3 | 34 | 16.84 | [14.51, 19.13] |
| B1 minus P0 | 32 | 16.41 | [14.02, 18.76] |
| B1 minus P | 33 | 16.66 | [14.15, 19.16] |
| B1 minus ORACLE | 34 | 16.98 | [14.7, 19.22] |

## All instances (tardiness may differ)

| Comparison | n | mean kWh | 95% paired bootstrap CI |
|---|---:|---:|---:|
| B1 -> B0 (regen hardware) | 36 | 242.9 | [214, 271.2] |
| B2 vs B1 (shared DC, same FIFO) | 36 | 15.78 | [13.27, 18.23] |
| B3 vs B2 (static optimisation) | 36 | 0.6876 | [0.4245, 0.9755] |
| P0 vs B3 (rolling adaptation) | 36 | 0.003489 | [-0.05182, 0.06811] |
| P vs P0 (AI forecast, dE_AI) | 36 | -0.4505 | [-0.6305, -0.2825] |
| P vs B1-OPT | 36 | 16.02 | [13.6, 18.38] |
| P vs B1p-OPT (kill test) | 36 | 2.134 | [1.432, 2.846] |
| ORACLE vs P (oracle gap) | 36 | 0.6017 | [0.3921, 0.8264] |
| ORACLE vs B1p-OPT (ceiling of shared DC) | 36 | 2.736 | [1.839, 3.646] |
| B1 minus B1-OPT | 36 | 3.947e-16 | [-8.684e-15, 1.026e-14] |
| B1 minus B1p | 36 | 13.89 | [10.75, 16.93] |
| B1 minus B1p-OPT | 36 | 13.89 | [10.75, 16.93] |
| B1 minus B2 | 36 | 15.78 | [13.27, 18.23] |
| B1 minus B3 | 36 | 16.47 | [14.18, 18.69] |
| B1 minus P0 | 36 | 16.47 | [14.19, 18.7] |
| B1 minus P | 36 | 16.02 | [13.6, 18.38] |
| B1 minus ORACLE | 36 | 16.62 | [14.39, 18.81] |

## Per-method intervals

SIM_ASSUMED_PROFILE; bootstrap 95% intervals over instances.

| Method | Metric | mean | 95% CI | n |
|---|---|---:|---:|---:|
| B0 | net_kwh | 350.7 | [317.4, 383.7] | 36 |
| B0 | peak_import_kw | 60.31 | [57.61, 62.91] | 36 |
| B0 | matching_ratio | 0 | [0, 0] | 36 |
| B0 | TT_h | 0.03472 | [0, 0.09722] | 36 |
| B0 | makespan_h | 11.56 | [11.07, 12.08] | 36 |
| B0 | completed_jobs | 10 | [10, 10] | 36 |
| B0 | violations | 0 | [0, 0] | 36 |
| B1 | net_kwh | 107.8 | [102.7, 112.7] | 36 |
| B1 | peak_import_kw | 36.94 | [31.98, 41.9] | 36 |
| B1 | matching_ratio | 0 | [0, 0] | 36 |
| B1 | TT_h | 0.03472 | [0, 0.09722] | 36 |
| B1 | makespan_h | 11.56 | [11.07, 12.08] | 36 |
| B1 | completed_jobs | 10 | [10, 10] | 36 |
| B1 | violations | 0 | [0, 0] | 36 |
| B1-OPT | net_kwh | 107.8 | [102.7, 112.7] | 36 |
| B1-OPT | peak_import_kw | 30.4 | [26.34, 34.62] | 36 |
| B1-OPT | matching_ratio | 0 | [0, 0] | 36 |
| B1-OPT | TT_h | 0 | [0, 0] | 36 |
| B1-OPT | makespan_h | 13.57 | [13.1, 14.01] | 36 |
| B1-OPT | completed_jobs | 10 | [10, 10] | 36 |
| B1-OPT | violations | 0 | [0, 0] | 36 |
| B1p | net_kwh | 93.91 | [90.88, 96.59] | 36 |
| B1p | peak_import_kw | 35.82 | [30.84, 40.79] | 36 |
| B1p | matching_ratio | 0 | [0, 0] | 36 |
| B1p | TT_h | 0.03472 | [0, 0.09722] | 36 |
| B1p | makespan_h | 11.56 | [11.07, 12.08] | 36 |
| B1p | completed_jobs | 10 | [10, 10] | 36 |
| B1p | violations | 0 | [0, 0] | 36 |
| B1p-OPT | net_kwh | 93.91 | [90.88, 96.59] | 36 |
| B1p-OPT | peak_import_kw | 28.84 | [24.61, 33.23] | 36 |
| B1p-OPT | matching_ratio | 0 | [0, 0] | 36 |
| B1p-OPT | TT_h | 0 | [0, 0] | 36 |
| B1p-OPT | makespan_h | 13.55 | [13.08, 14] | 36 |
| B1p-OPT | completed_jobs | 10 | [10, 10] | 36 |
| B1p-OPT | violations | 0 | [0, 0] | 36 |
| B2 | net_kwh | 92.02 | [88.83, 94.92] | 36 |
| B2 | peak_import_kw | 35.8 | [30.84, 40.78] | 36 |
| B2 | matching_ratio | 0.298 | [0.1966, 0.4011] | 36 |
| B2 | TT_h | 0.03472 | [0, 0.09722] | 36 |
| B2 | makespan_h | 11.56 | [11.07, 12.08] | 36 |
| B2 | completed_jobs | 10 | [10, 10] | 36 |
| B2 | violations | 0 | [0, 0] | 36 |
| B3 | net_kwh | 91.33 | [88.07, 94.36] | 36 |
| B3 | peak_import_kw | 25.42 | [22.28, 28.65] | 36 |
| B3 | matching_ratio | 0.407 | [0.2725, 0.5434] | 36 |
| B3 | TT_h | 0.03472 | [0, 0.1042] | 36 |
| B3 | makespan_h | 13.81 | [13.3, 14.32] | 36 |
| B3 | completed_jobs | 10 | [10, 10] | 36 |
| B3 | violations | 0 | [0, 0] | 36 |
| P0 | net_kwh | 91.32 | [88.06, 94.36] | 36 |
| P0 | peak_import_kw | 25.06 | [21.99, 28.25] | 36 |
| P0 | matching_ratio | 0.4073 | [0.2725, 0.5426] | 36 |
| P0 | TT_h | 0.05556 | [0, 0.1389] | 36 |
| P0 | makespan_h | 14.58 | [14, 15.11] | 36 |
| P0 | completed_jobs | 10 | [10, 10] | 36 |
| P0 | violations | 0 | [0, 0] | 36 |
| P | net_kwh | 91.78 | [88.55, 94.74] | 36 |
| P | peak_import_kw | 30.82 | [26.11, 35.65] | 36 |
| P | matching_ratio | 0.3371 | [0.2267, 0.4498] | 36 |
| P | TT_h | 0.05556 | [0, 0.1667] | 36 |
| P | makespan_h | 12.54 | [11.88, 13.23] | 36 |
| P | completed_jobs | 10 | [10, 10] | 36 |
| P | violations | 0 | [0, 0] | 36 |
| ORACLE | net_kwh | 91.17 | [87.89, 94.23] | 36 |
| ORACLE | peak_import_kw | 25.28 | [22.14, 28.55] | 36 |
| ORACLE | matching_ratio | 0.4316 | [0.2885, 0.5756] | 36 |
| ORACLE | TT_h | 0 | [0, 0] | 36 |
| ORACLE | makespan_h | 13.88 | [13.35, 14.38] | 36 |
| ORACLE | completed_jobs | 10 | [10, 10] | 36 |
| ORACLE | violations | 0 | [0, 0] | 36 |

Limitations: oracle solves use a 60 s limit versus 10 s per rolling solve; the replanner can widen flex windows to deadlines and omits downtime from optimization, although replay enforces downtime. Comparisons are descriptive and not fully matched on compute budget or planning constraints.
