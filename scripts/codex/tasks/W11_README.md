# W11_README — Reproducibility runbook
Account: .codex-E. Effort: medium.
Owner files: README.md, docs/runbook.md, notebooks/colab_pipeline.md
Read: AGENTS.md, CLAUDE.md, docs/system_spec.md, src/regenate (module docstrings + CLIs only), scripts/codex, the Colab notebook steps in
  docs/ai_plan.md and src/regenate/data/ds05.py docstring.
Contract: README (what ReGenATE is, positioning, results summary pointing to reports with boundary labels, how to install, test, run);
docs/runbook.md with the exact command sequence to reproduce every result folder (runs/oracle_v1, rolling_v1, sens_v1, biz_v1, oracle_grounded,
twin_v1, ai/ds02, ai/ds04, DS05 Colab pipeline: download via figshare API -> regenate.data.ds05 -> ds05_bench -> v2_campaign), expected
runtimes, and data licences/sources. notebooks/colab_pipeline.md: the Colab cell sequence (no tokens, use Colab secrets).
Gate: every command in the runbook exists (`python -m <module> --help` succeeds for each module referenced).
