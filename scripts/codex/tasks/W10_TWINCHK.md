# W10_TWINCHK — Bus stability KPI for real schedules (mentor KPI "bus stability", M06)
Account: .codex-C. Effort: medium.
Owner files: runs/twin_check/**, reports/safety/bus_stability_kpi.md
Read: AGENTS.md, src/regenate/simulation/bus_twin.py (check_plan), runs/rolling_v1/timeseries.parquet + ladder.csv,
  reports/safety/bus_twin.md. Do not edit src/.
Contract: for every S3 instance and methods B2, B1p-OPT, P0, P, ORACLE in rolling_v1 (render source/sink per slot from
schedules + regenate.evaluation.oracle_campaign.load/render if timeseries lacks per-method data), run check_plan with the default
twin parameters; table per method: approval rate, v_min/v_max distribution, i_peak, chopper energy, violation kinds. Also one
"uncoordinated burst" negative control per instance. Label SIM_ASSUMED_PROFILE; state that this checks simulation logic only.
Gate: report exists with counts per method; failures listed, never dropped.

## Run 2 (lead)
Root cause: twin AFE = 20 kW (slide 12) but bench_v1 cell import peaks are 34-50 kW -> undervoltage collapse and I=P/V blow-up. Do: (1) report this as an AFE sizing finding (AFE must be >= peak import, which is exactly why peak reduction matters); (2) rerun with P_afe_max sized per instance = 1.2 x max ledger import of B2 (state it) and with a fixed 60 kW; (3) after the first undervoltage the run must stop integrating that plan (no currents after collapse) - implement in runs/twin_check scripts, not in src. Same tables.
