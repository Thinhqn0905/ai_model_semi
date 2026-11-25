"""bench v2 end-to-end on synthetic DS05-like cycles (real data lives on Colab)."""
import numpy as np
import pandas as pd
from regenate.data.bench_v2 import make_instance, render_traces, fifo
from regenate.evaluation.v2_campaign import run_one
from regenate.forecasting.ds05_bench import order_cycles


def synth(n=40):
    rng = np.random.default_rng(0)
    cyc = pd.DataFrame(dict(use_case=np.where(np.arange(n) % 2, "TOU", "FFR"), period="2020_March",
                            cycle_file=[f"c{k}" for k in range(n)], cycle_no=np.arange(n), error=""))
    arrs = {}
    for k in range(n):
        L = int(rng.integers(120, 200)); t = np.arange(L); cut = int(L * rng.uniform(0.3, 0.6))
        ch = np.where(t < cut, 0.2, 0.0); ds = np.where(t >= cut + 5, 0.18, 0.0)
        arrs[f"c{k}"] = (ch, ds, np.full(L, 8.0), np.full(L, 25.0))
    cyc = order_cycles(cyc); cyc["dur_h"] = [len(arrs[f][0]) / 60 for f in cyc.cycle_file]
    return cyc, arrs


def test_instance_and_render_energy():
    cyc, arrs = synth()
    inst = make_instance(cyc, arrs, 0, n_jobs=4, n_stations=2, split="train")
    a, s = fifo(inst)
    p_in, p_rec, _ = render_traces(inst, a, s, 0.25, True)
    want = sum(inst["traces"][j][0].sum() / 60 for j in a)          # kWh of all true charge traces
    assert abs(p_in.sum() * 0.25 - want) < 1e-9
    assert all(inst["jobs"].prev_file != inst["jobs"].cycle_file)


def test_ladder_runs_and_oracle_not_worse_than_inrack():
    cyc, arrs = synth()
    inst = make_instance(cyc, arrs, 1, n_jobs=4, n_stations=2, split="train")
    rows, _ = run_one(inst, engine=None, flex=0.5, time_limit=10)
    r = {x["method"]: x for x in rows}
    assert {"B0", "B1", "B1p", "B2", "B1-OPT", "B1p-OPT", "B3", "ORACLE", "P0"} <= set(r)
    assert r["ORACLE"]["net_kwh"] <= r["B1p-OPT"]["net_kwh"] + 1e-6
    assert all(x["violations"] == 0 for x in rows)


class StubEngine:
    """Returns fixed predictions; exercises the P1..P4 profile paths without trained models."""
    def predict(self, telemetry, elapsed_min, prev_cycle, use_case):
        q = lambda v: np.array([0.8 * v, v, 1.2 * v])
        return dict(sink_power={h: q(0.1) for h in (1, 4, 16)}, source_power={h: q(0.15) for h in (1, 4, 16)},
                    remaining_duration=q(45.0), prediction_valid=True, physics_check="ok")


def test_ai_variants_profiles_and_run():
    from regenate.forecasting.ai_engine import make_profile_fn
    cyc, arrs = synth()
    inst = make_instance(cyc, arrs, 2, n_jobs=4, n_stations=2, split="train")
    obs = dict(elapsed_h=1.5)
    for v in ("P1", "P2", "P3", "P4"):
        pin, prec, aux = make_profile_fn(inst, v, StubEngine())(0, obs)
        assert len(pin) >= 6 and (pin >= 0).all() and (prec >= 0).all()
    p4 = make_profile_fn(inst, "P4", StubEngine())(0, obs); p2 = make_profile_fn(inst, "P2", StubEngine())(0, obs)
    assert len(p4[0]) >= len(p2[0])                                   # P90 remaining is longer than P50
    rows, _ = run_one(inst, StubEngine(), flex=0.5, time_limit=10, methods=["P0", "P1", "P3", "P4"])
    assert {r["method"] for r in rows} == {"P0", "P1", "P3", "P4"} and all(r["violations"] == 0 for r in rows)


def test_diagnostic_variants_perfect_and_truth():
    from regenate.data.bench_v2 import job_profile
    from regenate.forecasting.ai_engine import make_profile_fn
    cyc, arrs = synth()
    inst = make_instance(cyc, arrs, 3, n_jobs=4, n_stations=2, split="train")
    tru = job_profile(inst, 0, 0.25, "truth")
    assert np.allclose(make_profile_fn(inst, "TR_RUN")(0, dict(elapsed_h=1.0))[0], tru[0])
    assert np.allclose(make_profile_fn(inst, "TR_RUN")(0, None)[0], job_profile(inst, 0, 0.25, "nominal")[0])
    p2 = make_profile_fn(inst, "P2*")(0, dict(elapsed_h=1.0))
    assert len(p2[0]) == len(tru[0])                                  # perfect remaining duration -> true length
    rows, _ = run_one(inst, None, flex=0.5, time_limit=10, methods=["P0", "P1*", "P2*", "TR_RUN", "TR_ALL"])
    assert {r["method"] for r in rows} == {"P0", "P1*", "P2*", "TR_RUN", "TR_ALL"} and all(r["violations"] == 0 for r in rows)


