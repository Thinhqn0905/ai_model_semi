# Industry mentor feedback (reviewer.pdf, received 2026-11-24)

## Positioning
- Present ReGenATE as an **intelligent energy-coordination solution**, not "an AI scheduler".
- Chain: smart device recovers → AI predicts when energy is available/needed → automation
  matches eligible tests → shared DC transfers → grid import drops.
- AI does not create the saving; the hypothesis is: can AI prediction + automated scheduling
  increase directly reused regen energy vs regen-to-AC and conventional scheduling?
- Suggested pitch: "Regenerative hardware already saves energy. ReGenATE asks whether
  production-aware scheduling can recover the energy that existing regeneration still leaves
  on the table. We prove that increment first in shadow mode..."

## Required KPIs
1. Incremental grid kWh saved vs B1 (primary). 2. Peak grid kW. 3. Energy matching ratio
(regen energy directly consumed by another station). 4. Throughput/makespan, FPY, test
integrity = hard constraint. 5. Bus stability (excursions, protection events).
6. AI incremental benefit P − P0. 7. Oracle gap Oracle − P. With CIs across scenarios.
Financial: kWh × tariff → $/yr → CAPEX/OPEX → payback (include conversion losses, retrofit,
requalification effort). Say clearly when it does not pay back.

## Baseline ladder
No recovery → existing regeneration (B1) → shared DC normal scheduling → shared DC +
optimization → shared DC + AI forecast + optimization → oracle. Show what each layer adds.

## Method / Go-No-Go
- Scope: one long-duration, high-power burn-in or power-cycling cell, many similar stations.
  Best fit: makers of complete power converters/supplies/modules; wafer foundry is weak fit.
- First gate: **scheduling flexibility + incremental kWh** — how often source/sink overlap,
  how far starts can move, energy left after conversion losses. If small, stop (valid result).
- Main Go/No-Go = end of shadow mode: clear incremental kWh over B1 after losses, zero
  test-integrity violations, engineer acceptance.
- Barriers: vendor compatibility/bus voltages, isolation & fault protection, requalification,
  OT change management, payback. Minimum evidence: measured profiles, bus stability +
  protection study, FMEA, vendor support, payback vs site threshold.

## Data
- Synthetic scheduling + clearly labelled simulated profiles grounded in datasheets/vendor
  specs + LV prototype is OK for concept feasibility. Present as potential, not site savings.
  Run wide sensitivity.
- Site data priority: (1) time-aligned per-station power profiles; (2) movable start windows &
  constraints; (3) converter efficiency curves; (4) cell AC import/export; (5) quality records.
- Essential constraints: lot priority, due dates, oven capacity, ramps, shifts, max delay.

## Water
Electricity first; water is a separate workstream, no quantitative claim without cooling-loop
flow/ΔT, heat load, chiller/tower water metering.

## Avoid
Borrowing vendor results; retrofit first; AI as a given (must beat matched non-AI optimizer);
fab-wide extrapolation or multiple segments at once; trading quality for energy.
