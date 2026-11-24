# W7_BIZ — Business case v1: FIN-A / FIN-B / FIN-C payback from simulation results (WP10.1, E19, mentor M16)
Account: .codex-E. Effort: medium.
Owner files: src/regenate/economics/business_case.py, tests/test_business_case.py, runs/biz_v1/**, reports/economics/business_case_v1.md
Read: AGENTS.md, Instruction/Mentor_Feedback.md (financial), Instruction/Project_Profile.md (Feasibility), docs/decisions.md,
  src/regenate/economics/model.py + configs/economics_v1.yaml, runs/rolling_v1/ladder.csv, runs/rolling_v1/timeseries.parquet,
  runs/oracle_v1/results.csv, reports/economics/economics_method.md.
Contract:
- Per scenario (S1 negative control, S3 target), take per-instance paired deltas from ladder.csv: FIN-A = B1-OPT vs B1 (software on
  regen-to-AC), FIN-B = P0 (and P) vs B2 (optimisation on an existing shared DC), FIN-C = P0 vs B1 (full retrofit incl. bus).
  Scale a simulated instance to annual operation explicitly: operating hours/year and instances-per-year as config (ASSUMED),
  state the cell size the bench represents (kW). Energy cost with TOU tariff from economics config, export credit sweep {0, 0.5, 1};
  peak saving only if a demand charge is configured (run both with and without).
- CAPEX/OPEX per FIN option from slide 16 estimates (ASSUMED estimate) with x{0.5,1,2} sensitivity; payback, NPV (8 %, 10 y);
  "not reached" when saving <= 0. Use paired-CI lower/upper bounds of the kWh delta to give a payback range.
- Report: table per option and scenario, a clear sentence on which option is financially justified under which conditions,
  and that S1 (converter burn-in) gives zero shared-DC saving (D001). Label SIM_ASSUMED_PROFILE.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_biz tests/test_business_case.py` (hand example; zero saving ->
not reached; demand charge toggle) and runs/biz_v1/business_case.csv exists.

## Run 2 (lead decision)
Inputs ARE matched by construction: runs/rolling_v1/ladder.csv rows share instance_id, workload, profile and ledger; pair by instance_id. Use the equal-TT subset when TT differs and report n. Cost inputs: slide-16 estimates labelled ASSUMED (that is the accepted boundary until quotes exist). Finish payback/NPV with those, write the report and set STATUS from the gate only.

## Run 3 (lead correction — base case was wrong)
Base case must be alpha_ex = 1: the test cell sits behind the plant main meter, so energy it "exports" is consumed by other plant loads 1:1 (docs/decisions.md D001 point 3, system_spec s5: net = import - export). alpha < 1 is ONLY a sensitivity for a facility that is net-exporting to the grid. Re-state every headline table at alpha=1 (keep alpha 0/0.5 as sensitivity rows), recompute payback/NPV, and say explicitly in the report that the previous alpha=0 headline overstated FIN-B (it counted only import reduction). Do not change anything else.
