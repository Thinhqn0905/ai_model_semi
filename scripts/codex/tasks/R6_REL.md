# R6_REL — final reproducible release package (md only; no slides file, presentation as markdown)
Account: default. Effort: medium.
Owner files: RELEASE.md, README.md, reports/final/presentation_run4.md, reports/final/qa_backup_run4.md, reports/run4/mentor_data_request.md
Read: AGENTS.md, docs/decisions.md (D001-D021), docs/runbook.md, docs/handoff_run4.md, docs/raw_binding_manifest.md, reports/final/Run4_Final_Evaluation_Report.md,
  reports/run4/screenshots/README.md, notebooks/colab_pipeline.md, requirements.txt, data/manifests/dataset_registry.json, scripts/shoot_dashboard.py.
Contract: RELEASE.md = version "run4-final", what is frozen (D019-D021), environment (python + requirements, Colab runtimes), data acquisition
(scripts/download_public_data.py, DS05/DS07 figshare IDs), exact commands per experiment family (v2_campaign incl. --prm/--plan_prm, facility.py,
fin_facility.py, eta.py, facility_load.py --reuse, run4_figs + colab_collect_run4.py), where raw results live (Drive paths + sha256 manifest), dashboard demo
(`streamlit run app/dashboard.py`, screenshots, shoot_dashboard.py), figures (Drive folder -> reports/run4/figures), tests (`python -m pytest -q`),
known defects/limitations, simulation vs site acceptance. README: short project overview + link to RELEASE.md and the final report.
presentation_run4.md: 15-20 slide outline (title, problem, reference cell, physics/kill test, engine, electrical, AI (ETA PASS; scheduling/billing
NO-GO), facility/multi-cell, economics FIN-B 5-10 cells with missing-cost limits, contribution decomposition, readiness, site requirements, Go/No-Go)
with speaker notes; numbers copied from the final report with source paths. Q&A + mentor data request: refresh to D021 state.
Gate: files exist; every number cites a source path.
