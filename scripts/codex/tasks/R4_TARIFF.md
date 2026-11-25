# R4_TARIFF — Run 4 WP-H official tariff registry + monthly billing engine (D014, D015; mentor M16; additional research)
Account: default. Effort: medium. Web search allowed (official sources only).
Owner files: data/tariffs/**, src/regenate/economics/billing.py, tests/test_billing.py, reports/run4/tariff_registry.md
Read: AGENTS.md, docs/run3_plan.md, reports/run3/economics_v3.md, src/regenate/economics/fin_options.py (do not edit it).
Contract:
1. One YAML per tariff in data/tariffs/: TAR01_MY_TNB_RP4_MV_general.yaml, TAR01_MY_TNB_RP4_MV_TOU.yaml (Peninsular Malaysia,
   schedule effective Jul 2025 - Dec 2027: https://www.mytnb.com.my/tariff and the official PDF schedule; MD definition page
   https://www.tnb.com.my/commercial-industrial/maximum-demand/how-do-you-calculate-md-charge), TAR02_VN_actual.yaml (EVN currently
   applicable industrial TOU tariff for the relevant voltage class, official EVN/MOIT decision), TAR02_VN_trial.yaml (EVN two-component
   paper trial from Oct 2025, clearly status TRIAL_NOT_PAYABLE), TAR03_SG.yaml (SP Group tariff/UOS + contracted capacity rules).
   Every numeric field: value, unit, currency, source_url, source_page/section, access_date, status in {VERIFIED, NOT_VERIFIED}.
   Reference values in the user plan (e.g. RM 0.2983/kWh, RM 29.43 + 59.84/kW/month, RM 200/month) must be CHECKED against the
   official document; if you cannot open the document, keep the value with status NOT_VERIFIED and say why. Never invent values.
   Record: billing interval (e.g. 30-min MD), aligned vs sliding interval (NOT_VERIFIED if not documented), TOU windows, peak-period
   eligibility for MD, taxes/adjustments (e.g. AFA/ICPT surcharges if applicable), export rules, penalties (connected-load charge).
2. billing.py: `monthly_bill(power_kw, timestamps, tariff) -> dict` for a 1-min (or any regular) import-power series of ONE meter:
   energy charge (TOU-aware), demand terms from the max average over the tariff's billing interval (aligned intervals by default,
   option sliding), only in eligible periods if the tariff says so, fixed/retail fees, contracted-capacity handling for SG
   (excess-capacity charge only above contract; contract is an input, never auto-downsized), export credit per tariff rule
   (default 0 unless documented). Per-component breakdown + billed demand kW + its timestamp. Months split by calendar month in the
   tariff's local time; the caller passes timestamps already mapped (do not shift time zones yourself).
3. Tests (hand-computed): flat load bill; a 1-min spike shorter than the interval raises MD by spike/interval-length only; TOU split;
   SG excess capacity; NOT_VERIFIED fields propagate a flag into the result.
4. Report: table per tariff with every field, status and source; what is still NOT_VERIFIED; that VN-TRIAL is not payable;
   that these are geographical counterfactuals for DS07 Korean factories, not their actual tariffs.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_bill tests/test_billing.py` passes; all 5 YAML load.

## Run 2 (lead) — evidence standard
VERIFIED requires: a saved copy of the official document in data/tariffs/sources/ (sha256 in data/tariffs/sources/README.md), the exact quoted text line(s) and the page/table number in the YAML field (quote:, page:). If you cannot download/open the document, the field is NOT_VERIFIED regardless of the reference value in the plan. Re-check every currently VERIFIED field against this standard. Then resolve: Malaysia MD definition (30-min interval, aligned or sliding, peak-period eligibility for MV TOU), MV TOU energy windows, ICPT/AFA surcharges, connected-load charge rule, Vietnam actual tariff (official decision number + rates), Singapore UOS/contracted capacity current schedule. Finish with the gate.

## Run 3 (lead) — facts read by the lead from https://www.mytnb.com.my/tariff (HTTP 200, 2026-11-25; the RP4 PDF URL returns 404, tnb.com.my MD page returns 403 to automated clients)
- ToU hours: "On Monday to Friday / Peak : 2 PM to 10 PM / Off-Peak : 10 PM to 2 PM"; "On Saturday and Sunday / Off-Peak throughout the day (24 hours)".
- "for Non-Domestic Medium Voltage and High Voltage customers, Maximum Demand which occurs during Off-Peak period will not be charged."
- Mapping: old C1/E1/F1 -> "Non-Domestic Medium Voltage General Tariff"; old C2/E2/F2 -> "Non-Domestic Medium Voltage ToU Tariff".
- "In RP4, the ICPT mechanism has been replaced by the Fuel Adjustment", "updated monthly" (rate via singlebuyer.com.my, not read).
Record these as VERIFIED (source = that page, quote as above). Rates (energy/capacity/network/retail) stay NOT_VERIFIED unless you obtain the official schedule from another official TNB/Suruhanjaya Tenaga URL (try https://www.st.gov.my and other mytnb.com.my paths). MD interval length stays NOT_VERIFIED unless quoted from an official page. Update billing.py so MD for TNB MV tariffs is computed over the peak window only (Mon-Fri 14:00-22:00). Finish with the gate.
