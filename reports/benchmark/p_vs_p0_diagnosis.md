# P vs P0 diagnostic

Boundary: SIM_ASSUMED_PROFILE. bench_v1 S3 synthetic storage/bidirectional cycling with assumed recipe power profiles and i.i.d. duration/power deviations; no measured site evidence. Campaign P/P0 share instances, profile, bus parameters, flex and nominal optimizer settings; realized tardiness can differ. Values are descriptive when tardiness differs. Time-limited reruns can differ from the saved campaign; compare the intervention within the new reruns.

## Original S3 campaign per instance

| instance_id | P_minus_P0_net_kwh | P_minus_P0_peak_import_kw | P_replans | P_accepted | P0_replans | P0_accepted |
| --- | --- | --- | --- | --- | --- | --- |
| n010_tau02_r00_S3_0 | 0.32062 | 26.229 | 39 | 39 | 44 | 44 |
| n010_tau02_r00_S3_1 | 0.53689 | 9.9409 | 35 | 35 | 38 | 38 |
| n010_tau02_r01_S3_0 | 1.0662 | 12.857 | 40 | 40 | 59 | 59 |
| n010_tau02_r01_S3_1 | 0.94671 | 2.4581 | 57 | 57 | 61 | 61 |
| n010_tau02_r02_S3_0 | 1.1575 | 10.905 | 46 | 46 | 54 | 54 |
| n010_tau02_r02_S3_1 | 1.297 | 14.734 | 44 | 44 | 61 | 61 |
| n010_tau05_r00_S3_0 | 0.5915 | 10.218 | 40 | 40 | 58 | 58 |
| n010_tau05_r00_S3_1 | 0.68113 | 9.6582 | 46 | 46 | 63 | 63 |
| n010_tau05_r01_S3_0 | 1.5422 | 17.269 | 41 | 41 | 57 | 57 |
| n010_tau05_r01_S3_1 | 1.1348 | -2.3283 | 42 | 42 | 63 | 63 |
| n010_tau05_r02_S3_0 | 0.50423 | 9.4231 | 63 | 63 | 68 | 68 |
| n010_tau05_r02_S3_1 | 0.72331 | 9.5179 | 46 | 46 | 61 | 61 |
| n010_tau08_r00_S3_0 | 0.19411 | 8.8226 | 46 | 46 | 58 | 58 |
| n010_tau08_r00_S3_1 | 1.7766 | 17.657 | 40 | 40 | 54 | 54 |
| n010_tau08_r01_S3_0 | 0.80993 | 11.177 | 48 | 48 | 65 | 65 |
| n010_tau08_r01_S3_1 | 1.3209 | 5.511 | 48 | 48 | 54 | 54 |
| n010_tau08_r02_S3_0 | 0.85767 | 7.0913 | 45 | 45 | 60 | 60 |
| n010_tau08_r02_S3_1 | 0.75837 | 12.484 | 42 | 42 | 60 | 60 |

Accepted counts include no-op cached replans. Per-job start differences, including moved jobs, are in `runs/pdiag/job_starts.csv`.

## Prediction error by elapsed fraction of nominal duration

| bin | n | P_mae_h | P0_mae_h |
| --- | --- | --- | --- |
| 0-.25 | 169 | 3.1454 | 0.37091 |
| .25-.5 | 168 | 3.174 | 0.38126 |
| .5-.75 | 153 | 1.5701 | 0.38244 |
| .75-1 | 55 | 0.25379 | 0.34314 |
| 1+ | 5 | 0.012488 | 0.37004 |

Errors use the simulator continuous duration parameter, not its discretized realized completion time; observations are repeated and correlated within jobs. The P0 column evaluates nominal predictions on the identical P observations. Full per-replan predictions and true kappas: `runs/pdiag/predictions.csv`.

## Four-instance replay and 50% intervention

| instance_id | method | net_kwh | peak_import_kw | TT_h | completed_jobs | violations | n_replans | n_accepted | n_solves | reasons |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| n010_tau02_r00_S3_0 | P0 | 65.085 | 21.61 | 0 | 10 | 0 | 41 | 41 | 10 |  |
| n010_tau02_r00_S3_0 | P | 65.695 | 51.959 | 0 | 10 | 0 | 39 | 39 | 13 |  |
| n010_tau02_r00_S3_0 | P50 | 65.227 | 22.113 | 0 | 10 | 0 | 41 | 41 | 22 |  |
| n010_tau02_r00_S3_1 | P0 | 66.849 | 33.172 | 0 | 10 | 0 | 38 | 38 | 8 |  |
| n010_tau02_r00_S3_1 | P | 67.183 | 35.478 | 0 | 10 | 0 | 35 | 35 | 14 |  |
| n010_tau02_r00_S3_1 | P50 | 66.951 | 33.172 | 0 | 10 | 0 | 39 | 39 | 19 |  |
| n010_tau02_r01_S3_0 | P0 | 84.899 | 39.778 | 0 | 10 | 0 | 62 | 62 | 10 |  |
| n010_tau02_r01_S3_0 | P | 86.114 | 42.085 | 0 | 10 | 0 | 40 | 40 | 21 |  |
| n010_tau02_r01_S3_0 | P50 | 85.224 | 39.778 | 0 | 10 | 0 | 52 | 52 | 22 |  |
| n010_tau02_r01_S3_1 | P0 | 95.969 | 38.7 | 0 | 10 | 0 | 61 | 61 | 12 |  |
| n010_tau02_r01_S3_1 | P | 96.975 | 41.159 | 0 | 10 | 0 | 63 | 63 | 22 |  |
| n010_tau02_r01_S3_1 | P50 | 96.056 | 28.656 | 0 | 10 | 0 | 60 | 60 | 21 |  |

P50 minus P net kWh: mean -0.6270, paired bootstrap 95% CI [-0.9045, -0.3495], n=4; small selected sample, not a general efficacy claim. P50 uses nominal duration and kappa until elapsed >= 50% nominal.

| method | attempts | solves | cache_hits |
| --- | --- | --- | --- |
| P | 177 | 70 | 107 |
| P0 | 202 | 40 | 162 |
| P50 | 192 | 84 | 108 |

## Mechanism and limits

The P cache key includes running predicted duration and kappa, while P0 uses nominal values; changes can trigger new solves even if queued jobs are unchanged. Calls and cache hits are logged in `runs/pdiag/calls.csv`; counts alone do not establish causality or show that more solves caused lost overlap. The original replay attempts include accepted no-ops. A changed prediction can alter the remaining running profiles and therefore the queued plan; realized start differences show association, not a causal attribution. Replanner snaps replan time upward to 0.25 h and Replay snaps starts to the instance render grid for both methods; no isolated snapping intervention was performed, so its contribution is NOT_VERIFIED. The 50% intervention tests a combined early duration and kappa suppression, not duration error in isolation.

Recommended AI-G10 gate: evaluate P against matched P0 on held-out cells/instances with identical solver budget, profile, bus limits, start rules and production constraints; require a paired 95% CI showing lower M0 kWh for P, no throughput/tardiness or safety regression, and monitor elapsed-fraction prediction errors and plan churn. Otherwise retain P0. Bus voltage excursions are not simulated; FPY and test integrity are not established.

Evidence: `runs/pdiag/campaign_comparison.csv`, `job_starts.csv`, `predictions.csv`, `duration_mae.csv`, `calls.csv`, `call_summary.csv`, `reruns.csv`. Reproduction: set `PYTHONPATH=src` and run `python runs/pdiag/diagnose.py`; set `PDIAG_REPORT_ONLY=1` to regenerate from saved replay CSVs.
