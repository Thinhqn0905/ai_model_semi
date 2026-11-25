# R4_MONITOR — Run 4 WP-D cycle- and energy-deviation monitoring: code + tests (lead runs it on Colab; D010; mentor M06, M11, M12, M14)
Account: .codex-B. Effort: medium.
Owner files: src/regenate/forecasting/monitor.py, tests/test_monitor.py, reports/run4/ai_monitoring.md (method + placeholders PENDING_COLAB)
Read: AGENTS.md, src/regenate/forecasting/cycle_model.py (build_table, lag features; do not edit), src/regenate/data/ds05.py
  (cycle table columns: dur_h, e_charge_kwh, e_discharge_kwh, h_charge, h_discharge, h_rest, v_min, v_max, i_abs_max, rte,
  t_amb_mean_c, use_case, ord, split), reports/data/ds02_report.md. No training on this machine: tests on small synthetic data.
Contract — monitor.py with CLI `python -m regenate.forecasting.monitor --proc DIR --out DIR`:
1. Cycle-level deviation scores per completed cycle, using only that cycle's own summary vs history up to the previous cycle:
   statistical baselines (recipe limits = previous cycle +-x %, rolling historical quantiles, MAD z-score, EWMA residual, Shewhart/CUSUM
   on log duration and log energies) vs learned (Isolation Forest, One-Class SVM, conditional quantile regression residual = the Run 3
   cycle model's |log ratio| residual vs its P10-P90 band).
2. Labels: DS05 has no fault labels -> (a) NATURAL deviations: report score distributions and the top-k flagged cycles with their
   features (for engineer review, no accuracy claim); (b) CONTROLLED perturbations as SYNTHETIC stress tests on held-out test cycles
   (duration x1.3, charge energy x1.2, rte -10 %, missing rest phase): precision/recall/F1, PR-AUC, detection rate at matched false
   alarm rate (alarms per 1,000 normal cycles and per operating hour), labelled SYNTHETIC_INJECTED (never "real faults").
3. Thresholds chosen on val only; metrics on test; inference time per cycle.
4. Report skeleton with the claims rules: advisory only, no predictive-maintenance / downtime / avoided-failure claims, never replaces
   independent protection.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_mon tests/test_monitor.py` passes (synthetic injected
anomalies are detected above chance; thresholds use val only; CLI writes outputs).
