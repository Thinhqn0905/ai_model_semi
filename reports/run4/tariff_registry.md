# Tariff registry

Boundary: SOURCE_REPORTED; geographical counterfactuals for DS07 Korean factories, not their actual tariffs. VN trial is TRIAL_NOT_PAYABLE. The engine excludes taxes, adjustments, reactive power, connected-load and standby penalties; incomplete inputs make totals unsuitable as payable bills. Null is missing, never verified zero.

Malaysia schedule direct download returned HTTP 404; its fields remain NOT_VERIFIED. Malaysia TOU demand values previously in the registry were removed pending inspection of the original schedule. SG UOS excludes supply energy and GST; HT Large applicability depends on contract capacity. Vietnam actual is Decision 2892/QD-BCT and voltage above 1 kV to 35 kV.

## TAR01_MY_TNB_RP4_MV_general

| Field | Value | Unit | Currency | Status | Source and section |
|---|---|---|---|---|---|
| billing_interval_minutes | 30 | min | None | NOT_VERIFIED | [metering interval](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |
| energy_rates.normal | 0.2983 | MYR/kWh | MYR | NOT_VERIFIED | [Medium Voltage General energy](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |
| demand_rates.capacity | 29.43 | MYR/kW/month | MYR | NOT_VERIFIED | [Medium Voltage General capacity](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |
| demand_rates.network | 59.84 | MYR/kW/month | MYR | NOT_VERIFIED | [Medium Voltage General network](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |
| fixed_fees.retail | 200 | MYR/month | MYR | NOT_VERIFIED | [Medium Voltage General retail](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |
| export_rate | None | currency/kWh | None | NOT_VERIFIED | [export rule not established](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |
| adjustments | None | description | None | NOT_VERIFIED | [taxes and adjustments not established](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |
| penalty | None | description | None | NOT_VERIFIED | [section 4.2: 8.50 MYR/kW shortfall; reference depends on customer history; excluded from bill](https://www.tnb.com.my/assets/files/TNB_Connection_Charges_Book_2025_ENG.pdf) |

Other configuration: `{'interval_mode': 'aligned', 'windows': []}`.

## TAR01_MY_TNB_RP4_MV_TOU

| Field | Value | Unit | Currency | Status | Source and section |
|---|---|---|---|---|---|
| billing_interval_minutes | 30 | min | None | NOT_VERIFIED | [metering interval](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |
| energy_rates.peak | 0.3132 | MYR/kWh | MYR | NOT_VERIFIED | [Medium Voltage ToU peak](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |
| energy_rates.offpeak | 0.2723 | MYR/kWh | MYR | NOT_VERIFIED | [Medium Voltage ToU offpeak](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |
| demand_rates.capacity | None | MYR/kW/month | MYR | NOT_VERIFIED | [MV TOU rate requires review of original PDF; previous number removed](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |
| demand_rates.network | None | MYR/kW/month | MYR | NOT_VERIFIED | [MV TOU rate requires review of original PDF; previous number removed](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |
| fixed_fees.retail | 200 | MYR/month | MYR | NOT_VERIFIED | [Medium Voltage ToU retail](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |
| export_rate | None | currency/kWh | None | NOT_VERIFIED | [export rule not established](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |
| adjustments | None | description | None | NOT_VERIFIED | [taxes and adjustments not established](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |
| penalty | None | description | None | NOT_VERIFIED | [section 4.2: 8.50 MYR/kW shortfall; reference depends on customer history; excluded from bill](https://www.tnb.com.my/assets/files/TNB_Connection_Charges_Book_2025_ENG.pdf) |
| tou_windows_status | None | description | None | NOT_VERIFIED | [TOU windows not established](https://www.mytnb.com.my/tariff/PDF/Jadual%20Tarif%20Elektrik%20Semenanjung%20Jul%202025%20-%20Dis%202027.pdf) |

Other configuration: `{'interval_mode': 'aligned', 'windows': [], 'demand_eligible_periods': ['peak']}`.

## TAR02_VN_actual

| Field | Value | Unit | Currency | Status | Source and section |
|---|---|---|---|---|---|
| billing_interval_minutes | None | min | None | NOT_VERIFIED | [no demand charge established](https://evn.com.vn/userfile/User/tcdl/files/2026/11/1_QD-BCT_2026_2892-20261104131123509.pdf) |
| energy_rates.normal | 1814 | VND/kWh | VND | NOT_VERIFIED | [Appendix 1.2, above 1 kV to 35 kV; exact PDF page not independently confirmed](https://evn.com.vn/userfile/User/tcdl/files/2026/11/1_QD-BCT_2026_2892-20261104131123509.pdf) |
| energy_rates.offpeak | 1166 | VND/kWh | VND | NOT_VERIFIED | [Appendix 1.2, above 1 kV to 35 kV; exact PDF page not independently confirmed](https://evn.com.vn/userfile/User/tcdl/files/2026/11/1_QD-BCT_2026_2892-20261104131123509.pdf) |
| energy_rates.peak | 3348 | VND/kWh | VND | NOT_VERIFIED | [Appendix 1.2, above 1 kV to 35 kV; exact PDF page not independently confirmed](https://evn.com.vn/userfile/User/tcdl/files/2026/11/1_QD-BCT_2026_2892-20261104131123509.pdf) |
| export_rate | None | currency/kWh | None | NOT_VERIFIED | [export rule not established](https://evn.com.vn/userfile/User/tcdl/files/2026/11/1_QD-BCT_2026_2892-20261104131123509.pdf) |
| adjustments | None | description | None | NOT_VERIFIED | [taxes and adjustments not established](https://evn.com.vn/userfile/User/tcdl/files/2026/11/1_QD-BCT_2026_2892-20261104131123509.pdf) |
| penalty | None | description | None | NOT_VERIFIED | [penalties not established](https://evn.com.vn/userfile/User/tcdl/files/2026/11/1_QD-BCT_2026_2892-20261104131123509.pdf) |

Other configuration: `{'interval_mode': 'aligned', 'windows': [{'days': [0, 1, 2, 3, 4, 5, 6], 'start': '00:00', 'end': '06:00', 'period': 'offpeak'}, {'days': [0, 1, 2, 3, 4, 5], 'start': '17:30', 'end': '22:30', 'period': 'peak'}], 'voltage_class': 'above 1 kV to 35 kV; Decision 2892/QD-BCT, 31 October 2026'}`.

## TAR02_VN_trial

| Field | Value | Unit | Currency | Status | Source and section |
|---|---|---|---|---|---|
| billing_interval_minutes | 30 | min | None | NOT_VERIFIED | [metering interval](https://www.evn.com.vn/d/vi-VN/news/Trien-khai-thu-nghiem-gia-ban-le-dien-hai-thanh-phan-tu-thang-102025-60-142-505112) |
| export_rate | None | currency/kWh | None | NOT_VERIFIED | [export rule not established](https://www.evn.com.vn/d/vi-VN/news/Trien-khai-thu-nghiem-gia-ban-le-dien-hai-thanh-phan-tu-thang-102025-60-142-505112) |
| adjustments | None | description | None | NOT_VERIFIED | [taxes and adjustments not established](https://www.evn.com.vn/d/vi-VN/news/Trien-khai-thu-nghiem-gia-ban-le-dien-hai-thanh-phan-tu-thang-102025-60-142-505112) |
| penalty | None | description | None | NOT_VERIFIED | [penalties not established](https://www.evn.com.vn/d/vi-VN/news/Trien-khai-thu-nghiem-gia-ban-le-dien-hai-thanh-phan-tu-thang-102025-60-142-505112) |
| trial_rate | None | VND/kW/month | VND | NOT_VERIFIED | [paper trial rates not specified](https://www.evn.com.vn/d/vi-VN/news/Trien-khai-thu-nghiem-gia-ban-le-dien-hai-thanh-phan-tu-thang-102025-60-142-505112) |

Other configuration: `{'interval_mode': 'aligned', 'windows': [], 'tariff_status': 'TRIAL_NOT_PAYABLE'}`.

## TAR03_SG

| Field | Value | Unit | Currency | Status | Source and section |
|---|---|---|---|---|---|
| billing_interval_minutes | 30 | min | None | NOT_VERIFIED | [metering interval](https://www.spgroup.com.sg/search?q=Transformer+efficiency+99.1%25+as+per+IS+2026+standard) |
| energy_rates.normal | None | SGD/kWh | SGD | NOT_VERIFIED | [energy supply and TOU rates not established](https://www.spgroup.com.sg/search?q=Transformer+efficiency+99.1%25+as+per+IS+2026+standard) |
| export_rate | None | currency/kWh | None | NOT_VERIFIED | [export rule not established](https://www.spgroup.com.sg/search?q=Transformer+efficiency+99.1%25+as+per+IS+2026+standard) |
| adjustments | None | description | None | NOT_VERIFIED | [taxes and adjustments not established](https://www.spgroup.com.sg/search?q=Transformer+efficiency+99.1%25+as+per+IS+2026+standard) |
| penalty | None | description | None | NOT_VERIFIED | [penalties not established](https://www.spgroup.com.sg/search?q=Transformer+efficiency+99.1%25+as+per+IS+2026+standard) |
| contract_rate | 14.21 | SGD/kW/month | SGD | VERIFIED | [Table 9, HT Large, exclusive of GST](https://www.spgroup.com.sg/dam/jcr:ed6d35eb-7bb5-450c-8386-b61f0cc13142/Transmission%20Service%20Rate%20Schedule%20(effective%20from%201%20Jul%202026).pdf) |
| excess_rate | 21.32 | SGD/kW/month | SGD | VERIFIED | [Table 9, HT Large, exclusive of GST](https://www.spgroup.com.sg/dam/jcr:ed6d35eb-7bb5-450c-8386-b61f0cc13142/Transmission%20Service%20Rate%20Schedule%20(effective%20from%201%20Jul%202026).pdf) |

Other configuration: `{'interval_mode': 'aligned', 'windows': [], 'contract_rule': 'HT Large: contract is input; UCC applies to excess for normal consumers without embedded generation. Other schemes require additional rules.'}`.

Vietnam rates were found in the official decision, but remain NOT_VERIFIED until the exact page and quotation are checked against the saved PDF. Malaysia TOU windows, MD alignment, AFA, and connected-load applicability remain unresolved. Singapore supply energy, reactive, standby and export remain unverified or unimplemented.
