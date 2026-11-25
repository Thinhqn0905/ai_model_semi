# R5_RECON — reconcile NOT_VERIFIED bindings, M12 correction, simulation vs site acceptance, regenerate the final report
Account: default. Effort: medium.
Owner files: reports/final/parts/part1.md, part2.md, part3.md, reports/run4/mentor_compliance_run4.md, docs/traceability.md
Read: AGENTS.md, docs/raw_binding_manifest.md (authoritative raw bindings + solver/tardiness/violation facts), docs/decisions.md (D018, D019),
  reports/run3/e1_electrical_constraints.md (sizing + cost-optimised 20/16), reports/run4/economics_run4.md, reports/run4/prior_art.md (if present).
Contract: (1) Replace every NOT_VERIFIED raw-result binding that the manifest resolves with "<Drive path> (sha256 <prefix>)"; keep NOT_VERIFIED only
where the manifest has nothing. (2) Add the reconciliation facts (flex 1.0 incumbents, B3/AFE-10 infeasible, tardiness gap P0 vs one-shot,
violations) to sections 6, 7, 15. (3) M12 status: FAIL for AI scheduling benefit (evaluation completed; no matched AI benefit); keep ETA accuracy
as PASS under M14/G06. (4) Every section separates "simulation acceptance" vs "industrial site acceptance (not performed)". (5) Section 7:
AFE 20/16 cost-optimised candidate vs 20/32 reference. Then the lead re-assembles the report.
Gate: no unresolved NOT_VERIFIED where the manifest has data; M12 = FAIL with reason.
