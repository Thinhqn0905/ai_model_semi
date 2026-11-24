# W4_ASSUMP — Assumption register + metric audit of the legacy deck   [WP00 T00.3-T00.5, mentor M07 M09 M12]
Account: .codex-A. Effort: medium.
Owner files: reports/audit/assumption_register.csv, reports/audit/metric_audit.md, src/regenate/evaluation/assumptions.py,
  tests/test_assumptions.py
Read: AGENTS.md, docs/system_spec.md, docs/decisions.md, data/processed/provenance_*.json, configs/*.yaml,
  src/regenate/electrical/ledger.py (ElecParams), src/regenate/data/recipes.py, Instruction/Project_Profile.md,
  DS01_Quanh/code/regen_core.py (DEFAULTS), DS01_Quanh/code/summarize_regen.py, DS01_Quanh/results/regen_summary.txt.

## Contract
1. assumptions.py `collect() -> DataFrame` gathering every model parameter actually used by the new code
   (ElecParams defaults, bench_v1 config, recipe fractions, twin defaults if src/regenate/simulation/bus_twin.py
   exposes them, economics config) with: name, value, unit, module, provenance label
   (MEASURED/DATASHEET/DERIVED/SYNTHETIC/ASSUMED), source (file/page/url), grounding candidate (which dataset or
   datasheet could replace it, e.g. TIDA-010938 curves in data/processed/efficiency_points.parquet), and
   sensitivity priority (high if it enters dc_gain_bound or the S3 residual-source share). Write the CSV.
2. metric_audit.md (legacy deck, boundary NOT_VERIFIED for deck numbers):
   - P vs P0 sign: the deck says forecast +0.8 % while mean P 166.9 > P0 165.2 kWh. Show from summarize_regen.py
     how the % is computed (mean of per-instance % on the equal-TT subset vs ratio of means) and that the two can
     have opposite signs; state the correct paired definition dE_AI = E_P0 - E_P (system_spec s7).
   - "0.83 of the gap closed": legacy formula (B3 - P)/(B3 - B4) vs the plan's oracle gap; list why B4 is not a
     true oracle (heuristic, one-shot, seeded).
   - legacy B1 ledger credits AC return at alpha_ex instead of physical 1:1 netting behind M0 (D001 point 3).
   - legacy profile returns more than the oven demand (ret_frac 0.8 vs dem_hold 0.3).
   - M0-M4 inconsistency between slide 10 and 11 -> replaced by system_spec s3.
   - FMEA mentions "tune order, speed": speed change is not a ReGenATE decision (system_spec s1).
   - IEC 62443 / SEMI E187 are design directions, not certifications.
Gate: `python -m pytest -q tests/test_assumptions.py` (every row has a label in the allowed set; no duplicate names
within a module; at least the ElecParams fields present) and both report files exist.
