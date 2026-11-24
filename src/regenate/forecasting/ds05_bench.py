"""Branch C — DS05 (Lboro second-life battery sweat test) AI benchmark: Model A (source/sink power), Model B
(remaining duration + cycle energy), quantiles P10/P50/P90. Runs where the processed DS05 lives (Colab).

Decision points every `stride` minutes inside each cycle (60-s bins from regenate.data.ds05). Only past information:
lags of the running cycle + the PREVIOUS cycle of the same module (same use case) at the same elapsed time.
Split per module (use case): chronological 70/15/15 by cycle order; test cycles are never seen in training.
  python -m regenate.forecasting.ds05_bench --proc /content/ds05_proc --out runs/ai/ds05
"""
import argparse, json, re, time
from pathlib import Path
import numpy as np
import pandas as pd

HORIZONS = (1, 4, 16)          # 15-min slots ahead (15 min, 1 h, 4 h)
SLOT = 15                      # bins (minutes) per scheduler slot
LAGS = (1, 2, 3, 5, 10, 15, 30, 60)
QS = (0.1, 0.5, 0.9)


def period_key(period):
    """Chronological key of a period folder like '2021_August_November' or 'April to June/2019_February_March'."""
    m = re.search(r"(20\d\d)_([A-Za-z]+)", period)
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
              "november", "december"]
    if not m:
        return (9999, 0)
    mo = m.group(2).lower()
    return (int(m.group(1)), months.index(mo) + 1 if mo in months else 0)


def order_cycles(cyc):
    cyc = cyc[cyc.error.fillna("") == ""].copy()
    cyc["pkey"] = cyc.period.map(period_key)
    cyc = cyc.sort_values(["use_case", "pkey", "cycle_no", "cycle_file"])
    cyc["ord"] = cyc.groupby("use_case").cumcount()
    n = cyc.groupby("use_case").ord.transform("max") + 1
    cyc["split"] = np.where(cyc.ord < 0.7 * n, "train", np.where(cyc.ord < 0.85 * n, "val", "test"))
    return cyc


def cycle_arrays(tr):
    """dict cycle_file -> (p_ch, p_dis, v, t_amb) numpy arrays on the 60-s grid."""
    out = {}
    for f, g in tr.groupby("cycle_file", sort=False):
        g = g.sort_values("t_s")
        out[f] = (g.p_charge_w.to_numpy(float) / 1000, g.p_discharge_w.to_numpy(float) / 1000,
                  g.v.to_numpy(float), g["t_amb_c"].to_numpy(float) if "t_amb_c" in g else np.zeros(len(g)))
    return out


def _slot_mean(a, b, h):
    s = b + (h - 1) * SLOT
    return a[s:s + SLOT].mean() if s + SLOT <= len(a) else np.nan


def features_at(ch, ds, v, ta, b, prev):
    """Decision-time features at bin b of a running cycle (only bins < b) + previous cycle of the module."""
    pch, pds = (prev[0], prev[1]) if prev is not None else (None, None)
    f = dict(elapsed_min=b, v_last=v[b - 1], t_amb=ta[b - 1])
    for k in LAGS:
        f[f"ch_l{k}"] = ch[b - k] if b - k >= 0 else np.nan
        f[f"ds_l{k}"] = ds[b - k] if b - k >= 0 else np.nan
    lo15, lo60 = max(0, b - 15), max(0, b - 60)
    f["ch_m15"], f["ds_m15"] = ch[lo15:b].mean(), ds[lo15:b].mean()
    f["ch_m60"], f["ds_m60"] = ch[lo60:b].mean(), ds[lo60:b].mean()
    f["e_ch_sofar"], f["e_ds_sofar"] = ch[:b].sum() / 60, ds[:b].sum() / 60
    f["prev_len_min"] = len(pch) if pch is not None else np.nan
    for h in HORIZONS:
        f[f"prev_ch_h{h}"] = _slot_mean(pch, b, h) if pch is not None else np.nan
        f[f"prev_ds_h{h}"] = _slot_mean(pds, b, h) if pds is not None else np.nan
    f["prev_rem_min"] = (len(pch) - b) if pch is not None else np.nan
    return f


