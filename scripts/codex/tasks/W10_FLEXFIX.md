# W10_FLEXFIX — Complete the flexibility study (oracle at missing flex points)
Account: .codex-E. Effort: medium.
Owner files: runs/oracle_flexfix/**, reports/benchmark/rolling_flex.md
Read: AGENTS.md, reports/benchmark/rolling_flex.md, src/regenate/evaluation/oracle_campaign.py (CLI), runs/rolling_flex.
Contract: run `python -m regenate.evaluation.oracle_campaign --out runs/oracle_flexfix --n 10 --seeds 0 1 --scenarios S3 --flex 0.1 0.5
--time_limit 30 --workers 6`; update rolling_flex.md with the missing ORACLE / B1p-OPT comparisons per flex. For flex 0 explain that the
rolling P0 window rule (latest >= FIFO start) differs from the oracle rule and report both as-is rather than claiming a decomposition.
Label SIM_ASSUMED_PROFILE. Gate: every flex point 0, 0.1, 0.25, 0.5, 1.0 has ORACLE and P0 rows or a listed failure.
