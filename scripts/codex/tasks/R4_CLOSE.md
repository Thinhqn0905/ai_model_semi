# R4_CLOSE — close Run 4 (D018): integrate pending results, final reports, claims, M01-M16 traceability (md only)
Account: .codex-A. Effort: medium.
Owner files: reports/final/report_run4.md, reports/run4/mentor_compliance_run4.md, docs/traceability.md, reports/run4/tariff_registry.md,
  reports/run4/facility_billing.md (AI-BILL section only), reports/run3/e1_electrical_constraints.md (twin sizing section only),
  Instruction/NeedtoDo.md, Instruction/Session_Checklist.md
Read: AGENTS.md, docs/decisions.md (D006-D018), docs/handoff_run4.md, reports/run3/*.md, reports/run4/*.md, runs/claims.jsonl.
Contract:
1. If runs/run4/run4_final_summary.md and runs/run4/screen_sizing_summary.csv exist (downloaded by the user from Drive), copy their numbers into
   the AI-BILL and twin-sizing sections (with the Drive path); otherwise mark both PENDING with the Drive path. AI-BILL rule (D017/D018): adopt
   only if P0-BILL:ai beats P0-BILL:hist and P0-E1-Peak with a factory-clustered CI excluding 0; else record FAIL and stop AI scheduling.
2. Tariff registry: 30-min MD interval VERIFIED (TNB page, D018); keep any other NOT_VERIFIED items.
3. report_run4.md: two separate sections "Experimental validation (simulation, public/measured data)" and "Industrial site acceptance
   (not done: requires site data, shadow mode, protection qualification, costs)"; preferred scenario FIN-B 5-10 cells with conditional
   payback ~3.0 y / 1.2-1.4 y and the missing-cost break-even limits; reference cell FINAL (D018).
4. Compliance M01-M16 + G01-G12 final statuses; traceability rows for every M-ID -> evidence file; claims.jsonl cross-check (every headline
   number in report_run4.md has a claim id).
5. NeedtoDo: only remaining external items (mentor: semiconductor applicability, site data/deployment; owner: archive the TNB MD page copy).
Gate: report has both sections; 16 M rows; 12 G rows; every number cites a source path.
