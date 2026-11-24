import pytest

from regenate.economics.thermal import cooling_load, heat_rejected_kwh, q_dot, water_estimate


def test_heat_and_cooling_balance():
    ledger = {"loss_kwh": 2, "dump_kwh": 3, "dut_in_kwh": 10,
              "recoverable_kwh": 6, "hvac_kwh": 1}
    heat = heat_rejected_kwh(ledger)
    assert heat == 9
    assert cooling_load(heat, 3) == 3
    assert q_dot(2, 4, 10, 13) == 24
    with pytest.raises(ValueError):
        cooling_load(heat, 0)


def test_water_requires_cited_coefficient_and_defaults_to_unverified():
    with pytest.raises(TypeError):
        water_estimate(9)
    with pytest.raises(ValueError):
        water_estimate(9, 1, citation="")
    assert water_estimate(9, 2, citation="site record")["label"] == "NOT_VERIFIED"
    assert water_estimate(9, 2, citation="meter record", metered=True) == {
        "water_l": 18, "label": "METERED", "citation": "meter record"}

