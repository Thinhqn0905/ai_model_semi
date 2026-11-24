# DS04 machine and external forecasting audit

Evidence boundary: MEASURED source observations; DERIVED summaries and split. These are manufacturing machines, not semiconductor test cells.

Split: Per company and asset, sort distinct timestamps chronologically; first 70% train, next 15% val, remainder test. All rows at a timestamp share a split.
Company A status codes 0/1/2/3 map to idle/manual/auto/alarm. Company B Alarm/Standby/Production/Loading/Tooling map to their lowercase names; MachineOn is approximated as idle, not a measured idle label. Original codes are retained in status_raw.
Company B does not provide items or cycle time; these remain null. Company A cycle_time is total time for items in a time span, not remaining time.

## Company A
Assets: 0, 1, 2, 3, 4, 5, 6, 7, 8; rows: 1520330; span: 2021-03-30 10:39:11+00:00 to 2022-10-27 12:55:00+00:00.
Positive sampling intervals (seconds): {300.0: 1318456, 5.0: 17995, 1.0: 10376, 11.0: 4940, 6.0: 4808}; missing timestamp values: 0; duplicate asset/timestamps: 0. Gaps may indicate missing observations; without a fixed cadence their count cannot be inferred reliably.
Status counts: {'manual': 708998, 'auto': 696999, 'alarm': 114333}.
Power range kW by status: {'alarm': {'min': 0.0, 'max': 6789633.0}, 'auto': {'min': 0.0, 'max': 644.0}, 'manual': {'min': 0.0, 'max': 16777216.0}}.
power_avg integer-quantised: True; missing power values: 0.

## Company B
Assets: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17; rows: 1568736; span: 2021-11-16 15:47:00+00:00 to 2022-11-16 15:46:00+00:00.
Positive sampling intervals (seconds): {60.0: 1559287, 120.0: 4941, 180.0: 938, 300.0: 165, 240.0: 158}; missing timestamp values: 0; duplicate asset/timestamps: 0. Gaps may indicate missing observations; without a fixed cadence their count cannot be inferred reliably.
Status counts: {'production': 649903, 'standby': 619342, 'idle': 182708, 'alarm': 50467, 'loading': 50142, 'tooling': 16174}.
Power range kW by status: {'alarm': {'min': 0.0452308, 'max': 857.725}, 'idle': {'min': 0.100762, 'max': 866.874}, 'loading': {'min': 0.113077, 'max': 694.584}, 'production': {'min': 0.089566, 'max': 31241.6}, 'standby': {'min': 0.0167936, 'max': 358.613}, 'tooling': {'min': 0.814155, 'max': 185.0657475}}.
power_avg integer-quantised: False; missing power values: 0.

## Forecasting suitability
Next-slot power and state transitions are feasible within each asset, subject to gaps, duplicate times, chronological evaluation and differing sampling intervals. Remaining cycle time is not directly labelled; Company A's total cycle time does not identify elapsed/remaining cycle time and Company B lacks cycle time. These records cannot establish semiconductor test-cell performance or regenerative power behaviour.

## External benchmarks (UCI archives; no parquet produced)
Appliances energy prediction: 19735 rows, 2016-01-11 17:00:00 to 2016-05-27 18:00:00, interval counts in seconds {600.0: 19734}; columns: date, Appliances, lights, T1, RH_1, T2, RH_2, T3, RH_3, T4, RH_4, T5, RH_5, T6, RH_6, T7, RH_7, T8, RH_8, T9, RH_9, T_out, Press_mm_hg, RH_out, Windspeed, Visibility, Tdewpoint, rv1, rv2. Household appliance load and weather/humidity variables support an external next-slot forecast benchmark, not industrial transfer validation; timestamps are timezone-unspecified.
ElectricityLoadDiagrams: 140256 rows, 2011-01-01 00:15:00 to 2015-01-01 00:00:00, interval counts in seconds {900.0: 140255}; columns: timestamp plus 370 customer series (MT_001 through MT_370). Customer electricity demand supports an external load forecasting benchmark, not machine-state or test-cell validation; timestamps are timezone-unspecified and early zeros may reflect unavailable series.
