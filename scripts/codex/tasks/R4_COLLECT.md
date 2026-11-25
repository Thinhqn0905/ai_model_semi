# R4_COLLECT — Colab result collector for the Run 4 figure generator
Account: .codex-B. Effort: medium.
Owner files: scripts/colab_collect_run4.py, tests/test_collect_run4.py
Read: AGENTS.md, src/regenate/visualization/run4_figs.py (expected ROOT layout), scripts/codex/tasks/R4_FIGS.md.
Contract: `python scripts/colab_collect_run4.py --drive /content/drive/MyDrive/semiexpo/ai_runs --local /content/ai_runs --out ROOT` builds the
layout run4_figs expects by COPYING (never modifying) files from: local /content/ai_runs/{run3,run4}/... and Drive ai_runs/{run3,run4,
run4_rt2,run4_rt3}/..., plus v2_flex025_n100.csv, fin_v3_ds06.csv; prints a table of found/missing inputs per figure. If a file exists in
several places, prefer the newest mtime and log it. No network. Tests with a tmp dir tree.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_col tests/test_collect_run4.py`.
