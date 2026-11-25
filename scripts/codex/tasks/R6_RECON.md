# R6_RECON — reconcile contradictory statuses, decision IDs, tariff provenance, figure availability, raw bindings
Account: .codex-A. Effort: medium.
Owner files: reports/final/parts/part1.md, part2.md, part3.md, reports/final/reconciliation_log.md, reports/run4/mentor_compliance_run4.md, docs/traceability.md
Read: AGENTS.md, docs/decisions.md (D001-D021: decision IDs must match exactly), docs/raw_binding_manifest.md, data/tariffs/*.yaml + sources/README.md,
  reports/final/parts/part1.md (final figure status table at the end is authoritative), reports/run4/*.md, reports/run3/*.md.
Contract: find and fix contradictions across parts/compliance/traceability: (a) any status that differs between documents for the same item
(e.g. M-ID statuses, gate statuses, AI-BILL = NO-GO, M12 = FAIL, AFE 20/16 candidate, 3-cell payback 4.0/5.0 y on known CAPEX only);
(b) decision IDs cited that do not exist or with wrong content; (c) tariff provenance (TNB rates VERIFIED p.2 PDF sha256 e6634bbe..., 30-min MD
VERIFIED D018, peak window VERIFIED, holidays NOT documented); (d) figure availability must match the final figure status table; (e) raw bindings
from docs/raw_binding_manifest.md; (f) the P0 violation: 1/100 (instance v2_test_n10_s62, 1 AFE-shortfall step, 0.259 kWh) in the Run 4 default
engine, safety fix D021 (verification pending: ai_runs/run4/v2_safe_p0). Log every change in reconciliation_log.md (file, old, new, reason).
Gate: reconciliation_log.md lists changes; no contradictory status remains for the items above.
