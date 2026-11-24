"""Paired statistics and section-7 KPIs over runs/<campaign>/results.csv (unit = instance)."""
import numpy as np
import pandas as pd


def paired_ci(a, b, n_boot=10_000, seed=0, level=0.95):
    """Mean of (a - b) over paired instances with a percentile bootstrap CI."""
    d = np.asarray(a, float) - np.asarray(b, float)
    if d.size == 0:
        return dict(n=0, mean=np.nan, lo=np.nan, hi=np.nan, wins=0)
    rng = np.random.default_rng(seed)
    bs = d[rng.integers(0, d.size, (n_boot, d.size))].mean(1)
    q = (1 - level) / 2
    return dict(n=int(d.size), mean=float(d.mean()), median=float(np.median(d)), std=float(d.std(ddof=1)) if d.size > 1 else 0.0,
                lo=float(np.quantile(bs, q)), hi=float(np.quantile(bs, 1 - q)), wins=int(np.sum(d > 1e-9)))


def wide(df, value="net_kwh"):
    return df.pivot_table(index="instance_id", columns="method", values=value, aggfunc="first")


COMPARISONS = [  # (label, a, b): positive mean = b uses less than a
    ("B1 -> B0 (regen hardware)", "B0", "B1"),
    ("B2 vs B1 (shared DC, same FIFO)", "B1", "B2"),
    ("B3 vs B2 (static optimisation)", "B2", "B3"),
    ("P0 vs B3 (rolling adaptation)", "B3", "P0"),
    ("P vs P0 (AI forecast, dE_AI)", "P0", "P"),
    ("P vs B1-OPT", "B1-OPT", "P"),
    ("P vs B1p-OPT (kill test)", "B1p-OPT", "P"),
    ("ORACLE vs P (oracle gap)", "P", "ORACLE"),
    ("ORACLE vs B1p-OPT (ceiling of shared DC)", "B1p-OPT", "ORACLE"),
]


def ladder_table(df, value="net_kwh", equal_tt=True, tol=1e-6):
    """Paired comparisons; with equal_tt only instances where both methods have the same TT."""
    W = wide(df, value); T = wide(df, "TT_h")
    out = []
    for label, a, b in COMPARISONS:
        if a not in W or b not in W:
            continue
        m = W[[a, b]].notna().all(1)
        if equal_tt:
            m &= (T[a] - T[b]).abs() <= tol
        r = paired_ci(W.loc[m, a], W.loc[m, b])
        base = W.loc[m, a]
        r["pct_of_a"] = float(100 * r["mean"] / base.mean()) if m.any() and base.mean() > 0 else np.nan
        out.append(dict(comparison=label, a=a, b=b, **r))
    return pd.DataFrame(out)


def match_ratio(df):
    return df["direct_reuse_kwh"] / df["recoverable_kwh"].where(df["recoverable_kwh"] > 0)
