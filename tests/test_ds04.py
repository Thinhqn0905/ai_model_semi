import json
from pathlib import Path
import pandas as pd


def test_ds04_schema_and_chronology():
    root = Path(__file__).resolve().parents[1]
    d = pd.read_parquet(root / "data/processed/ds04_machines.parquet")
    assert set(["company", "asset", "ts", "status", "status_raw", "power_kw", "items", "cycle_time_s", "split"]).issubset(d.columns)
    assert str(d.ts.dtype) == "datetime64[ns, UTC]"
    assert set(d.status) <= {"idle", "manual", "auto", "alarm", "standby", "loading", "tooling", "production"}
    assert set(d.split) == {"train", "val", "test"}
    bounds = d.groupby(["company", "asset", "split"]).ts.agg(["min", "max"]).unstack("split")
    assert (bounds["max"]["train"] < bounds["min"]["val"]).all()
    assert (bounds["max"]["val"] < bounds["min"]["test"]).all()
    assert json.loads((root / "data/processed/provenance_ds04.json").read_text(encoding="utf-8"))["split_rule"]
