# R3_AUDIT — Run 3 WP-A metric audit v3 + experiment manifest (mentor M03, M04, M09, M10, M12, M13)
Account: default. Effort: medium.
Owner files: reports/run3/metric_audit_v3.md, runs/run3/manifest_run2.json, runs/run3/audit/**
Read: AGENTS.md, docs/run3_plan.md, docs/system_spec.md, docs/decisions.md, reports/audit/metric_audit.md,
  src/regenate/electrical/ledger.py, src/regenate/evaluation/{oracle_campaign,v2_campaign,stats,rolling_campaign}.py,
  src/regenate/optimization/{milp,rolling}.py, runs/{oracle_v1,rolling_v1,rolling_flex,sens_v1,biz_v1,oracle_grounded}/**,
  results/ai_ds05_branchC/*, reports/ai/*.md. Do NOT edit src/ or existing reports (Run 2 is frozen).
Contract:
1. Manifest: for every local run dir list command/args (manifest.json if present), seeds, n instances, methods, sha256 of the
   results csv, boundary label, and which report numbers come from it. Mark DS06/Colab runs (results only on Drive,
   MyDrive/semiexpo/ai_runs) as "REMOTE, local rerun pending".
2. Recompute from raw CSVs every headline number in reports/ai/*.md, reports/benchmark/*.md, reports/economics/*.md that has a
   local source; table: claim, report value, recomputed value, match yes/no.
3. Audit units (kW, kWh, h, slot), sign convention (p_rec >= 0 is source), net = import - export, no double counting of direct
   reuse, and that every comparison in stats.COMPARISONS is paired by instance_id on the same workload.
4. Oracle fairness: per comparison give objective (lexicographic TT -> energy -> peak), constraints, information, one-shot vs
   rolling. Flag explicitly that ORACLE (one-shot, truth) vs P0 (rolling, recipe) is NOT an information-only matched pair.
5. Solver: count status / mip_gap / time-limit hits per method from CSV columns; a time-limited incumbent is "incumbent", not
   optimum. Give the share of instances with gap > 0.
6. List every finding as OK / ISSUE (with file:line) / NOT_VERIFIED. No code fixes; recommend fixes.
Gate: report exists with sections 1-6; manifest json loads; every ISSUE has a file reference.

## Run 2 (lead)
Finish sections 2 and 4 completely in this run (every headline number with a local source; every comparison in stats.COMPARISONS plus ORACLE/P0/P1-P4). Do not return CONTINUE for work that is possible with local files; DS06 remote rows stay "REMOTE, rerun on Colab in progress (runs/run3/v2_diag)".

## Run 3 (lead) — final
DS06 numbers were recomputed by the lead on Colab (notebook semiexpo_ai.ipynb cells 32-49) and are written in reports/run3/{root_cause_analysis,ai_run3,e1_electrical_constraints,economics_v3}.md with Drive source paths. Mark them "REMOTE, recomputed by lead on Colab" (not locally re-verifiable). Check instead that every DS06 number quoted in reports/run3/*.md is consistent across those files (same value for the same claim), list inconsistencies with file:line. Add the reproducibility facts: DS05 local rebuild = Colab (14,755 cycles, 2 errors, runs/ds05_local_build.log); Branch C retrain identical (55/55 metrics); DS06 Run 3 P0/B1p-OPT/ORACLE/B1 = Run 2 to 3 decimals; all one-shot MILPs optimal gap 0. Then finish and return ALL_PASS if the gate passes.
