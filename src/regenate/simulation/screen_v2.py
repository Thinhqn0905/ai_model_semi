"""Run 3 E1 — bus-twin screening of DS06 (bench v2) schedules: are plans that respect the MILP electrical limits approved more often?
  python -m regenate.simulation.screen_v2 --proc /content/ds05_proc --runs DIR [DIR ...] --out OUT.csv [--afe 20]
Per (instance, method): render TRUE station traces, per-station residual DC source/sink after local self-use (same definition as
the ledger/MILP D1/R1), then bus_twin.check_plan with TwinParams(p_afe_max_kw=afe). Boundary SIM_DATA_PROFILE (twin ASSUMED).
"""
import argparse, re
from pathlib import Path
import numpy as np
import pandas as pd
from regenate.data.bench_v2 import load_proc, make_instance, render_traces
from regenate.electrical.ledger import ElecParams
from regenate.simulation.bus_twin import check_plan, TwinParams


def residuals(inst, sch, prm):
    assign = dict(zip(sch.job_id.astype(int), sch.station.astype(int)))
    starts = dict(zip(sch.job_id.astype(int), sch.start_h.astype(float)))
    p_in, p_rec, _ = render_traces(inst, assign, starts, inst["dt_h"], truth=True)
    demand, supply = p_in / prm.eta_sup_dc, p_rec * prm.eta_rl_dc
    own = np.minimum(demand, supply)
    return supply - own, demand - own


def screen(proc, run_dirs, afe=20.0, link_a=80.0, methods=None, max_inst=None):
    cyc, arrs = load_proc(proc); prm = ElecParams(); rows = []
    tp = TwinParams(p_afe_max_kw=afe, i_link_max_a=link_a, p_link_max_kw=link_a * TwinParams().v_nom / 1000)
    for d in run_dirs:
        sch = pd.read_parquet(Path(d) / "schedules.parquet")
        if methods:
            sch = sch[sch.method.isin(methods)]
        if max_inst:
            sch = sch[sch.instance_id.isin(sorted(sch.instance_id.unique(), key=lambda x: int(x.rsplit("s", 1)[1]))[:max_inst])]
        for iid, g in sch.groupby("instance_id"):
            m = re.match(r"v2_(\w+)_n(\d+)_s(\d+)", iid); split, n_jobs, seed = m.group(1), int(m.group(2)), int(m.group(3))
            inst = make_instance(cyc, arrs, seed, n_jobs=n_jobs, n_stations=8, split=split)
            for meth, s in g.groupby("method"):
                src, sink = residuals(inst, s, prm)
                r = check_plan(src, sink, inst["dt_h"] * 3600, tp)
                kinds = sorted({v[1] for v in r.get("violations", [])})            # (time_s, kind, value)
                rows.append(dict(run=Path(d).name, instance_id=iid, method=meth, afe_kw=afe, link_a=link_a, approved=bool(r["approved"]),
                                 v_min=r.get("v_min"), v_max=r.get("v_max"), i_peak=r.get("i_peak"), kinds="|".join(map(str, kinds)),
                                 peak_sink_kw=float(sink.sum(0).max()), peak_src_kw=float(src.sum(0).max()),
                                 max_step_kw=float(np.abs(np.diff(sink.sum(0) - src.sum(0))).max()) if sink.shape[1] > 1 else 0.0))
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--proc", required=True); ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--out", required=True); ap.add_argument("--afe", type=float, default=20.0); ap.add_argument("--link_a", type=float, default=80.0)
    ap.add_argument("--methods", nargs="+", default=None); ap.add_argument("--max_inst", type=int, default=None)
    a = ap.parse_args()
    d = screen(a.proc, a.runs, a.afe, a.link_a, a.methods, a.max_inst); d.to_csv(a.out, index=False)
    print(d.groupby(["run", "method"]).agg(n=("approved", "size"), approved=("approved", "mean"), peak_sink=("peak_sink_kw", "mean"),
                                           max_step=("max_step_kw", "mean")).round(3).to_string())


if __name__ == "__main__":
    main()
