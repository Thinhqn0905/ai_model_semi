# W3_DASH — Engineer dashboard skeleton (offline demonstrator)   [WP11, mentor M01 M05 M11 M14 M16]
Account: .codex-A. Effort: medium.
Owner files: app/**, src/regenate/evaluation/mock_results.py, tests/test_dashboard_data.py,
  reports/product/dashboard.md
Read: AGENTS.md, docs/system_spec.md (3, 6, 7, 10), Instruction/Mentor_Feedback.md (Positioning, KPIs),
  src/regenate/economics/model.py (interface only).

## Contract
- mock_results.py: `make_mock_campaign(out_dir, seed)` writes results.csv / schedules.parquet /
  timeseries.parquet / manifest.json with EXACTLY the section-10 schema, every row boundary="MOCK".
- app/dashboard.py (Streamlit + Plotly), loads any runs/<campaign>/ folder chosen in the sidebar:
  1 Overview: KPI tiles (incremental kWh vs B1, peak kW, R_match, dE_AI = P0 - P, oracle gap, violations)
    computed with the section-7 formulas; a banner showing the boundary label of the data (MOCK /
    SIM_ASSUMED_PROFILE / ...) on every page; never hard-code numbers.
  2 Baseline ladder: bar chart of net kWh per method in ladder order B0 B1 B1-OPT B1p B1p-OPT B2 B3 P0 P
    ORACLE, paired differences with 95 % bootstrap CI (helper in app, seed 0).
  3 Schedule: original (FIFO / B3) vs proposed Gantt for one instance; shift per job.
  4 Energy: import / export / direct-reuse time series for the selected methods.
  5 Engineer approval: Approve / Reject with reason; append to runs/<campaign>/decision_log.csv
    (timestamp, instance, method, decision, reason); rejected -> original plan remains "active".
  6 Finance: annual saving / payback via regenate.economics (inputs editable in sidebar); show
    "payback not reached" when saving <= 0.
- Title: "ReGenATE — Intelligent Energy Coordination for Regenerative Test Cells" (mentor M01).
  Footer: "Offline functional demonstrator / shadow-mode emulator — not connected to a real MES".
Gate: `python -m pytest -q tests/test_dashboard_data.py` (mock schema == section 10 columns, KPI helpers on a
hand example, decision log append) and `python -m streamlit run app/dashboard.py --server.headless true`
starts without exception for 20 s on a mock campaign (kill it afterwards; capture the log in reports/product/).

## Run 2 (lead): verify every page headlessly
Use `streamlit.testing.v1.AppTest.from_file("app/dashboard.py")`, select each of the 6 pages (via the sidebar
widget), `.run()`, and assert `not at.exception` on a mock campaign; also run it once on runs/oracle_v1 if that
folder has results.csv (real schema, boundary SIM_ASSUMED_PROFILE; methods may be missing P0/P — pages must
degrade gracefully with a "not available yet" note, not crash). Add these as tests in tests/test_dashboard_data.py.
