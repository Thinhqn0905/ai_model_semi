# Figure inputs

Run `python -m regenate.visualization.generate_all_figures --campaign runs/oracle_v1 --out reports/figures` with `src` on PYTHONPATH. Missing inputs are skipped. Each input requires a single `boundary` value; mixed boundaries are rejected. The exception is the datasheet efficiency file, whose DATASHEET provenance is labelled VENDOR_REPORTED. Schedules obtain their boundary from the matched instance and flexibility in results.csv. F08 is the paired difference in net grid kWh against B1 with a 95% bootstrap interval over instances; compare only matched configurations and inspect tardiness and other constraints separately.

| Figure | Input (relative to campaign unless stated) | Columns |
|---|---|---|
| F01, F02 | forecast_predictions.parquet | t, actual, pred, lower, upper, boundary |
| F03 | horizon_metrics.csv | horizon, mae, boundary |
| F04 | benchmark/results.csv | train_dataset, test_dataset, metric (nmae or skill), value, boundary |
| F05 | data/processed/efficiency_points.parquet | device, load_frac, eta, provenance |
| F06 | timeseries.parquet | t_h, source_kw, sink_kw, link_cap_kw, boundary |
| F07 | bus_transients.csv | t_s, v_bus, v_min, v_max, boundary |
| F08 | results.csv | instance_id, flex if present, method, net_kwh, boundary |
| F09 | ablation_results.csv | variant, value, boundary |
| F10 | sensitivity_results.csv | flexibility, efficiency, value, boundary |
| F11 | forecast_predictions.parquet | model, error, boundary |
| F12 | quantile_calibration.csv | nominal, empirical, boundary |
| F13 | schedules.parquet plus results.csv | instance_id, flex if present, method, job_id, station, start_h, end_h; results boundary |
| F14 | ledger_totals.csv | source, target, value, boundary (ledger flows in common units) |
| F15 | runtime_metrics.csv | model, latency_ms, mae, boundary |

`model_metrics.csv` is reserved for model-level summaries and is not needed when prediction rows provide the F02 metrics. F14 image export requires Plotly and Kaleido. F06 requires source and sink at the same electrical boundary and an explicit link cap; aggregated ledger totals do not establish these time series.

For the oracle campaign, `python -m regenate.visualization.build_oracle_timeseries` reconstructs one S3 instance at one recorded flexibility for ORACLE and B1p-OPT, using the recorded slot and electrical parameters and true rendered profiles. It verifies each reconstructed M0 net energy against results.csv. The additional F06 columns are residual source at the receiving link boundary (after link efficiency), residual sink, and the campaign link cap; `direct_kw` is the actual topology-specific shared-link transfer. The section-10 fields and instance, method, flexibility and boundary are retained. F06 shows the ORACLE schedule only; B1p-OPT is included for traceability, not treated as shared-link transfer.
