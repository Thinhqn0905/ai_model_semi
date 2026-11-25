# DS08 EWELD metadata audit

Boundary: **SOURCE_REPORTED**; this is a metadata and publication audit, not a local measurement or ReGenATE result. The unmodified API response is [ds08_metadata.json](../../data/manifests/ds08_metadata.json), retrieved from the [versioned Figshare API](https://api.figshare.com/v2/articles/21893808/versions/3). No dataset archive was downloaded.

## Figshare metadata

The saved JSON lists the following entire downloadable file, and no individual customer files. MB below means decimal megabytes, calculated from the JSON byte count. The MD5 is source-reported, not independently verified against downloaded data.

| File | Bytes | MB | Supplied / computed MD5 |
|---|---:|---:|---|
| EWELD.zip | 258090540 | 258.09054 | eea1455aff6518aae1fbfc397b178111 |

License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Dataset DOI: https://doi.org/10.6084/m9.figshare.21893808.v3. The API description identifies the associated industrial and commercial load paper but does not provide sampling, dates, customer categories, inner filenames, units, or coverage.

## Paper description

Boundary: **SOURCE_REPORTED** separately from the API: [Liu et al., Scientific Data, DOI 10.1038/s41597-023-02503-6](https://www.nature.com/articles/s41597-023-02503-6), especially tables 1, 2, 4 and 5 and Data integrity. The paper describes anonymized South China industrial and commercial customers, including manufacturing (section C) and services, not residential customers. It reports 386 customer CSVs, U1 through U386, organized by industry section and division; measurements are interval energy in kWh at 15-minute resolution. The overall electricity date range is June 2016 through August 2022, with customer-specific periods and gaps; it does not imply complete coverage for every customer. The CSV columns are `Time` and `Value`. The paper identifies manufacturing examples U57, U106, U108, U157 and U243, but their published ranges do not establish complete calendar months.

## Smallest subset plan and limits

**NOT_VERIFIED:** A qualifying minimum subset of at least 10 manufacturing customers with at least 6 complete calendar months each cannot be named or sized from the saved metadata or paper. The only source-listed downloadable candidate is `EWELD.zip`, total 258.09054 MB; it exceeds the 5 MB download limit and is not a verified qualifying subset. The five paper-named manufacturing examples above are candidates for screening, not a sufficient or verified selection. The internal file sizes, exact archive paths, customer-to-file mapping beyond paper examples, per-month completeness, timestamp convention and timezone remain unknown. No representative sample or complete-month guarantee is established.

If a compliant individually accessible source or a separately authorized transfer becomes available, inspect the archive index and customer classification; select manufacturing CSVs, validate every expected quarter-hour and duplicate timestamp in each calendar month, and stop after finding the minimum qualifying set. Record exact selected filenames and transfer sizes before downloading. Do not fill missing measurements to claim completeness.

## Facility adapter requirements

`src/regenate/evaluation/facility.py` currently reads `Data_list/Factories/{name}.csv` from a DS07 ZIP: first column timestamp parsed as `%Y-%m-%d %H:%M`, second column numeric kW; it returns a one-minute series with missing minutes as NaN. An EWELD adapter would select a verified customer CSV and parse its `Time` and `Value` columns, confirm timezone and whether timestamps mark interval start or end, convert each 15-minute kWh value to mean kW by dividing by 0.25 hours, and map that mean to its 15 constituent minutes on the correctly aligned grid. Missing quarter-hours must remain missing for all constituent minutes, with duplicates and invalid values explicitly checked. Preserve the existing aligned demand-window coverage logic; document that the resulting minute values are interval averages, not measured minute fluctuations. The existing loader cannot consume the EWELD ZIP layout or kWh values directly.

## Local gate output

SOURCE_REPORTED: metadata consistency check passed; saved API response and audit exist. This checks metadata transcription only, not archive contents or customer completeness.
