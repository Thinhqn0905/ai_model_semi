# W11_SLIDES — Final deck (pptx) from the outline and real figures
Account: .codex-B. Effort: medium.
Owner files: reports/final/ReGenATE_final.pptx, reports/final/build_slides.py, reports/final/slides_notes.md
Read: AGENTS.md, reports/final/slides_outline.md, reports/final/report_draft.md, docs/traceability.md, reports/figures/INDEX.md,
  Instruction/Mentor_Feedback.md (pitch wording), docs/decisions.md (D001-D004), reports/ai/ai_exp12_ds06.md, reports/sensitivity/sens_v1.md,
  reports/economics/business_case_v1.md.
Contract: python-pptx script building 14-16 slides 16:9 + 4 backup slides: title (energy-coordination positioning, mentor M01), context, gap,
why converter burn-in gives 0 (D001) and why storage/bidirectional cycling is the target cell, system architecture (no AI hype), data
(DS01-DS05 roles + provenance labels), method (ledger + exact MILP + rolling + twin), results: baseline ladder (F08), Go/No-Go map
(F10/sensitivity table), AI: forecasting accuracy (F03/F04/F12) THEN downstream AI-EXP12 honest result (F09), peak, business case
(alpha=1 base, demand-charge dependence), safety (failure injection + twin), roadmap shadow -> pilot, ask. Every number on a slide
carries a small boundary tag (SIM_ASSUMED_PROFILE / SIM_DATA_PROFILE / LOCAL_RUN / VENDOR_REPORTED) and comes from the cited report;
no invented numbers; vendor precedents labelled VENDOR_REPORTED. Speaker notes per slide in slides_notes.md (Vietnamese).
Gate: the pptx opens with python-pptx, slide count 18-20, and a script check that every number string on slides appears in a cited source file.

## Run 2 (lead) — final content update
Add the latest evidence: D005 (peak-aware optimizer adopted, AI not adopted for scheduling), reports/ai/ai_exp12_ds06.md (n=100,
flex 1.0, peak-aware sections), reports/ai/branch_C_ds05.md (CQR section), reports/safety/bus_stability_kpi.md (AFE/link sizing finding:
coordinated plans approved 28-39 % vs 0 % uncoordinated; 80 A / 20 kW from the old deck are undersized for an 8-station cell),
reports/sensitivity/sens_v1.md + F10. Figure-embedded numbers: accept as generated from the cited CSVs (do not re-verify image text);
the gate is the native slide text check only.
