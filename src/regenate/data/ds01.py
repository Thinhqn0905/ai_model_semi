"""Read the synthetic CMC DS01 instances without assigning physical units."""
import json
from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "DS01_Quanh" / "instances"
OUT = ROOT / "data" / "processed"
NOTE = "Time is abstract units; physical time and power units are not established."


def load_instance(path):
    path = Path(path)
    inst = json.loads(path.read_text(encoding="utf-8"))
    inst["instance_id"] = path.stem
    return inst


def to_frames(inst):
    iid = inst["instance_id"]
    jobs = []
    for j in range(inst["n"]):
        jobs.append(dict(instance_id=iid, job_id=j, release_u=0, due_u=inst["due_dates"][j],
                         size=inst["sizes"][j], p_stage1_u=inst["p1"][j],
                         p_stage2_u=inst["p2"][j], p_stage3_u=inst["p3"][j],
                         p_stage4_workload_u=inst["eta4"][j], tau=inst["tau"],
                         replicate=inst["replicate"], seed=inst["seed"],
                         provenance="SYNTHETIC", unit_note=NOTE))
    stations = []
    for stage, count in enumerate(inst["m"], 1):
        for machine in range(count):
            run = inst.get(f"P{stage}_run")
            idle = inst.get(f"P{stage}_idle")
            stations.append(dict(instance_id=iid, stage=stage, machine_id=machine,
                capacity=inst["Q"][machine] if stage == 3 else None,
                p_run_kw=None, p_idle_kw=None,
                p_run_source_units=run[machine] if run else None,
                p_idle_source_units=idle[machine] if idle else None,
                alpha_source_units=inst["alpha"][machine] if stage == 4 else None,
                speeds=inst["speeds"] if stage == 4 else None,
                provenance="SYNTHETIC", unit_note=NOTE))
    return pd.DataFrame(jobs), pd.DataFrame(stations)


def build_all():
    paths = sorted(SOURCE.glob("n*_tau*_r*.json"))
    if len(paths) != 180:
        raise ValueError(f"Expected 180 instances, found {len(paths)}")
    instances = [load_instance(p) for p in paths]
    if len({i["instance_id"] for i in instances}) != 180:
        raise ValueError("Duplicate instance IDs")
    frames = [to_frames(i) for i in instances]
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = pd.concat([f[0] for f in frames], ignore_index=True)
    stations = pd.concat([f[1] for f in frames], ignore_index=True)
    jobs.to_parquet(OUT / "ds01_jobs.parquet", index=False)
    stations.to_parquet(OUT / "ds01_stations.parquet", index=False)
    provenance = {"label": "SYNTHETIC", "source_path": "DS01_Quanh/instances/",
                  "license": "CC BY 4.0 (instance data); MIT (source code)",
                  "units": NOTE, "transform": "JSON to rows; release_u=0 assumes all jobs initially available; machine arrays retain source order; no physical unit conversion",
                  "instance_count": len(paths), "job_rows": len(jobs), "station_rows": len(stations)}
    (OUT / "provenance_ds01.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    counts = Counter((i["n"], i["tau"]) for i in instances)
    vals = lambda key: [v for i in instances for row in i[key] for v in (row if isinstance(row, list) else [row])]
    span = lambda x: f"{min(x)}–{max(x)}"
    report = ["# DS01 audit", "", "Boundary: SYNTHETIC instance data; not measurements or ReGenATE performance.",
              f"Source: DS01_Quanh/instances/ ({len(paths)} files); data license CC BY 4.0; generator code MIT.",
              "", "| n jobs | tau | instances | machines per stage |", "|---:|---:|---:|---|"]
    for (n, tau), count in sorted(counts.items()):
        m = next(i["m"] for i in instances if i["n"] == n and i["tau"] == tau)
        report.append(f"| {n} | {tau} | {count} | {m} |")
    report += ["", f"Processing times S1/S2/S3 (abstract units): {span(vals('p1'))} / {span(vals('p2'))} / {span(vals('p3'))}; S3 is per-job per-oven burn-in batch processing input.",
               f"Stage 4 workload: {span(vals('eta4'))} source workload units; processing duration depends on tester speed.",
               f"Oven capacity: {span(vals('Q'))} job-size units; job sizes: {span(vals('sizes'))}.",
               f"Due dates: {span(vals('due_dates'))} abstract units. Tau is the generator's expected tardy fraction (higher means tighter), not observed tardiness.",
               f"P3_run: {span(vals('P3_run'))}; P3_idle: {span(vals('P3_idle'))} in unverified source power units, not asserted as kW.",
               "", "No regen traces are provided; the oven is a pure consumer in this dataset. Time is abstract and cannot establish kWh or a regenerative test-cell result.",
               "", "OPEN QUESTION: What externally justified mapping from one abstract time unit to hours is appropriate for the intended test cell? No mapping is selected.",
               "", "Release time is not specified in the JSON; release_u=0 is an explicit availability assumption. Missing machine power/capacity values remain null; stage 4 run power depends on speed.",
               f"", f"Build output: data/processed/provenance_ds01.json; {len(jobs)} job rows and {len(stations)} station rows (SYNTHETIC)."]
    (ROOT / "reports/data/ds01_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"SYNTHETIC: {len(paths)} instances, {len(jobs)} jobs, {len(stations)} stations; output: {OUT / 'provenance_ds01.json'}")


if __name__ == "__main__":
    build_all()
