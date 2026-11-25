# DS07 quality method

Boundary: SOURCE_REPORTED DS07 / DERIVED processing; not ReGenATE performance. Timestamps are naive local Asia/Seoul. Read factory CSVs directly from the archive; retain original timestamps and source paths. Flag zero and values above Q3 + 10 IQR per factory, retaining all observations. Detect missing minute rows; do not interpolate. Monthly coverage is observed minutes divided by calendar minutes; energy sums observed kW divided by 60, excluding gaps. Demand maxima use complete, clock-aligned 15/30/60-minute windows. Load factor is observed mean divided by observed maximum; weekday/weekend means use observed minutes. Partial months and missing rows lower coverage and can bias energy and demand.

PENDING_COLAB: per-factory quality, gaps, coverage, monthly energy and demand summaries.
