"""Rolling-horizon replanner for P0 / P (WP07). Same MILP, constraints, period and time limit for both;
they differ ONLY in the information used for prediction:
  P0 : recipe nominal duration and kappa = 1 for every job (no learning, no in-progress update)
  P  : running jobs' total duration and kappa re-estimated from the observed M2 trace (least squares over the
       recipe shape, `estimate_running`); queued jobs use `prior(job)` (default nominal — see docs D002: in
       bench_v1 the queued-job deviation is i.i.d. noise, so no prior can beat nominal in expectation).
The replanner returns plans only for NOT-started jobs; Replay freezes running/done jobs and applies the
engineer gate and fallback.
"""
import math
import numpy as np
from regenate.data.generator import render
from regenate.electrical.ledger import ElecParams
from regenate.optimization.milp import Job, solve


def _profile(inst, jid, dur_h, kappa, slot_h):
    """Slot profile of one job with a hypothesised duration and kappa (shape = recipe)."""
    one = inst["jobs"].loc[inst["jobs"].job_id == jid].copy()
    one["dur_true_h"] = dur_h; one["kappa_true"] = kappa
    p_in, p_rec, aux = render(dict(inst, jobs=one), {jid: 0}, {jid: 0.0}, slot_h, truth=True)
    return p_in[0], p_rec[0], aux[0]


def estimate_running(inst, jid, trace, dt_h, n_grid=41):
    """(dur_h, kappa) minimising squared error of the observed partial trace vs the recipe shape."""
    row = inst["jobs"].set_index("job_id").loc[jid]
    obs = np.r_[np.asarray(trace["p_in_kw"]), np.asarray(trace["p_rec_kw"])]
    n = len(trace["p_in_kw"])
    if n == 0 or not np.any(obs):
        return float(row.dur_nom_h), 1.0
    best = (np.inf, float(row.dur_nom_h), 1.0)
    for d in np.linspace(0.5, 1.5, n_grid) * float(row.dur_nom_h):
        d = max(d, n * dt_h)                                        # cannot have ended already
        pi, pr, _ = _profile(inst, jid, d, 1.0, dt_h)
        shape = np.r_[np.pad(pi, (0, max(0, n - len(pi))))[:n], np.pad(pr, (0, max(0, n - len(pr))))[:n]]
        k = float(shape @ obs / (shape @ shape)) if shape @ shape > 0 else 1.0
        err = float(np.sum((obs - k * shape) ** 2))
        if err < best[0] - 1e-12:
            best = (err, float(d), k)
    return best[1], best[2]


class Replanner:
    def __init__(self, inst, mode="P0", slot_h=0.25, prm=None, flex=1.0, time_limit=10.0, prior=None, profile_fn=None):
        """profile_fn(jid, run_obs_or_None) -> (p_in, p_rec, p_aux) predicted FULL-job slot profile (bench v2 / AI
        variants). When given it replaces predict()/_profile(); mode is then only a label."""
        self.profile_fn = profile_fn
        self.inst, self.mode, self.slot, self.prm = inst, mode, slot_h, prm or ElecParams()
        self.flex, self.time_limit = flex, time_limit
        self.J = inst["jobs"].set_index("job_id")
        self.prior = prior or (lambda r: (float(r.dur_nom_h), 1.0))
        self.S = list(inst["stations"].station_id)
        self._key = None; self.n_solves = 0; self.solve_s = 0.0

    def predict(self, jid, run_obs):
        r = self.J.loc[jid]
        if run_obs is None:
            return self.prior(r) if self.mode == "P" else (float(r.dur_nom_h), 1.0)
        if self.mode == "P0":
            return float(r.dur_nom_h), 1.0
        return estimate_running(self.inst, jid, run_obs["partial_power_trace"], self.inst["dt_h"])

    def __call__(self, obs):
        t = obs["t_h"]; sl = self.slot; t0 = math.ceil(t / sl - 1e-9) * sl
        running = obs["running"]; queued = [j for j in obs["queued"] if j not in running]
        if not queued:
            return {}
        if self.profile_fn is not None:
            prof = {j: self.profile_fn(j, running.get(j)) for j in list(running) + queued}
            pred = {j: (len(prof[j][0]) * sl, 1.0) for j in prof}
            key = (tuple(sorted(queued)), tuple(sorted((j, len(prof[j][0]), round(float(np.sum(prof[j][0]) - np.sum(prof[j][1])), 4))
                                                      for j in running)))
        else:
            prof = None
            pred = {j: self.predict(j, running.get(j)) for j in list(running) + queued}
            key = (tuple(sorted(queued)), tuple(sorted((j, round(v[0], 6), round(v[1], 6)) for j, v in pred.items() if j in running)))
        if key == self._key:
            return {}                                                 # nothing new -> keep plan
        jobs, ids, free = [], [], {s: 0 for s in self.S}
        for j, ro in running.items():                                 # fixed: remaining profile, start now
            d, k = pred[j]; pi, pr, ax = prof[j] if prof else _profile(self.inst, j, d, k, sl)
            e = int(round(ro["elapsed_h"] / sl)); rem = max(1, len(pi) - e)
            pi, pr, ax = (np.pad(a, (0, max(0, e + rem - len(a))))[e:e + rem] for a in (pi, pr, ax))
            jobs.append(Job(0, 0, (self.J.loc[j, "due_h"] - t0) / sl, pi, pr, ax)); ids.append(j)
            free[ro["station"]] = rem
        n_fixed = len(jobs)
        for j in queued:
            r = self.J.loc[j]; d, k = pred[j]; pi, pr, ax = prof[j] if prof else _profile(self.inst, j, d, k, sl)
            rel = max(0, math.ceil((r.release_h - t0) / sl - 1e-9))
            lat = int(math.floor((min(r.deadline_h - d, r.release_h + self.flex * r.max_shift_h) - t0) / sl + 1e-9))
            jobs.append(Job(rel, max(rel, lat), (r.due_h - t0) / sl, pi, pr, ax)); ids.append(j)
        K = max(j.latest + j.dur for j in jobs) + 1
        res = solve(jobs, len(self.S), K, "DC", self.prm, sl, time_limit=self.time_limit,
                    fixed={i: 0 for i in range(n_fixed)})
        if not res.starts:                                            # widen windows to deadlines only
            for jb, j in zip(jobs[n_fixed:], queued):
                r = self.J.loc[j]
                jb.latest = max(jb.release, int((r.deadline_h - pred[j][0] - t0) // sl))
            K = max(j.latest + j.dur for j in jobs) + 1
            res = solve(jobs, len(self.S), K, "DC", self.prm, sl, time_limit=self.time_limit,
                        fixed={i: 0 for i in range(n_fixed)})
        self.n_solves += 1; self.solve_s += res.info.get("solve_s", 0.0)
        if not res.starts:
            raise RuntimeError(f"replan infeasible: {res.status}")
        plan = {}
        for i in sorted(range(n_fixed, len(jobs)), key=lambda i: res.starts[i]):
            s = min(self.S, key=lambda s: (free[s] > res.starts[i], free[s]))   # earliest-free station
            plan[ids[i]] = (s, t0 + res.starts[i] * sl)
            free[s] = max(free[s], res.starts[i]) + jobs[i].dur
        self._key = key
        return plan
