"""Build the DS04 machine dataset and its source audit."""
from pathlib import Path
from zipfile import ZipFile
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data/processed"
REPORT = ROOT / "reports/data/ds04_report.md"
RULE = "Per company and asset, sort distinct timestamps chronologically; first 70% train, next 15% val, remainder test. All rows at a timestamp share a split."


def build():
    a = pd.read_csv(ROOT / "DS04_SME/company_A.csv", usecols=["ts", "asset", "status", "power_avg", "items", "cycle_time"])
    with ZipFile(ROOT / "DS04_SME/company_B.zip") as archive:
        with archive.open("company_B.csv") as f:
            b = pd.read_csv(f, usecols=["ts", "asset", "status", "power_avg"])
    frames = []
    for company, frame, mapping in [("A", a, {"0": "idle", "1": "manual", "2": "auto", "3": "alarm"}),
                                    ("B", b, {"Alarm": "alarm", "Standby": "standby", "MachineOn": "idle", "Production": "production", "Loading": "loading", "Tooling": "tooling"})]:
        frame["company"] = company
        frame["ts"] = pd.to_datetime(frame["ts"], utc=True, errors="raise")
        frame["status_raw"] = frame["status"].astype(str).str.replace(r"\.0$", "", regex=True)
        frame["status"] = frame["status_raw"].map(mapping)
        if frame["status"].isna().any() or frame["ts"].isna().any() or frame["asset"].isna().any():
            raise ValueError("Unknown status or missing asset/timestamp")
        frames.append(frame.rename(columns={"power_avg": "power_kw", "cycle_time": "cycle_time_s"}))
    d = pd.concat(frames, ignore_index=True).sort_values(["company", "asset", "ts"], kind="stable")
    timestamps = d[["company", "asset", "ts"]].drop_duplicates().copy()
    g = timestamps.groupby(["company", "asset"], sort=False)["ts"]
    rank = g.cumcount()
    count = g.transform("size")
    if (count < 3).any():
        raise ValueError("Each asset needs at least three distinct timestamps")
    timestamps["split"] = np.where(rank < (count * .70).astype(int), "train", np.where(rank < (count * .85).astype(int), "val", "test"))
    d = d.merge(timestamps, on=["company", "asset", "ts"], validate="many_to_one")
    d = d[["company", "asset", "ts", "status", "status_raw", "power_kw", "items", "cycle_time_s", "split"]]
    OUT.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    d.to_parquet(OUT / "ds04_machines.parquet", index=False)
    provenance = {"label": "MEASURED", "sources": ["DS04_SME/company_A.csv", "DS04_SME/company_B.zip:company_B.csv"], "url": "https://www.mdpi.com/1424-8220/23/13/6078", "license": "Research and educational use per DS04_SME/README.md; verify source terms before reuse", "units": {"power_kw": "kW (source-described)", "cycle_time_s": "s", "ts": "UTC"}, "transforms": "UTC timestamps; status mapping; chronological split; missing B items and cycle times remain null", "split_rule": RULE}
    (OUT / "provenance_ds04.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    lines = ["# DS04 machine and external forecasting audit", "", "Evidence boundary: MEASURED source observations; DERIVED summaries and split. These are manufacturing machines, not semiconductor test cells.", "", f"Split: {RULE}", "Company A status codes 0/1/2/3 map to idle/manual/auto/alarm. Company B Alarm/Standby/Production/Loading/Tooling map to their lowercase names; MachineOn is approximated as idle, not a measured idle label. Original codes are retained in status_raw.", "Company B does not provide items or cycle time; these remain null. Company A cycle_time is total time for items in a time span, not remaining time.", ""]
    for company, part in d.groupby("company"):
        gaps = part.groupby("asset")["ts"].diff().dt.total_seconds()
        lines += [f"## Company {company}", f"Assets: {', '.join(map(str, sorted(part.asset.unique())))}; rows: {len(part)}; span: {part.ts.min()} to {part.ts.max()}.", f"Positive sampling intervals (seconds): {gaps[gaps > 0].value_counts().head(5).to_dict()}; missing timestamp values: {part.ts.isna().sum()}; duplicate asset/timestamps: {part.duplicated(['asset', 'ts']).sum()}. Gaps may indicate missing observations; without a fixed cadence their count cannot be inferred reliably.", f"Status counts: {part.status.value_counts().to_dict()}.", f"Power range kW by status: {part.groupby('status').power_kw.agg(['min', 'max']).to_dict('index')}.", f"power_avg integer-quantised: {bool((part.power_kw.dropna() % 1 == 0).all())}; missing power values: {part.power_kw.isna().sum()}.", ""]
    lines += ["## Forecasting suitability", "Next-slot power and state transitions are feasible within each asset, subject to gaps, duplicate times, chronological evaluation and differing sampling intervals. Remaining cycle time is not directly labelled; Company A's total cycle time does not identify elapsed/remaining cycle time and Company B lacks cycle time. These records cannot establish semiconductor test-cell performance or regenerative power behaviour.", "", "## External benchmarks (UCI archives; no parquet produced)"]
    with ZipFile(ROOT / "predict_ai_electrics/appliances+energy+prediction.zip") as z:
        with z.open("energydata_complete.csv") as f:
            u = pd.read_csv(f)
    times = pd.to_datetime(u.date)
    lines += [f"Appliances energy prediction: {len(u)} rows, {times.min()} to {times.max()}, interval counts in seconds {times.diff().dt.total_seconds().value_counts().head(3).to_dict()}; columns: {', '.join(u.columns)}. Household appliance load and weather/humidity variables support an external next-slot forecast benchmark, not industrial transfer validation; timestamps are timezone-unspecified."]
    with ZipFile(ROOT / "predict_ai_electrics/electricityloaddiagrams20112014.zip") as z:
        with z.open("LD2011_2014.txt") as f:
            reader = pd.read_csv(f, sep=";", decimal=",", usecols=[0], chunksize=20000)
            t = pd.concat([chunk.iloc[:, 0] for chunk in reader], ignore_index=True)
        with z.open("LD2011_2014.txt") as f:
            columns = pd.read_csv(f, sep=";", nrows=0).columns
    t = pd.to_datetime(t)
    lines += [f"ElectricityLoadDiagrams: {len(t)} rows, {t.min()} to {t.max()}, interval counts in seconds {t.diff().dt.total_seconds().value_counts().head(3).to_dict()}; columns: timestamp plus {len(columns)-1} customer series ({columns[1]} through {columns[-1]}). Customer electricity demand supports an external load forecasting benchmark, not machine-state or test-cell validation; timestamps are timezone-unspecified and early zeros may reflect unavailable series."]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Built {OUT / 'ds04_machines.parquet'} ({len(d)} rows); audit: {REPORT}")


if __name__ == "__main__":
    build()
