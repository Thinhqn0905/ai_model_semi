# R4_HOLIDAY — Run 4 public-holiday treatment in the billing engine (D017.3)
Account: .codex-C. Effort: low.
Owner files: src/regenate/economics/billing.py, tests/test_billing.py
Read: AGENTS.md, data/tariffs/TAR01_MY_TNB_RP4_MV_TOU.yaml (holidays field NOT_VERIFIED), src/regenate/economics/billing.py.
Contract: monthly_bill accepts an optional `holidays` iterable of dates (or tariff['holiday_dates']); on those dates every minute is
'offpeak' when the tariff has windows (so it is energy off-peak and excluded from ToU MD). Default None = current behaviour. Add a
helper `my_public_holidays(year)` that uses the `holidays` package if installed (country 'MY', subdiv None) and raises a clear error
otherwise; do not hardcode dates. Tests: a holiday weekday peak spike is excluded from ToU MD but included in General MD; default unchanged.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_hol tests/test_billing.py`.
