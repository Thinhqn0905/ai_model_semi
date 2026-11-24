# Figure index

DS05: measured battery cycles; DS02/DS04: measured datasets. SIM_ASSUMED_PROFILE: simulated assumed profiles. SIM_DATA_PROFILE: simulated DS05 cycles with assumed station scaling and windows.

| Figure | Input | Boundary |
|---|---|---|
| F01 | No DS05 prediction rows supplied | NOT_VERIFIED (missing) |
| F02 | No DS05 prediction rows supplied | NOT_VERIFIED (missing) |
| F03 | results\ai_ds05_branchC\model_metrics.csv | LOCAL_RUN(DS05 MEASURED) |
| F04 | runs\ai\ds02\model_metrics.csv, runs\ai\ds04\model_metrics.csv, results\ai_ds05_branchC\model_metrics.csv | LOCAL_RUN (MEASURED DATA: DS02, DS04, DS05) |
| F05 | data\processed\efficiency_points.parquet | VENDOR_REPORTED |
| F06 | runs\oracle_v1\timeseries.parquet | SIM_ASSUMED_PROFILE |
| F07 | runs\twin_v1\controls.json | SIM_ASSUMED_PROFILE |
| F08 | runs\rolling_v1\ladder.csv | SIM_ASSUMED_PROFILE |
| F09 | reports\ai\ai_exp12_ds06.md | SIM_DATA_PROFILE |
| F10 | runs\sens_v1\sensitivity_results.csv | SIM_ASSUMED_PROFILE |
| F11 | No DS05 prediction rows supplied | NOT_VERIFIED (missing) |
| F12 | results\ai_ds05_branchC\model_metrics.csv | LOCAL_RUN(DS05 MEASURED) |
| F13 | runs\oracle_v1\schedules.parquet, runs\oracle_v1\results.csv | SIM_ASSUMED_PROFILE |
| F14 | runs\rolling_v1\ladder.csv | SIM_ASSUMED_PROFILE |
| F15 | results\ai_ds05_branchC\runtime_metrics.csv, results\ai_ds05_branchC\model_metrics.csv | LOCAL_RUN(DS05 MEASURED) |

F10 (F10.png/pdf) shows one-at-a-time S3 gain in kWh and percent with paired 95% confidence intervals and the S1 zero control. F10b (F10b.png/pdf) shows S3 gain against flexibility; F10_grid (F10_grid.png/pdf) shows the available flex × link-efficiency grid. Input: runs/sens_v1/sensitivity_results.csv. Boundary: SIM_ASSUMED_PROFILE. Solver gaps are not reflected in the intervals; see reports/sensitivity/sens_v1.md.
