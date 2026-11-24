from pathlib import Path
import numpy as np
import pytest
from regenate.data.ds01 import load_instance, to_frames, SOURCE


@pytest.mark.parametrize("name", ["n005_tau02_r00.json", "n020_tau05_r03.json", "n100_tau08_r09.json"])
def test_instance_round_trip(name):
    inst = load_instance(SOURCE / name)
    jobs, stations = to_frames(inst)
    assert len(jobs) == inst["n"]
    assert len(stations) == sum(inst["m"])
    assert not jobs[["instance_id", "job_id", "release_u", "due_u", "size", "p_stage1_u", "p_stage2_u", "p_stage3_u", "p_stage4_workload_u", "unit_note"]].isna().any().any()
    assert not stations[["instance_id", "stage", "machine_id", "unit_note"]].isna().any().any()
    for j, row in jobs.iterrows():
        assert row.due_u == inst["due_dates"][j]
        assert row["size"] == inst["sizes"][j]
        for stage, key in [(1, "p1"), (2, "p2"), (3, "p3"), (4, "eta4")]:
            column = f"p_stage{stage}_u" if stage < 4 else "p_stage4_workload_u"
            assert list(row[column]) == inst[key][j]
    for _, row in stations.iterrows():
        stage, machine = row.stage, row.machine_id
        for kind in ("run", "idle"):
            values = inst.get(f"P{stage}_{kind}")
            actual = row[f"p_{kind}_source_units"]
            assert actual == values[machine] if values else np.isnan(actual)
        if stage == 3:
            assert row.capacity == inst["Q"][machine]
        if stage == 4:
            assert row.alpha_source_units == inst["alpha"][machine]
            assert row.speeds == inst["speeds"]

