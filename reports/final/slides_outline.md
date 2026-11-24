# Presentation outline

Pitch: ?Regenerative hardware already saves energy. ReGenATE asks whether production-aware scheduling can recover the energy that existing regeneration still leaves on the table. We prove that increment first in shadow mode.? (Instruction/Mentor_Feedback.md, SOURCE_REPORTED). Figures are proposed mappings, not evidence of availability; see docs/figures.md.

| Slide | Story and figure mapping | Evidence / boundary |
|---|---|---|
| Context | Existing regeneration and incremental opportunity; F14 ledger | docs/figures.md, NOT_VERIFIED until populated |
| Target | Suitable cycling cell and flexibility gate; F06 | docs/decisions.md; reports/figures/F06.png, SIM_ASSUMED_PROFILE |
| Physics | Converter no-go and cycling residual-source mechanism; F14 | docs/decisions.md, ANALYTIC_UNIT_TEST; reports/figures/F14.html, SIM_ASSUMED_PROFILE |
| Data | Data roles and efficiency grounding; F05 | reports/figures/F05.png, VENDOR_REPORTED |
| Architecture | Forecast, constrained scheduler, twin and approval; F13 | reports/figures/F13.png, SIM_ASSUMED_PROFILE |
| Forecast | Trajectory and uncertainty; F01, F02, F03 | [[PENDING: reports/figures/F01.png]]; [[PENDING: reports/figures/F02.png]]; reports/figures/F03.png, LOCAL_RUN on MEASURED DS05; NOT_VERIFIED |
| Transfer | Cross-domain forecasting; F04 | reports/figures/F04.png, LOCAL_RUN on MEASURED data |
| Oracle and ladder | Incremental cell energy against regeneration with paired intervals; F08 | reports/figures/F08.png; runs/oracle_v1, SIM_ASSUMED_PROFILE |
| AI value | Measured-cycle kill test and AI variants worse than nominal; recommend optimization-only for energy; peak-aware P0 adopted; AI peak benefit unproven; F09 | reports/benchmark/rolling_v1.md, SIM_ASSUMED_PROFILE; reports/ai/ai_exp12_ds06.md; docs/decisions.md D004, SIM_DATA_PROFILE; docs/decisions.md D005; reports/figures/F09.png, SIM_DATA_PROFILE |
| Robustness | Sensitivity and forecast errors; F10, F11, F12 | reports/figures/F10.png, SIM_ASSUMED_PROFILE; [[PENDING: reports/figures/F11.png]], NOT_VERIFIED; reports/figures/F12.png; reports/ai/branch_C_ds05.md, LOCAL_RUN on MEASURED DS05 (CQR duration under-covered) |
| Safety | Bus screening, failure responses and independent protection; F07 | reports/safety/failure_injection.md, SIM_ASSUMED_PROFILE; reports/figures/F07.png; reports/safety/bus_stability_kpi.md, SIM_ASSUMED_PROFILE |
| Deployment | Latency and operational constraints; F15 | reports/figures/F15.png, LOCAL_RUN on MEASURED DS05 |
| Economics and decision | Costs, payback, shadow gate, pilot and separate water workstream | reports/economics/business_case_v1.md, SIM_ASSUMED_PROFILE + ASSUMED; reports/economics/water_method.md, NOT_VERIFIED |
