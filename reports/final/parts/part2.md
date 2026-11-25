# 6 Energy optimisation ladder B0..ORACLE

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

# 7 Electrical feasibility

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

# 8 Facility level

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

# 9 Multi-cell

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

# 10 Tariff validation

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

SOURCE_REPORTED, geographic counterfactuals, not actual DS07 bills. TNB schedule [official PDF](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf), p.2: General “Setiap kilowatt permintaan maksimum sebulan”; ToU adds “semasa tempoh puncak”. General uses whole-month MD, ToU peak-period MD. The older registry's General peak-only entry is superseded (`reports/run4/facility_billing.md`, `reports/final/report_run4.md`). TNB's [MD page](https://www.tnb.com.my/commercial-industrial/maximum-demand/how-do-you-calculate-md-charge) verifies 30-minute MD (D018); alignment and public-holiday handling remain NOT_VERIFIED.

MV General energy 0.2983 MYR/kWh, demand capacity 29.43 and network 59.84 MYR/kW/month; MV ToU energy peak/off-peak 0.3132/0.2723 MYR/kWh. TNB MV/HV schedule rates and peak window are VERIFIED against p.2 of the owner-supplied official PDF, SHA-256 e6634bbeec72c58c6d544c0d73953dda5616b742131453a73e889d307395a43e; holiday treatment is NOT documented. The older registry status is superseded. Source `reports/run4/tariff_registry.md`, `reports/run4/economics_run4.md`; source schedule `data/tariffs/sources/Tariff-TNB-pdf.pdf`; n/CI not applicable. Vietnam actual rates are NOT_VERIFIED pending exact page; [VN trial](https://www.evn.com.vn/d/vi-VN/news/Trien-khai-thu-nghiem-gia-ban-le-dien-hai-thanh-phan-tu-thang-102025-60-142-505112) is TRIAL_NOT_PAYABLE; [Singapore schedule](https://www.spgroup.com.sg/dam/jcr:ed6d35eb-7bb5-450c-8386-b61f0cc13142/Transmission%20Service%20Rate%20Schedule%20(effective%20from%201%20Jul%202026).pdf) contract/excess rates are 14.21/21.32 SGD/kW/month, SOURCE_REPORTED, table 9 (`reports/run4/tariff_registry.md`). Billing-engine test output path NOT_VERIFIED; incomplete calculations exclude charges listed in the registry.

# 11 Economics

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

# 12 Contribution decomposition

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

Values below are paired reductions with 95% CI, SIM_DATA_PROFILE, not additive: subsets, information, objectives and tardiness differ; topology-only attribution and raw reconciliation NOT_VERIFIED. Source `reports/run4/contribution_decomposition.md`; raw `MyDrive/semiexpo/ai_runs/v2_flex025_n100.csv`.

| Layer and baseline | n | Mean reduction kWh [95% CI] |
|---|---:|---|
| Hardware B0 → B1 | 100 | 57.49 [55.61, 59.41] |
| Static scheduling B2 → B3 | 99 | 0.218 [0.189, 0.248] |
| Rolling B3 → P0 | 99 | 0.018 [0.009, 0.028] |
| Topology B1p-OPT → B2 | — | NOT_VERIFIED: scheduling also changes |

Peak and billing contributions are joint E1/peak and facility effects, not isolated additive benefits; see sections 8–9. AI energy benefit is not demonstrated: P0 → P5s -0.004 kWh [-0.010, 0.004], SIM_DATA_PROFILE, n=100, raw `MyDrive/semiexpo/ai_runs/run3/v2_p5/results.csv` (`reports/run3/ai_run3.md`). AI-BILL completed: NO-GO (learned forecast +0.10 kW [0.00, +0.30] vs historical profile, -0.84 [-2.70, +1.31] vs P0-E1-Peak; section 5, D020); no AI adoption claim.


Run 4 default P0 has 1/100 modeled AFE-shortfall violations: instance `v2_test_n10_s62`, one step, 0.259 kWh (SIM_DATA_PROFILE; `MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv`, sha256 57cd90452ba6e187). D021 specifies an E1-screened nominal plan and fallback, FIFO only if infeasible with `initial_plan=fifo_unscreened`, and planning at 18 kW against a 20 kW scoring limit. Verification is pending at `ai_runs/run4/v2_safe_p0`; this is not a safety PASS.

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
