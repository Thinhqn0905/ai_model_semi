# ReGenATE - Run 4 Final Evaluation Report (consolidated)

Repository github.com/Thinhqn0905/ai_model_semi; local D:/Subject_ProjectClass/semipox. Raw-result bindings: docs/raw_binding_manifest.md
(Drive MyDrive/semiexpo/ai_runs/drive_manifest.json). Decisions D001-D019 (docs/decisions.md). Dashboard screenshots: reports/run4/screenshots/
(16 pages). Prior art: reports/run4/prior_art.md.
Evidence categories: MEASURED (DS05 cycles, DS07 facility loads), SIM_DATA_PROFILE (DS06), SIM_ASSUMED_PROFILE (bench_v1), VENDOR_REPORTED /
DATASHEET, SOURCE_REPORTED (official tariff documents), ASSUMED (annualisation, FX 0.21 USD/MYR, cost estimates), NOT_VERIFIED.
SIMULATION ACCEPTANCE (this report) is separate from INDUSTRIAL SITE ACCEPTANCE (not performed: site data, shadow mode, protection
qualification, actual costs).
Missing sections: none

## 1 Dataset

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

Registry and provenance: `data/manifests/dataset_registry.json`, `reports/run4/dataset_registry.md`. Counts below are SOURCE_REPORTED or MEASURED source observations; CI and baseline not applicable. Unknown fields are NOT_VERIFIED.

| Dataset / source | Samples; features; split; role and provenance |
|---|---|
| DS01 project source | 180 synthetic instances; jobs, machines, processing and due dates; split not recorded; scheduling benchmark. `reports/data/ds01_report.md`, `DS01_Quanh/instances/` |
| DS02 https://doi.org/10.5281/zenodo.18524234 | A/B 86,399 rows each, C 122,109; voltage, current, power, state; chronological 70/15/15 benchmark split; bus context, signs and clocks undocumented. `reports/data/ds02_report.md`, `reports/run3/cross_dataset_benchmark.md` |
| DS03 equipment and EDC sources | Sample count and split not recorded; electrical specifications and sequences; equipment grounding; vendor figures distinct from measurements. `data/manifests/dataset_registry.json`, `reports/data/ds03_report.md` |
| DS04 SME loads | A 1,520,330 rows; B 1,568,736; power and status; per-asset chronological 70/15/15; forecasting, not semiconductor cells. `reports/data/ds04_report.md` |
| DS05 https://doi.org/10.17028/rd.lboro.28732490.v2 | 14,755 valid cycles; power and duration; per-module chronological 70/15/15; measured battery-cycler proxy. `reports/ai/branch_C_ds05.md`, `results/ai_ds05_branchC/*` |
| DS06 derived scheduling benchmark | 100 paired test instances in main campaign; test-split DS05 cycles, assumed station scaling and windows; scheduling evaluation. `reports/ai/ai_exp12_ds06.md`, `MyDrive/semiexpo/ai_runs/v2_flex025_n100.csv` |
| DS07 https://doi.org/10.6084/m9.figshare.14822256.v9 | Sample count not recorded in registry; facility demand kW; split per experiment; measured background, unsynchronized with cell. `data/manifests/dataset_registry.json`, `reports/run4/facility_billing.md`, `MyDrive/semiexpo/ds07_raw` |
| DS08 https://doi.org/10.6084/m9.figshare.21893808.v3 | MISSING local data; publication reports 386 customer CSVs, time and interval energy; split not established; external candidate. `reports/run4/ds08_audit.md` |

## 2 AI benchmark

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

MEASURED observations, derived forecast metrics; no site or energy claim. Full model-by-horizon NMAE, skill and coverage tables are in `reports/ai/branch_A_ds02.md`, `reports/ai/branch_B_ds04.md`, with raw metric paths `runs/ai/ds02/model_metrics.csv`, `runs/ai/ds04/model_metrics.csv`; model definitions and matched splits are in `reports/run3/cross_dataset_benchmark.md`. DS05 model-by-target skill and coverage are in `reports/ai/branch_C_ds05.md`, raw `results/ai_ds05_branchC/*`. Baselines are persistence for DS02/DS04 and previous cycle for DS05. MAE, RMSE, sample counts, latency and model size are NOT_VERIFIED where not recorded in those tables; CI not recorded. Strongest baseline varies by dataset and horizon; do not infer it across incompatible protocols. Model size: not recorded. Additional metrics absent from the source tables remain NOT_VERIFIED.


### Recorded model tables

Boundary MEASURED source observations; derived metrics; baseline persistence (DS02/DS04), previous cycle (DS05); confidence intervals, sample counts per row and model size not recorded in these reports. NMAE is dimensionless; coverage is a fraction. MAE, RMSE and latency are not recorded in these report tables unless shown below; missing values are NOT_VERIFIED. Model IDs and protocols: `reports/run3/cross_dataset_benchmark.md`.

DS02: `reports/ai/branch_A_ds02.md`; raw `runs/ai/ds02/model_metrics.csv`.

| dataset | horizon | model | nmae | skill_vs_persistence | coverage80 |
| --- | --- | --- | --- | --- | --- |
| A | 1 | M0 | 0.0049 | 0.0 | 0.7533 |
| A | 1 | M1 | 0.0053 | -0.0769 | 0.7711 |
| A | 1 | M2 | 0.0036 | 0.2654 | 0.7749 |
| A | 1 | M3 | 0.0037 | 0.2526 | 0.8051 |
| A | 1 | M4 | 0.004 | 0.1899 | 0.7904 |
| A | 1 | M5 | 0.0037 | 0.2549 | 0.8422 |
| A | 1 | M6 | 0.0043 | 0.1337 | 0.8206 |
| A | 6 | M0 | 0.0051 | 0.0 | 0.8129 |
| A | 6 | M1 | 0.0056 | -0.102 | 0.9301 |
| A | 6 | M2 | 0.0045 | 0.1096 | 0.8207 |
| A | 6 | M3 | 0.0051 | 0.0045 | 0.8377 |
| A | 6 | M4 | 0.0061 | -0.1972 | 0.8121 |
| A | 6 | M5 | 0.0037 | 0.2639 | 0.8455 |
| A | 6 | M6 | 0.0044 | 0.1414 | 0.8144 |
| A | 30 | M0 | 0.0052 | -0.0015 | 0.8995 |
| A | 30 | M1 | 0.0122 | -1.3405 | 1.0 |
| A | 30 | M2 | 0.0134 | -1.5819 | 0.8291 |
| A | 30 | M3 | 0.0163 | -2.1475 | 0.8315 |
| A | 30 | M4 | 0.0146 | -1.8024 | 0.8085 |
| A | 30 | M5 | 0.0037 | 0.2786 | 0.8718 |
| A | 30 | M6 | 0.0045 | 0.1415 | 0.9802 |
| B | 1 | M0 | 0.0051 | -0.0003 | 0.9992 |
| B | 1 | M1 | 0.0059 | -0.1559 | 0.9753 |
| B | 1 | M2 | 0.0059 | -0.1554 | 0.9667 |
| B | 1 | M3 | 0.0054 | -0.0543 | 0.9582 |
| B | 1 | M4 | 0.0067 | -0.3203 | 0.9149 |
| B | 1 | M5 | 0.0042 | 0.1773 | 0.8554 |
| B | 1 | M6 | 0.004 | 0.2075 | 0.8763 |
| B | 6 | M0 | 0.0057 | 0.0002 | 0.9977 |
| B | 6 | M1 | 0.0099 | -0.745 | 0.889 |
| B | 6 | M2 | 0.0251 | -3.4439 | 0.7609 |
| B | 6 | M3 | 0.0278 | -3.9143 | 0.7686 |
| B | 6 | M4 | 0.0288 | -4.0856 | 0.7306 |
| B | 6 | M5 | 0.0045 | 0.1958 | 0.823 |
| B | 6 | M6 | 0.0046 | 0.178 | 0.9177 |
| B | 30 | M0 | 0.0056 | -0.0003 | 1.0 |
| B | 30 | M1 | 0.0091 | -0.6206 | 0.8964 |
| B | 30 | M2 | 0.0405 | -6.2327 | 0.7017 |
| B | 30 | M3 | 0.0466 | -7.3051 | 0.7097 |
| B | 30 | M4 | 0.0457 | -7.1513 | 0.693 |
| B | 30 | M5 | 0.0045 | 0.1895 | 0.8552 |
| B | 30 | M6 | 0.0044 | 0.2171 | 0.928 |
| C | 1 | M0 | 0.0477 | 0.0 | 0.7083 |
| C | 1 | M1 | 0.043 | 0.0976 | 0.6906 |
| C | 1 | M2 | 0.0446 | 0.0655 | 0.6254 |
| C | 1 | M3 | 0.0455 | 0.0455 | 0.6331 |
| C | 1 | M4 | 0.0452 | 0.0525 | 0.616 |
| C | 1 | M5 | 0.0454 | 0.0473 | 0.7254 |
| C | 1 | M6 | 0.0427 | 0.104 | 0.7398 |
| C | 6 | M0 | 0.064 | 0.0 | 0.6814 |
| C | 6 | M1 | 0.0588 | 0.0812 | 0.6593 |
| C | 6 | M2 | 0.0654 | -0.0216 | 0.5607 |
| C | 6 | M3 | 0.0633 | 0.0115 | 0.5867 |
| C | 6 | M4 | 0.0631 | 0.0135 | 0.5629 |
| C | 6 | M5 | 0.0621 | 0.0293 | 0.7191 |
| C | 6 | M6 | 0.0592 | 0.0751 | 0.7452 |
| C | 30 | M0 | 0.1032 | 0.0 | 0.5946 |
| C | 30 | M1 | 0.0994 | 0.0372 | 0.5649 |
| C | 30 | M2 | 0.1148 | -0.1121 | 0.4458 |
| C | 30 | M3 | 0.1144 | -0.1085 | 0.4554 |
| C | 30 | M4 | 0.1161 | -0.1246 | 0.4453 |
| C | 30 | M5 | 0.1119 | -0.0837 | 0.6131 |
| C | 30 | M6 | 0.1013 | 0.0187 | 0.6345 |

