"""Run 3 AI14/AI15: source/sink phase segmentation and phase-aligned recipe forecasting on DS05 cycles.

A cycle is a sequence of phases C (charge = sink), D (discharge = source), I (rest) on 1-min bins.
AI14: timing error of each phase transition when predicted by the time-indexed recipe (previous cycle, same module).
AI15: phase-aligned recipe: align the previous cycle by phase index (not by elapsed time); the running phase ends at
      max(elapsed in phase, recipe phase length); later phases follow the recipe. Uses only past telemetry.
"""
import numpy as np

THR_KW = 0.01      # module-level kW above which a bin is C or D (rest otherwise)
MIN_BINS = 3       # shorter runs are merged into the previous phase (debounce)


def states(ch, ds, thr=THR_KW):
    ch, ds = np.asarray(ch, float), np.asarray(ds, float)
    return np.where(ch > thr, "C", np.where(ds > thr, "D", "I"))


def segments(ch, ds, thr=THR_KW, min_bins=MIN_BINS):
    """[(state, start_bin, length)] with runs shorter than min_bins merged into the previous segment."""
    st = states(ch, ds, thr); out = []
    for i, s in enumerate(st):
        if out and out[-1][0] == s:
            out[-1][2] += 1
        elif out and out[-1][2] < min_bins and len(out) > 1 and out[-2][0] == s:
            short = out.pop(); out[-1][2] += short[2] + 1         # flicker: fold back into the phase before it
        else:
            out.append([s, i, 1])
    merged = []
    for s, b, n in out:
        if merged and merged[-1][0] == s:
            merged[-1][2] += n
        else:
            merged.append([s, b, n])
    return [tuple(x) for x in merged]


def transitions(ch, ds, **kw):
    """Bins at which a new phase starts (excluding 0)."""
    return [b for _, b, _ in segments(ch, ds, **kw)[1:]]


def is_phase_structured(seg, max_phases=20):
    """FFR-like cycles flip every few bins: no usable phase structure."""
    return 1 < len(seg) <= max_phases


def phase_at(seg, b):
    """(phase index, bins elapsed in that phase) at bin b (b = number of observed bins)."""
    for k, (_, s0, n) in enumerate(seg):
        if b < s0 + n:
            return k, b - s0
    return len(seg) - 1, b - seg[-1][1]


def aligned_forecast(obs_ch, obs_ds, prev_ch, prev_ds):
    """Phase-aligned remaining trajectory (ch, ds) after the observed bins, module kW per 1-min bin.
    Falls back to the time-indexed recipe tail when phases cannot be matched."""
    b = len(obs_ch); prev_ch, prev_ds = np.asarray(prev_ch, float), np.asarray(prev_ds, float)
    tail = (prev_ch[b:], prev_ds[b:])
    so, sp = segments(obs_ch, obs_ds), segments(prev_ch, prev_ds)
    if not (is_phase_structured(sp) and so) or len(so) > len(sp) or any(a[0] != c[0] for a, c in zip(so, sp)):
        return tail, False
    k, e = phase_at(so, b)
    st, s0, n = sp[k]
    rem_cur = max(n - e, 0)
    lvl_c = float(np.mean(obs_ch[-min(e, 5):])) if e > 0 else float(np.mean(prev_ch[s0:s0 + n]))
    lvl_d = float(np.mean(obs_ds[-min(e, 5):])) if e > 0 else float(np.mean(prev_ds[s0:s0 + n]))
    cur_c, cur_d = np.full(rem_cur, lvl_c), np.full(rem_cur, lvl_d)   # running phase: persistence of its level
    rest = s0 + n
    return (np.r_[cur_c, prev_ch[rest:]], np.r_[cur_d, prev_ds[rest:]]), True


def transition_errors(cur_ch, cur_ds, prev_ch, prev_ds, at_bins):
    """For each decision bin b: |predicted - true| bins of the NEXT transition after b, for the time-indexed recipe
    (AI00) and the phase-aligned recipe (AI15). Returns list of (b, err_recipe, err_aligned) or NaN when none."""
    tt = transitions(cur_ch, cur_ds); out = []
    tp = transitions(prev_ch, prev_ds)
    for b in at_bins:
        nxt = [t for t in tt if t > b]
        if not nxt:
            continue
        true_t = nxt[0]
        rec = [t for t in tp if t > b]
        e_rec = abs(rec[0] - true_t) if rec else np.nan
        (fc, fd), ok = aligned_forecast(cur_ch[:b], cur_ds[:b], prev_ch, prev_ds)
        ta = transitions(np.r_[cur_ch[:b], fc], np.r_[cur_ds[:b], fd])
        al = [t for t in ta if t > b]
        e_al = abs(al[0] - true_t) if al else np.nan
        out.append((b, e_rec, e_al))
    return out
