# Run 3 plan (2026-11-25, lead) — md deliverables only, no slides (user instruction)

Run 2 is frozen: existing `reports/`, `runs/`, `results/` are not overwritten; Run 3 writes to `reports/run3/`, `runs/run3/`.

## Repository status audit (short)
| Area | State | Gap for Run 3 |
|---|---|---|
| Ledger B0/B1/B1p/DC + ELEC tests | done, tests pass | none (audit only) |
| Exact MILP + rolling Replanner + Replay | done | no electrical limits inside MILP (post-check only) -> WP-E |
| DS05 processing / Branch C forecasters | done on Colab; raw CSV on Drive only | rebuild locally from `DS5.zip` (reproducibility check) |
| DS06 ladder P0..P4 | done on Colab (Drive CSVs) | ORACLE is one-shot, P0 rolling -> headroom not matched; rerun locally |
| AI integration | P1-P4 use 3-horizon interpolation, running jobs only | root cause unknown -> AI14/AI15/AI18 |
| Bus twin | approximate, stops at first UV | record all violations, transient model -> WP-E |
| Economics | FIN-A/B/C v1, payback 61.7 y | break-even CAPEX, missing-cost flags -> WP-F |
| Cross-dataset heatmap | inconsistent IDs/skill refs | WP-C |
| Demonstrator | dashboard on stored outputs | end-to-end offline pipeline + decision log -> WP-D/14 |

## Dependency-aware order
```text
A0 local DS05 rebuild -> A1 retrain (same seed) -> A2 DS06 matched rerun (+ rolling oracles)
                                                    |-> A3 root-cause decomposition (lead)
                                                    |-> B  AI14 -> AI15 -> AI18 (lead)
E1 MILP electrical limits (lead) ------------------> A2' rerun with limits -> twin approval
WP-A audit (codex default)   WP-C xbench (codex A)   WP-F econ (codex B)
WP-E twin/transient (codex C)   demonstrator pipeline (codex E)
all -> mentor compliance audit M01-M16 (lead, last)
```

## Key new experiments (lead)
- **A3 information decomposition** (M09, M12): rolling MILP with TRUE profiles for (a) all jobs = R-ORACLE,
  (b) running jobs only, (c) queued jobs only. Gives the matched headroom available to each AI integration point.
  If (b) ~ 0, running-job forecasting cannot help by construction.
- **AI14** transition timing error of recipe vs AI; **AI15** phase-aware forecast (phase sequence + per-phase duration
  + per-phase power) used as a full trajectory instead of 3-point interpolation; **AI18** selective use with CQR
  confidence and P0 fallback. Model selection on validation; DS06 test split held out.
- **E1** AFE import/export cap and shared-link cap as hard MILP constraints; compare twin approval vs post-check.

Status per campaign: PASS / FAIL / INCONCLUSIVE / BLOCKED per `docs/system_spec.md` result schema.