DS04: `reports/ai/branch_B_ds04.md`; raw `runs/ai/ds04/model_metrics.csv`.

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

DS05: `reports/ai/branch_C_ds05.md`; raw `results/ai_ds05_branchC/*`; held-out test samples 22,178, target-dependent availability not recorded; skill relative to previous cycle, units target kW or minutes.

| Target (module kW / minutes) | AI01 persistence | AI03 ridge | AI04 RF | AI05 XGBoost | AI10 quantile LGBM (P50) | AI10 coverage P10-P90 |
|---|---|---|---|---|---|---|
| sink power, slot +1 (15 min) | -0.92 | -0.42 | 0.43 | 0.44 | **0.47** | 0.82 |
| sink power, slot +4 (1 h) | -2.61 | -0.92 | 0.20 | **0.31** | 0.21 | 0.77 |
| sink power, slot +16 (4 h) | -4.43 | -1.69 | 0.30 | **0.37** | 0.29 | 0.78 |
| source power, slot +1 | -0.93 | -0.44 | 0.32 | 0.35 | **0.36** | 0.80 |
| source power, slot +4 | -2.51 | -1.06 | 0.03 | **0.17** | 0.12 | 0.75 |
| source power, slot +16 | -3.96 | -1.41 | -0.08 | **0.19** | 0.19 | 0.77 |
| remaining duration (min) | n/a | -0.10 | 0.71 | **0.72** (MAE 73 min) | 0.67 (MAE 87 vs 261 min) | 0.72 |
| Target | coverage80 before | after CQR |
|---|---|---|
| sink +1 / +4 / +16 slots | 0.815 / 0.774 / 0.780 | 0.858 / 0.823 / 0.828 |
| source +1 / +4 / +16 slots | 0.804 / 0.754 / 0.773 | 0.842 / 0.792 / 0.797 |
| remaining duration | 0.720 | 0.755 |

## 3 AI ETA

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

MEASURED DS05 held-out data; previous-cycle baseline; CI not recorded. Battery cycles are a proxy. `reports/run4/ai_eta.md`; raw `MyDrive/semiexpo/ai_runs/run4/eta/`; TCN raw `ai_runs/run4/eta_tcn/`. RMSE and relative-error summaries not recorded in these tables.

| Task / model | n | MAE min | Skill | Coverage | Latency ms/sample |
|---|---:|---:|---:|---:|---:|
| T1 previous / AI18 selected | 2,210 | 290.7 / 116.5 | 0 / 0.60 | not recorded | 0 / 0.012 |
| T1 RF / quantile LGBM CQR | 2,210 | 552 / 188.5 | -0.90 / 0.35 | not recorded / 0.780 | <0.03 / 0.033 |
| T2 previous / RF selected | 24,141 | 154.4 / 62.0 | 0 / 0.60 | not recorded | 0 / 0.009 |
| T2 quantile LGBM CQR / TCN CQR | 24,141 | 99.6 / 104.1 | 0.36 / 0.33 | 0.756 / 0.767 | 0.036 / 0.19 CPU |

T1 normal MAE previous/AI18 7.9/10.2 min, abnormal 2,240/849 min; T2 normal previous/RF 47.3/32.9 min, abnormal 760.3/226.9 min; subset n not recorded. `reports/run4/ai_eta.md`, `MyDrive/semiexpo/ai_runs/run4/eta/`. CQR coverage is empirical, not a guaranteed bound; TCN run's matched-key verification is unresolved in `reports/run4/ai_eta_tcn.md`.


Additional ETA models and progress bins: MEASURED held-out DS05; baseline previous cycle; CI and subset n not recorded; MAE in minutes, skill and coverage dimensionless; `reports/run4/ai_eta.md`, raw `MyDrive/semiexpo/ai_runs/run4/eta/`, TCN `ai_runs/run4/eta_tcn/` (matched keys NOT_VERIFIED).

T1 (total duration before start), test n = 2,210 cycles:
| Model | MAE | skill | coverage80 | predict ms |
|---|---|---|---|---|
| previous cycle (recipe) | 290.7 | 0 | - | 0 |
| median of last 5 | 293.6 | -0.01 | - | 0 |
| EWMA | 269.3 | +0.07 | - | 0 |
| ridge / RF / XGBoost / LightGBM (point, raw target) | 950 / 552 / 1,307 / 589 | -2.27 / -0.90 / -3.50 / -1.03 | - | <0.03 |
| quantile LightGBM P50 (+CQR) | 188.5 | +0.35 | 0.710 -> **0.780** | 0.033 |
| **AI18 gated (Run 3 model)** | **116.5** | **+0.60** (reproduces Run 3 0.599) | - | 0.012 |
| Model | MAE all | skill | 0-25 % | 25-50 % | 50-75 % | 75-100 % | coverage80 | width80 |
|---|---|---|---|---|---|---|---|---|
| previous cycle | 154.4 | 0 | 428.1 | 184.6 | 114.2 | 70.8 | - | - |
| **random forest** | **62.0** | **+0.60** | 109.6 (+0.74) | 58.3 (+0.68) | 46.3 (+0.59) | 63.1 (+0.11) | - | - |
| quantile LightGBM P50 + CQR | 99.6 | +0.36 | 178.7 | 89.9 | 86.9 | 90.9 (-0.29) | **0.756** | 338 |

## 4 AI downstream

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

SIM_DATA_PROFILE: measured DS05 cycles with assumed scaling and windows; paired n=100 against P0, positive means reduction; paired 95% CI. Common instances and ledger within each campaign; equality of tardiness is not universal, so the comparisons do not isolate causal effects. Site performance NOT_VERIFIED. `reports/ai/ai_exp12_ds06.md`, `MyDrive/semiexpo/ai_runs/v2_flex025_n100.csv`; `reports/run3/root_cause_analysis.md`, `MyDrive/semiexpo/ai_runs/run3/v2_diag/results.csv`; `reports/run3/ai_run3.md`, `MyDrive/semiexpo/ai_runs/run3/v2_p5/results.csv`, `MyDrive/semiexpo/ai_runs/run3/v2_{pq_gated,pq_ungated,pqstar}/results.csv`, `MyDrive/semiexpo/ai_runs/run3/v2_pqd/results.csv`.

| Variant | Energy reduction kWh [CI] | Peak reduction kW [CI] | Tardiness reduction h [CI] |
|---|---|---|---|
| P0 | baseline | baseline | baseline |
| P1 | -0.018 [-0.030,-0.005] | -0.34 [-0.83,0.13] | not recorded |
| P2 | -0.019 [-0.031,-0.007] | -0.25 [-0.73,0.23] | not recorded |
| P3 | -0.024 [-0.038,-0.009] | -0.57 [-1.08,-0.06] | not recorded |
| P4 | -0.026 [-0.041,-0.012] | -0.40 [-1.00,0.20] | not recorded |
| P5 / P5s | -0.022 [-0.034,-0.010] / -0.004 [-0.010,0.004] | -0.54 [-1.08,-0.00] / -0.20 [-0.52,0.09] | not recorded |
| PQ / PQ5 | -0.019 [-0.036,-0.006] / -0.034 [-0.052,-0.018] | -0.39 [-0.86,0.06] / -0.86 [-1.56,-0.19] | -0.005 / 0.007; CI not recorded |
| PQd / PQd* | -0.019 [-0.036,-0.005] / -0.002 [-0.015,0.012] | not recorded | 0.003 [0.000,0.008] / 0.048 [0.017,0.087] |
| PQ* | 0.008 [-0.007,0.022] | 0.04 [-0.48,0.54] | 0.048; CI not recorded |
| P1* / P2* | -0.005 [-0.017,0.007] / 0.000 [-0.009,0.009] | -0.52 [-1.11,0.05] / -0.02 [-0.36,0.33] | not recorded |
| P3* / P4* | -0.009 [-0.022,0.003] | -0.27 [-0.86,0.32] | not recorded |
| TR_RUN / TR_Q / TR_ALL | 0.024 [0.013,0.037] / 0.049 [0.035,0.064] / 0.094 [0.077,0.112] | 0.16 [-0.25,0.57] / 0.82 [0.31,1.36] / 1.12 [0.59,1.65] | paired CI not recorded |
| ORACLE | 0.094 [0.077,0.112] | 1.14 [0.57,1.72] | paired CI not recorded |

