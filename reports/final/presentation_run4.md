# Run 4 presentation outline

All numerical claims below derive from `reports/final/Run4_Final_Evaluation_Report.md`; source boundaries and raw paths accompany the relevant slide. Intervals are 95% confidence intervals as reported. Site outcomes NOT_VERIFIED.

## Slide 1: Title

ReGenATE: production-aware coordination of regenerative energy.

Speaker notes: ReGenATE: production-aware coordination of regenerative energy. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 2: Problem

Measure incremental grid energy at M0 against existing regenerative AC B1.

Speaker notes: Measure incremental grid energy at M0 against existing regenerative AC B1. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 3: Reference cell

A Chroma 17020-type battery cycling reference; semiconductor applicability is conditional on measured station-boundary residual source.

Speaker notes: A Chroma 17020-type battery cycling reference; semiconductor applicability is conditional on measured station-boundary residual source. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 4: Physics and kill test

Local reuse precedes shared transfer. No residual source means no incremental shared-link energy benefit in the analytic kill test.

Speaker notes: Local reuse precedes shared transfer. No residual source means no incremental shared-link energy benefit in the analytic kill test. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 5: Architecture

P0-E1-Peak schedules permitted starts; engineer advisory is separate.

Speaker notes: P0-E1-Peak schedules permitted starts; engineer advisory is separate. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 6: Electrical

Screened nominal MILP fallback and independent protection are essential; the FIFO infeasibility fallback is explicitly unscreened.

Speaker notes: Screened nominal MILP fallback and independent protection are essential; the FIFO infeasibility fallback is explicitly unscreened. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 7: Baseline ladder

Use matched instances, profiles, bus limits and tardiness; examine M0 energy, peak, matching and production constraints.

Speaker notes: Use matched instances, profiles, bus limits and tardiness; examine M0 energy, peak, matching and production constraints. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 8: Energy result

B1 to P0-E1-Peak: 3.077 kWh [2.967, 3.186], n=100, SIM_DATA_PROFILE; raw `MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv`. Tardiness matching and attribution remain incomplete.

Speaker notes: B1 to P0-E1-Peak: 3.077 kWh [2.967, 3.186], n=100, SIM_DATA_PROFILE; raw `MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv`. Tardiness matching and attribution remain incomplete. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 9: Peak result

B1 to P0-E1-Peak: 4.54 kW [3.76, 5.31], n=100, SIM_DATA_PROFILE; same raw campaign. Do not add energy and peak outcomes.

Speaker notes: B1 to P0-E1-Peak: 4.54 kW [3.76, 5.31], n=100, SIM_DATA_PROFILE; same raw campaign. Do not add energy and peak outcomes. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 10: AI

ETA assessment PASS on held-out battery data; learned scheduling and AI-BILL are NO-GO. Advisory forecasting does not prove downstream savings.

Speaker notes: ETA assessment PASS on held-out battery data; learned scheduling and AI-BILL are NO-GO. Advisory forecasting does not prove downstream savings. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 11: Facility

Simulated cells are paired with measured but unsynchronised DS07 factory loads and counterfactual tariffs; these are not site bills.

Speaker notes: Simulated cells are paired with measured but unsynchronised DS07 factory loads and counterfactual tariffs; these are not site bills. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 12: Multi-cell

General demand reduction B2 to P0: 5.99 kW [4.53, 7.41] for 5 cells, and 15.12 kW [11.48, 18.12] for 10 cells; n=70 facility-months, SIM_DATA_PROFILE + MEASURED unsynchronised; raw `MyDrive/semiexpo/ai_runs/run4/fac_gen_5cells` and `fac_gen_10cells`.

Speaker notes: General demand reduction B2 to P0: 5.99 kW [4.53, 7.41] for 5 cells, and 15.12 kW [11.48, 18.12] for 10 cells; n=70 facility-months, SIM_DATA_PROFILE + MEASURED unsynchronised; raw `MyDrive/semiexpo/ai_runs/run4/fac_gen_5cells` and `fac_gen_10cells`. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 13: Economics

FIN-B prioritizes existing compatible infrastructure; 5?10 cells is a conditional scenario, with installation, requalification and support costs missing. Site payback NOT_VERIFIED.

Speaker notes: FIN-B prioritizes existing compatible infrastructure; 5?10 cells is a conditional scenario, with installation, requalification and support costs missing. Site payback NOT_VERIFIED. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 14: Contribution decomposition

Hardware recovery is pre-existing; shared topology and scheduling contributions are not fully isolated. No AI energy or peak benefit is demonstrated.

Speaker notes: Hardware recovery is pre-existing; shared topology and scheduling contributions are not fully isolated. No AI energy or peak benefit is demonstrated. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 15: Readiness

The simulation and dashboard support concept review. Protection, integration, baseline reconciliation and site quality remain open.

Speaker notes: The simulation and dashboard support concept review. Protection, integration, baseline reconciliation and site quality remain open. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 16: Site requirements

Request synchronized station and facility metering, production windows, vendor permissions, converter curves, tariff, quality and full costs.

Speaker notes: Request synchronized station and facility metering, production windows, vendor permissions, converter curves, tariff, quality and full costs. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

## Slide 17: Go / No-Go

Conditional GO for simulation and shadow preparation; NO-GO for site deployment and automatic AI scheduling until site evidence and acceptance are established.

Speaker notes: Conditional GO for simulation and shadow preparation; NO-GO for site deployment and automatic AI scheduling until site evidence and acceptance are established. Source: `reports/final/Run4_Final_Evaluation_Report.md`; decisions `docs/decisions.md`.

