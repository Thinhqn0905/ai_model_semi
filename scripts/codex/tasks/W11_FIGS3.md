# W11_FIGS3 — Go/No-Go map and flexibility figures from completed sensitivity
Account: .codex-A. Effort: medium.
Owner files: src/regenate/visualization/plot_sensitivity.py, reports/figures/**, docs/figures.md
Read: AGENTS.md, runs/sens_v1/sensitivity_results.csv, reports/sensitivity/sens_v1.md, reports/benchmark/rolling_flex.md, reports/figures/INDEX.md.
Contract: F10 = one-at-a-time tornado/bar chart of S3 gain (B1p-OPT - ORACLE, kWh and %) with CI per sweep (flex, eta_afe, eta_link,
p_link_max, n_stations, allow_export) and the S1 control at 0; plus the 2-D flex x eta_link heatmap if the grid exists. F10b = gain vs
flexibility line (S3) with CI. Captions carry SIM_ASSUMED_PROFILE. Update INDEX.md.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_figs3 tests/test_figures.py` passes and F10 files exist.
