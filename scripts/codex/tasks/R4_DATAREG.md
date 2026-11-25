# R4_DATAREG — Run 4 dataset registry, reusable downloader, DS07 processing module (D013; G01; mentor M07, M08)
Account: .codex-B. Effort: medium.
Owner files: data/manifests/dataset_registry.json, scripts/download_public_data.py, src/regenate/data/ds07.py, tests/test_ds07.py,
  tests/test_download.py, reports/run4/ds07_quality.md (method part; the lead fills numbers from Colab), reports/run4/dataset_registry.md
Read: AGENTS.md, reports/data/ds0{1,2,3,4}_report.md, src/regenate/data/ds05.py (pattern), reports/ai/branch_C_ds05.md.
Facts measured by the lead on Colab (use them, do not re-download DS05 or DS07 locally; the user machine is weak):
  DS07 figshare article 14822256 v9, DOI 10.6084/m9.figshare.14822256.v9, CC BY 4.0, files Data_list.zip (10,861,504 B,
  md5 cc3911b3f9e1125468e864a24540cfe0, sha256 f8794dc10e8892ead63f431eb55c6a4d6c6411c09a3d58aa29a07c54a14b57fc) and Code_list.zip
  (6,035 B, md5 398ed0baae9c9a33466e811860f4c3b3; R scripts, never executed). Data_list/Factories/{Cement_1, Cement_2, Forge_1,
  Forge_2, Metal_1, Metal_2, Metal_3, Paper, Steel_1, Steel_2}.csv with columns Time ('2019-03-01 0:00'), 'Power consumption' (kW),
  1-min, 2019-03-01..2019-09-30, rows 276,938-308,160 (gaps are MISSING ROWS, not NaN), min 0 kW; plus
  System_demand/System load(Korea, 2019.03~06.).csv and DR_information/Industy DR Information.xlsx.
  DS05: figshare 28732490 v2 (doi 10.17028/rd.lboro.28732490.v2), local D:/.../DS5.zip 9,066,300,821 B (hash it locally once:
  sha256 streaming, 8 MB chunks, single process), processed 14,755 valid cycles / 2 errors.
Contract:
1. download_public_data.py: resolve figshare articles via https://api.figshare.com/v2/articles/{id}/versions/{v}; streaming download
   with HTTP Range resume, retries/timeout, size + md5 (figshare computed_md5) + sha256 check, disk-space check, skip verified files,
   safe zip extraction (reject absolute paths and '..'), write a per-dataset download manifest; never substitute another version.
   Tests with a mocked HTTP layer (no network in tests).
2. dataset_registry.json: DS01-DS08 entries (id, title, DOI, repository, version, license, URLs, files+sizes+hashes, measurement
   boundary, sampling, units, provenance, role, limitations). DS08 (EWELD, figshare 21893808 v3) metadata only via the API if
   reachable from this machine (small JSON request), no data download. Unknown fields = null with a note; never invent.
3. ds07.py: `load_factory(zip_path, name)` and `build(zip_path, out_dir)` -> facility_load.parquet with schema facility_id,
   timestamp (naive local KST as in the file; record tz as Asia/Seoul in metadata), power_kw, sample_interval_seconds=60,
   data_quality_flag ('ok', 'zero', 'outlier' via a documented robust rule, e.g. > Q3 + 10 IQR, flagged not removed),
   original_timestamp, source_file; plus a gap table (start, end, minutes) and per-month summary: energy kWh, coverage %,
   max 15/30/60-min aligned average demand and timestamps, load factor, weekday/weekend means. No interpolation of gaps (gaps stay
   missing; a separate function may fill gaps <= 5 min by linear interpolation as an explicit, flagged option).
   Tests on synthetic data: gap detection, aligned 30-min max, coverage, outlier flag.
4. reports/run4/dataset_registry.md: human-readable registry table; reports/run4/ds07_quality.md: method only + placeholders the
   lead fills (mark PENDING_COLAB).
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_ds07 tests/test_ds07.py tests/test_download.py` passes;
registry JSON loads with 8 entries.
