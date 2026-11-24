# Legacy benchmark audit

All numeric results below: **SIM_ASSUMED_PROFILE**. Legacy stress return = 0.80 × batch-mean true kappa × P3_run; stress demand = 0.30 × P3_run. The ledger also includes ramp, idle and tester demand. This profile can return more than rack demand and is not a validated physical converter profile. Legacy grid kWh is import minus 0.5 × export, not physical net M0 energy. Same instance and profile for each method; FIFO and optimized schedules can have different tardiness. B4 is a heuristic perfect-profile plan, not a proven exact oracle.

Reproduction vs stored CSV: max absolute TT difference 0.000000; kWh difference 0.000000. Extended results vs reproduction after rounding: TT 0.000000, kWh 0.000000. Inputs: `runs/legacy/regen_results_repro.csv`, `DS01_Quanh/results/regen_results.csv`, `runs/legacy/legacy_results.csv`.

Means with paired-instance bootstrap 95% intervals (10,000 resamples, seed 0); kWh comparisons require equal TT for the methods compared.

## All instances (n=18)

| Method | TT mean [95% CI] | grid kWh mean [95% CI] |
|---|---:|---:|
| B0 | 150.972 [94.472, 214.168] | 368.889 [315.813, 422.867] |
| B1 | 150.972 [94.472, 214.168] | 202.108 [170.260, 233.939] |
| B1-OPT | 13.537 [4.519, 24.167] | 129.591 [105.929, 155.592] |
| B1p | 150.972 [94.472, 214.168] | 163.150 [135.786, 190.806] |
| B1p-OPT | 13.593 [4.574, 24.186] | 101.787 [80.486, 125.009] |
| B2 | 150.972 [94.472, 214.168] | 140.954 [116.426, 166.196] |
| B3 | 13.963 [4.685, 24.963] | 104.577 [83.456, 128.111] |
| B4 | 13.315 [4.518, 23.741] | 78.065 [55.890, 102.681] |
| P0 | 13.500 [4.611, 23.982] | 81.474 [59.426, 105.925] |
| P | 13.556 [4.555, 24.371] | 81.138 [58.337, 106.350] |

## Subset TT(P) == TT(B3) (n=12)

| Method | TT mean [95% CI] | grid kWh mean [95% CI] |
|---|---:|---:|
| B0 | 120.583 [66.330, 179.375] | 388.418 [321.887, 450.680] |
| B1 | 120.583 [66.330, 179.375] | 220.460 [181.439, 256.695] |
| B1-OPT | 3.528 [0.000, 8.861] | 114.494 [90.547, 140.816] |
| B1p | 120.583 [66.330, 179.375] | 180.829 [147.290, 212.192] |
| B1p-OPT | 3.528 [0.000, 8.861] | 86.339 [65.692, 108.905] |
| B2 | 120.583 [66.330, 179.375] | 158.860 [129.100, 187.015] |
| B3 | 3.528 [0.000, 8.861] | 92.420 [72.017, 116.317] |
| B4 | 3.528 [0.000, 8.861] | 58.660 [38.942, 82.528] |
| P0 | 3.528 [0.000, 8.861] | 63.544 [43.701, 87.558] |
| P | 3.528 [0.000, 8.861] | 61.094 [40.941, 85.954] |

## Per instance

| n | tau | rep | P − P0 grid kWh | TT P / P0 | B3 ret/demand | Any batch stress return > demand |
|---:|---:|---:|---:|---:|---:|---|
| 10 | 0.2 | 0 | -3.047 | 0.000 / 0.000 | 0.411 | True |
| 10 | 0.2 | 1 | -4.276 | 0.000 / 0.000 | 0.738 | True |
| 10 | 0.2 | 2 | +7.365 | 0.000 / 0.000 | 0.747 | True |
| 10 | 0.5 | 0 | -10.885 | 0.000 / 0.000 | 0.772 | True |
| 10 | 0.5 | 1 | +0.000 | 9.000 / 9.000 | 0.526 | True |
| 10 | 0.5 | 2 | +14.737 | 0.000 / 0.667 | 0.636 | True |
| 10 | 0.8 | 0 | -1.848 | 23.667 / 24.667 | 0.686 | True |
| 10 | 0.8 | 1 | +0.000 | 32.000 / 32.000 | 0.692 | True |
| 10 | 0.8 | 2 | +3.464 | 54.667 / 54.667 | 0.588 | True |
| 20 | 0.2 | 0 | -10.159 | 0.000 / 0.000 | 0.728 | True |
| 20 | 0.2 | 1 | -1.114 | 0.000 / 0.000 | 0.694 | True |
| 20 | 0.2 | 2 | -1.934 | 0.000 / 0.000 | 0.616 | True |
| 20 | 0.5 | 0 | -8.289 | 0.000 / 0.000 | 0.684 | True |
| 20 | 0.5 | 1 | +1.147 | 0.000 / 0.000 | 0.693 | True |
| 20 | 0.5 | 2 | +1.787 | 0.000 / 0.000 | 0.650 | True |
| 20 | 0.8 | 0 | +13.736 | 73.333 / 69.000 | 0.570 | True |
| 20 | 0.8 | 1 | -6.736 | 41.000 / 42.667 | 0.485 | True |
| 20 | 0.8 | 2 | +0.000 | 10.333 / 10.333 | 0.501 | True |

Kill test (matched TT, n=14): P − B1p-OPT grid kWh mean [95% CI] = -24.225 [-31.482, -17.786]. Positive favors B1p-OPT; exclude unequal-TT cases from energy comparisons.

B3→B4 gap formula as coded: (B3 kWh − P kWh) / (B3 kWh − B4 kWh), only where denominator > 1e-9. This is not an exact-oracle gap; compare energy only at matching TT.
Equal-TT B3/P/B4 valid-denominator gap share (n=11): 0.921 [0.862, 0.972].

**NOT_VERIFIED**: slide-14 figures 598.6 … 166.9 kWh are not reproduced by this code; the code that produced them is lost.

Peak kW, throughput, bus excursions and true oracle gap are not provided by this legacy ledger/run; no claim is made for them.

## Paired differences at equal TT

SIM_ASSUMED_PROFILE. Values are mean [bootstrap 95% CI] in legacy grid-score kWh.
- B1 ? P: n=0, unavailable.
- P ? P0: n=14, -1.853 [-4.507, +0.685].
