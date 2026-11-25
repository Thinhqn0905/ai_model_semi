# R6_VERIFY — verification of production constraints, multi-cell feasibility, solver scalability, FIN-B cost sensitivity
Account: .codex-B. Effort: medium.
Owner files: reports/run4/verification_run4.md
Read: AGENTS.md, docs/raw_binding_manifest.md, src/regenate/optimization/milp.py, src/regenate/evaluation/{v2_campaign,facility}.py, reports/run4/economics_run4.md,
  reports/run3/e1_electrical_constraints.md, reports/run4/facility_billing.md.
Facts measured by the lead (Colab, 2026-11-25): solver time per instance (s) mean/median/max: ORACLE 3.52/1.98/29.18, B1p-OPT 0.06/0.05/0.17,
P0 (rolling, all replans) 9.61/5.44/131.91, TR_ALL 2.68/2.50/7.44 (n=200 rows over v2_e1_peak100 + v2_diag); all one-shot MILPs optimal gap 0 except
flex 1.0 (ORACLE 17/26, B3 18/26 time-limit incumbents) and AFE-10 (3/30 infeasible). Instance size: 10 jobs x 8 stations, 15-min slots.
Contract: (1) production constraints: list what is enforced (release, latest start, deadline window, station capacity, tardiness objective) and the
evidence that the same constraints apply to every method (code references) + deadline violations per file from the manifest; (2) multi-cell
feasibility: cells are scheduled independently per DS06 instance (each instance feasible under E1), facility simulation adds traces without overlap
(place()); state that cross-cell electrical coupling is not modelled (separate AFE per cell assumed) and that centralised multi-cell scheduling was
only tested via P0-BILL 5-cell cases; (3) solver scalability: table above + what is NOT tested (larger instances); (4) FIN-B cost sensitivity: link the
missing-cost table in economics_run4.md and state break-even limits per cell count. Separate simulation acceptance vs site acceptance.
Gate: file exists with the four sections; every number cites a source.
