"""Run 3 AI19-lite / queued-job forecasting: predict the NEXT cycle of a module before it starts (the information the
TR_Q decomposition showed to carry the largest headroom). Cycle-level LightGBM on the history of the same module only.
  python -m regenate.forecasting.cycle_model --proc /content/ds05_proc --out /content/ai_runs/run3/cycle_model
Targets (ratio to the previous cycle = the recipe P0 uses): log(dur/dur_prev), log(E_ch/E_ch_prev), log(E_ds/E_ds_prev).
Baselines: AI00 previous cycle (ratio 1), AI02 median of the last 5 cycles. Model selection on val; test is reported only.
Output pred table (one row per cycle_file, features from earlier cycles only) feeds make_profile_fn variant PQ.
"""
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd

EPS = 1e-6
TARGETS = {"dur": "dur_h", "ech": "e_charge_kwh", "eds": "e_discharge_kwh"}


def build_table(cyc):
    """One row per cycle with lagged features of the same use case (module); no information from the cycle itself."""
    c = cyc[cyc.error.fillna("") == ""].sort_values(["use_case", "ord"]).copy()
    g = c.groupby("use_case")
    for t, col in TARGETS.items():
        v = np.log(c[col].clip(lower=EPS))
        c[f"l_{t}"] = v
        for lag in (1, 2, 3):
            c[f"{t}_lag{lag}"] = g[f"l_{t}"].shift(lag)
        c[f"{t}_med5"] = g[f"l_{t}"].transform(lambda s: s.shift(1).rolling(5, min_periods=1).median())
        c[f"{t}_std5"] = g[f"l_{t}"].transform(lambda s: s.shift(1).rolling(5, min_periods=2).std())
        c[f"y_{t}"] = c[f"l_{t}"] - c[f"{t}_lag1"]                       # log ratio to the previous cycle
    for col in ("h_charge", "h_discharge", "h_rest", "t_amb_mean_c", "rte", "v_max", "v_min"):
        c[f"{col}_lag1"] = g[col].shift(1)
    c["uc_code"] = c.use_case.astype("category").cat.codes
    c["gap_h"] = (c.t0_s - g.t1_s.shift(1)) / 3600.0
    return c[c.dur_lag1.notna()].reset_index(drop=True)


def feature_cols(c):
    return [x for x in c.columns if x.endswith(("_lag1", "_lag2", "_lag3", "_med5", "_std5")) or x in ("uc_code", "gap_h")]   # no calendar index: avoid time extrapolation


def fit(c, seed=0):
    import lightgbm as lgb
    F = feature_cols(c); tr, va = c[c.split == "train"], c[c.split == "val"]
    models, rows = {}, []
    for t in TARGETS:
        best = None
        for leaves in (7, 15, 31):                                         # selection on validation only
            m = lgb.LGBMRegressor(n_estimators=400, learning_rate=0.03, num_leaves=leaves, min_child_samples=20,
                                  subsample=0.8, subsample_freq=1, colsample_bytree=0.8, random_state=seed, verbose=-1)
            m.fit(tr[F], tr[f"y_{t}"], eval_set=[(va[F], va[f"y_{t}"])], callbacks=[lgb.early_stopping(50, verbose=False)])
            mae = np.mean(np.abs(m.predict(va[F]) - va[f"y_{t}"]))
            if best is None or mae < best[0]:
                best = (mae, leaves, m)
        models[t] = best[2]; rows.append(dict(target=t, val_mae_log=best[0], leaves=best[1]))
    return models, F, pd.DataFrame(rows)


def evaluate(c, models, F):
    out = []
    for split in ("val", "test"):
        d = c[c.split == split]
        for t, col in TARGETS.items():
            true = d[col].clip(lower=EPS).values; prev = np.exp(d[f"{t}_lag1"].values)
            preds = {"AI00_prev_cycle": prev, "AI02_med5": np.exp(d[f"{t}_med5"].values),
                     "AI10_lgbm_cycle": prev * np.exp(models[t].predict(d[F]))}
            base = np.mean(np.abs(prev - true))
            for name, p in preds.items():
                for uc in [None] + sorted(d.use_case.unique()):
                    msk = np.ones(len(d), bool) if uc is None else (d.use_case == uc).values
                    mae = np.mean(np.abs(p[msk] - true[msk])); b = np.mean(np.abs(prev[msk] - true[msk]))
                    out.append(dict(split=split, target=t, use_case=uc or "ALL", model=name, n=int(msk.sum()), mae=mae,
                                    mape_median=float(np.median(np.abs(p[msk] - true[msk]) / np.maximum(true[msk], EPS))),
                                    skill_vs_prev=1 - mae / b if b > 0 else np.nan))
    return pd.DataFrame(out)


def pred_table(c, models, F):
    p = c[["cycle_file", "use_case", "split"]].copy()
    for t in TARGETS:
        p[f"r_{t}"] = np.exp(models[t].predict(c[F]))                    # predicted ratio to the previous cycle
    return p


def main():
    from regenate.data.bench_v2 import load_proc
    ap = argparse.ArgumentParser(); ap.add_argument("--proc", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=0); a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    cyc, _ = load_proc(a.proc)
    c = build_table(cyc); models, F, sel = fit(c, a.seed)
    ev = evaluate(c, models, F); ev.to_csv(out / "cycle_metrics.csv", index=False); sel.to_csv(out / "selection.csv", index=False)
    pred_table(c, models, F).to_parquet(out / "cycle_pred.parquet", index=False)
    import joblib; joblib.dump(dict(models=models, feats=F), out / "cycle_models.joblib")
    (out / "manifest.json").write_text(json.dumps(dict(args=vars(a), n=len(c), feats=F), indent=1))
    print(ev[(ev.use_case == "ALL")].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
