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
