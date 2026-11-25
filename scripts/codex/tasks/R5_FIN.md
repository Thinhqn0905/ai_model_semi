# R5_FIN — FIN-B completion: missing-cost sensitivity, NPV, holiday rule, tariff provenance, fix the 3-cell payback claim
Account: .codex-B. Effort: medium.
Owner files: reports/run4/economics_run4.md, reports/run4/tariff_registry.md
Read: AGENTS.md, docs/decisions.md (D017-D019), docs/raw_binding_manifest.md, reports/run4/economics_run4.md, reports/run4/facility_billing.md
  (holiday section), data/tariffs/*.yaml, data/tariffs/sources/README.md, reports/final/Run4_Final_Evaluation_Report.md (find payback claims).
Contract (copy numbers from the reports; derived arithmetic allowed only as shown and labelled DERIVED):
1. Missing-cost sensitivity table for FIN-B 1/3/5/10 cells x MV General/ToU: for missing costs M in {0, 2k, 5k, 10k, 20k} USD, simple payback
   = (4,220 + M) / annual net and 10-y NPV at 8 % = annual net x 6.710 - (4,220 + M) (annuity factor 6.710, state it); mark which cells reach
   3 y and 5 y. Use the annual net values already in economics_run4.md.
2. Holiday rule: add the holiday-sensitivity effect (facility_billing.md) as a scenario row (1 and 5 cells, ToU).
3. Tariff provenance: TNB rates VERIFIED from the PDF p.2 (sha256 e6634bbe...), 30-min MD VERIFIED (D018, TNB MD page), peak window VERIFIED
   (mytnb page), holidays NOT documented (sensitivity). VN/SG scenarios as in the registry.
4. Fix inconsistencies: the 3-cell payback is 4.0 y (MV General) and 5.0 y (MV ToU) on known CAPEX; any text claiming 3-cell 3-5 y success
   without the missing-cost condition must be corrected (list where you changed it).
Gate: both files updated; the sensitivity table exists; a "corrections" list exists.
