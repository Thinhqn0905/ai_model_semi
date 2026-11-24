# Sensitivity campaign

Boundary: SIM_ASSUMED_PROFILE. Bench v1 uses assumed station powers and synthetic phase profiles; these are not site measurements. Comparisons use net grid energy at M0, matched instances and equal tardiness. Positive gain is B1p-OPT minus ORACLE. Bootstrap 95% confidence intervals are paired by instance.

| Sweep | Value | Scenario | n | Gain kWh (mean; 95% CI) | Error |
|---|---|---|---:|---|---|
| flex | 0 | S3 | 18 | 3.787 [3.391, 4.167] |  |
| flex | 0 | S1 | 18 | -2.368e-15 [-7.105e-15, 2.368e-15] |  |
| flex | 0.1 | S3 | 18 | 4.985 [4.783, 5.162] |  |
| flex | 0.1 | S1 | 18 | -7.895e-16 [-5.526e-15, 3.947e-15] |  |
| flex | 0.25 | S3 | 18 | 5.454 [5.254, 5.616] |  |
| flex | 0.25 | S1 | 18 | 2.368e-15 [-1.579e-15, 7.895e-15] |  |
| flex | 0.5 | S3 | 18 | 5.629 [5.403, 5.811] |  |
| flex | 0.5 | S1 | 18 | -3.158e-15 [-7.895e-15, 7.895e-16] |  |
| flex | 1 | S3 | 18 | 5.549 [5.297, 5.75] |  |
| flex | 1 | S1 | 18 | -3.158e-15 [-7.105e-15, 0] |  |
| eta_afe | 0.94 | S3 | 18 | 12.39 [11.88, 12.79] |  |
| eta_afe | 0.94 | S1 | 18 | 2.368e-15 [0, 4.737e-15] |  |
| eta_afe | 0.96 | S3 | 18 | 7.839 [7.513, 8.096] |  |
| eta_afe | 0.96 | S1 | 18 | 2.368e-15 [-7.895e-16, 6.316e-15] |  |
| eta_afe | 0.98 | S3 | 18 | 3.315 [3.178, 3.427] |  |
| eta_afe | 0.98 | S1 | 18 | 7.895e-16 [-2.368e-15, 4.737e-15] |  |
| eta_link | 0.97 | S3 | 18 | 3.306 [3.166, 3.42] |  |
| eta_link | 0.97 | S1 | 18 | -3.158e-15 [-7.105e-15, 0] |  |
| eta_link | 0.99 | S3 | 18 | 5.549 [5.297, 5.75] |  |
| eta_link | 0.99 | S1 | 18 | -3.158e-15 [-7.105e-15, 0] |  |
| eta_link | 1.0 | S3 | 18 | 6.677 [6.41, 6.89] |  |
| eta_link | 1.0 | S1 | 18 | -3.158e-15 [-7.105e-15, 0] |  |
| p_link_max | 5 | S3 | 18 | 4.57 [4.412, 4.698] |  |
| p_link_max | 5 | S1 | 18 | -3.158e-15 [-7.105e-15, 0] |  |
| p_link_max | 10 | S3 | 18 | 5.32 [5.101, 5.492] |  |
| p_link_max | 10 | S1 | 18 | -3.158e-15 [-7.105e-15, 0] |  |
| p_link_max | 20 | S3 | 18 | 5.537 [5.314, 5.719] |  |
| p_link_max | 20 | S1 | 18 | -3.158e-15 [-7.105e-15, 0] |  |
| p_link_max | inf | S3 | 18 | 5.555 [5.304, 5.756] |  |
| p_link_max | inf | S1 | 18 | -3.158e-15 [-7.105e-15, 0] |  |
| n_stations | 4 | S3 | 18 | 5.179 [4.978, 5.336] |  |
| n_stations | 4 | S1 | 18 | 0 [0, 0] |  |
| n_stations | 8 | S3 | 18 | 5.56 [5.307, 5.763] |  |
| n_stations | 8 | S1 | 18 | -3.158e-15 [-7.105e-15, 0] |  |
| n_stations | 16 | S3 | 18 | 5.539 [5.31, 5.718] |  |
| n_stations | 16 | S1 | 18 | -2.368e-15 [-6.316e-15, 0] |  |
| allow_export | true | S3 | 18 | 5.554 [5.301, 5.756] |  |
| allow_export | true | S1 | 18 | -3.158e-15 [-7.105e-15, 0] |  |
| allow_export | false | S3 | 18 | 150.3 [143.8, 155.5] |  |
| allow_export | false | S1 | 18 | -3.158e-15 [-7.105e-15, 0] |  |
| cycle_scale | 0.5 | S3 | 18 | 3.748 [3.673, 3.816] |  |
| cycle_scale | 0.5 | S1 | 18 | -3.158e-15 [-7.105e-15, 0] |  |
| cycle_scale | 1 | S3 | 18 | 5.549 [5.297, 5.75] |  |
| cycle_scale | 1 | S1 | 18 | -3.158e-15 [-7.105e-15, 0] |  |
| cycle_scale | 2 | S3 | 0 | NOT_VERIFIED | cycle_scale must be in (0, 1] |
| cycle_scale | 2 | S1 | 0 | NOT_VERIFIED | cycle_scale must be in (0, 1] |
| unit_h | 0.5 | S3 | 18 | 3.403 [3.332, 3.469] |  |
| unit_h | 0.5 | S1 | 18 | 3.947e-16 [0, 1.184e-15] |  |
| unit_h | 1 | S3 | 18 | 5.549 [5.297, 5.75] |  |
| unit_h | 1 | S1 | 18 | -3.158e-15 [-7.105e-15, 0] |  |
| unit_h | 2 | S3 | 18 | 10.47 [9.971, 10.88] |  |
| unit_h | 2 | S1 | 18 | 1.579e-15 [-6.316e-15, 9.474e-15] |  |
| grid | 0_eta_0.97 | S3 | 18 | 2.26 [2.025, 2.486] |  |
| grid | 0_eta_0.99 | S3 | 18 | 3.787 [3.391, 4.167] |  |
| grid | 0_eta_1.0 | S3 | 18 | 4.542 [4.068, 4.998] |  |
| grid | 0.25_eta_0.97 | S3 | 18 | 3.25 [3.13, 3.347] |  |
| grid | 0.25_eta_0.99 | S3 | 18 | 5.454 [5.254, 5.616] |  |
| grid | 0.25_eta_1.0 | S3 | 18 | 6.567 [6.32, 6.767] |  |
| grid | 1_eta_0.97 | S3 | 18 | 3.306 [3.166, 3.42] |  |
| grid | 1_eta_0.99 | S3 | 18 | 5.56 [5.307, 5.763] |  |
| grid | 1_eta_1.0 | S3 | 18 | 6.682 [6.417, 6.894] |  |

