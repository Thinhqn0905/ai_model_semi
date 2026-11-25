"""Exact start-time MILP (HiGHS via scipy.optimize.milp) — one engine for B1-OPT, B1p-OPT, B3, P0, P, ORACLE.

Decision x[j,t] = 1 if job j starts at slot t (t in its allowed window). Recipe and duration fixed.
Lexicographic: (1) total tardiness, (2) net energy at M0 (ledger of regenate.electrical.ledger at slot
resolution). Peak is computed afterwards with the ledger (not optimised yet).

Station aggregation: stations are identical and every job is eligible on every station, so a start
plan is feasible iff at every slot #running <= S (interval graph colouring); stations are assigned
afterwards (`assign_stations`). Own-station reuse is then a per-job quantity, so in-rack use is
precomputed and only residual demand/source enter the LP.
shortcut: downtime is modelled as cell capacity per slot; exact only if downtime hits interchangeable
stations — upgrade to per-station x[j,s,t] if station-specific eligibility/downtime matters.
"""
from dataclasses import dataclass, field
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix, vstack, csr_matrix
from regenate.electrical.ledger import ElecParams


@dataclass
class Job:
    release: int                  # earliest start slot
    latest: int                   # latest start slot (deadline - dur and max_shift folded in)
    due: float                    # soft due (slot units) for tardiness
    p_in: np.ndarray              # kW per slot of the job (len = duration)
    p_rec: np.ndarray
    p_aux: np.ndarray = None      # AC aux kW per slot (chamber), optional

    @property
    def dur(self):
        return len(self.p_in)


@dataclass
class Result:
    starts: list
    tt: float
    net_kwh: float
    status: str
    mip_gap: float = 0.0
    info: dict = field(default_factory=dict)


def _coeffs(job, topology, prm):
    """Per-slot coefficients of the job on the cell, at the boundary the LP needs."""
    a = job.p_aux if job.p_aux is not None else np.zeros(job.dur)
    if topology in ("B0", "B1"):
        ac = job.p_in / prm.eta_sup_ac + a
        if topology == "B0":
            ac = ac + (job.p_rec / prm.cop if prm.hvac_on_dump else 0)
        else:
            ac = ac - job.p_rec * prm.eta_rl_ac
        return dict(ac=ac)
    d = job.p_in / prm.eta_sup_dc; r = job.p_rec * prm.eta_rl_dc; u = np.minimum(d, r)
    return dict(d1=d - u, r1=r - u, aux=a)


