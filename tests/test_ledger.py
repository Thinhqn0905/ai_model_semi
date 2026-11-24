"""ELEC-01..09 invariants of regenate.electrical.ledger (docs/system_spec.md s5)."""
import numpy as np
import pytest
from regenate.electrical.ledger import ledger, ElecParams, dc_gain_bound, TOPOLOGIES

DT = 1 / 60
rng = np.random.default_rng(0)


def random_case(S=4, K=200, storage=False):
    p_in = rng.uniform(0, 12, (S, K))
    if storage:   # energy-storage DUT: source only while not charging
        p_rec = np.where(rng.random((S, K)) < 0.5, rng.uniform(0, 12, (S, K)), 0.0)
        p_in = np.where(p_rec > 0, 0.0, p_in)
    else:         # converter DUT: output <= 0.9 * input
        p_rec = 0.9 * p_in * rng.uniform(0.5, 1.0, (S, K))
    return p_in, p_rec, rng.uniform(0, 2, (S, K))


@pytest.mark.parametrize("topo", TOPOLOGIES)
@pytest.mark.parametrize("storage", [False, True])
def test_elec01_02_balance_and_nonneg_losses(topo, storage):
    p_in, p_rec, aux = random_case(storage=storage)
    r = ledger(p_in, p_rec, aux, DT, topo)
    assert r["loss_kwh"] >= -1e-9
    assert np.all(r["p_import"] >= 0) and np.all(r["p_export"] >= 0)
    assert np.all(r["p_import"] * r["p_export"] == 0)        # never both in one step


def test_elec01_b1_losses_match_independent_formula():
    p_in, p_rec, aux = random_case()
    prm = ElecParams()
    r = ledger(p_in, p_rec, aux, DT, "B1", prm)
    expect = (p_in * (1 / prm.eta_sup_ac - 1) + p_rec * (1 - prm.eta_rl_ac)).sum() * DT
    assert r["loss_kwh"] == pytest.approx(expect, rel=1e-9)


@pytest.mark.parametrize("topo", TOPOLOGIES)
def test_elec03_04_idle(topo):
    z = np.zeros((3, 10))
    assert ledger(z, z, z, DT, topo)["import_kwh"] == 0
    r = ledger(z, z, np.full(10, 1.5), DT, topo)
    assert r["import_kwh"] == pytest.approx(1.5 * 10 * DT) and r["export_kwh"] == 0


def test_elec05_afe_limits():
    p_in = np.zeros((2, 5)); p_rec = np.full((2, 5), 20.0)
    prm = ElecParams(P_afe_max=10.0)
    r = ledger(p_in, p_rec, 0 * p_in, DT, "DC", prm)
    assert np.all(r["p_export"] <= 10.0 * prm.eta_afe_exp + 1e-9)
    assert r["dump_kwh"] > 0
    r2 = ledger(np.full((2, 5), 20.0), 0 * p_in, 0 * p_in, DT, "DC", prm)
    assert r2["afe_violation_steps"] == 5


def test_elec06_link_cap():
    p_in = np.array([[10.0] * 4, [0.0] * 4]); p_rec = np.array([[0.0] * 4, [10.0] * 4])
    r = ledger(p_in, p_rec, np.zeros(4), DT, "DC", ElecParams(P_link_max=3.0))
    assert np.all(r["direct"] <= 3.0 + 1e-12)


def test_elec07_self_use_bounded_by_own_demand():
    p_in, p_rec, aux = random_case(storage=True)
    prm = ElecParams()
    r = ledger(p_in, p_rec, aux, DT, "B1p", prm)
    assert np.all(r["self_use"] <= (p_in / prm.eta_sup_dc).sum(0) + 1e-9)


def test_elec08_no_double_counting():
    # station 0 pure source, station 1 pure sink, no aux: every recovered kWh ends in exactly one place
    p_rec = np.array([[10.0] * 6, [0.0] * 6]); p_in = np.array([[0.0] * 6, [4.0] * 6])
    prm = ElecParams(P_link_max=2.0)
    r = ledger(p_in, p_rec, np.zeros(6), DT, "DC", prm)
    src_dc = 10.0 * prm.eta_rl_dc
    used = r["self_use"] + r["direct"] / prm.eta_link + r["afe_exp_dc"] + r["dump"]
    assert np.allclose(used, src_dc)


def test_elec09_dc_equals_inrack_when_no_residual_source():
    p_in, p_rec, aux = random_case()                  # converter DUT: own demand >= own recovery
    a = ledger(p_in, p_rec, aux, DT, "DC"); b = ledger(p_in, p_rec, aux, DT, "B1p")
    assert a["net_kwh"] == pytest.approx(b["net_kwh"], rel=1e-12)
    assert a["direct_reuse_kwh"] == 0


def test_dc_gain_bound_exact_for_source_sink_pair():
    p_rec = np.array([[5.0] * 10, [0.0] * 10]); p_in = np.array([[0.0] * 10, [8.0] * 10])
    prm = ElecParams()
    gain = ledger(p_in, p_rec, np.zeros(10), DT, "B1p", prm)["net_kwh"] - \
        ledger(p_in, p_rec, np.zeros(10), DT, "DC", prm)["net_kwh"]
    R = 5.0 * prm.eta_rl_dc * 10 * DT
    assert gain == pytest.approx(dc_gain_bound(prm) * R, rel=1e-12)


def test_ordering_on_converter_burnin():
    p_in, p_rec, aux = random_case()
    e = {t: ledger(p_in, p_rec, aux, DT, t)["net_kwh"] for t in TOPOLOGIES}
    assert e["B0"] > e["B1"] > e["B1p"] >= e["DC"] - 1e-9
