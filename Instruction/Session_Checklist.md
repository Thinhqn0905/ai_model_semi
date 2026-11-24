# Session Checklist / Milestones (lead-managed)

Status: `todo` / `in_progress` / `done` / `blocked`. Codex = gpt-6.1-terra medium (high only for hard
tasks, justified). Accounts: default, A, B, C, E. Never codex-D.

| # | WP / Step | Owner | Status | Gate / evidence |
|---|---|---|---|---|
| 1 | Harness + codex-dispatch skill | lead | done | 2026-11-24 |
| 2 | Context: deck + mentor -> Project_Profile, Mentor_Feedback | lead | done | |
| 3 | System spec v1 (`docs/system_spec.md`) | lead | done | |
| 4 | WP03 energy ledger + ELEC-01..09 | lead | done | tests/test_ledger.py 20 pass |
| 5 | D001 kill-test physics (`docs/decisions.md`) | lead | done | analytic + tests |
| 6 | WP05 exact MILP oracle engine | lead | done | tests/test_milp.py == brute force |
| 7 | WP01 DS01 audit+loader | default | done | tests/test_ds01.py |
| 8 | WP01 DS02 audit+loader | A | done | tests/test_ds02.py |
| 9 | WP01 DS03 efficiency curves | B | done | 300+ TIDA-010938 points |
| 10 | WP01 DS04 audit+loader | C | done | tests/test_ds04.py |
| 11 | WP00 legacy reproduction + OPT baselines | E | done | exact repro, runs/legacy |
| 12 | WP04 benchmark generator (S1/S2/S3) | default | done | bench_v1, 270 inst |
| 13 | WP10 economics module | A | done | tests/test_economics.py |
| 14 | WP06 E10 DS04 forecasting baselines | C | done | runs/forecast_ds04 |
| 15 | WP11 dashboard (6 pages, AppTest) | A | done | tests/test_dashboard_data.py |
| 16 | WP05 E04-E06 oracle campaign + Go/No-Go | lead | done | runs/oracle_v1: S1/S2 NO-GO, S3 GO |
| 17 | WP02 target-cell decision | USER | blocked | D001 options |
| 18 | WP01 DS05 download+process on Colab | lead | done | 14,755 cycles, Drive semiexpo/ds05_proc |
| 19 | WP07 rolling P0/P replanner + replay | lead | in_progress | rolling.py smoke OK |
| 19b | WP09.2 bus twin, WP10.2 water, WP00 assumption/metric audit | C/C/A | done | |
| 19c | W5: figures F01-F15 (A), sensitivity (B), failure injection (C), AI framework DS02/DS04 (default) | workers | in_progress | |
| 19d | AI core: DS05 Branch C bench (Colab), DS06 bench v2, AI engine, P0..P4 ablation | lead | in_progress | code+tests done, runs on Colab |
| 19e | W7: DS03 grounding (A), business case (E), failure verify (C), traceability+report (default), sensitivity (B) | workers | in_progress | |
| 20 | WP08 ladder v1 (rolling_v1) + DS06 ladder n=100 (AI-EXP12) | lead/E | done | D003, D004 |
| 21 | WP09 sensitivity (sens_v1), failure injection, grounding | B/C/A | done | S1=0 everywhere; S3 gain 3-12 kWh by eta_afe |
| 22 | WP10 business case (alpha=1 base) | E | done | energy alone: no payback; demand charge needed |
| 23 | Peak-aware 3rd lexicographic level + DS06 run | lead | in_progress | Colab v2_peak |
| 24 | CQR calibration (AI-G04) | lead | in_progress | Colab ds05_cqr2 |
| 25 | Bus twin KPI (AFE sizing finding) | C | in_progress | W10_TWINCHK run 2 |
| 26 | Deliverables: figures, slides pptx, README/runbook, Q&A, traceability | A/B/E/default | in_progress | |

Timeline target (plan IX): 25/11 data audit, 26/11 electrical, 27/11 bench v1, 28/11 oracle Go/No-Go,
29/11 P0/P end-to-end, 30/11 main experiments, 01/12 integration, 02/12 freeze.
