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


def _residual_totals(jobs, starts, K, prm):
    from regenate.optimization.milp import _coeffs
    D, R = np.zeros(K), np.zeros(K)
    for t, j in zip(starts, jobs):
        c = _coeffs(j, "DC", prm); D[t:t + j.dur] += c["d1"]; R[t:t + j.dur] += c["r1"]
    return D, R


@pytest.mark.parametrize("field,val", [("P_bus_max", 9.0), ("dP_step_max", 10.0)])
def test_bus_limits_match_bruteforce(field, val):
    """E1: MILP with bus throughput / step caps equals brute force over plans that satisfy the caps."""
    jobs = jobs_mixed(); S, K, idle = 2, 14, 0.2
    prm = ElecParams(**{field: val})
    def ok(st):
        D, R = _residual_totals(jobs, st, K, prm)
        return (D.max() <= val + 1e-9 and R.max() <= val + 1e-9) if field == "P_bus_max" else np.abs(np.diff(D - R)).max() <= val + 1e-9
    best = None
    for st in itertools.product(*[range(j.release, min(j.latest, K - j.dur) + 1) for j in jobs]):
        run = np.zeros(K)
        for t, j in zip(st, jobs):
            run[t:t + j.dur] += 1
        if run.max() > S or not ok(st):
            continue
        tt = sum(max(0.0, t + j.dur - j.due) for t, j in zip(st, jobs))
        net = ledger(*render_slots(jobs, st, assign_stations(list(st), [j.dur for j in jobs], S), S, K, idle), DT, "DC", prm)["net_kwh"]
        if best is None or (round(tt, 9), net) < best:
            best = (round(tt, 9), net)
    r = solve(jobs, S, K, "DC", prm, DT, idle_kw=idle)
    assert best is not None and r.status == "optimal" and ok(r.starts)
    assert r.tt == pytest.approx(best[0], abs=1e-9) and r.net_kwh == pytest.approx(best[1], abs=1e-6)


def test_billing_peak_avoids_background_peak():
    """P0-BILL level: with a facility background spike, the cell's import moves away from it (energy unchanged)."""
    jobs = [Job(0, 6, 20, np.full(2, 6.0), np.zeros(2))]                      # one 2-slot sink job, free start in 0..6
    S, K = 1, 10
    bg = np.zeros(K); bg[0:2] = 100.0                                         # background peak in slots 0-1
    plain = solve(jobs, S, K, "DC", dt_h=DT, peak_stage=True)
    bill = solve(jobs, S, K, "DC", dt_h=DT, peak_stage=True, peak_bg=bg, peak_avg_slots=2)
    assert bill.net_kwh == pytest.approx(plain.net_kwh, abs=1e-6)
    assert bill.starts[0] >= 2                                                # not on top of the background peak
    assert bill.info["peak_kw_planned"] == pytest.approx(100.0, abs=1e-6)     # billed max = background alone
    floor = solve(jobs, S, K, "DC", dt_h=DT, peak_stage=True, peak_bg=np.zeros(K), peak_floor=50.0)
    assert floor.info["peak_kw_planned"] == pytest.approx(50.0, abs=1e-6)     # below the floor nothing is billed
