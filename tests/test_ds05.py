"""DS05 loader on a synthetic zip with the real column layout (real data lives on Colab)."""
import zipfile
import numpy as np
import pandas as pd
from regenate.data.ds05 import build, parse_cycle


def fake_cycle(n=600, p_ch=200.0, p_dis=150.0):
    t = np.arange(n) * 3.0
    p = np.where(t < 600, p_ch, np.where(t < 1200, 0.0, -p_dis))
    return pd.DataFrame({"POWER": p, "CURRENT": p / 8, "VOLTAGE": 8.0, "STEP_MODE": 2, "STATUS_IDX": 1,
                         "Cumulative_Time": t, "REAL_TIME": "x", "Cell1": 4.0, "Cell2": 4.0,
                         "Ambient Temperature": 25.0, "EXTRA": 1})


def test_parse_energy_and_sign():
    tr, s = parse_cycle(fake_cycle().to_csv(index=False).encode(), step_s=60)
    assert abs(s["e_charge_kwh"] - 200 * 600 / 3.6e6) < 1e-9
    assert abs(s["e_discharge_kwh"] - 150 * (1797 - 1200) / 3.6e6) < 1e-9
    assert abs(s["h_charge"] - 600 / 3600) < 1e-9 and s["rte"] > 0
    assert (tr.p_charge_w >= 0).all() and (tr.p_discharge_w >= 0).all()
    assert not ((tr.p_charge_w > 0) & (tr.p_discharge_w > 0)).any()       # bins align with the phase change here


def test_build_from_zip(tmp_path):
    zp = tmp_path / "s.zip"
    with zipfile.ZipFile(zp, "w") as z:
        for uc in ("TOU", "FFR"):
            for k in (1, 2):
                z.writestr(f"{uc}/2020_X/Cycle_{k}.csv", fake_cycle().to_csv(index=False))
        z.writestr("TOU/2020_X/Cycle_3.csv", "POWER,Cumulative_Time\n")      # empty -> recorded as error
    cyc = build(str(zp), tmp_path / "out", workers=1)
    assert len(cyc) == 5 and (cyc.error != "").sum() == 1
    assert (tmp_path / "out/ds05_traces/TOU.parquet").exists()
