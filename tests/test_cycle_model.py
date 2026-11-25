import numpy as np
import pandas as pd
from regenate.forecasting.cycle_model import build_table, fit, evaluate, pred_table, select_gates


def synth_cyc(n=400):
    rng = np.random.default_rng(0); rows = []
    for uc in ("A", "B"):
        dur = 5.0
        for i in range(n):
            dur = max(0.5, dur * 0.995 + rng.normal(0, 0.05))                  # slow drift: learnable vs previous cycle
            rows.append(dict(use_case=uc, ord=i, error="", dur_h=dur, e_charge_kwh=dur * 0.2, e_discharge_kwh=dur * 0.18,
                             h_charge=dur / 2, h_discharge=dur / 2, h_rest=0.1, t_amb_mean_c=25.0, rte=0.9, v_max=8.2, v_min=6.0,
                             t0_s=i * 1e5, t1_s=i * 1e5 + dur * 3600, cycle_file=f"{uc}{i}",
                             split="train" if i < 0.7 * n else ("val" if i < 0.85 * n else "test")))
    return pd.DataFrame(rows)


def test_cycle_model_leak_free_and_runs():
    c = build_table(synth_cyc())
    first = c.groupby("use_case").head(1)
    assert np.allclose(np.exp(first.dur_lag1.values), synth_cyc().groupby("use_case").head(1).dur_h.values)  # lag1 = previous cycle
    models, F, sel = fit(c)
    assert not any(f.startswith(("l_", "y_")) or f in ("dur_h", "e_charge_kwh") for f in F)       # no same-cycle info
    ev = evaluate(c, models, F); assert set(ev.model) == {"AI00_prev_cycle", "AI02_med5", "AI10_lgbm_cycle"}
    p = pred_table(c, models, F); assert {"r_dur", "r_ech", "r_eds"} <= set(p.columns) and (p.r_dur > 0).all()


def test_gate_off_equals_recipe():
    c = build_table(synth_cyc()); models, F, _ = fit(c)
    g = select_gates(c, models, F); g["th"] = None
    p = pred_table(c, models, F, g); assert np.allclose(p.r_dur, 1.0)
    ev = evaluate(c, models, F, select_gates(c, models, F))
    v = ev[(ev.split == "val") & (ev.use_case == "ALL")].set_index(["target", "model"]).mae
    for t in ("dur", "ech", "eds"):                     # gate selected on val can never be worse than the recipe on val
        assert v[(t, "AI18_gated")] <= v[(t, "AI00_prev_cycle")] + 1e-12
