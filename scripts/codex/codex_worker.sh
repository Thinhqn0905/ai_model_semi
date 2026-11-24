#!/bin/bash
# Single, manual, bounded Codex worker (ported from multisingal_accelerator harness).
#   CODEX_MANUAL_APPROVED=1 bash scripts/codex/codex_worker.sh <task_id> <account> <task_file> [model] [effort]
#   <account> = default | a CODEX_HOME dir, e.g. 'C:\Users\ADMIN\.codex-B'  (explicit, no rotation)
# Rules: user must set CODEX_MANUAL_APPROVED=1 (Claude never sets it alone); global max workers
# (CODEX_MAX_WORKERS, default 3); one owner per task_id (lock); one run, no loop/auto-restart;
# default effort medium, high only with CODEX_ALLOW_HIGH=1 + written justification in the task file.
cd "$(dirname "$0")/../.." || exit 2
if [ "$CODEX_MANUAL_APPROVED" != "1" ]; then echo "REFUSED: Codex workers are launched manually by the user (set CODEX_MANUAL_APPROVED=1)."; exit 3; fi
TID=$1; ACCT=$2; TASK=$3; MODEL=${4:-${CODEX_MODEL:-gpt-6.1-terra}}; EFFORT=${5:-medium}
[ -z "$TID" ] || [ -z "$ACCT" ] || [ -z "$TASK" ] && { echo "usage: codex_worker.sh <task_id> <account|default> <task_file> [model] [effort]"; exit 2; }
[ "$EFFORT" = xhigh ] && { echo "REFUSED: xhigh is not allowed; use high."; exit 7; }
[ "$EFFORT" != medium ] && [ "$EFFORT" != low ] && [ "$CODEX_ALLOW_HIGH" != 1 ] && { echo "REFUSED: effort $EFFORT needs CODEX_ALLOW_HIGH=1 with a written justification."; exit 6; }
[ -f "$TASK" ] || { echo "no such task file $TASK"; exit 2; }
D=runs/codex; R=$D/registry; mkdir -p $R/running $R/status
alive(){ [ -n "$1" ] && kill -0 "$1" 2>/dev/null; }
live=0; for f in $R/running/*.lock; do [ -e "$f" ] || continue; p=$(cut -d' ' -f1 "$f"); if alive "$p"; then live=$((live+1)); else rm -f "$f"; fi; done
MAXW=${CODEX_MAX_WORKERS:-3}
[ $live -ge $MAXW ] && { echo "REFUSED: $live Codex workers already running (global max $MAXW)."; exit 4; }
LK=$R/running/$TID.lock
[ -e "$LK" ] && { echo "REFUSED: task $TID already has an owner ($(cat $LK))."; exit 5; }
echo "$$ $ACCT $(date -Is)" > $LK; trap 'rm -f $LK' EXIT
if [ "$ACCT" = default ]; then ENVH="env -u CODEX_HOME"; else ENVH="env CODEX_HOME=$ACCT"; fi
LOG=$D/${TID}_$(date +%Y%m%d_%H%M%S).log
P="Read AGENTS.md, then only $TASK and the files it names; do not scan the repository. Continue from the work on disk; do not redo passed gates. Use effort/token sparingly: no polling, no repeated log dumps, no idle waiting. A long run is NOT a reason to stop: run it in the foreground and wait. You must make the changes in your task and run at least one real check (the command named in the task file) before returning; returning with no edits and no new run output is a failure. Answer in English only. Be terse: final message at most 15 lines (a gate table plus the STATUS line). Do not retry the same failing step more than twice. Never claim PASS without a run output path and an evidence boundary label. Edit only your own files. End with exactly one line: STATUS: ALL_PASS, STATUS: GATE_FAIL <reason>, or STATUS: CONTINUE <what is left>."
echo "$(date -Is) start $TID acct=$ACCT model=$MODEL effort=$EFFORT" >> $R/status/$TID.txt
SRCH=""; [ "$CODEX_SEARCH" = 1 ] && SRCH="--search"   # web search for literature tasks
$ENVH codex $SRCH exec -m $MODEL -c model_reasoning_effort=$EFFORT --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox -C . -o $D/${TID}_last.md "$P" < /dev/null > $LOG 2>&1
S=$(grep -o 'STATUS: [A-Z_]*' $D/${TID}_last.md 2>/dev/null | tail -1)
echo "$(date -Is) end $TID ${S:-NO_STATUS}" >> $R/status/$TID.txt
