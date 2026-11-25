# Mentor and work-package traceability



M identifiers below are a working mapping of mentor requirements, not identifiers asserted by the source. Status describes the deliverable, not site readiness.



| ID | Requirement | Status | Evidence and boundary |
|---|---|---|---|
| M01 | Intelligent energy coordination | PASS | `reports/run4/mentor_compliance_run4.md` (M01); site NOT_VERIFIED |
| M02 | One compatible test cell | BLOCKED | `reports/run4/mentor_compliance_run4.md` (M02); site NOT_VERIFIED |
| M03 | Flexibility and incremental energy gate | PARTIAL | `reports/run4/mentor_compliance_run4.md` (M03); site NOT_VERIFIED |
| M04 | Losses and consistent ledger | PARTIAL | `reports/run4/mentor_compliance_run4.md` (M04); site NOT_VERIFIED |
| M05 | Offline simulation to shadow gate and protected pilot | BLOCKED | `reports/run4/mentor_compliance_run4.md` (M05); site NOT_VERIFIED |
| M06 | Bus stability, protection, FMEA and compatibility | PARTIAL | `reports/run4/mentor_compliance_run4.md` (M06); site NOT_VERIFIED |
| M07 | Ground synthetic profiles in source data | PARTIAL | `reports/run4/mentor_compliance_run4.md` (M07); site NOT_VERIFIED |
| M08 | Site data priorities | BLOCKED | `reports/run4/mentor_compliance_run4.md` (M08); site NOT_VERIFIED |
| M09 | Strong baselines and perfect Oracle | PARTIAL | `reports/run4/mentor_compliance_run4.md` (M09); site NOT_VERIFIED |
| M10 | Incremental M0 kWh versus B1 | PARTIAL | `reports/run4/mentor_compliance_run4.md` (M10); site NOT_VERIFIED |
| M11 | FPY, throughput and test integrity | PARTIAL | `reports/run4/mentor_compliance_run4.md` (M11); site NOT_VERIFIED |
| M12 | AI incremental benefit over matched non-AI | FAIL | `reports/run4/mentor_compliance_run4.md` (M12); evaluation completed, matched AI scheduling benefit not demonstrated; site NOT_VERIFIED |
| M13 | Sensitivity and paired statistics | PARTIAL | `reports/run4/mentor_compliance_run4.md` (M13); site NOT_VERIFIED |
| M14 | Forecast power, duration and uncertainty; constrained optimizer decides | PARTIAL | `reports/run4/mentor_compliance_run4.md` (M14); site NOT_VERIFIED |
| M15 | Electricity first; water separate | PASS | `reports/run4/mentor_compliance_run4.md` (M15); site NOT_VERIFIED |
| M16 | Investment justification and payback | BLOCKED | `reports/run4/mentor_compliance_run4.md` (M16); site NOT_VERIFIED |

## Reviewer: what to avoid



- Borrowing vendor results: mark datasheet values VENDOR_REPORTED and never call them project savings.

- Retrofit first: establish a shadow-mode gate and engineer acceptance before a pilot.

- Assuming AI value: compare P and P0 on matched workloads; retain negative results.

- Fab-wide extrapolation or multiple segments: confine the case to a selected cell.

- Trading quality for energy: treat test integrity and production constraints as hard gates.



Source: `Instruction/Mentor_Feedback.md` (SOURCE_REPORTED); execution and site acceptance remain NOT_VERIFIED.


## Documentation gate output

Boundary: LOCAL_RUN; pending markers denote missing figure inputs, not verified results.

Command: `rg -c PENDING reports/final/report_draft.md reports/final/slides_outline.md`

```text
reports/final/slides_outline.md:2
```




Run 4 default P0 had 1/100 modeled AFE-shortfall violations: `v2_test_n10_s62`, one step, 0.259 kWh (SIM_DATA_PROFILE; `MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv`, sha256 57cd90452ba6e187). D021 verification (`MyDrive/semiexpo/ai_runs/run4/v2_safe_p0`; `reports/run3/e1_electrical_constraints.md`, Safety closure) reports 99/100 violation-free and zero unscreened fallbacks. FIFO is screened before execution; s62 remains a hardware-protection case. Industrial protection and site acceptance remain NOT_VERIFIED.
