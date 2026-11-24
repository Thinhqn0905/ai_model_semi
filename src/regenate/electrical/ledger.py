"""Energy ledger at the test-cell AC boundary (M0) for the four topologies of docs/system_spec.md s5.

One physical model for every topology, so B1 / B1p / DC differ only in which conversion paths exist:

  station s, step k (kW, >= 0):  p_in  = power delivered to the DUT (M2a)
                                 p_rec = DUT output absorbed by the regen load (M2b)
                                 p_aux = AC auxiliary load (chamber, fans)  (M3)
  B0  supply AC-fed (eta_sup_ac); p_rec dumped as heat; HVAC removes it (heat/cop).
  B1  supply AC-fed; regen load returns p_rec*eta_rl_ac to the cell AC bus. Netting on the AC bus
      behind M0 is physical (1:1), so stations already share energy through AC (two conversions).
  B1p each station has its own local DC bus: supply eta_sup_dc, regen load eta_rl_dc, own use first,
      residual through a per-station AFE (eta_afe_imp / eta_afe_exp) onto the cell AC bus.
  DC  like B1p, plus a shared link: residual source of one station feeds residual demand of another
      with eta_link, capped at P_link_max; the rest through one central AFE (capped at P_afe_max,
      surplus beyond the AFE is dumped in the chopper).

Export credit / tariffs are NOT applied here (regenate.economics). net = import - export.
"""
from dataclasses import dataclass, asdict
import numpy as np

TOPOLOGIES = ("B0", "B1", "B1p", "DC")


@dataclass
class ElecParams:
    # shortcut: scalar efficiencies; swap for regenate.data.ds03.eta_curve(load_frac) once WP01 lands.
    eta_sup_ac: float = 0.92    # AC -> DUT supply                  ASSUMED
    eta_sup_dc: float = 0.97    # DC bus -> DUT supply (DC/DC)      ASSUMED
    eta_rl_ac: float = 0.94     # regen load DUT -> AC (93-95 %)    VENDOR_REPORTED
    eta_rl_dc: float = 0.97     # regen load DUT -> DC bus          ASSUMED
    eta_afe_imp: float = 0.97   # AC -> DC (AFE rectifying)         ASSUMED (94-96 % slide 12)
    eta_afe_exp: float = 0.97   # DC -> AC (AFE regenerating)       ASSUMED
    eta_link: float = 0.99      # DC cable/breaker path between stations ASSUMED
    P_link_max: float = np.inf  # kW, direct-transfer capacity of the shared link
    P_afe_max: float = np.inf   # kW, central AFE capacity (DC topology)
    allow_export: bool = True   # False: surplus that cannot be used is dumped
    cop: float = 3.0            # HVAC COP for dumped heat (B0)      ASSUMED
    hvac_on_dump: bool = True

    def as_dict(self):
        return asdict(self)


def _as2d(a, S, K):
    a = np.asarray(a, dtype=float)
    if a.ndim == 1:
        a = np.broadcast_to(a[None, :] / S, (S, K))      # cell-level aux spread evenly
    if a.shape != (S, K):
        raise ValueError(f"expected shape {(S, K)}, got {a.shape}")
    if np.any(a < 0) or not np.all(np.isfinite(a)):
        raise ValueError("power arrays must be finite and >= 0 (direction lives in the name)")
    return a


