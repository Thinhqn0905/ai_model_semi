# R4_LOADAI — Run 4 WP-J facility-load forecaster for AI-BILL (code; lead runs on Colab) (D017.1; additional research)
Account: .codex-A. Effort: medium.
Owner files: src/regenate/forecasting/facility_load.py, tests/test_facility_load.py, reports/run4/ai_facility_load.md (method + PENDING_COLAB)
Read: AGENTS.md, src/regenate/evaluation/facility.py (load_ds07, bg_forecast, run_p0bill_block; do not edit), reports/run4/facility_billing.md.
Contract — CLI `python -m regenate.forecasting.facility_load --ds07 ZIP --out DIR`:
1. Per factory, 15-min mean load; chronological split per factory: Mar-Jun train, Jul val, Aug-Sep test (no shuffling). Decision times
   every 15 min; horizons 1..60 slots (15 h, the block length). Causal features only: lags (15 min .. 1 week), same time last 1-4 weeks,
   time of day, weekday, rolling stats up to t; missing slots stay NaN (tree models handle NaN; never fill from the future).
2. Models: persistence, seasonal (same slot last week), historical mean of last 4 weeks (= facility.bg_forecast 'hist'), ridge, RF,
   XGBoost, LightGBM, quantile LightGBM (P10/P50/P90) - one global model across factories with a factory id feature, target scaled by the
   factory's training median. Metrics on test per horizon bucket: MAE, NMAE, skill vs 'hist', peak-event recall (top-5 % slots of each
   month within the TNB peak window), P10-P90 coverage.
3. Export a predictor usable by facility.py: `predict(factory, t, n_slots) -> np.ndarray kW` loading a saved joblib; write
   forecasts parquet for all (factory, decision time) in Jul-Sep at block starts so facility.py can read them without the model.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_fl tests/test_facility_load.py` (synthetic: no future leakage
assertion, split order, predict shape).
