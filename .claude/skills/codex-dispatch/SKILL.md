---
name: codex-dispatch
description: Coordinate several Codex CLI accounts (CODEX_HOME profiles default, .codex-A..E) as bounded implementation workers for this ReGenATE project — write task files, assign one task per account with disjoint file ownership, launch via scripts/codex, check outputs. Use when the user asks to hand work to Codex / run Codex accounts / autopilot.
---

# Codex dispatch (semipox)

Accounts: `default` (no CODEX_HOME) and `C:\Users\ADMIN\.codex-A` … `.codex-E`. Each is a
separate login/quota. One account = one live task. Lead (Claude) plans, writes task files,
integrates and runs the final checks; Codex workers implement.

## 1. Split the work
- Only independent tasks with **disjoint file ownership** go in parallel. Shared files
  (e.g. `DS01_Quanh/code/regen_core.py`) have exactly one owner per campaign.
- Dependent tasks go in the same account queue or use a `done:<id>` gate.
- Default effort `medium`; `high` only for hard algorithm/debug work, justified in the task file.

## 2. Write a task file `scripts/codex/tasks/<ID>.md`
```
# <ID> — <title>
Owner files (edit only these): <paths>
Read: AGENTS.md, <exact files>          (no repo scan)
Contract: <inputs, outputs, formulas, constraints, matched-baseline rules>
Gate: <exact command>, expected output path under runs/<id>/
Evidence: label results per .claude/rules/evidence-integrity.md
Effort justification (only if high): ...
```

## 3. Launch (user must approve each campaign)
Single task (user types it, or approves Claude running it):
```
! cd /d/Subject_ProjectClass/semipox && CODEX_MANUAL_APPROVED=1 bash scripts/codex/codex_worker.sh <id> 'C:\Users\ADMIN\.codex-A' scripts/codex/tasks/<ID>.md
```
Multi-account queue: edit `$Q` in `scripts/codex/autopilot.ps1`, then run it in background
(`powershell -File scripts/codex/autopilot.ps1`). It probes each account, waits 30 min on
usage limits, respects gates and max runs per item.

Never set `CODEX_MANUAL_APPROVED=1` without the user's approval for that campaign.

## 4. Check
- Status: `runs/codex/registry/status/<id>.txt` (last line `end <id> STATUS: ...`).
- Final message: `runs/codex/<id>_last.md`; full log `runs/codex/<id>_<ts>.log`.
- A worker's STATUS line is not evidence: open its run output, rerun its gate yourself
  sequentially, then update `Instruction/NeedtoDo.md` / `Session_Checklist.md`.
- Never print or copy CODEX_HOME contents, auth files or provider config.