Perfect queued and running information are different interventions, not additive causal contributions. P0→P5s CI crosses zero; P0→ORACLE is a ceiling. Raw bindings are reconciled by the Drive manifest; MyDrive/semiexpo/ai_runs/run3/v2_diag/results.csv (sha256 4a8d6b74b0c8a154). `reports/run4/contribution_decomposition.md`, `reports/run3/metric_audit_v3.md`.

## 5 AI-BILL
Boundary: SIM_DATA_PROFILE cell + MEASURED DS07 facility (not synchronised); TNB ToU rule (peak-period 30-min MD); 1 cell; 6 factories
(Forge_1, Forge_2, Metal_1, Metal_3, Paper, Steel_1) x forecaster TEST months 2019-08/09 = 12 facility-months; factory-clustered paired
bootstrap CI (+ = lower billed-demand increment). Raw: Drive `MyDrive/semiexpo/ai_runs/run4/fac_aibill_*/facility_md.csv`, summary
`MyDrive/semiexpo/ai_runs/run4_final_summary.md`; forecaster `run4/facility_load/facility_predictor.joblib` (global LightGBM across factories,
Mar-Jun train, Jul val, Aug-Sep test, 2-h decision stride; src/regenate/forecasting/facility_load.py).

| Comparison | kW [95 % CI] | months better |
|---|---|---|
| P0-BILL hist -> P0-BILL ai (value of the learned forecast) | +0.10 [0.00, +0.30] | 1/12 |
| P0-E1-Peak -> P0-BILL ai | -0.84 [-2.70, +1.31] n.s. | 5/12 |
| P0-E1-Peak -> P0-BILL oracle (perfect background) | +2.56 [+0.90, +4.34] | 8/12 |
| P0-BILL ai -> P0-BILL oracle (headroom missed by AI) | +3.40 [+1.83, +4.76] | 9/12 |
Per facility-month MD increment, kW (P0-E1-Peak / P0-BILL ai / P0-BILL oracle): Forge_1 Aug 7.53/7.23/2.88, Sep 2.73/7.47/5.63; Forge_2 Aug
-0.73/-0.73/-0.73, Sep -0.22/6.47/-0.33; Metal_1 Aug 9.21/8.25/0.32, Sep 3.14/1.95/0.93; Metal_3 Aug -3.46/-3.46/-3.46, Sep 7.30/0.00/0.00;
Paper Aug 2.85/6.12/-0.16, Sep 9.76/8.64/3.01; Steel_1 Aug 1.06/2.68/0.00, Sep 0.00/4.57/0.31.
Earlier months (2019-05/07, 12 facility-months, reports/run4/facility_billing.md): P0-BILL hist -0.57 [-2.56, +0.89], oracle +0.94 [-0.80, +2.96] vs
P0-E1-Peak (n.s.); 5-cell P0-BILL worse than P0-E1-Peak by ~6 kW.
Forecaster accuracy (test months Aug-Sep, 10 factories, decision stride 2 h, metrics re-exported with `--reuse` after the duplicate-column fix,
no retraining; Drive `MyDrive/semiexpo/ai_runs/run4/facility_load_metrics/metrics.csv`), mean over factories:
| Horizon (15-min slots) | LightGBM skill vs hist | persistence skill vs hist | Q-LightGBM P50 skill | LightGBM peak recall | P10-P90 coverage |
|---|---|---|---|---|---|
| 1-4 | +0.32 | +0.66 | +0.30 | 0.08 | 0.62 |
| 5-16 | +0.29 | +0.34 | +0.27 | 0.07 | 0.60 |
| 17-32 | +0.24 | +0.04 | +0.24 | 0.07 | 0.60 |
| 33-60 | +0.19 | -0.23 | +0.20 | 0.06 | 0.60 |
MAE improves on the historical profile, but peak-event recall is <= 0.13 and intervals are under-covered (0.60 vs 0.80): the forecast does
not locate the facility peaks that drive the bill, which explains the downstream NO-GO.

**Go/No-Go: AI-BILL = NO-GO.** The learned facility-load forecast is indistinguishable from the historical-profile forecast (+0.10 kW, 1/12) and
does not beat the default engine. A perfect background forecast would give a significant billing gain in the test months (+2.56 kW vs
P0-E1-Peak) but not in May/July, so billing-aware scheduling is a conditional research lead that needs real facility meter data, not a
deployable function. Default remains P0-E1-Peak (D006/D019). No further AI scheduling experiments (D018/D019).

## 6 Energy optimisation ladder B0..ORACLE

Reconciliation (SIM_DATA_PROFILE): baselines are matched by instance within each file; P0 rows match across the diagnostic and Run 3 forecast files. In the Run 2 ladder B3 has one infeasible tardiness-stage instance (99/100 optimal); flex 1.0 has time-limit incumbents for ORACLE 17/26 and B3 18/26, so the reported oracle saving is a lower bound, not a certified optimum: MyDrive/semiexpo/ai_runs/v2_flex1/results.csv (sha256 43b3f53afd3a6284). Rolling P0 has higher mean tardiness than one-shot methods (0.18?0.25 h versus 0.105?0.174 h); energy comparisons are not equal-production unless an equal-tardiness subset is stated. In the merged E1 run B2 has 13/100 violations, P0 1/100, and optimized one-shot 0; PQd has 2/100: MyDrive/semiexpo/ai_runs/run4/v2_wpc_gated (sha256 f346ca242945923d), MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv (sha256 57cd90452ba6e187).

DS06 replays measured DS05 cycle shapes with assumed scaling and windows: **SIM_DATA_PROFILE**, site NOT_VERIFIED. Same ledger and paired instances are intended; differing tardiness and electrical conditions require reconciliation before causal claims (`reports/run3/metric_audit_v3.md`). Means below have no reported CI; raw result `MyDrive/semiexpo/ai_runs/v2_flex025_n100.csv`, source `reports/ai/ai_exp12_ds06.md`.

| Method | n | Net M0 kWh/instance | Peak kW | CI |
|---|---:|---:|---:|---|
| B0 / B1 / B1-OPT | 100 | 69.02 / 11.52 / 11.52 | 22.71 / 15.26 / 14.71 | Not reported |
| B1p / B1p-OPT / B2 | 100 | 9.45 / 9.45 / 8.69 | 14.71 / 14.23 / 14.64 | Not reported |
| B3 | 99 | 8.55 | 11.60 | Not reported |
| P0 / P1 / P2 / P3 / P4 / ORACLE | 100 | 8.45 / 8.46 / 8.47 / 8.47 / 8.47 / 8.35 | 11.34 / 11.68 / 11.58 / 11.90 / 11.74 / 10.19 | Not reported |

Primary comparison, B1 → P0-E1-Peak: 3.077 kWh saved [2.967, 3.186], peak reduction 4.54 kW [3.76, 5.31], paired 95% CI, n=100, SIM_DATA_PROFILE; raw `ai_runs/run4_rt2/v2_e1_peak100` and `run4_rt2/v2_e1_peak_b/results.csv`, `reports/run3/e1_electrical_constraints.md`. P0 tardiness 0.18 h versus 0.14 h one-shot, and P0 has one modeled violation versus 13 for B2: unequal tardiness and modeled violations limit this comparison; MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv (sha256 57cd90452ba6e187). P0 → ORACLE energy headroom 0.094 kWh [0.077, 0.112], n=100, SIM_DATA_PROFILE, `MyDrive/semiexpo/ai_runs/v2_flex025_n100.csv`; P1 versus P0 is 0.018 kWh worse [0.005, 0.030], same source. Import/export, direct reuse and matching ratio, throughput/makespan, solver runtime and gap for this matched ladder: NOT_VERIFIED here; do not infer them from net energy.

Additional matched ladder comparisons: n=100 except B3 n=99, paired 95% CI, SIM_DATA_PROFILE; baseline and raw `MyDrive/semiexpo/ai_runs/v2_flex025_n100.csv` (`reports/ai/ai_exp12_ds06.md`). Positive means lower energy or peak than baseline.

| Baseline -> method | kWh [CI] | peak kW [CI] | wins energy |
|---|---|---|---|
| B1 -> B2 | 2.84 [2.73, 2.95] | Not reported | 100/100 |
| B1p-OPT -> ORACLE | 1.094 [1.037, 1.148] | Not reported | 100/100 |
| P0 -> P1 | -0.018 [-0.030, -0.005] | -0.34 [-0.83, 0.13] | 27/100 |
| P0 -> P2 | -0.019 [-0.031, -0.007] | -0.25 [-0.73, 0.23] | 22/100 |
| P0 -> P3 | -0.024 [-0.038, -0.009] | -0.57 [-1.08, -0.06] | 27/100 |
| P0 -> P4 | -0.026 [-0.041, -0.012] | -0.40 [-1.00, 0.20] | 27/100 |
| P0 -> ORACLE | 0.094 [0.077, 0.112] | 1.14 [0.57, 1.72] | 94/100 |

