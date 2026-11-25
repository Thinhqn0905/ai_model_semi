# Contribution decomposition ? D016

All intervals are paired 95% confidence intervals. Positive values mean reduction. DS06 is SIM_DATA_PROFILE: measured DS05 battery cycles, assumed station scaling and operating windows; site performance NOT_VERIFIED. Comparisons have different subsets, information, objectives and electrical conditions and must not be added. Even where a paired interval is reported, changes in planning or tardiness prevent a pure causal attribution. Independent raw reconciliation is NOT_VERIFIED (`reports/run3/metric_audit_v3.md`).

| Contribution | Value and boundary | Interpretation and report |
|---|---|---|
| Hardware B0 ? B1 | 57.49 kWh [55.61, 59.41]; SIM_DATA_PROFILE | Regenerative hardware; not software benefit (`reports/ai/ai_exp12_ds06.md`). |
| Topology B1p-OPT ? B2 | Paired difference and CI NOT_VERIFIED; SIM_DATA_PROFILE | Different scheduling also changes; no isolated topology effect (`reports/ai/ai_exp12_ds06.md`, `reports/run3/metric_audit_v3.md`). |
| Topology B1p-OPT ? B3 | Paired difference and CI NOT_VERIFIED; SIM_DATA_PROFILE | Includes topology and scheduling differences (`reports/ai/ai_exp12_ds06.md`, `reports/run3/metric_audit_v3.md`). |
| Conventional scheduling B2 ? B3 | 0.218 kWh [0.189, 0.248]; SIM_DATA_PROFILE | Static scheduling comparison; tardiness and configuration matching require scrutiny (`reports/ai/ai_exp12_ds06.md`, `reports/run3/metric_audit_v3.md`). |
| Rolling B3 ? P0 | 0.018 kWh [0.009, 0.028]; SIM_DATA_PROFILE | Rolling comparison; not an isolated causal effect (`reports/ai/ai_exp12_ds06.md`, `reports/run3/metric_audit_v3.md`). |
| Peak/E1 P0 ? P0-E1-Peak | Billed-demand reduction 0.52 kW [0.08, 0.96]; SIM_DATA_PROFILE cell + MEASURED DS07 facility, unsynchronised counterfactual | TNB peak-period scenario; E1 and peak jointly change, so not an isolated peak effect; factory-clustered 95% CI; interval alignment NOT_VERIFIED (`reports/run4/facility_billing.md`). |
| AI energy P0 ? P5s | -0.004 kWh [-0.010, 0.004]; SIM_DATA_PROFILE | Best mean among listed Run 2?3 learned variants; CI crosses zero, no demonstrated gain (`reports/run3/ai_run3.md`, `reports/ai/ai_exp12_ds06.md`). |
| AI production P0 ? P-ETA-S | Tardiness reduction 0.0054 h [0.0000, 0.0158]; SIM_DATA_PROFILE | CI touches zero; energy worsens by 0.0274 kWh [0.0123, 0.0437]; not adopted (`reports/run4/ai_production_planning.md`). |
| Facility billing B2 ? P0-E1-Peak | MD increment reduction 1.73 kW [0.73, 2.68]; SIM_DATA_PROFILE cell + MEASURED DS07 facility, unsynchronised counterfactual | TNB peak-period scenario; tariff factory-clustered 95% CI; interval alignment NOT_VERIFIED (`reports/run4/facility_billing.md`). |

The 11.6% shared-link result is topology **plus optimisation**, not AI or software-only: B1p-OPT ? ORACLE is 1.094 kWh [1.037, 1.148], SIM_DATA_PROFILE (`reports/run3/root_cause_analysis.md`). The primary KPI is incremental grid kWh at M0 against B1, with matched instances, profiles, bus limits and tardiness; site outcome NOT_VERIFIED (`reports/run3/mentor_compliance_audit.md`).
