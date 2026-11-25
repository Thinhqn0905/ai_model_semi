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
