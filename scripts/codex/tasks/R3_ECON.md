# R3_ECON — Run 3 WP-F economics: FIN-A/B/C, break-even CAPEX, missing-cost flags (mentor M05, M15, M16)
Account: .codex-B. Effort: medium.
Owner files: src/regenate/economics/fin_options.py, tests/test_fin_options.py, configs/economics_v3.yaml, runs/run3/econ/**,
  reports/run3/economics_v3.md
Read: AGENTS.md, docs/run3_plan.md, Instruction/Mentor_Feedback.md (financial), src/regenate/economics/{model,business_case}.py,
  configs/economics_v1.yaml, reports/economics/{business_case_v1,economics_method,water_method}.md, runs/biz_v1/**,
  reports/ai/ai_exp12_ds06.md, runs/rolling_v1/ladder.csv. Do not edit business_case.py (Run 2 frozen): import from it.
Contract:
1. fin_options.py: input = a paired per-instance results CSV (columns instance_id, method, net_kwh, peak_kw: the v1/v2 campaign
   schema) + config. FIN-A software-only on existing regen-to-AC (B1 -> B1-OPT); FIN-B optimisation on an existing shared DC
   (B2 -> P0, and -> P0 peak-aware when present); FIN-C full retrofit (B1 -> P0). Behind-the-meter alpha=1 is the base case.
2. Report separately: (a) physical kWh saved, (b) energy bill saving, (c) export-credit effect (alpha 0/0.5/1 sensitivity only),
   (d) demand-charge saving ONLY when tariff.demand_charge is set (report with and without).
3. Annualisation explicit and ASSUMED in config (hours/year, cells, instances/year from instance duration).
4. CAPEX/OPEX/installation/requalification: every item has value + status in {QUOTED, ESTIMATE, MISSING}. MISSING items are never
   silently 0: compute "excluding missing items" and flag that result OPTIMISTIC.
5. Break-even CAPEX = PV of 10-y net savings at 8 %, per option; tornado sensitivity on tariff, demand charge, duty cycle, eta_AFE
   (from runs/sens_v1), CAPEX x0.5/1/2. Payback "not reached" when saving <= 0. Use paired-CI bounds for ranges.
6. Run now on runs/rolling_v1/ladder.csv (bench_v1 S3, SIM_ASSUMED_PROFILE). DS06 results will appear later at
   runs/run3/v2_*/results.csv: CLI takes --results so the lead can rerun; mark DS06 rows PENDING.
7. Report: table per option; one sentence per option: justified / not justified / justified only if (condition). Electricity
   first; water qualitative only (needs metering).
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_fin tests/test_fin_options.py` (hand NPV, break-even CAPEX
gives NPV=0, MISSING item flagged, demand-charge toggle, saving<=0 -> not reached) and runs/run3/econ/fin_v3.csv exists.

## Run 2 (lead)
eta_AFE sensitivity: use runs/sens_v1 as it is (it gives the shared-DC gain B1p-OPT -> ORACLE vs eta_AFE, not P0): convert that gain to break-even CAPEX per eta point and label it "ORACLE-level gain (upper bound), SIM_ASSUMED_PROFILE". DS06 stays PENDING (lead reruns with --results). Then finish the report and return ALL_PASS if the gate passes.
