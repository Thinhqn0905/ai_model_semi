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
