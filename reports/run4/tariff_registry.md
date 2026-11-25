# Tariff registry

Boundary: SOURCE_REPORTED where VERIFIED; remaining fields NOT_VERIFIED. These are geographical counterfactuals for DS07 Korean factories, not their actual tariffs. Partial estimates exclude unspecified components and must not be treated as payable bills. VN trial is TRIAL_NOT_PAYABLE. All dates are access dates.

## TAR01_MY_TNB_RP4_MV_general

| Field | Value | Unit | Currency | Status | Source / section | Access |
|---|---:|---|---|---|---|---|
| billing_interval_minutes | 30 | min | None | NOT_VERIFIED | [metering interval](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| energy_rates.normal | 0.2983 | MYR/kWh | MYR | VERIFIED | [Medium Voltage General energy](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| demand_rates.capacity | 29.43 | MYR/kW/month | MYR | VERIFIED | [Medium Voltage General capacity](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| demand_rates.network | 59.84 | MYR/kW/month | MYR | VERIFIED | [Medium Voltage General network](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| fixed_fees.retail | 200 | MYR/month | MYR | VERIFIED | [Medium Voltage General retail](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| export_rate | None | currency/kWh | None | NOT_VERIFIED | [export rule not established](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| adjustments | None | description | None | NOT_VERIFIED | [taxes and adjustments not established](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| penalty | None | description | None | NOT_VERIFIED | [penalties not established](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |

Non-numeric settings: {'interval_mode': 'aligned', 'windows': []}.

## TAR01_MY_TNB_RP4_MV_TOU

| Field | Value | Unit | Currency | Status | Source / section | Access |
|---|---:|---|---|---|---|---|
| billing_interval_minutes | 30 | min | None | NOT_VERIFIED | [metering interval](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| energy_rates.peak | 0.3132 | MYR/kWh | MYR | VERIFIED | [Medium Voltage ToU peak](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| energy_rates.offpeak | 0.2723 | MYR/kWh | MYR | VERIFIED | [Medium Voltage ToU offpeak](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| demand_rates.capacity | 30.19 | MYR/kW/month | MYR | VERIFIED | [Medium Voltage ToU peak capacity](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| demand_rates.network | 66.87 | MYR/kW/month | MYR | VERIFIED | [Medium Voltage ToU peak network](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| fixed_fees.retail | 200 | MYR/month | MYR | VERIFIED | [Medium Voltage ToU retail](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| export_rate | None | currency/kWh | None | NOT_VERIFIED | [export rule not established](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| adjustments | None | description | None | NOT_VERIFIED | [taxes and adjustments not established](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| penalty | None | description | None | NOT_VERIFIED | [penalties not established](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |
| tou_windows_status | None | description | None | NOT_VERIFIED | [TOU windows not established](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) | 2026-11-25 |

Non-numeric settings: {'interval_mode': 'aligned', 'windows': [], 'demand_eligible_periods': ['peak']}.

## TAR02_VN_actual

| Field | Value | Unit | Currency | Status | Source / section | Access |
|---|---:|---|---|---|---|---|
| billing_interval_minutes | None | min | None | NOT_VERIFIED | [no demand charge established](https://evn.com.vn/userfile/User/tcdl/files/2026/11/1_QD-BCT_2026_2892-20261104131123509.pdf) | 2026-11-25 |
| energy_rates.normal | 1814 | VND/kWh | VND | VERIFIED | [Appendix 1.2 medium voltage](https://evn.com.vn/userfile/User/tcdl/files/2026/11/1_QD-BCT_2026_2892-20261104131123509.pdf) | 2026-11-25 |
| energy_rates.offpeak | 1166 | VND/kWh | VND | VERIFIED | [Appendix 1.2 medium voltage](https://evn.com.vn/userfile/User/tcdl/files/2026/11/1_QD-BCT_2026_2892-20261104131123509.pdf) | 2026-11-25 |
| energy_rates.peak | 3348 | VND/kWh | VND | VERIFIED | [Appendix 1.2 medium voltage](https://evn.com.vn/userfile/User/tcdl/files/2026/11/1_QD-BCT_2026_2892-20261104131123509.pdf) | 2026-11-25 |
| export_rate | None | currency/kWh | None | NOT_VERIFIED | [export rule not established](https://evn.com.vn/userfile/User/tcdl/files/2026/11/1_QD-BCT_2026_2892-20261104131123509.pdf) | 2026-11-25 |
| adjustments | None | description | None | NOT_VERIFIED | [taxes and adjustments not established](https://evn.com.vn/userfile/User/tcdl/files/2026/11/1_QD-BCT_2026_2892-20261104131123509.pdf) | 2026-11-25 |
| penalty | None | description | None | NOT_VERIFIED | [penalties not established](https://evn.com.vn/userfile/User/tcdl/files/2026/11/1_QD-BCT_2026_2892-20261104131123509.pdf) | 2026-11-25 |

Non-numeric settings: {'interval_mode': 'aligned', 'windows': [{'days': [0, 1, 2, 3, 4, 5, 6], 'start': '00:00', 'end': '06:00', 'period': 'offpeak'}, {'days': [0, 1, 2, 3, 4, 5], 'start': '17:30', 'end': '22:30', 'period': 'peak'}], 'tou_windows_source': 'https://www.evn.com.vn/d/vi-VN/news/Quyet-dinh-so-963QD-BCT-ve-khung-gio-cao-diem-thap-diem-va-gio-binh-thuong-cua-he-thong-dien-quoc-gia--60-134-507803'}.

## TAR02_VN_trial

| Field | Value | Unit | Currency | Status | Source / section | Access |
|---|---:|---|---|---|---|---|
| billing_interval_minutes | 30 | min | None | NOT_VERIFIED | [metering interval](https://www.evn.com.vn/d/vi-VN/news/Trien-khai-thu-nghiem-gia-ban-le-dien-hai-thanh-phan-tu-thang-102025-60-142-505112) | 2026-11-25 |
| export_rate | None | currency/kWh | None | NOT_VERIFIED | [export rule not established](https://www.evn.com.vn/d/vi-VN/news/Trien-khai-thu-nghiem-gia-ban-le-dien-hai-thanh-phan-tu-thang-102025-60-142-505112) | 2026-11-25 |
| adjustments | None | description | None | NOT_VERIFIED | [taxes and adjustments not established](https://www.evn.com.vn/d/vi-VN/news/Trien-khai-thu-nghiem-gia-ban-le-dien-hai-thanh-phan-tu-thang-102025-60-142-505112) | 2026-11-25 |
| penalty | None | description | None | NOT_VERIFIED | [penalties not established](https://www.evn.com.vn/d/vi-VN/news/Trien-khai-thu-nghiem-gia-ban-le-dien-hai-thanh-phan-tu-thang-102025-60-142-505112) | 2026-11-25 |
| trial_rate | None | VND/kW/month | VND | NOT_VERIFIED | [paper trial rates not specified](https://www.evn.com.vn/d/vi-VN/news/Trien-khai-thu-nghiem-gia-ban-le-dien-hai-thanh-phan-tu-thang-102025-60-142-505112) | 2026-11-25 |

Non-numeric settings: {'interval_mode': 'aligned', 'windows': [], 'tariff_status': 'TRIAL_NOT_PAYABLE'}.

## TAR03_SG

| Field | Value | Unit | Currency | Status | Source / section | Access |
|---|---:|---|---|---|---|---|
| billing_interval_minutes | 30 | min | None | NOT_VERIFIED | [metering interval](https://www.spgroup.com.sg/search?q=Transformer+efficiency+99.1%25+as+per+IS+2026+standard) | 2026-11-25 |
| energy_rates.normal | None | SGD/kWh | SGD | NOT_VERIFIED | [energy supply and TOU rates not established](https://www.spgroup.com.sg/search?q=Transformer+efficiency+99.1%25+as+per+IS+2026+standard) | 2026-11-25 |
| export_rate | None | currency/kWh | None | NOT_VERIFIED | [export rule not established](https://www.spgroup.com.sg/search?q=Transformer+efficiency+99.1%25+as+per+IS+2026+standard) | 2026-11-25 |
| adjustments | None | description | None | NOT_VERIFIED | [taxes and adjustments not established](https://www.spgroup.com.sg/search?q=Transformer+efficiency+99.1%25+as+per+IS+2026+standard) | 2026-11-25 |
| penalty | None | description | None | NOT_VERIFIED | [penalties not established](https://www.spgroup.com.sg/search?q=Transformer+efficiency+99.1%25+as+per+IS+2026+standard) | 2026-11-25 |
| contract_rate | 15.07 | SGD/kW/month | SGD | NOT_VERIFIED | [Table 9 HT large April 2026](https://www.spgroup.com.sg/search?q=Transformer+efficiency+99.1%25+as+per+IS+2026+standard) | 2026-11-25 |
| excess_rate | 22.61 | SGD/kW/month | SGD | NOT_VERIFIED | [Table 9 HT large uncontracted April 2026](https://www.spgroup.com.sg/search?q=Transformer+efficiency+99.1%25+as+per+IS+2026+standard) | 2026-11-25 |

Non-numeric settings: {'interval_mode': 'aligned', 'windows': [], 'contract_rule': 'Contract capacity is customer input; never automatically resized.'}.

Malaysia ToU windows, alignment, taxes, export and penalties remain unverified. Vietnam taxes, export and trial rates remain unverified. Singapore rates are provisional because the July schedule and charging details were not independently inspected; supply tariff, windows, export and penalties remain unverified. Null values are missing, not confirmed zero. Verify applicability and all missing terms before any real bill.
