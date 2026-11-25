"""ReGenATE AI engine (Model A source/sink power, Model B remaining duration, Model C quantiles) + scheduler profiles.

Interface (user AI plan s13):
    eng = AIEngine.load("ai_models.joblib")
    eng.predict(telemetry=dict(ch=..., ds=..., v=..., t_amb=...), elapsed_min=b, prev_cycle=(ch, ds), use_case="TOU")
    -> {"source_power": {"p10","p50","p90"} per slot h in (1,4,16), "sink_power": ..., "remaining_duration": {...} minutes,
        "prediction_valid": bool, "physics_check": str}
Physics consistency: powers clipped to [0, rated]; remaining >= 1 slot; quantiles sorted. Invalid -> caller falls back
to the nominal recipe (AI-G10).

Scheduler variants (same rolling MILP; only the information differs):
  P0 nominal recipe (previous cycle of the module) for every job
  P1 power AI for running jobs (next 4 h from Model A P50), nominal length
  P2 duration AI for running jobs (nominal shape time-warped to elapsed + Model B P50 remaining)
  P3 joint (P1 power for next 4 h, P2 length)
  P4 robust joint (P3 with Model B P90 remaining -> station released later, conservative)
Queued jobs use the nominal recipe in every variant (no telemetry before start).
Run 3 diagnostic variants (same rolling MILP; information decomposition, not deployable):
  P1*..P4*  the P1..P4 integration fed with PERFECT forecasts (true slot means / true remaining) -> integration loss
  P5        phase-aligned recipe for running jobs (AI15a, no learning): previous cycle aligned by phase, not elapsed time
  P5s       P5 only for use cases selected on the VALIDATION split (AI18 selective; others fall back to P0)
  PQ        queued jobs: previous cycle time-warped/scaled by the cycle-level model (cycle_model.py); running jobs nominal
  PQ5       PQ for queued jobs + P5 for running jobs
  PQd/PQd*  duration-only queued-job forecast (recipe energy kept), gated model / perfect duration
  PQ*       PQ integration fed the TRUE duration/energy ratios (diagnostic: value of perfect cycle-level forecasts)
  TR_RUN    true full profile for running jobs only; TR_Q true profile for queued jobs only; TR_ALL rolling oracle
"""
import numpy as np
from regenate.forecasting.ds05_bench import HORIZONS, SLOT, features_at

TRACE_PER_SLOT = SLOT     # 1-min bins per 15-min slot


class AIEngine:
    def __init__(self, bundle, rated_kw=None, scale=1.0):
        self.m, self.feats, self.uc = bundle["models"], bundle["feats"], bundle["uc_codes"]
        self.cqr = bundle.get("cqr", {})              # conformal widening of P10/P90 (AI-G04), 0 if absent
        self.rated, self.scale = rated_kw, scale

    @classmethod
    def load(cls, path, **kw):
        import joblib
        return cls(joblib.load(path), **kw)

    def _row(self, f, use_case):
        f = dict(f, uc_code=self.uc.get(use_case, -1))
        return np.array([[f.get(c, np.nan) for c in self.feats]], float)

    def _q(self, target, X):
        out = np.sort(np.array([self.m[(target, q)].predict(np.nan_to_num(X, nan=-1.0))[0] for q in (0.1, 0.5, 0.9)]))
        w = self.cqr.get(target, 0.0)
        return np.array([out[0] - w, out[1], out[2] + w])

    def predict(self, telemetry, elapsed_min, prev_cycle, use_case):
        """telemetry arrays are module-level kW (as in training); outputs are module-level, multiply by scale outside."""
        ch, ds, v, ta = (np.asarray(telemetry[k], float) for k in ("ch", "ds", "v", "t_amb"))
        b = int(elapsed_min)
        X = self._row(features_at(ch, ds, v, ta, b, prev_cycle), use_case)
        res = dict(source_power={}, sink_power={}, remaining_duration=None)
        for h in HORIZONS:
            res["sink_power"][h] = np.clip(self._q(f"y_ch_h{h}", X), 0, None)
            res["source_power"][h] = np.clip(self._q(f"y_ds_h{h}", X), 0, None)
        res["remaining_duration"] = np.maximum(self._q("y_rem_min", X), SLOT)
        ok = all(np.all(np.isfinite(v)) for d in (res["sink_power"], res["source_power"]) for v in d.values())
        if self.rated:
            ok &= all(v[1] <= self.rated * 1.05 for d in (res["sink_power"], res["source_power"]) for v in d.values())
        res["prediction_valid"] = bool(ok); res["physics_check"] = "clipped>=0, sorted quantiles, rated" if ok else "fail"
        return res


