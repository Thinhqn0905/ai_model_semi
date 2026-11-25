Boundary: SIM_DATA_PROFILE cell + MEASURED DS07 facility (not synchronised); TNB ToU rule (peak-period 30-min MD); 1 cell; 6 factories
(Forge_1, Forge_2, Metal_1, Metal_3, Paper, Steel_1) x forecaster TEST months 2019-08/09 = 12 facility-months; factory-clustered paired
bootstrap CI (+ = lower billed-demand increment). Raw: Drive `MyDrive/semiexpo/ai_runs/run4/fac_aibill_*/facility_md.csv`, summary
`MyDrive/semiexpo/ai_runs/run4_final_summary.md`; forecaster `run4/facility_load/facility_predictor.joblib` (global LightGBM across factories,
Mar-Jun train, Jul val, Aug-Sep test, 2-h decision stride; src/regenate/forecasting/facility_load.py).

| Comparison | kW [95 % CI] | months better |
|---|---|---|
| P0-BILL hist -> P0-BILL ai (value of the learned forecast) | +0.10 [0.00, +0.30] | 1/12 |
| P0-E1-Peak -> P0-BILL ai | -0.84 [-2.70, +1.31] n.s. | 5/12 |
| P0-E1-Peak -> P0-BILL oracle (perfect background) | +2.56 [+0.90, +4.34] | 8/12 |
| P0-BILL ai -> P0-BILL oracle (headroom missed by AI) | +3.40 [+1.83, +4.76] | 9/12 |
Per facility-month MD increment, kW (P0-E1-Peak / P0-BILL ai / P0-BILL oracle): Forge_1 Aug 7.53/7.23/2.88, Sep 2.73/7.47/5.63; Forge_2 Aug
-0.73/-0.73/-0.73, Sep -0.22/6.47/-0.33; Metal_1 Aug 9.21/8.25/0.32, Sep 3.14/1.95/0.93; Metal_3 Aug -3.46/-3.46/-3.46, Sep 7.30/0.00/0.00;
Paper Aug 2.85/6.12/-0.16, Sep 9.76/8.64/3.01; Steel_1 Aug 1.06/2.68/0.00, Sep 0.00/4.57/0.31.
Earlier months (2019-05/07, 12 facility-months, reports/run4/facility_billing.md): P0-BILL hist -0.57 [-2.56, +0.89], oracle +0.94 [-0.80, +2.96] vs
P0-E1-Peak (n.s.); 5-cell P0-BILL worse than P0-E1-Peak by ~6 kW.
Forecaster accuracy table: NOT AVAILABLE - the metrics phase of facility_load.py failed ("cannot reindex on an axis with duplicate labels",
Colab runtime 2 log) after the model was trained; not repaired per D019/D020 (no further AI work). Unresolved defect.

**Go/No-Go: AI-BILL = NO-GO.** The learned facility-load forecast is indistinguishable from the historical-profile forecast (+0.10 kW, 1/12) and
does not beat the default engine. A perfect background forecast would give a significant billing gain in the test months (+2.56 kW vs
P0-E1-Peak) but not in May/July, so billing-aware scheduling is a conditional research lead that needs real facility meter data, not a
deployable function. Default remains P0-E1-Peak (D006/D019). No further AI scheduling experiments (D018/D019).
