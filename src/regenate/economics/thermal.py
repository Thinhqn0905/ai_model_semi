"""Thermal accounting derived from the electrical ledger; water is site-dependent."""
import math


def heat_rejected_kwh(ledger_out):
    """Cell heat from conversion, dump and DUT losses, excluding HVAC electricity."""
    return (ledger_out["loss_kwh"] + ledger_out["dump_kwh"]
            + ledger_out["dut_in_kwh"] - ledger_out["recoverable_kwh"])


def cooling_load(heat_kwh, dt_h):
    """Average thermal load in kW over dt_h hours."""
    if not math.isfinite(heat_kwh) or heat_kwh < 0 or not math.isfinite(dt_h) or dt_h <= 0:
        raise ValueError("heat must be nonnegative and duration positive, both finite")
    return heat_kwh / dt_h


def q_dot(m_dot_kg_s, cp, t_in, t_out):
    """Heat transfer in kW for kg/s, kJ/(kg K), and temperatures in degrees C."""
    if not all(math.isfinite(x) for x in (m_dot_kg_s, cp, t_in, t_out)) or m_dot_kg_s < 0 or cp <= 0:
        raise ValueError("flow must be nonnegative, heat capacity positive, and inputs finite")
    return m_dot_kg_s * cp * (t_out - t_in)


def water_estimate(heat_kwh, wue_l_per_kwh_th, *, citation, metered=False):
    """Estimate litres with an explicitly cited site-relevant coefficient."""
    if (not math.isfinite(heat_kwh) or heat_kwh < 0 or
            not math.isfinite(wue_l_per_kwh_th) or wue_l_per_kwh_th < 0 or
            not isinstance(citation, str) or not citation.strip()):
        raise ValueError("finite nonnegative heat and coefficient and a citation are required")
    return {"water_l": heat_kwh * wue_l_per_kwh_th,
            "label": "METERED" if metered else "NOT_VERIFIED", "citation": citation}

