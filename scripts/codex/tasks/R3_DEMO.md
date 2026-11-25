# R3_DEMO — Run 3 offline functional demonstrator pipeline + decision log (mentor M01, M05, M14)
Account: .codex-A (E quota exhausted until 21:56). Effort: medium.
Owner files: src/regenate/app/__init__.py, src/regenate/app/pipeline.py, tests/test_pipeline.py, app/dashboard.py,
  runs/run3/demo/**, reports/run3/demonstrator.md
Read: AGENTS.md, docs/run3_plan.md, docs/system_spec.md, reports/product/dashboard.md, app/dashboard.py,
  src/regenate/simulation/{replay,bus_twin}.py, src/regenate/optimization/rolling.py, src/regenate/evaluation/{oracle_campaign,v2_campaign}.py,
  src/regenate/data/{generator,bench_v2}.py, src/regenate/forecasting/ai_engine.py. Do not edit those modules (other owners).
Contract:
1. pipeline.py runs one instance end-to-end reusing existing code only (no new ledger/MILP logic): virtual edge-node replay
   (telemetry stream from instance traces) -> forecast engine (P0 recipe; AIEngine when --models is given) -> rolling Replanner
   -> validator (production: release/deadline/station; electrical: bus_twin.check_plan) -> engineer gate (auto-approve, or a
   rejection list for tests) -> schedule update (Replay) -> ledger + decision log. Outputs
   runs/run3/demo/<instance>/{decision_log.csv, ledger.csv, schedule.csv, summary.json} with boundary labels.
2. Works on bench_v1 instances now and on bench v2 when --proc data/ds05_proc exists.
3. `--report` writes a markdown run report (KPIs vs B1 and B1p-OPT for that instance, approvals/rejections, violations).
4. dashboard.py: add a page "Pipeline run" that reads runs/run3/demo/*/ (no hardcoded numbers): decision log, schedule
   before/after, ledger, approvals. Existing pages keep working (AppTest).
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_demo tests/test_pipeline.py tests/test_dashboard_data.py`
(engineer rejection -> fallback plan kept, ledger balance, one decision-log row per replan) and one demo run dir exists.

## Run 2 (lead)
Verify bench v2 with ONE instance only (data/ds05_proc exists locally; --split test, seed 0, time_limit <= 10 s, P0 only; the user machine is weak: no campaigns, no training). Install nothing new; tabulate removal is fine. Then run the full CLI with --report once and return ALL_PASS if the gate passes.
