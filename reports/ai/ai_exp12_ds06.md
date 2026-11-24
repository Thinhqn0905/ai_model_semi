# AI-EXP12 — Does forecasting reduce grid energy? DS06 (bench v2) ladder + AI ablation

Boundary: **SIM_DATA_PROFILE** — station jobs replay MEASURED DS05 cycles (shapes, durations, energies); scaling
(25 modules per station, ~6 kW), release/due/deadline windows and 8 stations are ASSUMED. Test-split cycles only (never
used to train the forecasters). Same ledger for every method; P0..P4 share the same rolling MILP, period 15 min,
time limit 20 s, flex 0.25 (max shift 1 h of the 4 h window). Source: Colab run, files on Drive
`MyDrive/semiexpo/ai_runs/v2_flex025_n100.csv` (= v2_ladder + v2_ladder_b), code `src/regenate/evaluation/v2_campaign.py`.
n = 100 paired instances (10 jobs each), 0 constraint violations; one B3 instance infeasible at the TT stage (n=99 there).

## Mean per instance
| | B0 | B1 | B1-OPT | B1p | B1p-OPT | B2 | B3 | P0 | P1 | P2 | P3 | P4 | ORACLE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| net kWh | 69.02 | 11.52 | 11.52 | 9.45 | 9.45 | 8.69 | 8.55 | 8.45 | 8.46 | 8.47 | 8.47 | 8.47 | 8.35 |
| peak kW | 22.71 | 15.26 | 14.71 | 14.71 | 14.23 | 14.64 | 11.60 | 11.34 | 11.68 | 11.58 | 11.90 | 11.74 | 10.19 |

## Paired comparisons (mean difference, 95 % bootstrap CI, wins)
| Comparison | kWh | % | wins |
|---|---|---|---|
| B0 -> B1 regen hardware | 57.49 [55.61, 59.41] | 83.3 | 100/100 |
| B1 -> B2 shared DC, same FIFO | 2.84 [2.73, 2.95] | 24.6 | 100/100 |
| B2 -> B3 static optimisation | 0.218 [0.189, 0.248] | 2.5 | 94/99 |
| B3 -> P0 rolling adaptation | 0.018 [0.009, 0.028] | 0.2 | 29/99 |
| **B1p-OPT -> ORACLE (kill test ceiling)** | **1.094 [1.037, 1.148]** | **11.6** | **100/100** |
| P0 -> ORACLE (headroom for perfect forecasts) | 0.094 [0.077, 0.112] | 1.1 | 94/100 |

AI ablation vs P0 (positive = better than P0):
| Variant | kWh | wins | peak kW | wins |
|---|---|---|---|---|
| P1 power AI | -0.018 [-0.030, -0.005] | 27/100 | -0.34 [-0.83, +0.13] | 33/100 |
| P2 duration AI | -0.019 [-0.031, -0.007] | 22/100 | -0.25 [-0.73, +0.23] | 35/100 |
| P3 joint | -0.024 [-0.038, -0.009] | 27/100 | -0.57 [-1.08, -0.06] | 34/100 |
| P4 joint, P90 duration | -0.026 [-0.041, -0.012] | 27/100 | -0.40 [-1.00, +0.20] | 37/100 |
| ORACLE (perfect forecast) | +0.094 [+0.077, +0.112] | 94/100 | +1.14 [+0.57, +1.72] | 65/100 |
Peak vs B1p-OPT: P0 -2.90 kW (-20.4 %), ORACLE -4.04 kW (-28.4 %).

## Conclusions (AI-G08 / AI-G09)
1. The shared-DC + scheduling value on measured bidirectional cycles is real: -11.6 % grid kWh vs optimised in-rack reuse,
   -20 % peak (P0) — the kill test is passed for the S3 cell type.
2. **AI-G08 FAILS for energy**: forecasting variants are 0.2-0.3 % worse than the recipe-based rolling optimizer (CI excludes 0),
   although the forecasters are far more accurate (Branch C skill 0.3-0.7). The headroom is tiny: even perfect forecasts
   gain only 1.1 % over P0, because rolling re-planning already reacts to every job end.
3. Mentor rule applied: for energy, recommend the simpler optimisation-only solution (P0). AI stays as an optional module
   whose value must be shown on peak (the largest remaining gap: ORACLE peak -1.14 kW vs P0) — tested next with a third
   lexicographic level (minimise peak at equal TT and energy), see `results/v2_peak` (pending).
4. Why the AI variants lose (hypotheses to verify): slot-level P50 interpolation between horizons +1/+4/+16 smooths phase
   transitions that the recipe shape keeps; AI is applied only to running jobs while queued jobs (most of the decision)
   use the recipe in every variant.