def _interp_slots(pred, n):
    """Per-slot P50 for slots 1..n from the predicted horizons (piecewise-linear in slot index)."""
    hs = np.array(HORIZONS, float); vals = np.array([pred[h][1] for h in HORIZONS])
    return np.interp(np.arange(1, n + 1), hs, vals)


def _warp(a, n):
    """Time-warp a 1-D profile to length n (linear resampling)."""
    if len(a) == 0 or n <= 0:
        return np.zeros(max(n, 0))
    return np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a)


def _perfect(trace, b, k):
    """Perfect forecast in the engine's output format: true slot-mean power at HORIZONS and true remaining minutes."""
    ch, ds = (np.asarray(x, float) / k for x in trace)
    sm = lambda a, h: a[b + (h - 1) * SLOT: b + h * SLOT].mean() if b + (h - 1) * SLOT < len(a) else 0.0
    rem = max(len(ch) - b, SLOT)
    return dict(sink_power={h: np.full(3, sm(ch, h)) for h in HORIZONS}, source_power={h: np.full(3, sm(ds, h)) for h in HORIZONS},
                remaining_duration=np.full(3, float(rem)), prediction_valid=True)


P5_USE_CASES = ("EFR", "PV", "PV-TOU")   # AI14 val split: aligned timing skill > 0.1 (runs/run3/ai14/ai14_val_summary.csv)


def _queued_pred(inst, jid, k, spm, r):
    """Previous-cycle recipe warped to the predicted duration and scaled to the predicted charge/discharge energy."""
    from regenate.data.bench_v2 import _bin
    pch, pds = (np.asarray(x, float) for x in inst["nominal"][jid])
    n = max(spm, int(round(len(pch) * r["r_dur"])))
    wc, wd = _warp(pch, n), _warp(pds, n)
    sc = r["r_ech"] * pch.sum() / max(wc.sum(), 1e-12); sd = r["r_eds"] * pds.sum() / max(wd.sum(), 1e-12)   # E = E_prev * r_e
    pin, prec = _bin(wc * sc, spm), _bin(wd * sd, spm)
    return pin, prec, np.zeros_like(pin)