## 7 Electrical feasibility

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

Reconciliation (SIM_DATA_PROFILE): baselines are matched by instance within each file; P0 rows match across the diagnostic and Run 3 forecast files. In the Run 2 ladder B3 has one infeasible tardiness-stage instance (99/100 optimal); flex 1.0 has time-limit incumbents for ORACLE 17/26 and B3 18/26, so the reported oracle saving is a lower bound, not a certified optimum: MyDrive/semiexpo/ai_runs/v2_flex1/results.csv (sha256 43b3f53afd3a6284). Rolling P0 has higher mean tardiness than one-shot methods (0.18?0.25 h versus 0.105?0.174 h); energy comparisons are not equal-production unless an equal-tardiness subset is stated. In the merged E1 run B2 has 13/100 violations, P0 1/100, and optimized one-shot 0; PQd has 2/100: MyDrive/semiexpo/ai_runs/run4/v2_wpc_gated (sha256 f346ca242945923d), MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv (sha256 57cd90452ba6e187).

D019 retains AFE 20 kW / bus 32 kW as the reference and identifies AFE 20 kW / bus 16 kW as the cost-optimised candidate. On the same 30 simulated instances the candidate has zero violations, 100% twin approval, and unchanged energy and tardiness; raw MyDrive/semiexpo/ai_runs/run4_rt3/v2_size_afe20_bus16 (sha256 9b253122). AFE 10 kW has three infeasible ORACLE cases: MyDrive/semiexpo/ai_runs/run4_rt3/v2_size_afe10_bus32 (sha256 ad65c2b5dcde9508).

| Comparison | Result | Boundary and raw evidence |
|---|---|---|
| E0 → E1 twin approval, ORACLE | 98% → 100%, n=50; P0 100% → 100%; CI not reported | SIM_DATA_PROFILE; `MyDrive/semiexpo/ai_runs/run3/v2_e1/results.csv`, `screen_e1.csv`; `reports/run3/e1_electrical_constraints.md` |
| E1 cost, ORACLE vs E0 | +0.0021 kWh [0.0006, 0.0043], paired 95% CI, n=50 | SIM_DATA_PROFILE; same run and report |
| Sizing, E1 | At 15 kW AFE / 32 kW bus, P0 has 1 violation and twin approval 0.967; at 20 / 16 kW, P0 and B2 have zero violations and approval 1.000; n=30, CI not reported | SIM_DATA_PROFILE; `ai_runs/run4_rt3/sizing_summary.csv`, `ai_runs/run4_rt3/screen_sizing_summary.csv`; `reports/run3/e1_electrical_constraints.md` |
| 10 kW AFE | ORACLE 27/30 solved; P0 twin approval 0.667; CI not reported | SIM_DATA_PROFILE; same sizing paths |

The later sizing screening table is the D019 simulation evidence; its older pending placeholder is superseded. UV and overcurrent are modeled rejection causes; actual voltage/current excursions and protection qualification are NOT_VERIFIED. Twin parameters are assumed; independent protection and engineer approval remain required. Failure injection v1 and v2 report simulation-only passes, respectively `runs/fail_v1/pytest_run3.log` and `runs/run3/fail/pytest_fail2_run2.log`, SIM_ASSUMED_PROFILE; case evidence `runs/fail_v1/` and `runs/run3/fail/`, sources `reports/safety/failure_injection.md`, `reports/run3/failure_injection_v2.md`.

Full sizing results, n=30, CI not reported, SIM_DATA_PROFILE; raw `ai_runs/run4_rt3/sizing_summary.csv`, `ai_runs/run4_rt3/screen_sizing_summary.csv`; `reports/run3/e1_electrical_constraints.md`. The reported screening is simulation only.

| AFE / bus kW | ORACLE solved; peak kW | P0 violations; peak kW | B2 violations | twin approval B2 / P0 / ORACLE |
|---|---|---|---|---|
| 10 / 32 | 27/30; 7.87 | 15; 8.85 | 66 | 0.100 / 0.667 / 1.000 of solved |
| 15 / 32 | 30/30; 8.62 | 1; 10.04 | 16 | 0.633 / 0.967 / 1.000 |
| 15 / 24 | 30/30; 8.62 | 1; 10.07 | 16 | Not reported |
| 20 / 16 | 30/30; 8.59 | 0; 10.19 | 0 | 1.000 / 1.000 / 1.000 |
| 20 / 24 | 30/30; 8.81 | 0; 10.23 | 0 | Not reported |
| 20 / 32 | 30/30; 8.81 | 0; 10.23 | 0 | Not reported |
| 30 / 32 | 30/30; 8.81 | 0; 10.23 | 0 | 1.000 / 1.000 / 1.000 |

E0 -> E1 twin approval for B2 is 94% -> 94% and B1p-OPT 92% -> 92%, n=50, CI not reported, SIM_DATA_PROFILE, raw `MyDrive/semiexpo/ai_runs/run3/v2_e1/results.csv`, `screen_e1.csv` (`reports/run3/e1_electrical_constraints.md`). V1 cases: forecast wrong, sensor loss, MES disconnect, AFE saturation, bus overvoltage, test delay, engineer reject, solver timeout, replanner exception; v2: solver timeout, invalid AI, NaN power, engineer rejection. Case-level simulated PASS evidence is the individual JSON files in `runs/fail_v1/` and `runs/run3/fail/`, SIM_ASSUMED_PROFILE, `reports/safety/failure_injection.md`, `reports/run3/failure_injection_v2.md`.

## 8 Facility level

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

DS06 simulated cells are added to unsynchronised measured DS07 facility loads, not site savings; **SIM_DATA_PROFILE + MEASURED**, site NOT_VERIFIED. DS08 robustness is MISSING: metadata audit only, no archive or qualifying complete customer subset (`reports/run4/ds08_audit.md`, `data/manifests/ds08_metadata.json`). DS07 uses 10 factories and 70 factory-months; factory-clustered paired 95% CI supersedes month-level CI. Source `reports/run4/facility_billing.md`, raw `MyDrive/semiexpo/ai_runs/run4/fac_grid_tnb/facility_md.csv` and `ai_runs/run4/fac_{gen,tou}_{3,5,10}cells`.

| Baseline → method | Rule | Mean MD reduction kW [95% CI] | Factories won | n |
|---|---|---|---|---|
| B2 → P0-E1-Peak | General | 2.12 [0.86, 3.32] | 9/10 | 70 |
| B2 → P0-E1-Peak | ToU | 1.73 [0.73, 2.68] | 8/10 | 70 |
| B1p-OPT → P0-E1-Peak | ToU | 1.06 [-0.22, 2.30] | 8/10 | 70 |

Median coincidence of cell peak with billed demand is 0.09 for P0-E1-Peak and 0.24 for B2, all-hours, n=70; CI and full win/tie/loss breakdown not reported (`reports/run4/facility_billing.md`, raw `ai_runs/run4/fac_grid_tnb/`). The 100-instance-pool ToU B2 → P0 effect is 1.93 kW [0.69, 3.07], n=70; the earlier peak-level and perfect-information effects are WITHDRAWN because their larger-pool CIs include zero (`ai_runs/run4_rt2/fac_{gen,tou}_1cell_n100`). Holiday-off-peak sensitivity gives 0.97 kW [-0.01, 1.91] for one cell and 3.13 [0.98, 5.20] for five, n=70, factory-clustered CI; raw `ai_runs/run4_rt2/`, source `reports/run4/facility_billing.md`. Holiday treatment is NOT_VERIFIED.

Full factory-clustered comparisons, n=70 facility-months, 10 factories, 95% CI, SIM_DATA_PROFILE + unsynchronised MEASURED; General raw MyDrive/semiexpo/ai_runs/run4/fac_grid (sha256 6e669d46a861fe54), ToU raw `MyDrive/semiexpo/ai_runs/run4/fac_grid_tnb/facility_md.csv`; `reports/run4/facility_billing.md`. Factory ties/losses are not reported and must not be inferred from wins.

| Baseline -> method | General kW [CI], factories won | ToU kW [CI], factories won |
|---|---|---|
| B1p-OPT -> P0-E1-Peak | 1.86 [0.83, 2.79], 9/10 | 1.06 [-0.22, 2.30], 8/10 |
| B2 -> P0 | 1.89 [0.73, 3.02], 9/10 | 1.21 [0.41, 2.03], 7/10 |
| P0 -> P0-E1-Peak | 0.23 [-0.11, 0.61], 4/10 | 0.52 [0.08, 0.96], 7/10; withdrawn as non-robust |
| P0-E1-Peak -> ORACLE-E1-Peak | 0.22 [-0.02, 0.48], 7/10 | 0.59 [0.09, 1.03], 7/10; withdrawn as non-robust |

