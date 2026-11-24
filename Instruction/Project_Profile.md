# Project Profile — ReGenATE (from Progress_23_11_2026.pdf)

Title: AI-Driven Energy-Aware Test Scheduling for Cross-Station Power Recirculation in
Semiconductor Testing Facilities. SEMI TECH Zoomers Challenge 2026, Group 17 - Pod 4, HCMUS.

## Problem
Burn-in with resistive loads turns DUT energy into heat (grid pays, HVAC pays again). Regen
loads return 93–95 % to AC (VENDOR_REPORTED). Gap: cross-rack DC reuse only happens when a
returning rack and a demanding rack overlap in time; nobody schedules for that overlap.
Base model: Quanh, Phuc & Hanh, CMC 2026, doi:10.32604/cmc.2026.088630 (hybrid flow shop,
lexicographic TT then TEC, E-TTLBO; code in DS01_Quanh, MIT).

## What ReGenATE adds
- Second objective = grid kWh at M0 (TT stays first).
- Rolling 15-min re-plan with quantile-GBM power forecasts (P10/P50/P90, 4–8 h horizon).
- E-TTLBO-ReGen: 6 strings [S1..S6], 8 operators, running batches frozen, seeded from B3.
- Bus twin rejects plans violating V_min ≤ V_bus ≤ V_max, |I| ≤ I_max, P_direct ≤ P_link,max, ramp.
- Engineer approves every plan; only start times are written. Never touches recipe/PLC.

## Architecture
- Server (on-prem, IEC 62443 / SEMI E187): forecast, scheduler, bus twin, approval UI.
- Edge nodes (read-only): M0 grid meter (1 Hz), M1 DC bus (100 Hz–1 kHz, tau_afe = 80 ms),
  M2 burn-in rack (1–10 Hz, STEP = 6 steps/slot), M3 final test/ATE, M4 MES gateway.
- Plant: 400 VDC link (safe 380–420 V), 40 mF, 20 kW bidirectional AFE (94–96 %), chopper
  15 kW at 415 V, current limit 80 A, PLC protection < 10 ms independent of AI.

## Ledger (regen_core.py)
D = min(Ret, Dem, P_dc); imp = (Dem − η_dc·D)/η_imp; exp = (Ret − D)·η_afe;
E_M0 = Σ (imp − α_ex·exp)·Δt.

## Baseline ladder & current results (SIM_ASSUMED_PROFILE, output = 90 % input, 18 runs)
| Rung | Setup | Grid kWh |
|---|---|---|
| B0 | No recovery, FIFO | 598.6 |
| B1 | Grid return, FIFO | 269.6 |
| B1' | In-rack reuse, FIFO | 251.4 |
| B2 | Shared bus, FIFO | 257.8 |
| B1-opt | Grid return, optimized | 174.0 |
| B3 | Shared bus, static plan (base paper) | 178.8 |
| P0 | Rolling, no forecast | 165.2 |
| P | ReGenATE (forecast + rolling) | 166.9 |
| B1'-opt | In-rack reuse, optimized (kill test) | 162.6 |
| Oracle | Perfect forecast | 163.8 |

Headline: −4.2 % kWh vs B1-opt, −14.7 % peak kW, 0.83 of gap to oracle closed, forecast adds
+0.8 % (not significant). **Kill test not passed**: B1'-opt is 2.8 % below P (18/18). On equal
terms (98 %, no cap) bus and in-rack tie — bus only helps when racks are out of step.
Sensitivity table (slide 19) uses an earlier invalid profile (returned > input) — rerun pending.

## Feasibility (one 50 kW cell, estimate)
CAPEX $30,114 (meters 4,406; server 4,220; converter+bus+safety 21,838); saving ≈ $2.5k/yr ⇒
payback > 10 yr. Tariff VN $0.078/kWh base. FMEA: bus OV (54), tests cannot shift (48),
bad forecast (40), wrong start (28).

## Roadmap
Phase 1 shadow (meters only) → Phase 2 shadow on grid return (main gate: kWh below B1, 0 test
violations) → Phase 3 shared-bus pilot (bus study, FMEA, payback).
Known limits: assumed profile, 15-min slots on base-paper time units vs 80 h burn-in,
only 10/20-job instances.