def make_profile_fn(inst, variant, engine=None, dt_h=0.25, p5_use_cases=P5_USE_CASES, cycle_pred=None):
    """profile_fn(jid, run_obs) for regenate.optimization.rolling.Replanner on a bench-v2 instance."""
    from regenate.data.bench_v2 import job_profile
    J = inst["jobs"].set_index("job_id"); k = inst["meta"]["modules_per_station"]
    spm = int(round(dt_h / inst["trace_dt_h"]))       # trace bins per slot

    base, perfect = variant.rstrip("*"), variant.endswith("*")

    def fn(jid, run_obs):
        nom = job_profile(inst, jid, dt_h, "nominal")
        if variant.startswith("TR_"):
            use_truth = {"TR_ALL": True, "TR_RUN": run_obs is not None, "TR_Q": run_obs is None}[variant]
            return job_profile(inst, jid, dt_h, "truth") if use_truth else nom
        if variant in ("PQ*", "PQd*") and run_obs is None:        # perfect cycle-level ratios, same warp integration
            (tc, td), (pc, pd_) = inst["traces"][jid], inst["nominal"][jid]
            r = dict(r_dur=len(tc) / max(len(pc), 1), r_ech=float(np.sum(tc)) / max(float(np.sum(pc)), 1e-12),
                     r_eds=float(np.sum(td)) / max(float(np.sum(pd_)), 1e-12))
            if variant == "PQd*":
                r.update(r_ech=1.0, r_eds=1.0)
            return _queued_pred(inst, jid, k, spm, r)
        if variant in ("PQ", "PQ5", "PQd") and run_obs is None:
            cf = J.loc[jid, "cycle_file"]
            if cycle_pred is None or cf not in cycle_pred:
                return nom
            r = dict(cycle_pred[cf])
            if variant == "PQd":                                   # duration only: recipe energy kept
                if abs(np.log(max(r["r_dur"], 1e-12))) < 1e-12:
                    return nom
                r.update(r_ech=1.0, r_eds=1.0)
            return _queued_pred(inst, jid, k, spm, r)
        if variant in ("P5", "P5s", "PQ5") and run_obs is not None:
            if variant == "P5s" and J.loc[jid, "use_case"] not in p5_use_cases:
                return nom
            from regenate.data.bench_v2 import _bin
            from regenate.forecasting.phase import aligned_forecast
            b = int(round(run_obs["elapsed_h"] / inst["trace_dt_h"]))
            ch_t, ds_t = (np.asarray(x, float) / k for x in inst["traces"][jid])
            pch, pds = (np.asarray(x, float) / k for x in inst["nominal"][jid])
            (fc, fd), _ = aligned_forecast(ch_t[:b], ds_t[:b], pch, pds)
            fc, fd = (np.r_[o[:b], f] if len(f) else np.r_[o[:b], o[b - 1:b]] for o, f in ((ch_t, fc), (ds_t, fd)))
            pin, prec = _bin(fc, spm) * k, _bin(fd, spm) * k
            return pin, prec, np.zeros_like(pin)
        if run_obs is None or base in ("P0", "P5", "P5s", "PQ", "PQ5", "PQd") or variant in ("PQ*", "PQd*") or (engine is None and not perfect):
            return nom
        b = int(round(run_obs["elapsed_h"] / inst["trace_dt_h"]))          # minutes elapsed (observed telemetry)
        e = b // spm                                                       # whole slots elapsed
        if b < 60:
            return nom                                                     # model trained from 60 min onwards
        ch_t, ds_t = (x / k for x in inst["traces"][jid])                 # module-level telemetry (past only used)
        ch_t, ds_t = ch_t[:b], ds_t[:b]
        v, ta = (np.asarray(x[:b], float) for x in inst["telem"][jid])
        prev = tuple(x / k for x in inst["nominal"][jid])
        if perfect:
            p = _perfect(inst["traces"][jid], b, k)
        else:
          try:
            p = engine.predict(dict(ch=np.r_[ch_t, 0], ds=np.r_[ds_t, 0], v=np.r_[v, v[-1]], t_amb=np.r_[ta, ta[-1]]),
                               b, prev, J.loc[jid, "use_case"])
          except Exception:
            return nom
        if not p["prediction_valid"]:
            return nom
        obs_in = np.array([ch_t[i * spm:(i + 1) * spm].mean() for i in range(e)]) * k
        obs_rec = np.array([ds_t[i * spm:(i + 1) * spm].mean() for i in range(e)]) * k
        n_nom_rem = max(1, len(nom[0]) - e)
        rem_q = np.asarray(p["remaining_duration"], float)
        if not np.all(np.isfinite(rem_q)):
            return nom                                                     # AI-G10 fallback on non-finite duration
        if base in ("P2", "P3"):
            n_rem = max(1, int(round(rem_q[1] / (spm))))
        elif base == "P4":
            n_rem = max(1, int(round(rem_q[2] / (spm))))
        else:
            n_rem = n_nom_rem
        tail_in = _warp(nom[0][e:], n_rem) if base in ("P2", "P3", "P4") else np.pad(nom[0][e:], (0, max(0, n_rem - n_nom_rem)))[:n_rem]
        tail_rec = _warp(nom[1][e:], n_rem) if base in ("P2", "P3", "P4") else np.pad(nom[1][e:], (0, max(0, n_rem - n_nom_rem)))[:n_rem]
        if base in ("P1", "P3", "P4"):
            m = min(16, n_rem)
            tail_in[:m] = _interp_slots(p["sink_power"], m) * k
            tail_rec[:m] = _interp_slots(p["source_power"], m) * k
        pin = np.r_[obs_in, np.clip(tail_in, 0, None)]; prec = np.r_[obs_rec, np.clip(tail_rec, 0, None)]
        if not (np.all(np.isfinite(pin)) and np.all(np.isfinite(prec))):
            return nom                                                     # AI-G10: never pass non-finite power on
        return pin, prec, np.zeros_like(pin)

    return fn