100-pool results, same n and boundary, raw `ai_runs/run4_rt2/fac_{gen,tou}_1cell_n100`, `reports/run4/facility_billing.md`:

| Baseline -> method | General kW [CI]; factories | ToU kW [CI]; factories |
|---|---|---|
| B2 -> P0-E1-Peak | 1.94 [1.12, 2.80]; 9/10 | 1.93 [0.69, 3.07]; 8/10 |
| B1p-OPT -> P0-E1-Peak | 1.94 [0.57, 3.19]; 8/10 | 2.18 [0.98, 3.21]; 8/10 |
| P0 -> P0-E1-Peak | 0.13 [-0.20, 0.48]; 6/10 | -0.00 [-0.30, 0.30]; 4/10 |
| P0-E1-Peak -> ORACLE-E1-Peak | 0.38 [-0.11, 0.88]; 6/10 | -0.04 [-0.55, 0.48]; 4/10 |

## 9 Multi-cell

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

Independent scheduling behind one meter; same boundary, n=70 and clustered CI as section 8. Raw `ai_runs/run4/fac_{gen,tou}_{3,5,10}cells`; source `reports/run4/facility_billing.md`.

| Cells | Baseline → method | General MD reduction kW [95% CI] | ToU MD reduction kW [95% CI] |
|---|---|---|---|
| 1 | B2 → P0-E1-Peak | 2.12 [0.86, 3.32] | 1.73 [0.73, 2.68] |
| 3 | B2 → P0-E1-Peak | 4.55 [2.59, 6.41] | 3.34 [1.07, 5.72] |
| 5 | B2 → P0-E1-Peak | 5.99 [4.53, 7.41] | 5.11 [2.92, 7.42] |
| 10 | B2 → P0-E1-Peak | 15.12 [11.48, 18.12] | 12.26 [9.14, 15.02] |

Coordinated P0-BILL five-cell cases worsened billed demand against P0-E1-Peak; n=2, CI not reported, SIM_DATA_PROFILE + unsynchronised MEASURED, raw `ai_runs/run4/`, `reports/run4/facility_billing.md`. Multi-cell energy, feasibility and solver scalability are NOT_VERIFIED as matched summaries; monetary estimates are in section 11.

P0-E1-Peak -> ORACLE-E1-Peak ToU reductions, same n, boundary and raw as above: 1 cell 0.59 [0.09, 1.03], 3 cells 0.01 [-0.95, 0.95], 5 cells 0.01 [-0.79, 0.87], 10 cells 1.91 [0.73, 3.02] kW; the one-cell result is withdrawn under the larger-pool test (`reports/run4/facility_billing.md`). Coordinated five-cell cases, P0-E1-Peak -> P0-BILL: 13.4 -> 19.2 and 17.8 -> 23.8/25.4 kW, approximately 23 kWh/month more; n=2, CI not reported, raw `ai_runs/run4/`, SIM_DATA_PROFILE + unsynchronised MEASURED (`reports/run4/facility_billing.md`).

## 10 Tariff validation

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