Positive shared-DC gain with CI excluding zero: flex=0 (S3), flex=0.1 (S3), flex=0.25 (S3), flex=0.5 (S3), flex=1 (S3), eta_afe=0.94 (S3), eta_afe=0.96 (S3), eta_afe=0.98 (S3), eta_link=0.97 (S3), eta_link=0.99 (S3), eta_link=1.0 (S3), p_link_max=5 (S3), p_link_max=10 (S3), p_link_max=20 (S3), p_link_max=inf (S3), n_stations=4 (S3), n_stations=8 (S3), n_stations=16 (S3), allow_export=true (S3), allow_export=false (S3), cycle_scale=0.5 (S3), cycle_scale=1 (S3), unit_h=0.5 (S3), unit_h=1 (S3), unit_h=2 (S3), grid=0_eta_0.97 (S3), grid=0_eta_0.99 (S3), grid=0_eta_1.0 (S3), grid=0.25_eta_0.97 (S3), grid=0.25_eta_0.99 (S3), grid=0.25_eta_1.0 (S3), grid=1_eta_0.97 (S3), grid=1_eta_0.99 (S3), grid=1_eta_1.0 (S3).
Full metrics and errors: runs/sens_v1/sensitivity_results.csv. Solver gaps are reported there; no measured bus-stability or site evidence is implied.

S1 negative control: S1 paired instances=450; max absolute difference kWh=5.68434188608e-14. maximum reported MIP gap=0.171045. Solver gaps limit interpretation of optimized comparisons; CI alone does not account for optimization error.
The 2x cycle-scale cases could not run: the generator rejects scale above 1. See the failed rows in the CSV.
