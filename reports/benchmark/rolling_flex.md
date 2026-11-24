# Rolling P0 across flexibility

Boundary: SIM_ASSUMED_PROFILE; simulated assumed profiles, bench_v1 S3, 10 jobs, seeds 0 and 1.

Differences are paired by instance; 95% percentile bootstrap intervals. Positive energy differences favor the second method. Peak is P0 minus B1p-OPT. All available pairs are shown; tardiness can differ.

| Flex | Instances | B1p-OPT − P0 kWh | P0 − ORACLE kWh | B2 − P0 kWh | Peak P0 − B1p-OPT kW |
|---:|---:|---:|---:|---:|---:|
| 0 | 18 | 4.317 [3.977, 4.640] (n=18) | -0.531 [-1.030, -0.034] (n=18) | 0.531 [0.034, 1.030] (n=18) | -14.186 [-17.836, -10.503] (n=18) |
| 0.1 | 18 | unavailable (oracle baseline missing) | unavailable (oracle baseline missing) | unavailable (oracle baseline missing) | unavailable (oracle baseline missing) |
| 0.25 | 18 | 5.169 [4.943, 5.360] (n=18) | 0.302 [0.236, 0.374] (n=18) | 1.382 [1.022, 1.762] (n=18) | -7.108 [-10.357, -3.694] (n=18) |
| 0.5 | 18 | unavailable (oracle baseline missing) | unavailable (oracle baseline missing) | unavailable (oracle baseline missing) | unavailable (oracle baseline missing) |
| 1.0 | 18 | 5.325 [5.086, 5.531] (n=18) | 0.263 [0.177, 0.356] (n=18) | 1.538 [1.176, 1.923] (n=18) | -13.411 [-16.698, -9.955] (n=18) |

Flex 0 is the topology-only reference; the change in B1p-OPT − P0 at higher flex includes the effect of scheduling flexibility, but is descriptive and is not a causal decomposition.
Change in mean shared-DC gain relative to flex 0 (kWh): 0.25: +0.852, 1.0: +1.008.

Oracle rows for flex 0.1 and 0.5 are absent from runs/oracle_v1/results.csv; comparisons at those points cannot be calculated. At flex 0, six B3 rows are infeasible; the requested comparisons use other baselines.

Rolling replanning can widen flex windows to deadlines and omits downtime from optimization, although replay enforces downtime. Oracle uses a different solve budget; results are descriptive. Bus voltage excursions are not simulated.

Failures: {"0.1 baseline": "oracle rows absent", "0.5 baseline": "oracle rows absent"}
