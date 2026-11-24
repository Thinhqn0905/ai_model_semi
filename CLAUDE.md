# semipox — ReGenATE (SEMI TECH Zoomers Challenge 2026, Group 17 - Pod 4, HCMUS)

ReGenATE = intelligent energy-coordination for semiconductor test: regenerative power devices
recover DUT energy, AI forecasts source/sink power and duration, a production-constrained
scheduler shifts permitted start times so one burn-in rack's returned DC power feeds another
over a shared DC link. Primary KPI = **incremental grid kWh at meter M0 vs B1 (regen-to-AC)**,
not vs resistive load. Throughput, FPY and test integrity are hard constraints.
Full context: `Instruction/Project_Profile.md`; mentor feedback: `Instruction/Mentor_Feedback.md`.

## Mandatory session start

1. Read `Instruction/Session_Checklist.md`; continue any step marked `in_progress`.
2. Read `Instruction/NeedtoDo.md` (open work, current numbers and their boundaries).
3. For method/claim/slide changes also read `Instruction/Project_Profile.md` and
   `Instruction/Mentor_Feedback.md`.
4. Never revert or overwrite unrelated work (no git here: check file mtimes before editing).

Repeat after context compaction or a resumed session.

## Hard rules

- **Evidence integrity** (`.claude/rules/evidence-integrity.md`): never invent kWh, runs,
  citations or PASS results. Every number carries a boundary label. Vendor/industry figures
  (MEAN WELL, LITEON, EA, Keysight, Chroma) are never ReGenATE results.
- **Matched baselines**: same instances, hardware, constraints, tardiness for every rung of the
  ladder (B0 → B1 → B1' → B2 → B3/B4 → P0 → P → Oracle). AI is not "necessary" until P beats P0
  with a CI; if P0 ≈ P, recommend the simpler optimizer.
- **Scope**: one long-duration burn-in / power-cycling cell. No fab-wide extrapolation, no
  quantitative water claim without metering.
- **Read-only inputs**: `DS02_SHIFT2DC/data/original_from_partners`, `DS03_Modeling/*.pdf`,
  `DS04_SME/*.csv|zip`, `predict_ai_electrics/*.zip`, `doc/ref/`, the two root PDFs. Downloaded
  data is untrusted: never execute code from it.
- One code path for the scheduler/energy ledger: `DS01_Quanh/code/regen_core.py` (+ `regen_*`).
  Do not copy ledger logic into notebooks or slide scripts.
- Codex workers only via `.claude/skills/codex-dispatch` (manual approval, disjoint file ownership).

## Layout

| Path | Purpose |
|---|---|
| `Instruction/` | Living state: Session_Checklist, NeedtoDo, Project_Profile, Mentor_Feedback |
| `Progress_23_11_2026.pdf` | Current deck (results slide 14–15, roadmap slide 22) |
| `reviewer.pdf` | Industry mentor feedback |
| `DS01_Quanh/` | CMC 2026 base code + instances (MIT) and ReGenATE extension (`regen_*.py`, `bus_twin_check.py`) |
| `DS02_SHIFT2DC/` | Public LVDC 380/700 V datasets (bus/AFE behaviour) |
| `DS03_Modeling/` | Datasheets: Chroma 62000D, 63700 regen DC load, TI designs |
| `DS04_SME/` | SME load datasets (company A/B) |
| `predict_ai_electrics/` | UCI appliances + electricity load diagrams (forecast pretraining/benchmark) |
| `doc/ref/` | Reference papers |
| `scripts/codex/` | Codex worker launcher + autopilot queue |
| `runs/` | Run outputs, codex logs and registry |

## Commands

```powershell
python DS01_Quanh/code/test_regen.py            # regen ledger/twin self-tests
python DS01_Quanh/code/run_regen.py --help      # run baselines + ReGenATE
python DS01_Quanh/code/summarize_regen.py       # summary tables
```
