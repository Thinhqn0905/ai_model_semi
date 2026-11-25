# Contribution decomposition ? D016

Positive savings mean lower grid energy or billed demand. Intervals are paired confidence intervals as reported. Do not add rows: datasets, subsets, topology, timing and objectives differ. DS06 is SIM_DATA_PROFILE, based on measured DS05 battery cycles with assumed cell scaling and windows; remote results are NOT_VERIFIED by independent local raw reconciliation. Financial values are ASSUMED. Sources: `reports/run3/root_cause_analysis.md`, `reports/run3/metric_audit_v3.md`, `reports/run3/economics_v3.md`.

| Contribution / comparison | Reported value and boundary | Interpretation and source |
|---|---|---|
| Hardware B0 ? B1 | SIM_ASSUMED_PROFILE: 242.9 kWh [214, 271.2], equal tardiness; complete configuration binding NOT_VERIFIED | Hardware recovery in the assumed-profile study, not DS06 or site benefit (`reports/run3/metric_audit_v3.md`). |
| Topology B1p-OPT ? B2 | NOT_VERIFIED: value and paired CI not established in named reports | Also changes scheduling; cannot isolate topology (`reports/run3/metric_audit_v3.md`). |
| Topology B1p-OPT ? B3 | NOT_VERIFIED: value and paired CI not established in named reports | Planning and information may differ; no clean topology attribution (`reports/run3/metric_audit_v3.md`). |
| Conventional scheduling B2 ? B3 | NOT_VERIFIED: value and paired CI not established in named reports | Realized tardiness and configuration matching needed (`reports/run3/metric_audit_v3.md`). |
| Rolling B3 ? P0 | SIM_DATA_PROFILE: B3 8.55 and P0 8.446 kWh/instance, paired difference and CI NOT_VERIFIED | Descriptive means only; constraints/planning differ (`reports/run4/p0_architecture.md`, `reports/run3/metric_audit_v3.md`). |
| Peak/E1 P0 ? P0-E1-Peak | SIM_DATA_PROFILE + MEASURED unsynchronized facility counterfactual: billed-demand reduction 0.23 kW [-0.12, 0.60], not significant | E1 plus peak level, not a separate causal peak effect (`reports/run4/facility_billing.md`). |
| AI energy P0 ? gated PQ | SIM_DATA_PROFILE: -0.016 kWh [-0.030, -0.003], equal-tardiness pairs | Negative saving means increased energy; this is a reported tested variant, not a proven global best (`reports/run3/ai_run3.md`). |
| AI production P0 ? PQd | SIM_DATA_PROFILE: tardiness reduction 0.003 h [0.000, 0.008]; perfect-duration ceiling 0.048 h [0.017, 0.087] | Learned result does not establish operational value; ceiling uses future information (`reports/run3/ai_run3.md`). |
| Facility billing B2 ? P0-E1-Peak | SIM_DATA_PROFILE cell + MEASURED DS07 unsynchronized facility counterfactual: billed-demand increment reduction 2.12 kW [1.08, 3.11] | Assumed aligned billing and synthetic cell placement; not a site bill (`reports/run4/facility_billing.md`). |

The **11.6%** figure is SIM_DATA_PROFILE: shared-link topology **plus optimisation**, comparing B1p-OPT with ORACLE; it is neither AI nor software-only (`reports/run3/root_cause_analysis.md`, `docs/decisions.md`). The associated reported difference is 1.094 kWh [1.037, 1.148], and one-shot truth and rolling comparisons must not be treated as equivalent causal pairs (`reports/run3/root_cause_analysis.md`, `reports/run3/metric_audit_v3.md`). Primary KPI remains incremental M0 grid kWh versus B1, with matched instances, profiles, electrical limits and tardiness; incomplete matching is NOT_VERIFIED (`reports/run3/mentor_compliance_audit.md`).
