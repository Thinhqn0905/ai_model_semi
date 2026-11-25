"""Assumed lumped bus model; simulation screening only, never protection."""
from dataclasses import dataclass
import numpy as np
from scipy.integrate import solve_ivp


@dataclass
class Params:
    v_nom: float = 400.0
    capacitance_f: float = 0.04
    resistance_ohm: float = 0.1
    inductance_h: float = 0.01
    afe_limit_a: float = 50.0
    droop_a_per_v: float = 0.5
    afe_tau_s: float = 0.08
    v_min: float = 380.0
    v_max: float = 420.0
    link_limit_a: float = 80.0


def simulate(power_kw, duration_s=0.2, params=None, afe_trip=False, link_trip=False):
    """Positive station power consumes; link current flows from AFE to bus.

    Integrate source work, station work and resistor heat as state variables.
    Terminate at 10 V, before the constant-power singularity invalidates the model.
    """
    p = params or Params()
    if min(p.capacitance_f, p.resistance_ohm, p.inductance_h, p.afe_tau_s, duration_s) <= 0:
        raise ValueError('positive electrical parameters required')
    def tripped(value, t):
        return value if isinstance(value, bool) else t >= value
    def rhs(t, y):
        v, current, afe = y[:3]
        load = float(power_kw(t) if callable(power_kw) else power_kw) * 1000
        load_i = load / max(v, 10.0)
        target = 0.0 if tripped(afe_trip, t) else np.clip(p.droop_a_per_v * (p.v_nom - v), -p.afe_limit_a, p.afe_limit_a)
        # The controlled source drives the RL link toward its limited current command.
        di = 0.0 if tripped(link_trip, t) else (afe - current) * p.resistance_ohm / p.inductance_h
        dv = ((0.0 if tripped(link_trip, t) else current) - load_i) / p.capacitance_f
        source_power = v * (0.0 if tripped(link_trip, t) else current) + p.resistance_ohm * current**2 + p.inductance_h * current * di
        return [dv, di, (target - afe) / p.afe_tau_s, source_power, load, p.resistance_ohm * current**2]
    def collapse(t, y):
        return y[0] - 10.0
    collapse.terminal = True
    collapse.direction = -1
    sol = solve_ivp(rhs, (0, duration_s), [p.v_nom, 0, 0, 0, 0, 0], max_step=0.001,
                    rtol=1e-9, atol=1e-10, events=collapse)
    if not sol.success:
        raise RuntimeError(sol.message)
    v, current = sol.y[0], sol.y[1]
    return {'time_s': sol.t, 'voltage_v': v, 'current_a': current,
            'source_j': sol.y[3, -1], 'load_j': sol.y[4, -1], 'loss_j': sol.y[5, -1],
            'stored_j': .5*p.capacitance_f*(v[-1]**2-p.v_nom**2) + .5*p.inductance_h*current[-1]**2,
            'violated': bool(np.any((v < p.v_min) | (v > p.v_max) | (np.abs(current) > p.link_limit_a)) or sol.t_events[0].size)}
