# R4_FIGS — Run 4 figure generator F16-F32 from result CSVs (lead runs it on Colab where the CSVs live)
Account: .codex-A. Effort: medium.
Owner files: src/regenate/visualization/run4_figs.py, tests/test_run4_figs.py, reports/run4/figures/INDEX.md
Read: AGENTS.md, src/regenate/visualization/common.py (house style; reuse save()), reports/run3/*.md, reports/run4/*.md (numbers and
  schemas), src/regenate/evaluation/{v2_campaign,facility}.py (CSV schemas), src/regenate/evaluation/stats.py (paired_ci, wide).
CLI: `python -m regenate.visualization.run4_figs --runs ROOT --out DIR` where ROOT contains (each optional; a missing input -> that
figure is written to INDEX.md as BLOCKED with the missing path, never drawn from invented data):
  run3/v2_diag/results.csv (methods B1,B2,B1p-OPT,ORACLE,P0,TR_RUN,TR_Q,TR_ALL,P1*..P4*), run3/v2_pqstar, run3/v2_pqd, run3/v2_p5,
  run3/v2_pq_gated, run3/v2_e1, run3/v2_e1_peak, run3/screen_e1.csv, run4/v2_wpc_gated, run4/fac_grid_tnb/facility_md.csv,
  run4/fac_bill_tnb_*/facility_md.csv, run4/fac_p0bill_*/facility_md.csv, run3/fin_v3_ds06.csv, run4/eta/metrics_T1.csv, metrics_T2.csv,
  run4/monitor/*.csv, ds07 facility monthly summary if present.
Figures (PNG 300 dpi + PDF + SVG, one provenance json each: inputs, sha256, command): F16 information-value decomposition (bars with
paired CI vs P0: TR_ALL, TR_Q, PQ*, PQd*, TR_RUN; energy and tardiness panels); F17 probabilistic ETA (q10-q90 band vs true, sample
cycles); F18 ETA error vs cycle progress bins; F19 tardiness/production KPIs (P0 vs PQd vs PQd*); F21 AI downstream contribution
forest plot (all AI variants vs P0, energy and TT); F22 E0 vs E1 twin approval and rejection reasons; F24 contribution decomposition
(B0->B1 hardware, B1p-OPT->B2 topology, B2->P0 software, P0->P0-E1-Peak peak/E1, P0->AI; energy kWh with CIs); F25 FIN-A/B/C;
F26 DS07 facility monthly billed demand profile; F27 cell peak vs facility MD increment (coincidence scatter); F28 monthly billed
demand increment by method; F30 billing-aware P0 vs P0-BILL vs ORACLE-BILL; F32 break-even CAPEX vs annual benefit.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_f4 tests/test_run4_figs.py` (tiny synthetic CSVs in a tmp dir:
figures written, missing input -> BLOCKED line, provenance json present).

## Run 2 (lead)
F24 input: ROOT/v2_flex025_n100.csv (Run 2 DS06, n=100, methods B0,B1,B1-OPT,B1p,B1p-OPT,B2,B3,P0,P1..P4,ORACLE; columns as v2_campaign results: instance_id, method, net_kwh, peak_import_kw, TT_h, ...) for B0->B1 (hardware), B1p-OPT->B2 / ->B3 (topology), B2->B3 (scheduling), B3->P0 (rolling); ROOT/run3/v2_e1_peak/results.csv for P0 -> P0-E1-Peak is NOT paired with Run 2 (different run) -> use run3/v2_e1 vs run3/v2_e1_peak (same 50 instances) for the peak level and say so in the caption. Pair only within one file. Validate the other schemas with tiny fixtures built from the column lists in v2_campaign.py/facility.py. Complete everything now and return ALL_PASS when the gate passes.
