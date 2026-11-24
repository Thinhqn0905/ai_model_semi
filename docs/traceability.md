# Mentor and work-package traceability



M identifiers below are a working mapping of mentor requirements, not identifiers asserted by the source. Status describes the deliverable, not site readiness.



| ID | Requirement | Work package | Evidence | Status | Boundary | Remaining gap |

|---|---|---|---|---|---|---|

| M01 | Position as energy coordination | WP00 | Instruction/Mentor_Feedback.md | DONE | SOURCE_REPORTED | Apply to final presentation |

| M02 | Select suitable target cell | WP02 | docs/decisions.md | PARTIAL | NOT_VERIFIED | User must choose target |

| M03 | Establish flexibility and energy gate | WP04/WP05 | docs/decisions.md; runs/oracle_v1 | PARTIAL | SIM_ASSUMED_PROFILE | Site profiles and flexibility needed |

| M04 | Compare incremental grid energy against existing regeneration | WP08 | reports/benchmark/rolling_v1.md | PARTIAL | SIM_ASSUMED_PROFILE | Matched site evidence needed |

| M05 | Report peak and matching ratio | WP08 | reports/benchmark/rolling_v1.md | PARTIAL | SIM_ASSUMED_PROFILE | Site metering required |

| M06 | Preserve throughput, quality and test integrity | WP07/WP08 | reports/benchmark/rolling_v1.md; reports/product/replay.md; reports/ai/ai_exp12_ds06.md | PARTIAL | SIM_ASSUMED_PROFILE | Quality records and site validation needed |

| M07 | Assess bus stability and protection | WP09 | reports/safety/bus_twin.md; reports/safety/bus_stability_kpi.md | PARTIAL | SIM_ASSUMED_PROFILE | Hardware protection study needed |

| M08 | Demonstrate forecast increment against optimizer | WP06/WP07 | reports/benchmark/rolling_v1.md; reports/ai/ai_exp12_ds06.md; docs/decisions.md D004/D005 | PARTIAL | SIM_ASSUMED_PROFILE; SIM_DATA_PROFILE | AI variants show no significant peak improvement; site validation needed |

| M09 | Quantify oracle gap and uncertainty | WP05/WP08 | reports/benchmark/rolling_v1.md | PARTIAL | SIM_ASSUMED_PROFILE | Complete data-grounded matched ladder |

| M10 | Use matched baseline ladder | WP08 | docs/system_spec.md; reports/benchmark/rolling_v1.md | PARTIAL | SIM_ASSUMED_PROFILE | Extend matched campaign |

| M11 | Ground profiles and validate sensitivity | WP01/WP09 | reports/electrical/grounding.md; reports/benchmark/rolling_flex.md; reports/ai/branch_C_ds05.md | PARTIAL | SIM_ASSUMED_PROFILE + DATASHEET | CQR duration intervals remain under-covered; site traces and matched sensitivity needed |

| M12 | Model operational constraints | WP04/WP07 | docs/system_spec.md; reports/product/replay.md; reports/ai/ai_exp12_ds06.md; docs/decisions.md D004/D005 | PARTIAL | SIM_ASSUMED_PROFILE; SIM_DATA_PROFILE | DS06 operating windows are assumed; verify site-specific limits |

| M13 | Evaluate safety and failure responses | WP09 | reports/safety/failure_injection.md; reports/safety/fmea_v2.md | PARTIAL | SIM_ASSUMED_PROFILE | Integrate and validate independent protection |

| M14 | Quantify full business case | WP10 | reports/economics/business_case_v1.md; runs/biz_v1/business_case.csv; docs/decisions.md D004/D005 | PARTIAL | SIM_ASSUMED_PROFILE + ASSUMED; SIM_DATA_PROFILE | Energy recommendation is optimization-only; verify site costs and annual scaling |

| M15 | Stage shadow decision before pilot | WP11 | Instruction/Mentor_Feedback.md; reports/product/dashboard.md | PARTIAL | NOT_VERIFIED | Site shadow evidence and engineer acceptance |

| M16 | Treat cooling water separately | WP10 | reports/economics/water_method.md | PARTIAL | NOT_VERIFIED | Cooling-loop and water meters |



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
