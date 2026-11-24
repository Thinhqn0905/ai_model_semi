# DS01 audit

Boundary: SYNTHETIC instance data; not measurements or ReGenATE performance.
Source: DS01_Quanh/instances/ (180 files); data license CC BY 4.0; generator code MIT.

| n jobs | tau | instances | machines per stage |
|---:|---:|---:|---|
| 5 | 0.2 | 10 | [2, 2, 2, 2] |
| 5 | 0.5 | 10 | [2, 2, 2, 2] |
| 5 | 0.8 | 10 | [2, 2, 2, 2] |
| 10 | 0.2 | 10 | [2, 2, 2, 2] |
| 10 | 0.5 | 10 | [2, 2, 2, 2] |
| 10 | 0.8 | 10 | [2, 2, 2, 2] |
| 20 | 0.2 | 10 | [3, 3, 2, 2] |
| 20 | 0.5 | 10 | [3, 3, 2, 2] |
| 20 | 0.8 | 10 | [3, 3, 2, 2] |
| 30 | 0.2 | 10 | [3, 3, 2, 2] |
| 30 | 0.5 | 10 | [3, 3, 2, 2] |
| 30 | 0.8 | 10 | [3, 3, 2, 2] |
| 50 | 0.2 | 10 | [4, 4, 3, 3] |
| 50 | 0.5 | 10 | [4, 4, 3, 3] |
| 50 | 0.8 | 10 | [4, 4, 3, 3] |
| 100 | 0.2 | 10 | [4, 4, 3, 3] |
| 100 | 0.5 | 10 | [4, 4, 3, 3] |
| 100 | 0.8 | 10 | [4, 4, 3, 3] |

Processing times S1/S2/S3 (abstract units): 1–10 / 1–10 / 1–10; S3 is per-job per-oven burn-in batch processing input.
Stage 4 workload: 1–8 source workload units; processing duration depends on tester speed.
Oven capacity: 3–3 job-size units; job sizes: 1–3.
Due dates: 6–222 abstract units. Tau is the generator's expected tardy fraction (higher means tighter), not observed tardiness.
P3_run: 20.0–20.0; P3_idle: 2.0–2.0 in unverified source power units, not asserted as kW.

No regen traces are provided; the oven is a pure consumer in this dataset. Time is abstract and cannot establish kWh or a regenerative test-cell result.

OPEN QUESTION: What externally justified mapping from one abstract time unit to hours is appropriate for the intended test cell? No mapping is selected.

Release time is not specified in the JSON; release_u=0 is an explicit availability assumption. Missing machine power/capacity values remain null; stage 4 run power depends on speed.

Build output: data/processed/provenance_ds01.json; 6450 job rows and 1920 station rows (SYNTHETIC).

## Gate output (SYNTHETIC)

Command: python -m pytest -q tests/test_ds01.py
...                                                                      [100%]
3 passed in 1.16s
Exit code: 0

Command: python -m regenate.data.ds01
SYNTHETIC: 180 instances, 6450 jobs, 1920 stations; output: D:\Subject_ProjectClass\semipox\data\processed\provenance_ds01.json
Exit code: 0