def solve(jobs, S, K, topology="DC", prm=None, dt_h=0.25, idle_kw=0.0, cap=None,
          tt_first=True, tt_slack=1e-6, time_limit=60.0, fixed=None, peak_stage=False, e_tol=1e-4):
    """fixed: {job_index: start_slot} frozen decisions (rolling horizon).
    peak_stage: third lexicographic level — minimise peak M0 import s.t. TT <= TT* and energy <= E*(1+e_tol)."""
    prm = prm or ElecParams()
    cap = np.full(K, S, float) if cap is None else np.asarray(cap, float)
    fixed = fixed or {}
    # --- start variables
    win = []
    for j, jb in enumerate(jobs):
        if j in fixed:
            ts = [fixed[j]]
        else:
            ts = [t for t in range(jb.release, jb.latest + 1) if t + jb.dur <= K]
        if not ts:
            return Result([], np.inf, np.inf, "infeasible-window", info=dict(job=j))
        win.append(ts)
    xi = []; col = 0
    for ts in win:
        xi.append(list(range(col, col + len(ts)))); col += len(ts)
    nx = col
    nT = len(jobs)                                     # tardiness vars
    dc = topology == "DC"; inrack = topology == "B1p"
    # LP energy vars per slot k: DC: [x_link, e_imp, e_exp, dump] ; B1p: [e_exp_res, dump] ; B0/B1: none
    nv_k = 4 if dc else (2 if inrack else 0)
    nE = nv_k * K
    n = nx + nT + nE
    iT, iE = nx, nx + nT
    C = [_coeffs(jb, topology, prm) for jb in jobs]

    rows, lo, hi = [], [], []

    def add(row, l, h):
        rows.append(row); lo.append(l); hi.append(h)

    # each job starts exactly once
    for j in range(len(jobs)):
        r = lil_matrix((1, n)); r[0, xi[j]] = 1; add(r, 1, 1)
    # capacity per slot
    occ = lil_matrix((K, n))
    for j, jb in enumerate(jobs):
        for v, t in zip(xi[j], win[j]):
            occ[t:t + jb.dur, v] = 1
    rows.append(occ); lo.extend([-np.inf] * K); hi.extend(cap.tolist())
    # tardiness: T_j >= sum (t+dur) x - due
    for j, jb in enumerate(jobs):
        r = lil_matrix((1, n)); r[0, xi[j]] = [t + jb.dur for t in win[j]]; r[0, iT + j] = -1
        add(r, -np.inf, jb.due)

    # build per-slot linear expressions of the job-dependent profiles: M_key[k, :] @ z
    def prof_matrix(key):
        M = lil_matrix((K, n))
        for j, jb in enumerate(jobs):
            p = C[j][key]
            for v, t in zip(xi[j], win[j]):
                for tau in np.nonzero(p)[0]:
                    M[t + tau, v] += p[tau]
        return M.tocsr()

    run = occ.tocsr()
    const_ac = idle_kw * S                             # idle stations: idle_kw * (S - running)
    run_ac = -idle_kw * run
    if topology in ("B0", "B1"):
        ACM = prof_matrix("ac") + run_ac
    else:
        D1, R1, AUX = prof_matrix("d1"), prof_matrix("r1"), prof_matrix("aux")
        ACM = AUX + run_ac
        E = lambda m, k: iE + nv_k * k + m
        if dc and np.isfinite(prm.P_bus_max):          # E1: total residual sink / source on the shared bus
            rows.append(D1); lo.extend([-np.inf] * K); hi.extend([prm.P_bus_max] * K)
            rows.append(R1); lo.extend([-np.inf] * K); hi.extend([prm.P_bus_max] * K)
        if dc and np.isfinite(prm.dP_step_max):        # E1: |net(k) - net(k-1)| <= dP (net residual DC demand)
            NET = (D1 - R1).tolil(); dN = NET[1:] - NET[:-1]
            rows.append(dN); lo.extend([-prm.dP_step_max] * (K - 1)); hi.extend([prm.dP_step_max] * (K - 1))
        for k in range(K):
            if dc:                                     # x <= D1, x <= eta_link R1, x <= Plink
                r = D1[k].tolil(); r[0, E(0, k)] = -1; add(r, 0, np.inf)
                r = (prm.eta_link * R1[k]).tolil(); r[0, E(0, k)] = -1; add(r, 0, np.inf)
                # e_imp = D1 - x   ;  e_imp <= P_afe
                r = D1[k].tolil(); r[0, E(0, k)] = -1; r[0, E(1, k)] = -1; add(r, 0, 0)
                # e_exp + dump = R1 - x/eta_link
                r = R1[k].tolil(); r[0, E(0, k)] = -1 / prm.eta_link; r[0, E(2, k)] = -1; r[0, E(3, k)] = -1
                add(r, 0, 0)
            else:                                      # B1p: e_exp + dump = R1
                r = R1[k].tolil(); r[0, E(0, k)] = -1; r[0, E(1, k)] = -1; add(r, 0, 0)
        ACM = ACM.tolil()
        for k in range(K):
            if dc:
                ACM[k, E(1, k)] += 1 / prm.eta_afe_imp
                ACM[k, E(2, k)] -= prm.eta_afe_exp
                ACM[k, E(3, k)] += (1 / prm.cop if prm.hvac_on_dump else 0)
            else:
                ACM[k, E(0, k)] -= prm.eta_afe_exp
                ACM[k, E(1, k)] += (1 / prm.cop if prm.hvac_on_dump else 0)
            # B1p residual demand imports per station: add D1/eta_imp
        if inrack:
            ACM = ACM + D1 / prm.eta_afe_imp
        ACM = csr_matrix(ACM)
    A = vstack([csr_matrix(r) for r in rows]).tocsr()
    cons = LinearConstraint(A, np.array(lo), np.array(hi))
    lb = np.zeros(n); ub = np.full(n, np.inf); ub[:nx] = 1
    if dc:
        for k in range(K):
            ub[iE + 4 * k + 0] = prm.P_link_max
            ub[iE + 4 * k + 1] = prm.P_afe_max
            ub[iE + 4 * k + 2] = prm.P_afe_max if prm.allow_export else 0.0
    elif inrack and not prm.allow_export:
        for k in range(K):
            ub[iE + 2 * k] = 0.0
    integ = np.zeros(n); integ[:nx] = 1
    bounds = Bounds(lb, ub)
    energy_obj = np.asarray(ACM.sum(0)).ravel() * dt_h          # net kWh (const part added after)
    opts = dict(time_limit=time_limit, disp=False, mip_rel_gap=1e-6)

    tt_obj = np.zeros(n); tt_obj[iT:iT + nT] = 1
    tt_star = None
    if tt_first:
        r1 = milp(tt_obj, constraints=cons, integrality=integ, bounds=bounds, options=opts)
        if r1.x is None:
            return Result([], np.inf, np.inf, f"tt-stage:{r1.message}")
        tt_star = r1.fun
        cons = [cons, LinearConstraint(csr_matrix(tt_obj), -np.inf, tt_star + tt_slack + 1e-9 * abs(tt_star))]
    r2 = milp(energy_obj, constraints=cons, integrality=integ, bounds=bounds, options=opts)
    if r2.x is None:
        return Result([], np.inf, np.inf, f"energy-stage:{r2.message}")
    z = r2.x; peak_info = {}
    if peak_stage:                                     # append imp[k] (K) and peak (1) columns
        from scipy.sparse import hstack
        cons_l = cons if isinstance(cons, list) else [cons]
        pad = lambda M: hstack([csr_matrix(M), csr_matrix((M.shape[0], K + 1))]).tocsr()
        ext = [LinearConstraint(pad(c.A), c.lb, c.ub) for c in cons_l]
        I = csr_matrix((np.ones(K), (np.arange(K), np.arange(K))), shape=(K, K))
        ext.append(LinearConstraint(hstack([-ACM, I, csr_matrix((K, 1))]).tocsr(), const_ac, np.inf))
        ext.append(LinearConstraint(hstack([csr_matrix((K, n)), -I, csr_matrix(np.ones((K, 1)))]).tocsr(), 0, np.inf))
        ext.append(LinearConstraint(pad(csr_matrix(energy_obj)), -np.inf, r2.fun + e_tol * abs(r2.fun) + 1e-6))
        c3 = np.zeros(n + K + 1); c3[-1] = 1
        b3 = Bounds(np.r_[lb, np.zeros(K + 1)], np.r_[ub, np.full(K + 1, np.inf)])
        r3 = milp(c3, constraints=ext, integrality=np.r_[integ, np.zeros(K + 1)], bounds=b3, options=opts)
        if r3.x is not None:
            z = r3.x[:n]; peak_info = dict(peak_kw_planned=float(r3.fun), peak_status=r3.message)
        else:
            peak_info = dict(peak_status=f"peak-stage failed: {r3.message}")
    starts = [win[j][int(np.argmax(z[xi[j]]))] for j in range(len(jobs))]
    tt = float(sum(max(0.0, s + jb.dur - jb.due) for s, jb in zip(starts, jobs)))
    net = float(energy_obj @ z + const_ac * K * dt_h)
    gap = float(getattr(r2, "mip_gap", 0.0) or 0.0)
    return Result(starts, tt, net, "optimal" if r2.status == 0 else r2.message, gap,
                  dict(tt_star=tt_star, n_bin=nx, **peak_info))


def assign_stations(starts, durs, S):
    """Greedy interval colouring; exact for identical stations when capacity <= S holds."""
    order = sorted(range(len(starts)), key=lambda j: starts[j])
    free = [0] * S; out = [None] * len(starts)
    for j in order:
        s = min(range(S), key=lambda i: (free[i] > starts[j], free[i]))
        if free[s] > starts[j]:
            raise ValueError("capacity violated")
        out[j] = s; free[s] = starts[j] + durs[j]
    return out


def render_slots(jobs, starts, stations, S, K, idle_kw=0.0):
    """(S, K) p_in, p_rec, p_aux at slot resolution for regenate.electrical.ledger."""
    p_in = np.zeros((S, K)); p_rec = np.zeros((S, K)); aux = np.full((S, K), idle_kw)
    for jb, t, s in zip(jobs, starts, stations):
        sl = slice(t, t + jb.dur)
        p_in[s, sl] += jb.p_in; p_rec[s, sl] += jb.p_rec
        aux[s, sl] += (jb.p_aux if jb.p_aux is not None else 0) - idle_kw
    return p_in, p_rec, aux
