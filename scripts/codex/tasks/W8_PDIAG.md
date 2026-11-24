# W8_PDIAG — Why is P worse than P0 on bench_v1? (diagnostic, AI-G10 input)
Account: .codex-A. Effort: medium.
Owner files: runs/pdiag/**, reports/benchmark/p_vs_p0_diagnosis.md
Read: AGENTS.md, docs/decisions.md (D002, D003), src/regenate/optimization/rolling.py (Replanner, estimate_running),
  src/regenate/simulation/replay.py, src/regenate/evaluation/rolling_campaign.py, runs/rolling_v1/results.csv + schedules.parquet.
  Do not edit src/.
Contract (scripts under runs/pdiag/ import the package):
1. Per S3 instance: P - P0 kWh and peak, n_replans, n accepted, start-time differences per job, which jobs moved.
2. Estimator quality: for every replan of P log (job, elapsed_h, predicted dur vs true dur, predicted kappa vs true) — reproduce by
   re-running Replay for 4 instances with a wrapped Replanner that records predictions (subclass in runs/pdiag, no src edits).
   Report MAE of duration prediction of P vs nominal (P0) as a function of elapsed fraction.
3. Hypotheses to test with evidence: (a) estimator error early in a job, (b) more replans -> plan churn moves good overlaps, (c)
   cache key differences, (d) start snapping. Re-run P with estimator disabled until elapsed >= 50 % of nominal to test (a).
4. Report with label SIM_ASSUMED_PROFILE, a clear mechanism statement and a recommended reliability gate for AI-G10.
Gate: reports/benchmark/p_vs_p0_diagnosis.md exists with tables backed by runs/pdiag/*.csv.
