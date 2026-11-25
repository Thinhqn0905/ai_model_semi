# R4_DEMO2 — Run 4 demonstrator extension: facility load, tariff selector, monthly bill, FIN comparison (section 21)
Account: .codex-B. Effort: medium.
Owner files: app/dashboard.py, src/regenate/app/facility_view.py, tests/test_dashboard_run4.py, reports/run4/demonstrator_v2.md
Read: AGENTS.md, app/dashboard.py, reports/run3/demonstrator.md, src/regenate/economics/billing.py (monthly_bill), data/tariffs/*.yaml,
  src/regenate/evaluation/facility.py (load_ds07, billed_demand), reports/run4/facility_billing.md. Do not edit billing.py/facility.py.
Contract: new dashboard pages reading only files (results dir configurable via env REGENATE_RESULTS, default runs/): (1) Facility
load: pick DS07 facility + month (needs the DS07 zip path; if absent show "data not available"), plot load and billed-demand
interval; (2) Tariff selector: list data/tariffs/*.yaml with each field's VERIFIED/NOT_VERIFIED status shown next to the value;
(3) Monthly bill: baseline vs method from facility_md.csv rows (md_increment_kw) x selected tariff demand rates + energy rate;
NOT_VERIFIED inputs make the result banner "NOT_VERIFIED"; (4) FIN-A/B/C table from fin_v3_ds06.csv if present + break-even CAPEX
(3-y, 5-y simple, discounted 10-y 8 %); (5) report export (markdown) of the current page. Evidence labels shown on every number
(MEASURED, VENDOR_REPORTED, DATASHEET, DERIVED, SIM_DATA_PROFILE, SIM_ASSUMED_PROFILE, ASSUMED, NOT_VERIFIED). No hardcoded results.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_d2 tests/test_dashboard_run4.py tests/test_dashboard_data.py`
(AppTest renders the new pages with tiny fixtures; NOT_VERIFIED banner appears when a tariff field is unverified).

## Run 2 (lead)
fin_v3_ds06.csv schema (produced by fin_options.build + columns set, dc_usd_kw_month): boundary, scenario, option, baseline, method, n, excluded_tt, alpha, demand_enabled, physical_kwh, physical_ci_low, physical_ci_high, peak_kw, peak_ci_low, peak_ci_high, energy_bill_usd, export_credit_effect_usd, demand_saving_usd, annual_net_usd, annual_ci_low, annual_ci_high, capex_usd, opex_usd, missing, qualification, break_even_capex_usd, break_even_ci_low, break_even_ci_high, npv_usd, payback_years, set, dc_usd_kw_month. Use annual_net_usd for break-even. An incremental (not full payable) monthly bill is the intended view: label it so. Finish the gate and return ALL_PASS.
