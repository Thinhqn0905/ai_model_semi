# W1_LEGACY — reproduce legacy 18-run benchmark + add OPT baselines on legacy code   [WP00 T00.2, mentor M09 M12]
Account: .codex-E. Effort: medium.
Owner files: runs/legacy/** (scripts and outputs), reports/audit/legacy_results.md
Read: AGENTS.md, docs/system_spec.md (6, 7), DS01_Quanh/README_REGEN.md (sections 4, 6, 7),
  DS01_Quanh/code/regen_core.py, regen_baselines.py, regen_ttlbo.py, run_regen.py, summarize_regen.py,
  test_regen.py. DS01_Quanh is READ-ONLY: import it by inserting DS01_Quanh/code into sys.path.
Contract:
1. Run legacy checks with cwd = DS01_Quanh/code: `python test_regen.py`, `python bus_twin_check.py`.
   Save stdout to runs/legacy/legacy_tests.txt.
2. Reproduce: `python run_regen.py --n 10 20 --tau 0.2 0.5 0.8 --reps 3 --budget quick
   --out <abs path>/runs/legacy/regen_results_repro.csv`. Compare with DS01_Quanh/results/regen_results.csv
   per (n,tau,rep,method): report max abs diff of TT and kWh.
3. runs/legacy/legacy_ext.py: for the same 18 instances add B1-OPT (ttlbo_regen on evaluate6 with arch
   "B1", true kappa, seeded with the B3 chromosome) and B1p-OPT (arch "B1p"), same "oneshot" budget as B4.
   Write runs/legacy/legacy_results.csv: n,tau,rep,method,TT,kWh,imp,exp,direct,ret,demand for
   B0,B1,B1-OPT,B1p,B1p-OPT,B2,B3,B4,P0,P (reuse the seeds of run_regen.py so B0..P match step 2).
4. Profile check: per instance report ret/demand energy ratio from ledger() and whether return > demand
   during stress (legacy profile: return = ret_frac*kappa*P3_run vs demand = dem_hold*P3_run).
5. reports/audit/legacy_results.md: mean tables (all instances and equal-TT subset TT(P)==TT(B3)) for
   every method; per-instance P - P0 with sign; B3->B4 gap formula as coded; kill test B1p-OPT vs P;
   statement that slide-14 numbers (598.6 ... 166.9 kWh) are NOT reproduced by this code (the code that
   produced them is lost): label them NOT_VERIFIED. Label all new numbers SIM_ASSUMED_PROFILE (legacy profile).
Gate: runs/legacy/legacy_results.csv has 18 instances x 10 methods and the report exists.