def test_p5_phase_aligned_runs():
    from regenate.forecasting.ai_engine import make_profile_fn
    cyc, arrs = synth()
    inst = make_instance(cyc, arrs, 4, n_jobs=4, n_stations=2, split="train")
    pin, prec, _ = make_profile_fn(inst, "P5")(0, dict(elapsed_h=1.0))
    assert len(pin) >= 4 and (pin >= 0).all() and (prec >= 0).all()
    rows, _ = run_one(inst, None, flex=0.5, time_limit=10, methods=["P0", "P5", "P5s"])
    assert all(r["violations"] == 0 for r in rows)


def test_pq_queued_prediction_energy_and_length():
    from regenate.forecasting.ai_engine import make_profile_fn
    cyc, arrs = synth()
    inst = make_instance(cyc, arrs, 5, n_jobs=4, n_stations=2, split="train")
    cf = inst["jobs"].set_index("job_id").loc[0, "cycle_file"]
    nom = make_profile_fn(inst, "P0")(0, None)
    pin, prec, _ = make_profile_fn(inst, "PQ", cycle_pred={cf: dict(r_dur=1.5, r_ech=1.2, r_eds=0.8)})(0, None)
    e = lambda a: a.sum() * 0.25
    assert abs(len(pin) - 1.5 * len(nom[0])) <= 1
    tol = lambda a, b: 2 * 0.25 * max(a.max(), b.max())     # partial last slot of _bin is averaged over fewer minutes
    assert abs(e(pin) - 1.2 * e(nom[0])) <= tol(pin, nom[0])
    assert abs(e(prec) - 0.8 * e(nom[1])) <= tol(prec, nom[1])
    assert np.allclose(make_profile_fn(inst, "PQ", cycle_pred={})(0, None)[0], nom[0])     # no prediction -> recipe


def test_pq_star_uses_true_length_and_nominal_when_running():
    from regenate.data.bench_v2 import job_profile
    from regenate.forecasting.ai_engine import make_profile_fn
    cyc, arrs = synth()
    inst = make_instance(cyc, arrs, 6, n_jobs=4, n_stations=2, split="train")
    f = make_profile_fn(inst, "PQ*")
    assert len(f(0, None)[0]) == len(job_profile(inst, 0, 0.25, "truth")[0])
    assert np.allclose(f(0, dict(elapsed_h=1.0))[0], job_profile(inst, 0, 0.25, "nominal")[0])


def test_pqd_keeps_recipe_energy():
    from regenate.forecasting.ai_engine import make_profile_fn
    cyc, arrs = synth()
    inst = make_instance(cyc, arrs, 7, n_jobs=4, n_stations=2, split="train")
    cf = inst["jobs"].set_index("job_id").loc[0, "cycle_file"]; nom = make_profile_fn(inst, "P0")(0, None)
    pin, prec, _ = make_profile_fn(inst, "PQd", cycle_pred={cf: dict(r_dur=2.0, r_ech=5.0, r_eds=5.0)})(0, None)
    assert abs(len(pin) - 2 * len(nom[0])) <= 1
    assert abs(pin.sum() - nom[0].sum()) <= 2 * max(pin.max(), nom[0].max())     # energy kept within one partial slot
    assert np.allclose(make_profile_fn(inst, "PQd", cycle_pred={cf: dict(r_dur=1.0, r_ech=5.0, r_eds=5.0)})(0, None)[0], nom[0])


def test_safe_initial_plan_respects_e1_and_plan_margin():
    from regenate.electrical.ledger import ElecParams
    from regenate.evaluation.v2_campaign import safe_initial
    cyc, arrs = synth()
    inst = make_instance(cyc, arrs, 8, n_jobs=4, n_stations=2, split="train")
    fa, fs = fifo(inst)
    plan, kind = safe_initial(inst, 0.5, 0.25, ElecParams(P_afe_max=50, P_bus_max=60), fa, fs, 10)
    assert kind == "milp_e1" and set(plan) == set(fa)
    rows, _ = run_one(inst, None, flex=0.5, time_limit=10, prm=ElecParams(P_afe_max=50), plan_prm=ElecParams(P_afe_max=45), methods=["P0"])
    assert rows[0]["initial_plan"] == "milp_e1" and rows[0]["violations"] == 0
