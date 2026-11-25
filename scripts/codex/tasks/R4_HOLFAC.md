# R4_HOLFAC — holiday sensitivity option for the facility billed-demand simulation (D017.3)
Account: .codex-C. Effort: medium.
Owner files: src/regenate/evaluation/facility.py (ONLY the md_window / billed_demand / argument parsing parts), tests/test_facility.py
Read: AGENTS.md, src/regenate/evaluation/facility.py, src/regenate/economics/billing.py (my_public_holidays), data/tariffs/TAR01_MY_TNB_RP4_MV_TOU.yaml.
Contract: add `--holidays {none,MY}` (default none = unchanged results). With MY, dates returned by billing.my_public_holidays(year) are
treated as off-peak: excluded from the md_window (ToU MD) in billed_demand and masked in the ORACLE-BILL / P0-BILL billing level (same
masking as off-window slots). Record the holiday list used in manifest.json. Do not change anything else in facility.py.
Tests: a weekday holiday peak-window spike is ignored with --holidays MY and counted without it; default unchanged.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_hf tests/test_facility.py`.
