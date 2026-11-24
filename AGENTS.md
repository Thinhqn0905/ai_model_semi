# semipox — ReGenATE (agents / Codex workers)

Read CLAUDE.md, Instruction/Session_Checklist.md, Instruction/NeedtoDo.md and the task file
you were given. Read Instruction/Project_Profile.md and Instruction/Mentor_Feedback.md only when
the task changes method, claims or slides. Read applicable .claude/rules explicitly. Do not scan
the whole tree; read only the files your task names.

Reply to the user in Vietnamese. Codex worker final messages are in English (see the launcher).

- Evidence boundaries (`.claude/rules/evidence-integrity.md`) apply to every number. A worker's
  final text is not evidence; the run directory and its summary are.
- Every comparison uses the same instances, profile, bus limits and tardiness for all baselines.
  Primary KPI = incremental grid kWh vs B1 at M0; also peak kW, matching ratio, P − P0,
  Oracle − P, throughput/tardiness, bus excursions. Report mean ± CI over runs.
- Energy ledger and scheduler live in DS01_Quanh/code (regen_core.py is the single source).
  Do not fork it into notebooks or slide scripts.
- Raw data under DS02/DS03/DS04/predict_ai_electrics and doc/ref are read-only.
- Edit only the files your task owns. No reviewer committees; the lead integrates and runs
  final checks sequentially. Local runs are short CPU runs; no parallel duplicate campaigns.
- Never publish credentials, CODEX_HOME contents or raw provider configuration.