def make_samples(cyc, arrs, stride=15, min_hist=60):
    """Rows of features + targets (Model A per horizon, Model B remaining duration)."""
    rows = []
    for uc, g in cyc.groupby("use_case"):
        prev = None
        for r in g.itertuples():
            a = arrs.get(r.cycle_file)
            if a is None:
                prev = None; continue
            ch, ds, v, ta = a; L = len(ch)
            for b in range(min_hist, L - SLOT, stride):
                f = dict(use_case=uc, cycle_file=r.cycle_file, split=r.split, ord=r.ord, has_prev=prev is not None,
                         **features_at(ch, ds, v, ta, b, prev))
                for h in HORIZONS:
                    f[f"y_ch_h{h}"] = _slot_mean(ch, b, h); f[f"y_ds_h{h}"] = _slot_mean(ds, b, h)
                f["y_rem_min"] = L - b
                rows.append(f)
            prev = a
    return pd.DataFrame(rows)


FEATS_DROP = ("use_case", "cycle_file", "split", "ord", "has_prev")


def feature_cols(df):
    return [c for c in df.columns if not c.startswith("y_") and c not in FEATS_DROP] + ["uc_code"]


def _lgb_q(X, y, Xv, q, seed=0, store=None, key=None):
    import lightgbm as lgb
    m = lgb.LGBMRegressor(objective="quantile", alpha=q, n_estimators=400, learning_rate=0.05, num_leaves=63,
                          min_child_samples=50, subsample=0.8, subsample_freq=1, colsample_bytree=0.8,
                          random_state=seed, verbose=-1)
    m.fit(X, y)
    if store is not None:
        store[(key, q)] = m
    return m.predict(Xv)


