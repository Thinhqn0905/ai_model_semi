"""Fine-step, assumed-parameter DC bus plan screening; not a protection system."""
from dataclasses import dataclass
import math
import numpy as np


@dataclass
class TwinParams:
    v_nom: float = 400.0
    v_min: float = 380.0
    v_max: float = 420.0
    capacitance_f: float = 0.04
    p_afe_max_kw: float = 20.0
    k_droop_kw_per_v: float = 2.0
    tau_afe_s: float = 0.08
    v_chop: float = 415.0
    p_chop_max_kw: float = 15.0
    i_link_max_a: float = 80.0
    p_link_max_kw: float = 32.0
    ramp_kw_per_s: float = 20.0
    loss_fraction: float = 0.0
    dt_s: float = 0.001


def check_plan(p_src_kw, p_sink_kw, slot_s, params=None):
    """Screen station-by-slot DC bus powers; carry state between boundary windows.

    Gaps between windows are omitted, so returned times and chopper energy describe
    simulated windows only, not the full plan. Initially the bus is idle at nominal V.
    """
    p = params or TwinParams()
    src = np.asarray(p_src_kw, dtype=float)
    sink = np.asarray(p_sink_kw, dtype=float)
    if src.ndim == 1:
        src = src[None, :]
    if sink.ndim == 1:
        sink = sink[None, :]
    if (src.ndim != 2 or src.shape != sink.shape or not src.size or
            not np.isfinite(src).all() or not np.isfinite(sink).all() or
            (src < 0).any() or (sink < 0).any()):
        raise ValueError('powers must be matching nonempty station-by-slot arrays of finite nonnegative kW')
    values = vars(p)
    if (not all(math.isfinite(x) for x in values.values()) or
            not math.isfinite(slot_s) or slot_s <= 0 or p.dt_s <= 0 or
            p.capacitance_f <= 0 or p.tau_afe_s <= 0 or p.dt_s > p.tau_afe_s or
            p.v_nom <= 0 or not 0 < p.v_min < p.v_max or
            not p.v_chop < p.v_max or min(p.p_afe_max_kw, p.k_droop_kw_per_v,
            p.p_chop_max_kw, p.i_link_max_a, p.p_link_max_kw, p.ramp_kw_per_s) < 0 or
            not 0 <= p.loss_fraction <= 1):
        raise ValueError('invalid twin parameters')
    # Merge overlapping +/- 2 s windows, including the start and end of the plan.
    end = src.shape[1] * slot_s
    windows = []
    for k in range(src.shape[1] + 1):
        a, b = max(0.0, k * slot_s - 2), min(end, k * slot_s + 2)
        if windows and a <= windows[-1][1]:
            windows[-1] = (windows[-1][0], b)
        else:
            windows.append((a, b))
    energy = 0.5 * p.capacitance_f * p.v_nom**2
    voltage = p.v_nom
    v_min = v_max = voltage
    afe = chop_kwh = i_peak = 0.0
    actual_src = np.zeros(src.shape[0])
    actual_sink = np.zeros(src.shape[0])
    violations = []
    active = set()
    for start, stop in windows:
        t = start
        while t < stop - 1e-12:
            dt = min(p.dt_s, stop - t)
            slot = min(int(t / slot_s), src.shape[1] - 1)
            actual_src += np.clip(src[:, slot] - actual_src, -p.ramp_kw_per_s * dt, p.ramp_kw_per_s * dt)
            actual_sink += np.clip(sink[:, slot] - actual_sink, -p.ramp_kw_per_s * dt, p.ramp_kw_per_s * dt)
            source, demand = actual_src.sum(), actual_sink.sum()
            direct = min(source, demand)
            current = max(source, demand) * 1000 / max(voltage, 1e-12)
            i_peak = max(i_peak, current)
            ref = np.clip(p.k_droop_kw_per_v * (p.v_nom - voltage), -p.p_afe_max_kw, p.p_afe_max_kw)
            afe += dt / p.tau_afe_s * (ref - afe)
            chop = p.p_chop_max_kw * np.clip((voltage - p.v_chop) / (p.v_max - p.v_chop), 0, 1)
            chop_kwh += chop * dt / 3600
            energy = max(0.0, energy + 1000 * (source - demand + afe - chop - p.loss_fraction * direct) * dt)
            voltage = math.sqrt(2 * energy / p.capacitance_f)
            v_min, v_max = min(v_min, voltage), max(v_max, voltage)
            checks = {'undervoltage': (voltage < p.v_min, voltage),
                      'overvoltage': (voltage > p.v_max, voltage),
                      'overcurrent': (current > p.i_link_max_a, current),
                      'direct_power': (direct > p.p_link_max_kw, direct)}
            for kind, (bad, value) in checks.items():
                if bad and kind not in active:
                    violations.append((t + dt, kind, float(value)))
                if bad:
                    active.add(kind)
                else:
                    active.discard(kind)
            t += dt
    return dict(approved=not violations, v_min=float(v_min), v_max=float(v_max),
                i_peak=float(i_peak), p_chop_kwh=float(chop_kwh), violations=violations)
