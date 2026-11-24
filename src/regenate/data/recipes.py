"""Synthetic recipes; DS03 sequence timing is derived, power levels are assumed."""
import pandas as pd

EDC = "data/processed/ds03_edc_cycles.parquet"

def recipes(scenario, aux_kw=0.2, cycle_scale=1.0):
    if not 0 < cycle_scale <= 1:
        raise ValueError("cycle_scale must be in (0, 1]")
    if scenario == "S1":
        phases = [("ramp_up", .1, .5, 0), ("stress", .8, 1, .9), ("ramp_down", .1, .5, 0)]
        origins = ["ASSUMED"] * len(phases)
    elif scenario == "S2":
        phases = [("load_step", .25, f, f * e) for f, e in zip((.25,.5,.75,1),(.85,.88,.91,.94))]
        origins = ["ASSUMED"] * len(phases)
    elif scenario == "S3":
        d = pd.read_parquet(EDC)
        d = d[d.cycle_id == sorted(d.cycle_id.unique())[0]].sort_values("ts").reset_index(drop=True)
        seconds = d.ts.diff().dt.total_seconds().shift(-1).fillna(0).clip(lower=0)
        groups = d.phase.ne(d.phase.shift()).cumsum()
        blocks = [(g.phase.iloc[0], float(seconds.loc[g.index].sum())) for _, g in d.groupby(groups, sort=False)]
        charge = sum(t for k,t in blocks if k == "charge")
        discharge = sum(t for k,t in blocks if k == "discharge")
        ratio = float(d.round_trip_efficiency.iloc[0])
        if min(charge, discharge) <= 0 or not 0 < ratio <= 1:
            raise ValueError("invalid DS03 cycle")
        total = sum(t for _,t in blocks)
        phases = [(k, t * cycle_scale / total, 1.0 if k == "charge" else 0.0, ratio * charge / discharge if k == "discharge" else 0.0) for k,t in blocks if t > 0]
        phases.append(("rest", 1.0-cycle_scale, 0.0, 0.0))
        origins = ["DERIVED(DS03 EDC); ASSUMED power scaling"] * (len(phases)-1) + ["ASSUMED rest; none observed"]
    else:
        raise ValueError(scenario)
    return pd.DataFrame([dict(recipe_id=scenario, scenario=scenario, phase_idx=i, kind=k, dur_frac=t, p_in_frac=a, p_rec_frac=b, p_aux_kw=aux_kw, provenance=origins[i]) for i,(k,t,a,b) in enumerate(phases)])
