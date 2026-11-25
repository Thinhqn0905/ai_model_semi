# Reconciliation log

Evidence boundary: document reconciliation using reported Drive bindings; independent Drive retrieval and site validation NOT_VERIFIED.

### reports/final/parts/part1.md
- Old: | AI-BILL and forecaster accuracy | not available | PENDING | expected `MyDrive/semiexpo/ai_runs/run4_final_summary.md` |
- New: | AI-BILL learned forecast | 12 facility-months | NO-GO; -0.84 kW vs P0-E1-Peak | factory-clustered [-2.70, 1.31]; D020, `MyDrive/semiexpo/ai_runs/run4_final_summary.md`; SIM_DATA_PROFILE + unsynchronized MEASURED |
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/final/parts/part1.md
- Old: Go only if AI beats both historical P0-BILL and P0-E1-Peak with factory-clustered CIs excluding zero; otherwise no-go after evaluation. `docs/handoff_run4.md`, `docs/decisions.md` D017. No result is claimed while pending.
- New: D020 concludes NO-GO: learned forecast improvement versus historical profile is +0.10 kW [0.00, 0.30], factory-clustered CI; the gate requires improvement against both baselines. Forecaster metrics export was repaired under D021 without retraining; raw verification remains pending.
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/final/parts/part1.md
- Old: Status is based on index evidence only; PASS requires inspection and is not inferred. Original index `reports/figures/INDEX.md`; run-4 index `reports/run4/figures/INDEX.md`; boundary NOT_VERIFIED unless otherwise listed. F01/F02/F11 explicitly missing prediction rows. F16–F32 local run-4 figure files missing; the index lists selected campaign inputs as blocked. Figure file paths and full source data for F16–F32 are not recorded in the index.

| Figure | Path / source data | Status |
|---|---|---|
| F01, F02, F11 | no prediction rows; `reports/figures/INDEX.md` | MISSING |
| F03, F12 | `results/ai_ds05_branchC/model_metrics.csv` | NOT_VERIFIED: figure path/inspection not established |
| F04 | `runs/ai/ds02/model_metrics.csv`, `runs/ai/ds04/model_metrics.csv`, `results/ai_ds05_branchC/model_metrics.csv` | NOT_VERIFIED |
| F05 | `data/processed/efficiency_points.parquet`; VENDOR_REPORTED | NOT_VERIFIED |
| F06 | `runs/oracle_v1/timeseries.parquet`; SIM_ASSUMED_PROFILE | NOT_VERIFIED |
| F07 | `runs/twin_v1/controls.json`; SIM_ASSUMED_PROFILE | NOT_VERIFIED |
| F08, F14 | `runs/rolling_v1/ladder.csv`; SIM_ASSUMED_PROFILE | NOT_VERIFIED |
| F09 | `reports/ai/ai_exp12_ds06.md`; SIM_DATA_PROFILE | NOT_VERIFIED |
| F10 | `F10.png/pdf`, `runs/sens_v1/sensitivity_results.csv`; SIM_ASSUMED_PROFILE | NOT_VERIFIED: location/inspection not established |
| F13 | `runs/oracle_v1/schedules.parquet`, `runs/oracle_v1/results.csv`; SIM_ASSUMED_PROFILE | NOT_VERIFIED |
| F15 | `results/ai_ds05_branchC/runtime_metrics.csv`, `results/ai_ds05_branchC/model_metrics.csv` | NOT_VERIFIED |
| F16 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F17 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F18 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F19 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F20 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F21 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F22 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F23 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F24 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F25 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F26 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F27 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F28 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F29 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F30 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F31 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |
| F32 | figure and source data not recorded; `reports/run4/figures/INDEX.md`; Drive transfer pending | MISSING |

DOCUMENT CHECK: six required sections present; missing metrics and raw source bindings explicitly flagged. Boundary: NOT_VERIFIED.


- New: Earlier index-only figure statuses are superseded by the final status table below. Drive-generated figures have not been independently retrieved locally.


- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/final/parts/part2.md
- Old: Registry marks individual rates NOT_VERIFIED while the later economics report marks rates verified: reconciliation needed. HV rate fields and exact quotations beyond the above: NOT_VERIFIED here.
- New: TNB MV/HV schedule rates and peak window are VERIFIED against p.2 of the owner-supplied official PDF, SHA-256 e6634bbeec72c58c6d544c0d73953dda5616b742131453a73e889d307395a43e; holiday treatment is NOT documented. The older registry status is superseded.
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/final/parts/part2.md
- Old: `run4/v2_e1_peak_b`
- New: `run4_rt2/v2_e1_peak_b/results.csv`
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/final/parts/part2.md
- Old: any missing cost removes it
- New: additional missing costs can extend the payback beyond that threshold
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/final/parts/part3.md
- Old: Screenshots: MISSING; no screenshot files are established by the supplied evidence (`reports/run4/figures/INDEX.md`).
- New: Dashboard screenshots are reported at `reports/run4/screenshots/` (final figure status in part 1); independent local inspection NOT_VERIFIED.
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/final/parts/part3.md
- Old: | D018 | Prefer FIN-B at 5?10 cells conditionally; shadow and site acceptance remain open. |
- New: | D018 | Prefer FIN-B at 5?10 cells conditionally; confirm 30-minute MD; site acceptance remains open. |
| D019 | Freeze architecture and reference AFE 20 / bus 32 kW; candidate AFE 20 / bus 16 kW; M12 FAIL. |
| D020 | AI-BILL NO-GO; retain AI for ETA and advisory. |
| D021 | Freeze architecture; E1-screened nominal fallback and AFE margin, with safety verification pending. |
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/final/parts/part3.md
- Old: Remaining work: retrieve AI-BILL and sizing results, reconcile claims and matched runs, obtain site/mentor evidence and complete protection and economic qualification
- New: Remaining work: independently retrieve reported AI-BILL and sizing results, verify D021 safety, reconcile remaining claims and matched runs, obtain site/mentor evidence and complete protection and economic qualification
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/run4/mentor_compliance_run4.md
- Old: D017.2
- New: D017 (item 2)
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/run4/mentor_compliance_run4.md
- Old: The source verdict says 1?3 cells do not reach 3?5 years but its table gives 3-cell MV General 4.0 years: this inconsistency requires lead reconciliation.
- New: The corrected three-cell paybacks are 4.0 years General and 5.0 years ToU on known CAPEX only; missing costs can extend them beyond the threshold (SIM_DATA_PROFILE plus unsynchronized MEASURED, ASSUMED finance; raw `ai_runs/run4/fin_fac_{gen,tou}_fx{0.21,0.24}/clustered_summary.csv`).
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/run4/mentor_compliance_run4.md
- Old: the 30-minute interval is owner-confirmed but documentarily NOT_VERIFIED, and holiday handling remains open.
- New: the 30-minute interval is VERIFIED by TNB under D018; the peak window and rates are VERIFIED in the official schedule p.2 (SHA-256 e6634bbeec72c58c6d544c0d73953dda5616b742131453a73e889d307395a43e); holiday handling is NOT documented.
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/run4/mentor_compliance_run4.md
- Old: AI-BILL PENDING (`docs/handoff_run4.md`).
- New: AI-BILL NO-GO (D020; `MyDrive/semiexpo/ai_runs/run4_final_summary.md`); independent retrieval NOT_VERIFIED.
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/run4/mentor_compliance_run4.md
- Old: missing costs and inconsistent 3-cell verdict; site NOT_VERIFIED.
- New: missing costs; corrected three-cell payback 4.0/5.0 years on known CAPEX only; site NOT_VERIFIED.
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/run4/mentor_compliance_run4.md
- Old: retrieve and evaluate pending AI-BILL outputs from the location in `docs/handoff_run4.md`. Reconcile the FIN-B three-cell verdict, tariff interval and full site costs.
- New: independently retrieve reported AI-BILL outputs and establish full site costs; AI-BILL is NO-GO under D020.
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/run4/mentor_compliance_run4.md
- Old: retrieve pending sizing twin screening (`docs/handoff_run4.md`); complete electrical sizing validation
- New: independently retrieve D019 sizing screening and verify D021 safety (`ai_runs/run4/v2_safe_p0`); complete electrical sizing validation
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/run4/mentor_compliance_run4.md
- Old: the source three-cell verdict contradicts its table (`reports/run4/economics_run4.md`). Sizing twin screening remains PENDING (`docs/handoff_run4.md`).
- New: the corrected three-cell table gives 4.0/5.0 years on known CAPEX only. D019 reports candidate AFE 20 / bus 16 kW screening on 30 instances (SIM_DATA_PROFILE; `ai_runs/run4_rt3/v2_size_afe20_bus16`, sha256 9b253122); independent retrieval remains pending.
- Reason: reconcile against decisions, final figure table, or raw binding manifest.

