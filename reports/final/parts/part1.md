# Final evaluation — part 1

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

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

SIM_DATA_PROFILE cell plus unsynchronized MEASURED DS07 facility; site NOT_VERIFIED. `reports/run4/facility_billing.md`; exact raw paths for the causal extended table are not recorded there.

| Method | n | Result vs P0-E1-Peak | CI / source |
|---|---:|---|---|
| P0-BILL hist | 12 facility-months | -0.57 kW reduction | factory-clustered [-2.56,0.89]; `reports/run4/facility_billing.md` |
| P0-BILL oracle background | 12 facility-months | 0.94 kW reduction | factory-clustered [-0.80,2.96]; `reports/run4/facility_billing.md` |
| P0-BILL persistence | 4 facility-months | individual results in source | CI not recorded; `reports/run4/facility_billing.md` |
| AI-BILL and forecaster accuracy | not available | PENDING | expected `MyDrive/semiexpo/ai_runs/run4_final_summary.md` |

Go only if AI beats both historical P0-BILL and P0-E1-Peak with factory-clustered CIs excluding zero; otherwise no-go after evaluation. `docs/handoff_run4.md`, `docs/decisions.md` D017. No result is claimed while pending.


Recorded individual ToU billing results: SIM_DATA_PROFILE plus unsynchronized MEASURED DS07, n=4 facility-months; baseline P0-E1-Peak; kW monthly increment, CI not recorded; raw results MyDrive/semiexpo/ai_runs/run4/fac_p0bill5_Forge_2 (sha256 f427310b) and MyDrive/semiexpo/ai_runs/run4/fac_p0bill5_Metal_1 (sha256 150ec779), source `reports/run4/facility_billing.md`.

| Facility-month | P0-E1-Peak | hist | persist | oracle background | ORACLE-E1-Peak |
|---|---:|---:|---:|---:|---:|
| Forge_2 2019-05 | 0.80 | 3.19 | 4.48 | 1.36 | 0.00 |
| Forge_2 2019-07 | 0.37 | -1.69 | -1.69 | 2.05 | 0.57 |
| Steel_1 2019-05 | -0.02 | -0.03 | -0.03 | -0.03 | -0.02 |
| Steel_1 2019-07 | -3.01 | -3.04 | -3.01 | -3.04 | -4.18 |

Extended results: ORACLE-E1-Peak vs P0-E1-Peak +0.27 kW [-1.14, 1.98]; hist to oracle +1.50 kW [-0.01, 3.15]; n=12 facility-months, factory-clustered CI; raw results MyDrive/semiexpo/ai_runs/run4/fac_p0bill_Forge_1 (sha256 3f97864b), MyDrive/semiexpo/ai_runs/run4/fac_p0bill_Forge_2 (sha256 f9b5e7b8), MyDrive/semiexpo/ai_runs/run4/fac_p0bill_Metal_1 (sha256 443e386b), MyDrive/semiexpo/ai_runs/run4/fac_p0bill_Metal_3 (sha256 40072 0c6), MyDrive/semiexpo/ai_runs/run4/fac_p0bill_Paper (sha256 469be4dd), MyDrive/semiexpo/ai_runs/run4/fac_p0bill_Steel_1 (sha256 fb2731dd); `reports/run4/facility_billing.md`.

## 16 Visualization index

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

Status is based on index evidence only; PASS requires inspection and is not inferred. Original index `reports/figures/INDEX.md`; run-4 index `reports/run4/figures/INDEX.md`; boundary NOT_VERIFIED unless otherwise listed. F01/F02/F11 explicitly missing prediction rows. F16–F32 local run-4 figure files missing; the index lists selected campaign inputs as blocked. Figure file paths and full source data for F16–F32 are not recorded in the index.

| Figure | Path / source data | Status |
|---|---|---|
| F01, F02, F11 | no prediction rows; `reports/figures/INDEX.md` | MISSING |
| F03, F12 | `results/ai_ds05_branchC/model_metrics.csv` | NOT_VERIFIED: figure path/inspection not established |
| F04 | `runs/ai/ds02/model_metrics.csv`, `runs/ai/ds04/model_metrics.csv`, `results/ai_ds05_branchC/model_metrics.csv` | NOT_VERIFIED |
| F05 | `data/processed/efficiency_points.parquet`; VENDOR_REPORTED | NOT_VERIFIED |
| F06 | `runs/oracle_v1/timeseries.parquet`; SIM_ASSUMED_PROFILE | NOT_VERIFIED |
| F07 | `runs/twin_v1/controls.json`; SIM_ASSUMED_PROFILE | NOT_VERIFIED |
| F08, F14 | `runs/rolling_v1/ladder.csv`; SIM_ASSUMED_PROFILE | NOT_VERIFIED |
| F09 | `reports/ai/ai_exp12_ds06.md`; SIM_DATA_PROFILE | NOT_VERIFIED |
| F10 | `F10.png/pdf`, `runs/sens_v1/sensitivity_results.csv`; SIM_ASSUMED_PROFILE | NOT_VERIFIED: location/inspection not established |
| F13 | `runs/oracle_v1/schedules.parquet`, `runs/oracle_v1/results.csv`; SIM_ASSUMED_PROFILE | NOT_VERIFIED |
| F15 | `results/ai_ds05_branchC/runtime_metrics.csv`, `results/ai_ds05_branchC/model_metrics.csv` | NOT_VERIFIED |
| F16 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F17 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F18 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F19 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F20 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F21 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F22 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F23 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F24 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F25 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F26 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F27 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F28 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F29 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F30 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F31 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F32 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |

DOCUMENT CHECK: six required sections present; missing metrics and raw source bindings explicitly flagged. Boundary: NOT_VERIFIED.
