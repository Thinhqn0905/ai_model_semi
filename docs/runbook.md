# Reproduction runbook

Run from the repository root. Install `requirements.txt`, set `PYTHONPATH=src` (PowerShell: `$env:PYTHONPATH='src'`; Linux/Colab: `export PYTHONPATH=src`). Inputs are read-only. Back up outputs first: commands may overwrite campaigns and reports. Reproduction requires the same source snapshot, dependencies, inputs and settings; manifests' code hashes can differ from the current checkout. Runtimes are NOT_VERIFIED: hardware and logs do not establish reliable durations; campaigns may take hours, DS05 download/processing depends on network and Colab resources.

## Sources and boundaries

DS01 CMC instances are MIT per `CLAUDE.md`; DS02 SHIFT2DC is [CC BY 4.0](https://doi.org/10.5281/zenodo.18524234); DS03 uses manufacturer/TI datasheet curves, subject to their source terms; DS04 partner machine files have no verified redistribution licence here and require the supplied local files; DS05 is [CC BY 4.0](https://doi.org/10.17028/rd.lboro.28732490.v2). Check source terms before redistribution. Simulation results below are SIM_ASSUMED_PROFILE unless their own artifacts establish otherwise; dataset measurements do not establish site savings. Compare matched instances and constraints, including tardiness, with paired confidence intervals.

## Benchmark and campaigns

```powershell
python -m regenate.data.generator --config configs/bench_v1.yaml
python -m regenate.evaluation.oracle_campaign --out runs/oracle_v1 --n 10 --seeds 0 1 --scenarios S1 S2 S3 --flex 0 0.25 1 --slot_h 0.25 --time_limit 60 --workers 10
python -m regenate.evaluation.rolling_campaign --bench data/generated/bench_v1 --oracle runs/oracle_v1/results.csv --out runs/rolling_v1 --report reports/benchmark/rolling_v1.md --workers 8
```

The grounded campaign's manifest supplies efficiency overrides; PowerShell quoting is shown below. These are datasheet-derived proxy efficiencies on assumed workloads, still SIM_ASSUMED_PROFILE.

```powershell
$prm = '{"eta_sup_ac":0.9742965,"eta_sup_dc":0.9931666666666666,"eta_rl_ac":0.974133,"eta_rl_dc":0.993,"eta_afe_imp":0.981,"eta_afe_exp":0.981,"eta_link":0.99}'
python -m regenate.evaluation.oracle_campaign --out runs/oracle_grounded --bench data/generated/bench_v1 --n 10 --seeds 0 1 --scenarios S1 S2 S3 --flex 0.25 --slot_h 0.25 --time_limit 30 --workers 6 --prm $prm
```

The following entry points lack argument parsing: `--help` invokes their workload, not help. Run only when ready to overwrite their outputs. Their current code is not proof of the exact historical code used.

```powershell
python -m regenate.evaluation.sensitivity
python -m regenate.economics.business_case
python -m regenate.data.ds02
python -m regenate.data.ds04
python -m regenate.forecasting.bench_ds02
python -m regenate.forecasting.bench_ds04v2
```

Sensitivity writes `runs/sens_v1`; business case writes `runs/biz_v1/business_case.csv` and requires its configured oracle/rolling inputs. The loaders produce `data/processed/ds02_bus.parquet` and `ds04_machines.parquet`; forecasting writes `runs/ai/ds02` and `runs/ai/ds04`. The twin folder contains test and legacy output, but its exact invocation and parameters are NOT_VERIFIED from the available artifacts; do not claim it reproduced. DS05 commands are in [the Colab sequence](../notebooks/colab_pipeline.md). Exact historical versions, runtimes and complete commands for every existing folder remain NOT_VERIFIED.

## CLI help check, 2026-11-25

Boundary: NOT_VERIFIED for campaign results; this checks CLI availability only. Actual console output from the check, recorded here as its run output:

```text
MODULE regenate.data.generator              EXIT 0
MODULE regenate.data.ds05                   EXIT 0
MODULE regenate.evaluation.oracle_campaign EXIT 0
MODULE regenate.evaluation.rolling_campaign EXIT 0
MODULE regenate.forecasting.ds05_bench      EXIT 0
MODULE regenate.evaluation.v2_campaign      EXIT 0
```

The universal help gate is NOT VERIFIED: the six workload entry points above do not implement help, and invoking them with `--help` can overwrite results. Adding proper help handling requires edits outside this task's owned files.