SOURCE_REPORTED, geographic counterfactuals, not actual DS07 bills. TNB schedule [official PDF](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf), p.2: General “Setiap kilowatt permintaan maksimum sebulan”; ToU adds “semasa tempoh puncak”. General uses whole-month MD, ToU peak-period MD. The older registry's General peak-only entry is superseded (`reports/run4/facility_billing.md`, `reports/final/report_run4.md`). TNB's [MD page](https://www.tnb.com.my/commercial-industrial/maximum-demand/how-do-you-calculate-md-charge) verifies 30-minute MD (D018); alignment and public-holiday handling remain NOT_VERIFIED.

MV General energy 0.2983 MYR/kWh, demand capacity 29.43 and network 59.84 MYR/kW/month; MV ToU energy peak/off-peak 0.3132/0.2723 MYR/kWh. TNB MV/HV schedule rates and peak window are VERIFIED against p.2 of the owner-supplied official PDF, SHA-256 e6634bbeec72c58c6d544c0d73953dda5616b742131453a73e889d307395a43e; holiday treatment is NOT documented. The older registry status is superseded. Source `reports/run4/tariff_registry.md`, `reports/run4/economics_run4.md`; source schedule `data/tariffs/sources/Tariff-TNB-pdf.pdf`; n/CI not applicable. Vietnam actual rates are NOT_VERIFIED pending exact page; [VN trial](https://www.evn.com.vn/d/vi-VN/news/Trien-khai-thu-nghiem-gia-ban-le-dien-hai-thanh-phan-tu-thang-102025-60-142-505112) is TRIAL_NOT_PAYABLE; [Singapore schedule](https://www.spgroup.com.sg/dam/jcr:ed6d35eb-7bb5-450c-8386-b61f0cc13142/Transmission%20Service%20Rate%20Schedule%20(effective%20from%201%20Jul%202026).pdf) contract/excess rates are 14.21/21.32 SGD/kW/month, SOURCE_REPORTED, table 9 (`reports/run4/tariff_registry.md`). Billing-engine test output path NOT_VERIFIED; incomplete calculations exclude charges listed in the registry.

## 11 Economics

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

FIN-A has no energy value by physics; FIN-B adds software to existing shared hardware; FIN-C includes unscoped hardware (`docs/decisions.md` D017; `reports/run4/economics_run4.md`). The following FIN-B estimates use B2 → P0-E1-Peak, n=70 facility-months, SIM_DATA_PROFILE + unsynchronised MEASURED, assumed annualisation and FX; factory-clustered ranges; raw `ai_runs/run4/fin_fac_{gen,tou}_fx{0.21,0.24}/`. Known site CAPEX USD 4,220 is an estimate; installation, requalification and support are MISSING. Paybacks are optimistic, site NOT_VERIFIED.

| Cells | MV General annual USD [range] | General payback y | MV ToU annual USD [range] | ToU payback y |
|---|---|---|---|---|
| 1 | 484 [201, 755] | 8.7 | 430 [185, 663] | 9.8 |
| 3 | 1,048 [608, 1,466] | 4.0 | 838 [284, 1,421] | 5.0 |
| 5 | 1,388 [1,060, 1,707] | 3.0 | 1,288 [752, 1,851] | 3.3 |
| 10 | 3,482 [2,662, 4,157] | 1.2 | 3,071 [2,310, 3,746] | 1.4 |

General five-cell CAPEX ceilings for 3/5/10 years are USD 4,164/6,940/9,314, respectively; ten-cell USD 10,445/17,408/23,362. Ten-year ceiling is discounted. 10-y NPV at 8 % on known CAPEX (factory-clustered mean, raw `ai_runs/run4/fin_fac_{gen,tou}_fx0.21/clustered_summary.csv`): MV General 1/3/5/10 cells -972/+2,814/+5,094/+19,142 USD; MV ToU -1,334/+1,402/+4,421/+16,388 USD (OPTIMISTIC: missing costs excluded). Monthly savings = annual/12. FX sensitivity is in the raw CSVs; tariff, holiday, missing OPEX and site costs materially affect conclusions (`reports/run4/economics_run4.md`). Corrected: three cells reach a five-year (not three-year) payback on known CAPEX only (MV General 4.0 y, MV ToU 5.0 y); additional missing costs can extend the payback beyond that threshold (`reports/run4/economics_run4.md`, correction note).

Complete published FIN-B rows below: B2 -> P0-E1-Peak, n=70, SIM_DATA_PROFILE + unsynchronised MEASURED, ASSUMED FX and annualisation, factory-clustered ranges; raw `ai_runs/run4/fin_fac_{gen,tou}_fx{0.21,0.24}/`, `reports/run4/economics_run4.md`. CAPEX ceilings in USD; 10-year ceiling discounted. Missing costs and source inconsistencies above apply.

| Tariff; cells | Annual USD [range] | 3 / 5 / 10-year ceiling USD | Payback years |
|---|---|---|---|
| MV General; 1 | 484 [201, 755] | 1,452 / 2,421 / 3,248 | 8.7 |
| MV General; 3 | 1,048 [608, 1,466] | 3,145 / 5,241 / 7,034 | 4.0 |
| MV General; 5 | 1,388 [1,060, 1,707] | 4,164 / 6,940 / 9,314 | 3.0 |
| MV General; 10 | 3,482 [2,662, 4,157] | 10,445 / 17,408 / 23,362 | 1.2 |
| MV ToU; 1 | 430 [185, 663] | 1,290 / 2,150 / 2,886 | 9.8 |
| MV ToU; 3 | 838 [284, 1,421] | 2,514 / 4,189 / 5,622 | 5.0 |
| MV ToU; 5 | 1,288 [752, 1,851] | 3,863 / 6,438 / 8,641 | 3.3 |
| MV ToU; 10 | 3,071 [2,310, 3,746] | 9,214 / 15,356 / 20,608 | 1.4 |
| HV General; 10 | 1,305 [1,019, 1,541] | 3,916 / 6,527 / 8,759 | 3.2 |
| HV ToU; 10 | 1,494 [1,142, 1,805] | 4,481 / 7,468 / 10,022 | 2.8 |

HV smaller-cell results are not tabulated in the source; `ai_runs/run4/fin_fac_{gen,tou}_fx{0.21,0.24}/clustered_summary.csv` requires retrieval. FIN-C hardware CAPEX, installation, qualification and support OPEX are MISSING; FIN-A value is bounded by the in-rack physics assumption (`docs/decisions.md`, `reports/run4/economics_run4.md`).

## 12 Contribution decomposition

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

Values below are paired reductions with 95% CI, SIM_DATA_PROFILE, not additive: subsets, information, objectives and tardiness differ; topology-only attribution and raw reconciliation NOT_VERIFIED. Source `reports/run4/contribution_decomposition.md`; raw `MyDrive/semiexpo/ai_runs/v2_flex025_n100.csv`.

| Layer and baseline | n | Mean reduction kWh [95% CI] |
|---|---:|---|
| Hardware B0 → B1 | 100 | 57.49 [55.61, 59.41] |
| Static scheduling B2 → B3 | 99 | 0.218 [0.189, 0.248] |
| Rolling B3 → P0 | 99 | 0.018 [0.009, 0.028] |
| Topology B1p-OPT → B2 | — | NOT_VERIFIED: scheduling also changes |

Peak and billing contributions are joint E1/peak and facility effects, not isolated additive benefits; see sections 8–9. AI energy benefit is not demonstrated: P0 → P5s -0.004 kWh [-0.010, 0.004], SIM_DATA_PROFILE, n=100, raw `MyDrive/semiexpo/ai_runs/run3/v2_p5/results.csv` (`reports/run3/ai_run3.md`). AI-BILL completed: NO-GO (learned forecast +0.10 kW [0.00, +0.30] vs historical profile, -0.84 [-2.70, +1.31] vs P0-E1-Peak; section 5, D020); no AI adoption claim.


Run 4 default P0 had 1/100 modeled AFE-shortfall violations: `v2_test_n10_s62`, one step, 0.259 kWh (SIM_DATA_PROFILE; `MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv`, sha256 57cd90452ba6e187). D021 verification (`MyDrive/semiexpo/ai_runs/run4/v2_safe_p0`; `reports/run3/e1_electrical_constraints.md`, Safety closure) reports 99/100 violation-free and zero unscreened fallbacks. FIFO is screened before execution; s62 remains a hardware-protection case. Industrial protection and site acceptance remain NOT_VERIFIED.

## Safety closure (D021): fallback screening and the residual P0 violation (Colab runtime 1, Drive `ai_runs/run4/v2_safe_p0`, `v2_safe_chk*`)
Changes (src/regenate/evaluation/v2_campaign.py `safe_initial`, `--plan_prm`): rolling P0 now starts from, and falls back to, a recipe-based
one-shot MILP that satisfies the E1 hard limits; fallback chain = MILP with planning margin (AFE 18 kW) -> MILP with the hard limits (20 kW) ->
FIFO screened on the recipe profiles with the hard limits (`fifo_screened_ok` / `fifo_screened_FAIL` recorded). FIFO is never executed
unscreened. Scoring always uses the hard limits (AFE 20 kW, bus 32 kW, step 10 kW).
| Run (n = 100, P0-E1-Peak) | violations | initial plan | energy vs previous P0 | peak vs previous P0 | tardiness vs previous P0 |
|---|---|---|---|---|---|
| previous (FIFO start, no margin), `run4_rt2/v2_e1_peak100` | 1 (s62) | FIFO | - | - | - |
| safety fix (MILP-E1 start, plan margin 18 kW), `run4/v2_safe_p0` | 1 (s62) | 99 milp_e1, 1 FIFO (s53, MILP infeasible; later screened ok) | -0.0017 kWh | -0.149 kW | +0.010 h |
Residual: instance v2_test_n10_s62 keeps 1 AFE-shortfall step (0.26 kWh, peak 20.62 kW) with planning margins 18, 17 and 16 kW alike; the plan
is feasible on the recipe, the shortfall comes from the true cycles deviating from the recipe (the ORACLE, which knows the true cycles,
has 0 violations). No recipe-based plan can guarantee it; it is a hardware-protection case (AFE current limit / station derating) and is
listed as a residual risk for site acceptance. Simulation acceptance: 99/100 instances violation-free, 0 unscreened fallbacks.

## 13 Industrial applicability

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

D018 fixes the reference as a Chroma 17020-type regenerative battery module cycling cell, rated 48 kW/cell; DS06 assumes 8 stations, 25 modules/station at 0.24 kW/module, 20 kW AFE, 32 kW link and 10 kW step. These are ASSUMED simulation settings, not vendor specifications; baseline and CI not applicable, n not applicable (`docs/decisions.md`, D007/D018; `reports/final/report_run4.md`; raw configuration binding NOT_VERIFIED). Chroma documents independent charge/discharge channels, reuse to charging channels or mains, recipes and protection (VENDOR_REPORTED; `reports/run4/vendor_reference.md`). Internal bus topology, external access and scheduling rights are NOT_VERIFIED.

Bidirectional DC-DC, battery-emulator, power-module cycling, storage and EV power-conversion testing are conditional transfer candidates. Each needs independently timed residual source and sink at the station boundary after local reuse; a bidirectional DUT alone is insufficient. Converter burn-in has no residual under the D001 assumptions (`reports/run4/industrial_use_case_matrix.md`; `docs/decisions.md`). Site validation needs synchronized signed station and facility metering, movable start windows, converter curves, vendor interface rights, quality records, tariffs, protection study and costs (`reports/run4/mentor_data_request.md`). Semiconductor applicability and site acceptance remain NOT_VERIFIED.


| Candidate | Eligibility and missing evidence |
|---|---|
| Battery module cycling | Reference; site residual phases, reuse, windows and mentor acceptance NOT_VERIFIED. |
| Bidirectional DC-DC validation | Conditional; net station traces after local reuse and independent windows needed. |
| Battery-emulator power electronics | Conditional; meter both net phases and document setup and starts. |
| Power-module cycling | Conditional; DUT topology, residual traces and independent starts needed. |
| Energy-storage module testing | Conditional; boundary traces, actual equipment and reuse needed. |
| EV power conversion | Conditional; net phases, topology and test constraints needed. |
| Converter burn-in | Ineligible under D001 assumptions; measured exceptions require review. |

Source and boundary: `reports/run4/industrial_use_case_matrix.md`, `docs/target_cell_spec.md`; site NOT_VERIFIED; vendor descriptions VENDOR_REPORTED.

## 14 Product readiness

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

The software-first deployment paths are FIN-A existing regen-to-AC, FIN-B existing compatible shared-energy infrastructure, and FIN-C full retrofit; FIN-B is preferred subject to site evidence (`docs/decisions.md`, D009/D018). The default is P0-E1-Peak with independent protection and twin screening; forecasting is advisory (`docs/decisions.md`, D006/D010/D012). Ledger, scheduler and simulation are documented in `src/regenate/electrical/ledger.py`, `src/regenate/optimization/milp.py`, `src/regenate/optimization/rolling.py`, and `src/regenate/simulation/replay.py` (`reports/run3/metric_audit_v3.md`). The file-backed dashboard provides facility load, tariff inputs, monthly charge estimates, FIN comparison and Markdown export; no live integration is established (`reports/run4/demonstrator_v2.md`). Dashboard screenshots are reported at `reports/run4/screenshots/` (final figure status in part 1); independent local inspection NOT_VERIFIED.

Offline demonstration: pipeline versus B1, n=1, net grid 10.086 versus 13.972 kWh, peak 13.429 versus 13.977 kW, equal tardiness 0 h, 10 completed jobs each and zero reported violations; CI unavailable, SIM_DATA_PROFILE. The source report has no exact raw-result path, so raw binding is NOT_VERIFIED (`reports/run3/demonstrator.md`). Failure injection reports invalid forecasts fall back to nominal and rejection executes FIFO; its test output is `runs/run3/fail/pytest_fail2_run2.log`, SIM_ASSUMED_PROFILE (`reports/run3/failure_injection_v2.md`). Solver stage status and missing gaps, matching, and dynamic protection remain unresolved (`reports/run3/metric_audit_v3.md`, `reports/final/report_run4.md`).


| Failure scenario | Simulation behavior and raw evidence |
|---|---|
| Solver timeout | Accepted plan retained; `runs/run3/fail/solver_timeout.json`. |
| Invalid AI / exception | Nominal fallback matched P0; `runs/run3/fail/ai_invalid.json`. |
| Nonfinite AI power | Finite nominal fallback; `runs/run3/fail/ai_nan.json`. |
| Engineer rejects | Initial FIFO executed; `runs/run3/fail/engineer_reject_all.json`. |

Boundary SIM_ASSUMED_PROFILE; `reports/run3/failure_injection_v2.md`. These checks do not establish physical safety.

## 15 Scientific evidence

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

Reconciliation (SIM_DATA_PROFILE): baselines are matched by instance within each file; P0 rows match across the diagnostic and Run 3 forecast files. In the Run 2 ladder B3 has one infeasible tardiness-stage instance (99/100 optimal); flex 1.0 has time-limit incumbents for ORACLE 17/26 and B3 18/26, so the reported oracle saving is a lower bound, not a certified optimum: MyDrive/semiexpo/ai_runs/v2_flex1/results.csv (sha256 43b3f53afd3a6284). Rolling P0 has higher mean tardiness than one-shot methods (0.18?0.25 h versus 0.105?0.174 h); energy comparisons are not equal-production unless an equal-tardiness subset is stated. In the merged E1 run B2 has 13/100 violations, P0 1/100, and optimized one-shot 0; PQd has 2/100: MyDrive/semiexpo/ai_runs/run4/v2_wpc_gated (sha256 f346ca242945923d), MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv (sha256 57cd90452ba6e187).

DS06 replays measured DS05 battery cycles with assumed scaling and timing: SIM_DATA_PROFILE, not semiconductor-site data. The diagnostic uses seeds 0–99, n=100, paired bootstrap 95% intervals and Drive raw results `MyDrive/semiexpo/ai_runs/run3/v2_diag/results.csv`; manifest binding MyDrive/semiexpo/ai_runs/run3/v2_diag/results.csv (sha256 4a8d6b74b0c8a154) (`reports/run3/root_cause_analysis.md`, `reports/run3/metric_audit_v3.md`). Facility studies use factory-clustered paired bootstrap intervals on unsynchronized MEASURED DS07 and SIM_DATA_PROFILE cells; exact campaign paths `ai_runs/run4/fac_{gen,tou}_{3,5,10}cells` and `MyDrive/semiexpo/ai_runs/run4/fac_grid_tnb/` (`reports/final/report_run4.md`).

Negative evidence includes station AI energy and production failures, monitoring failure, no stable P0-BILL gain and withdrawn larger-pool effects; AI-BILL is NO-GO (section 5, D020; raw `MyDrive/semiexpo/ai_runs/run4_final_summary.md`) (`reports/final/report_run4.md`, `docs/handoff_run4.md`). The metric audit identifies incomplete raw reconciliation, possible pairing collapse, unequal tardiness and planning constraints, incomplete solver status and one-shot versus rolling oracle differences; no site savings, safety, FPY or water outcome is established (`reports/run3/metric_audit_v3.md`).


| Diagnostic method | Result versus P0, kWh saved [paired 95% CI] | Evidence |
|---|---|---|
| TR_ALL / ORACLE | 0.094 [0.077, 0.112] | `MyDrive/semiexpo/ai_runs/run3/v2_diag/results.csv` |
| TR_Q | 0.049 [0.035, 0.064] | same raw file |
| TR_RUN | 0.024 [0.013, 0.037] | same raw file |
| P1* | -0.005 [-0.017, 0.007] | same raw file |
| P2* | 0.000 [-0.009, 0.009] | same raw file |
| P3* / P4* | -0.009 [-0.022, 0.003] | same raw file |

All rows: n=100, SIM_DATA_PROFILE; perfect-information diagnostics are not deployable. Tardiness differs between methods; causal matching is NOT_VERIFIED (`reports/run3/root_cause_analysis.md`, `reports/run3/metric_audit_v3.md`).

| Learned / information method | Energy saved versus P0, kWh [paired 95% CI] | Result |
|---|---|---|
| P5 | -0.022 [-0.034, -0.010] | FAIL |
| P5s | -0.004 [-0.010, 0.004] | FAIL, interval includes zero |
| PQ gated | -0.019 [-0.036, -0.006] | FAIL |
| PQ5 gated | -0.034 [-0.052, -0.018] | FAIL |
| PQ ungated | -0.045 [-0.066, -0.026] | FAIL |
| PQ* perfect cycle ratios | 0.008 [-0.007, 0.022] | not significant |
| TR_Q perfect queued profiles | 0.049 [0.035, 0.064] | diagnostic ceiling |

All rows: n=100, SIM_DATA_PROFILE, `reports/run3/ai_run3.md`; raw MyDrive/semiexpo/ai_runs/run3/v2_p5 (sha256 08e1bf44), MyDrive/semiexpo/ai_runs/run3/v2_pq_gated (sha256 9a345636), MyDrive/semiexpo/ai_runs/run3/v2_pq_ungated (sha256 17331443), MyDrive/semiexpo/ai_runs/run3/v2_pqd (sha256 42be5793), MyDrive/semiexpo/ai_runs/run3/v2_pqstar (sha256 0b3e7234). Production AI and automated monitoring also failed their downstream gates (`reports/run4/ai_production_planning.md`, `reports/run4/ai_monitoring.md`; raw monitoring `MyDrive/semiexpo/ai_runs/run4/monitor/`).

## 16 Visualization index

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

Earlier index-only figure statuses are superseded by the final status table below. Drive-generated figures have not been independently retrieved locally.

### Final figure status (Colab rerun 2026-11-25; files on Drive `MyDrive/semiexpo/ai_runs/run4/figures/` PNG+PDF+SVG+provenance JSON)
| Figure | Status | Note |
|---|---|---|
| F01, F02, F11 | MISSING | no matched per-sample prediction export for the Run 2 power forecaster in the collected inputs |
| F03-F10, F12-F15 | PASS (Run 2 files) | reports/figures/ (local repo) |
| F16, F19 | BLOCKED | generator requires identical P0 rows across campaign files; the numbers exist in reports/run4/p0_architecture.md and ai_production_planning.md |
| F17, F18 | GENERATED | ETA probabilistic band and error vs cycle progress (MEASURED DS05 test split) |
| F20, F23, F29, F31 | MISSING | not implemented (monitoring trade-off, AFE/link trade-off, energy vs demand cost split, payback heatmap); data in the cited reports |
| F21, F22, F24, F25, F27, F28, F30, F32 | GENERATED | SIM_DATA_PROFILE (+ MEASURED DS07 for F27/F28/F30) |
| F26 | BLOCKED | facility background differs between the General and ToU MD rules in the collected files |
Dashboard screenshots (16 pages, headless Chromium via Playwright): reports/run4/screenshots/ (local repo).


Run 4 default P0 had 1/100 modeled AFE-shortfall violations: `v2_test_n10_s62`, one step, 0.259 kWh (SIM_DATA_PROFILE; `MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv`, sha256 57cd90452ba6e187). D021 verification (`MyDrive/semiexpo/ai_runs/run4/v2_safe_p0`; `reports/run3/e1_electrical_constraints.md`, Safety closure) reports 99/100 violation-free and zero unscreened fallbacks. FIFO is screened before execution; s62 remains a hardware-protection case. Industrial protection and site acceptance remain NOT_VERIFIED.

## 17 Mentor compliance

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

Statuses below are inherited concept-level assessments, not fresh passes; each evidence source and gap is documented in `reports/run4/mentor_compliance_run4.md`. PASS is a documentation/decision assessment, with raw-run path NOT_VERIFIED except where identified below; it does not authorize deployment.

| ID | Requirement | Status | Remaining gap |
|---|---|---|---|
| M01 | Coordination | PASS | Presentation review; SOURCE_REPORTED  Evidence: `docs/traceability.md`. |
| M02 | Compatible cell | BLOCKED | Semiconductor transfer and site access NOT_VERIFIED  Evidence: `reports/run4/industrial_use_case_matrix.md`. |
| M03 | Flexibility and energy | PARTIAL | Matched baseline and site flexibility NOT_VERIFIED  Evidence: `reports/run4/contribution_decomposition.md`. |
| M04 | Loss ledger | PARTIAL | Site curves and configuration binding NOT_VERIFIED  Evidence: `reports/run3/metric_audit_v3.md`. |
| M05 | Shadow and pilot | BLOCKED | Site and engineer acceptance missing  Evidence: `reports/run4/demonstrator_v2.md`. |
| M06 | Protection and compatibility | PARTIAL | Hardware study and vendor approval missing  Evidence: `reports/run3/electrical_feasibility.md`. |
| M07 | Grounded profiles | PARTIAL | Battery proxy is not semiconductor data  Evidence: `docs/target_cell_spec.md`. |
| M08 | Site data | BLOCKED | Synchronized site records missing  Evidence: `reports/run4/mentor_data_request.md`. |
| M09 | Baselines and oracle | PARTIAL | Fairness and solver certificates incomplete  Evidence: `reports/run4/p0_architecture.md`. |
| M10 | Incremental M0 versus B1 | PARTIAL | Matched site evidence missing  Evidence: `reports/run3/e1_electrical_constraints.md`. |
| M11 | Quality and throughput | PARTIAL | Site FPY and integrity missing  Evidence: `reports/run3/failure_injection_v2.md`. |
| M12 | AI incremental value | FAIL | Evaluation completed; matched AI scheduling benefit not demonstrated; SIM_DATA_PROFILE, `MyDrive/semiexpo/ai_runs/run3/v2_diag/results.csv`  Evidence: `reports/run3/ai_run3.md`. |
| M13 | Statistics and sensitivity | PARTIAL | Complete raw reconciliation missing  Evidence: `reports/run4/facility_billing.md`. |
| M14 | Forecast and constrained optimizer | PARTIAL | Calibration and deployment validation missing  Evidence: `reports/run4/ai_eta.md`. |
| M15 | Electricity before water | PASS | Water metering missing; SOURCE_REPORTED, raw path NOT_VERIFIED  Evidence: `docs/traceability.md`. |
| M16 | Investment case | BLOCKED | Real costs and site contract missing  Evidence: `reports/run4/economics_run4.md`. |

## 18 Final decisions

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

| Decision | Disposition |
|---|---|
| D001 | Local reuse precedes shared transfer; residual source is required. |
| D002 | AI value depends on predictable uncertainty. |
| D003 | Oracle feasibility and first AI control: retain negative results. |
| D004 | Measured-cycle simulation: optimization carries the result. |
| D005 | Adopt peak-aware optimization; do not adopt AI for scheduling. |
| D006 | Default P0-E1-Peak; Run 3 analysis leaves the scheduling decision unchanged. |
| D007 | Battery cycling reference cell. |
| D008 | Semiconductor transfer conditional on station-boundary residual phases. |
| D009 | Software-first deployment with existing compatible infrastructure. |
| D010 | Retain ETA and advisory AI, subject to validation. |
| D011 | Conditional business case; full site costs required. |
| D012 | Electrical screening does not replace independent protection. |
| D013 | DS07 primary public facility dataset; DS08 optional. |
| D014 | TNB benchmark and Vietnam scenarios are counterfactual tariffs. |
| D015 | Evaluate monthly facility bills with actual tariff rules. |
| D016 | Separate hardware, topology, scheduling, peak and AI contributions. |
| D017 | Stop station scheduling AI and anomaly experiments; assess facility billing conditionally. |
| D018 | Prefer FIN-B at 5?10 cells conditionally; confirm 30-minute MD; site acceptance remains open. |
| D019 | Freeze architecture and reference AFE 20 / bus 32 kW; candidate AFE 20 / bus 16 kW; M12 FAIL. |
| D020 | AI-BILL NO-GO; retain AI for ETA and advisory. |
| D021 | Freeze architecture; E1-screened nominal fallback and AFE margin; simulation verification completed with residual s62 protection case. |

Source: `docs/decisions.md`; D018 cell range is ASSUMED deployment scenario, baseline and n/CI not applicable, raw site binding NOT_VERIFIED.

| Gate | Status | Evidence and boundary |
|---|---|---|
| G01 Reference cell | PARTIAL | `docs/decisions.md`; ASSUMED, site NOT_VERIFIED. |
| G02 Physics | PARTIAL | `docs/decisions.md`; analytic/unit test, run output NOT_VERIFIED. |
| G03 Matched comparisons | PARTIAL | `reports/run3/metric_audit_v3.md`; SIM_DATA_PROFILE; instance matching bound by `docs/raw_binding_manifest.md`, unequal tardiness remains. |
| G04 Information headroom | PARTIAL | `reports/run4/p0_architecture.md`; SIM_DATA_PROFILE, raw MyDrive/semiexpo/ai_runs/run3/v2_diag/results.csv (sha256 4a8d6b74b0c8a154). |
| G05 Energy AI | FAIL | `reports/run3/ai_run3.md`; SIM_DATA_PROFILE. |
| G06 ETA | PASS | `reports/run4/ai_eta.md`; MEASURED, `MyDrive/semiexpo/ai_runs/run4/eta/`. |
| G07 Production AI | FAIL | `reports/run4/ai_production_planning.md`; SIM_DATA_PROFILE. |
| G08 Electrical constraints | PASS | `reports/run3/e1_electrical_constraints.md`; SIM_DATA_PROFILE, `MyDrive/semiexpo/ai_runs/run3/v2_e1/results.csv`. |
| G09 Twin and protection | PARTIAL | `reports/run3/electrical_feasibility.md`; simulated screen, hardware NOT_VERIFIED. |
| G10 Facility billing | PARTIAL | `reports/run4/facility_billing.md`; SIM_DATA_PROFILE + MEASURED unsynchronized. |
| G11 Economics | PARTIAL | `reports/run4/economics_run4.md`; ASSUMED costs, site NOT_VERIFIED. |
| G12 Site acceptance | BLOCKED | `reports/run4/mentor_data_request.md`; SHADOW_SITE NOT_VERIFIED. |

Gate statuses are inherited assessments, not fresh validation (`reports/run4/mentor_compliance_run4.md`).

## 19 Research novelty

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

Prior work includes the CMC hybrid flow-shop scheduling baseline; vendor equipment already offers regeneration and channel reuse (`CLAUDE.md`, `reports/run4/vendor_reference.md`). The incremental proposal combines production-constrained coordination, explicit M0 accounting, electrical screening and facility billing evaluation; it is a system integration and evaluation, not a claim to invent regenerative hardware or vendor reuse (`reports/run4/contribution_decomposition.md`, `docs/decisions.md`). Shared-link results combine topology and optimization; isolated topology and software effects are NOT_VERIFIED. AI has no demonstrated downstream energy or peak benefit, and no site, fab-wide, water or safety claim is supported (`reports/final/report_run4.md`). The requested `reports/sources` directory is MISSING locally; a complete prior-art comparison and novelty against all publications remain NOT_VERIFIED.

## 20 Executive summary

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

The following are reported results, not independently reconciled site outcomes. Each interval is a 95% CI; differences are not additive. Drive raw bindings are listed in `docs/raw_binding_manifest.md`.

| Achievement / comparison | Mean and CI; n; boundary; raw path |
|---|---|
| B1 to P0-E1-Peak energy | 3.077 kWh [2.967, 3.186]; n=100; SIM_DATA_PROFILE; `ai_runs/run4_rt2/v2_e1_peak100` (`reports/final/report_run4.md`) |
| B1 to P0-E1-Peak peak | 4.54 kW [3.76, 5.31]; n=100; SIM_DATA_PROFILE; `ai_runs/run4_rt2/v2_e1_peak100` (`reports/final/report_run4.md`) |
| B2 to P0 energy | 0.160 kWh [0.080, 0.229]; n=100; SIM_DATA_PROFILE; `ai_runs/run4_rt2/v2_e1_peak100` (`reports/final/report_run4.md`) |
| B1p-OPT to ORACLE | 1.094 kWh [1.037, 1.148]; n=100; SIM_DATA_PROFILE; `MyDrive/semiexpo/ai_runs/run3/v2_diag/results.csv` (`reports/run3/root_cause_analysis.md`) |
| P0 to rolling truth | 0.094 kWh [0.077, 0.112]; n=100; SIM_DATA_PROFILE; same Drive path (`reports/run3/root_cause_analysis.md`) |
| P0 to queued truth | 0.049 kWh [0.035, 0.064]; n=100; SIM_DATA_PROFILE; same Drive path (`reports/run3/root_cause_analysis.md`) |
| P0 to running truth | 0.024 kWh [0.013, 0.037]; n=100; SIM_DATA_PROFILE; same Drive path (`reports/run3/root_cause_analysis.md`) |
| B2 to P0 facility demand, General, 5 cells | 5.99 kW [4.53, 7.41]; n=70 facility-months; SIM_DATA_PROFILE + MEASURED unsynchronized; MyDrive/semiexpo/ai_runs/run4/fac_gen_5cells (sha256 1263d44d) (`reports/final/report_run4.md`) |
| B2 to P0 facility demand, ToU, 5 cells | 5.11 kW [2.92, 7.42]; n=70 facility-months; same boundary, MyDrive/semiexpo/ai_runs/run4/fac_tou_5cells (sha256 53e74ab0) (`reports/final/report_run4.md`) |
| B2 to P0 facility demand, General, 10 cells | 15.12 kW [11.48, 18.12]; n=70 facility-months; same boundary, MyDrive/semiexpo/ai_runs/run4/fac_gen_10cells (sha256 7d0bf4f6) (`reports/final/report_run4.md`) |

Five principal weaknesses: site evidence absent; baseline matching and raw reconciliation incomplete; learned scheduling benefit failed; electrical protection and vendor access unvalidated; economics omit material site costs (`reports/final/report_run4.md`). Conditional GO for simulation and shadow preparation; NO-GO for site deployment and automatic station AI scheduling. Remaining work: reconcile remaining claims and production comparability, obtain site/mentor evidence and complete protection and economic qualification (`docs/handoff_run4.md`, `reports/run4/mentor_data_request.md`).


Run 4 default P0 had 1/100 modeled AFE-shortfall violations: `v2_test_n10_s62`, one step, 0.259 kWh (SIM_DATA_PROFILE; `MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv`, sha256 57cd90452ba6e187). D021 verification (`MyDrive/semiexpo/ai_runs/run4/v2_safe_p0`; `reports/run3/e1_electrical_constraints.md`, Safety closure) reports 99/100 violation-free and zero unscreened fallbacks. FIFO is screened before execution; s62 remains a hardware-protection case. Industrial protection and site acceptance remain NOT_VERIFIED.
