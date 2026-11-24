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
| 11 | WP00 legacy reproduction + OPT baselines | E | in_progress | runs/legacy |
| 12 | WP04 benchmark generator (S1/S2/S3) | default | done | bench_v1, 270 inst |
| 13 | WP10 economics module | A | done | tests/test_economics.py |
| 14 | WP06 E10 DS04 forecasting baselines | C | done | runs/forecast_ds04 |
| 15 | WP11 dashboard (6 pages, AppTest) | A | done | tests/test_dashboard_data.py |
| 16 | WP05 E04-E06 oracle campaign + Go/No-Go | lead | done | runs/oracle_v1: S1/S2 NO-GO, S3 GO |
| 17 | WP02 target-cell decision | USER | blocked | D001 options |
| 18 | WP01 DS05 audit | worker | blocked | DS05 download (~3-4h, 2026-11-25) |
| 19 | WP07 rolling P0/P replanner + replay | lead | in_progress | rolling.py smoke OK |
| 19b | WP09.2 bus twin, WP10.2 water, WP00 assumption/metric audit | C/C/A | done | |
| 19c | W5: figures F01-F15 (A), sensitivity (B), failure injection (C), AI framework DS02/DS04 (default) | workers | in_progress | |
| 19d | AI core: DS06 v2 + Model A/B/C + ablation P0..P5 | lead | in_progress | needs DS05 |
| 20 | WP08 full ladder, WP09 sensitivity/twin/failure | todo | todo | |

Timeline target (plan IX): 25/11 data audit, 26/11 electrical, 27/11 bench v1, 28/11 oracle Go/No-Go,
29/11 P0/P end-to-end, 30/11 main experiments, 01/12 integration, 02/12 freeze.
