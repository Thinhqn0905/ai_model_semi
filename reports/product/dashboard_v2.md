# Dashboard v2

The campaign selector discovers result or ladder CSVs, preferring the ladder. Scenario defaults to S3 and flexibility is selected separately when present. Evidence boundaries come from the loaded data. Missing schedules and time series are reported as unavailable.

Finance displays stored business-case rows filtered by export credit, CAPEX factor and demand charge, without calculating new financial estimates. Forecast skill and interval coverage are sourced from DS05 model metrics; accuracy does not establish energy savings (AI-EXP12 is separate). Approval decisions remain in the campaign decision log.

Campaign results and finance use their CSV evidence boundaries; DS05 forecasting is LOCAL_RUN on measured data. Neither constitutes a site measurement of energy savings.
