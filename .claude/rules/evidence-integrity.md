# Evidence Integrity (always applies)

Adapted from the msbio accelerator harness for ReGenATE energy/scheduling work.

1. **No invented observations.** Never fabricate kWh, kW, tardiness, run IDs, instance counts,
   citations or PASS labels. A script that ran is not proof its result is valid: check the
   instance set, the power profile, the bus limits and where the numbers came from. A prior
   agent answer or slide is a lead, not ground truth.
2. **Every number has a source and a boundary.**
   - `SOURCE_REPORTED` — from a paper (cite DOI + setup), e.g. CMC 2026 TEC −8.8…−21.7 %.
   - `VENDOR_REPORTED` — equipment/case-study figures (Keysight, Chroma, EA, MEAN WELL, LITEON).
     Never presented as ReGenATE savings.
   - `SIM_ASSUMED_PROFILE` — simulation on assumed power profiles (current results, e.g.
     output = 90 % of input). Always state the profile.
   - `SIM_DATA_PROFILE` — simulation with profiles fitted to a real trace/datasheet (name it).
   - `BENCH` — low-voltage demonstrator measurement. `SHADOW_SITE` — read-only site data.
   - `NOT_VERIFIED` when any binding is missing.
3. **Comparisons must be matched**: same instances, seeds, profile, bus cap/efficiency, export
   credit and tardiness across B0…Oracle. Report mean ± 95 % CI (paired over runs) before
   claiming one rung beats another; "not significant" must be said when true.
4. **Claim records.** Numbers promoted to `Instruction/NeedtoDo.md`, slides or the report go in
   `runs/claims.jsonl`: `{"claim_id","metric","value","unit","boundary","baseline","runs",
   "profile","command","script","limitations"}`.
5. **Fail closed.** Missing/stale/contradictory evidence ⇒ `NOT_VERIFIED`/`FAIL` with the actual
   error. Keep failed runs and negative results (e.g. the in-rack kill test) — do not hide them.
6. **Final answers** state what actually ran, at which boundary, and what is still pending.
