"""MILP oracle == brute-force lexicographic optimum scored by the shared ledger (all topologies)."""
import itertools
import numpy as np
import pytest
from regenate.electrical.ledger import ledger, ElecParams, TOPOLOGIES
from regenate.optimization.milp import Job, solve, assign_stations, render_slots

DT = 0.25


def jobs_mixed():
    ch = lambda n: np.r_[np.full(n, 6.0), np.zeros(n)]          # charge then discharge (S3-like)
    dis = lambda n: np.r_[np.zeros(n), np.full(n, 5.0)]
    return [
        Job(0, 4, 8, ch(2), dis(2), np.full(4, 0.3)),
        Job(0, 5, 9, np.r_[np.zeros(2), np.full(3, 4.0)], np.r_[np.full(2, 5.0), np.zeros(3)]),
        Job(1, 5, 10, np.full(3, 8.0), 0.9 * np.full(3, 8.0), np.full(3, 0.5)),   # converter burn-in
        Job(2, 6, 9, ch(2), dis(2)),
    ]


def brute(jobs, S, K, topo, prm, idle):
    best = None
    wins = [range(j.release, min(j.latest, K - j.dur) + 1) for j in jobs]
    for st in itertools.product(*wins):
        run = np.zeros(K)
        for t, j in zip(st, jobs):
            run[t:t + j.dur] += 1
        if run.max() > S:
            continue
        tt = sum(max(0.0, t + j.dur - j.due) for t, j in zip(st, jobs))
        stn = assign_stations(list(st), [j.dur for j in jobs], S)
        net = ledger(*render_slots(jobs, st, stn, S, K, idle), DT, topo, prm)["net_kwh"]
        key = (round(tt, 9), net)
        if best is None or key < best[0]:
            best = (key, st)
    return best


@pytest.mark.parametrize("topo", TOPOLOGIES)
@pytest.mark.parametrize("plink", [np.inf, 3.0])
def test_milp_matches_bruteforce(topo, plink):
    jobs = jobs_mixed(); S, K, idle = 2, 14, 0.2
    prm = ElecParams(P_link_max=plink)
    (tt_b, net_b), _ = brute(jobs, S, K, topo, prm, idle)
    r = solve(jobs, S, K, topo, prm, DT, idle_kw=idle)
    assert r.status == "optimal"
    assert r.tt == pytest.approx(tt_b, abs=1e-9)
    assert r.net_kwh == pytest.approx(net_b, abs=1e-6)
    stn = assign_stations(r.starts, [j.dur for j in jobs], S)       # plan re-scored by the ledger
    assert ledger(*render_slots(jobs, r.starts, stn, S, K, idle), DT, topo, prm)["net_kwh"] == \
        pytest.approx(r.net_kwh, abs=1e-6)


def test_fixed_starts_respected():
    jobs = jobs_mixed()
    free = solve(jobs, 2, 14, "DC")
    r = solve(jobs, 2, 14, "DC", fixed={0: 0})
    assert r.status == "optimal" and r.starts[0] == 0
    assert (r.tt, r.net_kwh) >= (free.tt, free.net_kwh - 1e-9)     # freezing can only cost
    assert solve(jobs, 2, 14, "DC", fixed={0: 3}).status.startswith("tt-stage")   # infeasible by hand check


def test_peak_stage_keeps_energy_and_lowers_peak():
    jobs = jobs_mixed(); S, K, idle = 2, 14, 0.2
    base = solve(jobs, S, K, "DC", dt_h=DT, idle_kw=idle)
    pk = solve(jobs, S, K, "DC", dt_h=DT, idle_kw=idle, peak_stage=True)
    assert pk.tt <= base.tt + 1e-9 and pk.net_kwh <= base.net_kwh * (1 + 1e-4) + 1e-6
    peak = lambda r: ledger(*render_slots(jobs, r.starts, assign_stations(r.starts, [j.dur for j in jobs], S), S, K, idle),
                            DT, "DC")["peak_import_kw"]
    assert peak(pk) <= peak(base) + 1e-6
    assert abs(pk.info["peak_kw_planned"] - peak(pk)) < 1e-6          # planned peak == ledger peak