def ledger(p_in, p_rec, p_aux, dt_h, topology="DC", prm=None):
    """Return a dict of per-step arrays (kW) and totals (kWh) at M0.

    p_in, p_rec: (S, K); p_aux: (S, K) or (K,) cell total; dt_h: step length in hours.
    """
    prm = prm or ElecParams()
    if topology not in TOPOLOGIES:
        raise ValueError(topology)
    p_in = np.atleast_2d(np.asarray(p_in, float)); S, K = p_in.shape
    p_in = _as2d(p_in, S, K); p_rec = _as2d(p_rec, S, K); p_aux = _as2d(p_aux, S, K)
    z = np.zeros(K)
    out = dict(direct=z.copy(), self_use=z.copy(), dump=z.copy(), hvac=z.copy(), afe_short=z.copy(),
               afe_imp_dc=z.copy(), afe_exp_dc=z.copy())
    aux = p_aux.sum(0)

    if topology == "B0":
        load = (p_in / prm.eta_sup_ac).sum(0) + aux
        out["dump"] = p_rec.sum(0)
        out["hvac"] = out["dump"] / prm.cop if prm.hvac_on_dump else z
        ac_net = load + out["hvac"]
    elif topology == "B1":
        load = (p_in / prm.eta_sup_ac).sum(0) + aux
        ret = (p_rec * prm.eta_rl_ac).sum(0)
        ac_net = load - ret
    else:
        d = p_in / prm.eta_sup_dc                       # demand on each station's DC input
        r = p_rec * prm.eta_rl_dc                       # source delivered by each regen load
        u = np.minimum(d, r)                            # own (in-rack) use
        d1, r1 = d - u, r - u                           # residuals (at most one side non-zero per s)
        out["self_use"] = u.sum(0)
        if topology == "DC":
            want = d1.sum(0); have = r1.sum(0) * prm.eta_link
            x = np.minimum.reduce([want, have, np.full(K, prm.P_link_max)])
            out["direct"] = x
            dem_res = want - x                          # to import through the central AFE
            src_res = r1.sum(0) - x / prm.eta_link      # to export through the central AFE
            imp_dc = np.minimum(dem_res, prm.P_afe_max)
            out["afe_short"] = dem_res - imp_dc         # demand the AFE cannot cover -> violation
            exp_dc = np.minimum(src_res, prm.P_afe_max) if prm.allow_export else z
            out["dump"] = src_res - exp_dc
            out["afe_imp_dc"], out["afe_exp_dc"] = imp_dc, exp_dc
            ac_net = imp_dc / prm.eta_afe_imp - exp_dc * prm.eta_afe_exp + aux
        else:                                           # B1p: per-station AFE, no shared link
            exp_dc = r1 if prm.allow_export else np.zeros_like(r1)
            out["dump"] = (r1 - exp_dc).sum(0)
            out["afe_imp_dc"], out["afe_exp_dc"] = d1.sum(0), exp_dc.sum(0)
            ac_net = (d1 / prm.eta_afe_imp).sum(0) - (exp_dc * prm.eta_afe_exp).sum(0) + aux
        if prm.hvac_on_dump:
            out["hvac"] = out["dump"] / prm.cop
            ac_net = ac_net + out["hvac"]

    imp = np.maximum(ac_net, 0.0); exp = np.maximum(-ac_net, 0.0)
    out.update(p_import=imp, p_export=exp)
    E = lambda a: float(np.sum(a) * dt_h)
    out.update(
        import_kwh=E(imp), export_kwh=E(exp), net_kwh=E(imp) - E(exp),
        peak_import_kw=float(imp.max(initial=0.0)),
        direct_reuse_kwh=E(out["direct"]), self_use_kwh=E(out["self_use"]),
        recoverable_kwh=E(p_rec.sum(0)), dump_kwh=E(out["dump"]), hvac_kwh=E(out["hvac"]),
        dut_in_kwh=E(p_in.sum(0)), aux_kwh=E(aux),
        afe_short_kwh=E(out["afe_short"]), afe_violation_steps=int(np.sum(out["afe_short"] > 1e-9)),
        topology=topology,
    )
    # loss = everything that entered the cell minus what reached a useful sink or left it
    out["loss_kwh"] = (out["import_kwh"] - out["export_kwh"]) - (out["dut_in_kwh"] - out["recoverable_kwh"]) \
        - out["aux_kwh"] - out["hvac_kwh"] - out["dump_kwh"] + out["afe_short_kwh"] / prm.eta_afe_imp
    return out


def dc_gain_bound(prm=None):
    """Max kWh saved by the shared link per kWh moved station->station, vs routing it through AC (B1p).

    Via AC: 1 kWh residual source -> eta_afe_exp*eta_afe_imp at the receiving DC input.
    Via link: eta_link. Saved AC import per kWh of residual source = (eta_link - eta_exp*eta_imp)/eta_imp.
    """
    prm = prm or ElecParams()
    return (prm.eta_link - prm.eta_afe_exp * prm.eta_afe_imp) / prm.eta_afe_imp
