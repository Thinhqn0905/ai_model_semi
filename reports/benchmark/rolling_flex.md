# Rolling P0 across flexibility

Boundary: SIM_ASSUMED_PROFILE; simulated assumed profiles, bench_v1 S3, 10 jobs, seeds 0 and 1.

Differences are paired by instance; 95% percentile bootstrap intervals. Positive energy differences favor the second method. Peak is P0 minus B1p-OPT. All available pairs are shown; tardiness can differ.

| Flex | Instances | B1p-OPT − P0 kWh | P0 − ORACLE kWh | B2 − P0 kWh | Peak P0 − B1p-OPT kW |
|---:|---:|---:|---:|---:|---:|
| 0 | 18 | 4.317 [3.977, 4.640] (n=18) | -0.531 [-1.030, -0.034] (n=18) | 0.531 [0.034, 1.030] (n=18) | -14.186 [-17.836, -10.503] (n=18) |
| 0.1 | 18 | 4.500 [4.176, 4.771] (n=18) | 0.484 [0.299, 0.687] (n=18) | 0.714 [0.269, 1.141] (n=18) | -7.343 [-12.475, -2.276] (n=18) |
| 0.25 | 18 | 5.169 [4.943, 5.360] (n=18) | 0.302 [0.236, 0.374] (n=18) | 1.382 [1.022, 1.762] (n=18) | -7.108 [-10.357, -3.694] (n=18) |
| 0.5 | 18 | 5.425 [5.209, 5.612] (n=18) | 0.200 [0.135, 0.277] (n=18) | 1.639 [1.282, 2.004] (n=18) | -12.585 [-17.103, -8.109] (n=18) |
| 1.0 | 18 | 5.325 [5.086, 5.531] (n=18) | 0.263 [0.177, 0.356] (n=18) | 1.538 [1.176, 1.923] (n=18) | -13.411 [-16.698, -9.955] (n=18) |

At flex 0, rolling P0 uses a different start-window rule from the oracle: the rolling latest start is at least the FIFO start, whereas the oracle applies its deadline and flex window rule. Report both as observed; their difference is not a topology-only reference or a causal decomposition.
Differences across flex points are descriptive because scheduling constraints and tardiness can differ.

Flex 0.1 and 0.5 oracle and B1p-OPT rows are from `runs/oracle_flexfix/results.csv`; P0 rows are from `runs/rolling_flex/`. At flex 0, six B3 rows are infeasible; the requested comparisons use other baselines. Equal-tardiness pair counts for the new points: flex 0.1: P0/ORACLE 15/18; P0/B1p-OPT 15/18; flex 0.5: P0/ORACLE 16/18; P0/B1p-OPT 16/18.

Rolling replanning can widen flex windows to deadlines and omits downtime from optimization, although replay enforces downtime. The new oracle campaign uses a 30 s per-solve limit and rolling uses 10 s; earlier oracle points use a 60 s limit; results are descriptive. Bus voltage excursions are not simulated.

Failures: none for the requested ORACLE and P0 rows.