def run(proc, out, stride=15, max_train=400_000, seed=0):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    cyc = order_cycles(pd.read_parquet(Path(proc) / "ds05_cycles.parquet"))
    arrs = {}
    for p in sorted((Path(proc) / "ds05_traces").glob("*.parquet")):
        arrs.update(cycle_arrays(pd.read_parquet(p)))
    df = make_samples(cyc, arrs, stride)
    df["uc_code"] = df.use_case.astype("category").cat.codes
    df.to_parquet(out / "samples.parquet", index=False)
    feats = feature_cols(df)
    tr = df[df.split == "train"]
    if len(tr) > max_train:
        tr = tr.sample(max_train, random_state=seed)
    te = df[df.split == "test"]
    preds, metrics, runtime = [], [], []
    store = {}
    targets = [(f"y_{c}_h{h}", f"prev_{c}_h{h}", f"{c}_l1") for c in ("ch", "ds") for h in HORIZONS] + \
              [("y_rem_min", "prev_rem_min", None)]
    from sklearn.linear_model import Ridge
    from sklearn.ensemble import RandomForestRegressor
    import xgboost as xgb
    for y, prevcol, lastcol in targets:
        m_tr = tr[y].notna(); m_te = te[y].notna()
        X, Y = tr.loc[m_tr, feats].fillna(-1).to_numpy(), tr.loc[m_tr, y].to_numpy()
        Xt, Yt = te.loc[m_te, feats].fillna(-1).to_numpy(), te.loc[m_te, y].to_numpy()
        cand = {}
        # AI00 recipe-from-history: previous cycle at the same elapsed time; fallback train median per use case
        med = tr.loc[m_tr].groupby("use_case")[y].median()
        base = te.loc[m_te, prevcol].fillna(te.loc[m_te, "use_case"].map(med)).to_numpy()
        cand["AI00_prev_cycle"] = dict(p50=base)
        if lastcol:
            cand["AI01_persistence"] = dict(p50=te.loc[m_te, lastcol].to_numpy())
        cand["AI02_uc_median"] = dict(p50=te.loc[m_te, "use_case"].map(med).to_numpy())
        for name, mk in (("AI03_ridge", lambda: Ridge(1.0)),
                         ("AI04_rf", lambda: RandomForestRegressor(200, min_samples_leaf=20, n_jobs=-1, random_state=seed)),
                         ("AI05_xgb", lambda: xgb.XGBRegressor(n_estimators=400, max_depth=8, learning_rate=0.05,
                                                               subsample=0.8, colsample_bytree=0.8, random_state=seed,
                                                               tree_method="hist"))):
            t0 = time.time(); mdl = mk().fit(X, Y); fit = time.time() - t0
            t0 = time.time(); p = mdl.predict(Xt); runtime.append(dict(target=y, model=name, fit_s=fit,
                                                                         predict_ms=1e3 * (time.time() - t0) / max(len(Xt), 1)))
            cand[name] = dict(p50=p)
        t0 = time.time()
        q = {qq: _lgb_q(X, Y, Xt, qq, seed, store, y) for qq in QS}
        lo, mid, hi = np.sort(np.vstack([q[0.1], q[0.5], q[0.9]]), axis=0)          # no quantile crossing
        runtime.append(dict(target=y, model="AI10_lgbm_quantile", fit_s=time.time() - t0, predict_ms=np.nan))
        cand["AI10_lgbm_quantile"] = dict(p10=lo, p50=mid, p90=hi)
        scale = max(np.mean(np.abs(Yt)), 1e-9)
        mae_pers = np.mean(np.abs(cand["AI00_prev_cycle"]["p50"] - Yt))
        for name, c in cand.items():
            e = c["p50"] - Yt
            row = dict(dataset="DS05", target=y, model=name, n_test=len(Yt), mae=np.mean(np.abs(e)),
                       rmse=np.sqrt(np.mean(e ** 2)), nmae=np.mean(np.abs(e)) / scale,
                       skill_vs_prev_cycle=1 - np.mean(np.abs(e)) / mae_pers if mae_pers > 0 else np.nan)
            if "p10" in c:
                row["coverage80"] = float(np.mean((Yt >= c["p10"]) & (Yt <= c["p90"])))
                row["pinball"] = float(np.mean([np.mean(np.maximum(qq * (Yt - c[k]), (qq - 1) * (Yt - c[k])))
                                                for qq, k in zip(QS, ("p10", "p50", "p90"))]))
            metrics.append(row)
        keep = te.loc[m_te, ["use_case", "cycle_file", "elapsed_min"]].reset_index(drop=True)
        best = cand["AI10_lgbm_quantile"]
        preds.append(keep.assign(target=y, y=Yt, p10=best["p10"], p50=best["p50"], p90=best["p90"],
                                 base=cand["AI00_prev_cycle"]["p50"]))
        print(y, "done", flush=True)
    import joblib
    joblib.dump(dict(models=store, feats=feats, uc_codes=dict(zip(df.use_case.astype("category").cat.categories,
                                                                   range(df.use_case.nunique())))), out / "ai_models.joblib")
    pd.DataFrame(metrics).assign(boundary="LOCAL_RUN(DS05 MEASURED)").to_csv(out / "model_metrics.csv", index=False)
    pd.DataFrame(runtime).to_csv(out / "runtime_metrics.csv", index=False)
    pd.concat(preds).to_parquet(out / "forecast_predictions.parquet", index=False)
    (out / "manifest.json").write_text(json.dumps(dict(proc=str(proc), stride=stride, max_train=max_train, seed=seed,
                                                       n_samples=len(df), n_train_used=len(tr), n_test=len(te),
                                                       split="per use case chronological 70/15/15"), indent=1))
    return pd.DataFrame(metrics)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--proc", required=True); ap.add_argument("--out", default="runs/ai/ds05")
    ap.add_argument("--stride", type=int, default=15); ap.add_argument("--max_train", type=int, default=400_000)
    a = ap.parse_args()
    print(run(a.proc, a.out, a.stride, a.max_train).round(4).to_string())