### reports/final/parts/part1.md
- Old: no complete P0 violation and D021 verification status.
- New: Run 4 default P0 has 1/100 modeled AFE-shortfall violations: instance `v2_test_n10_s62`, one step, 0.259 kWh (SIM_DATA_PROFILE; `MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv`, sha256 57cd90452ba6e187). D021 specifies an E1-screened nominal plan and fallback, FIFO only if infeasible with `initial_plan=fifo_unscreened`, and planning at 18 kW against a 20 kW scoring limit. Verification is pending at `ai_runs/run4/v2_safe_p0`; this is not a safety PASS.
- Reason: preserve the failed default-engine observation and distinguish the unverified safety fix.

### reports/final/parts/part2.md
- Old: no complete P0 violation and D021 verification status.
- New: Run 4 default P0 has 1/100 modeled AFE-shortfall violations: instance `v2_test_n10_s62`, one step, 0.259 kWh (SIM_DATA_PROFILE; `MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv`, sha256 57cd90452ba6e187). D021 specifies an E1-screened nominal plan and fallback, FIFO only if infeasible with `initial_plan=fifo_unscreened`, and planning at 18 kW against a 20 kW scoring limit. Verification is pending at `ai_runs/run4/v2_safe_p0`; this is not a safety PASS.
- Reason: preserve the failed default-engine observation and distinguish the unverified safety fix.

### reports/final/parts/part3.md
- Old: no complete P0 violation and D021 verification status.
- New: Run 4 default P0 has 1/100 modeled AFE-shortfall violations: instance `v2_test_n10_s62`, one step, 0.259 kWh (SIM_DATA_PROFILE; `MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv`, sha256 57cd90452ba6e187). D021 specifies an E1-screened nominal plan and fallback, FIFO only if infeasible with `initial_plan=fifo_unscreened`, and planning at 18 kW against a 20 kW scoring limit. Verification is pending at `ai_runs/run4/v2_safe_p0`; this is not a safety PASS.
- Reason: preserve the failed default-engine observation and distinguish the unverified safety fix.

### reports/run4/mentor_compliance_run4.md
- Old: no complete P0 violation and D021 verification status.
- New: Run 4 default P0 has 1/100 modeled AFE-shortfall violations: instance `v2_test_n10_s62`, one step, 0.259 kWh (SIM_DATA_PROFILE; `MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv`, sha256 57cd90452ba6e187). D021 specifies an E1-screened nominal plan and fallback, FIFO only if infeasible with `initial_plan=fifo_unscreened`, and planning at 18 kW against a 20 kW scoring limit. Verification is pending at `ai_runs/run4/v2_safe_p0`; this is not a safety PASS.
- Reason: preserve the failed default-engine observation and distinguish the unverified safety fix.

### docs/traceability.md
- Old: no complete P0 violation and D021 verification status.
- New: Run 4 default P0 has 1/100 modeled AFE-shortfall violations: instance `v2_test_n10_s62`, one step, 0.259 kWh (SIM_DATA_PROFILE; `MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv`, sha256 57cd90452ba6e187). D021 specifies an E1-screened nominal plan and fallback, FIFO only if infeasible with `initial_plan=fifo_unscreened`, and planning at 18 kW against a 20 kW scoring limit. Verification is pending at `ai_runs/run4/v2_safe_p0`; this is not a safety PASS.
- Reason: preserve the failed default-engine observation and distinguish the unverified safety fix.

## Check: python DS01_Quanh/code/test_regen.py

Boundary: LOCAL_RUN, ledger self-test only; exit code 0.

```text
all tests passed

```


## Reconciliation textual check

Boundary: LOCAL_RUN, document consistency only.

PASS: M01?M16 statuses match in all three tables; decision references exist; stale AI-BILL/sizing markers absent; P0 violation present in five owned documents. Scope: textual checks only.
