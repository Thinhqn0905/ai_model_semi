# ReGenATE

ReGenATE studies coordination of regenerative power and scheduling for one semiconductor burn-in cell. It compares a shared DC link and constrained start-time scheduling against regenerative AC baseline B1 at the cell meter M0. Forecasts inform the optimizer; throughput and test integrity remain constraints. It is a simulation research prototype, not a demonstrated site saving.

Results and limitations: [oracle](reports/benchmark/), [sensitivity](reports/sensitivity/sens_v1.md), [forecasting](reports/ai/), and [economics](reports/economics/). The existing oracle and rolling manifests label their station profiles **SIM_ASSUMED_PROFILE**; DS03-grounded efficiencies do not turn assumed workloads into site measurements. Forecasts on DS02/DS04 are external-data benchmarks, not semiconductor-cell evidence. Consult each report and its run files for matching, confidence intervals, and incomplete gates before making a claim.

From the repository root, with Python available:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:PYTHONPATH = 'src'
python -m pytest
python -m regenate.evaluation.oracle_campaign --help
```

See [runbook](docs/runbook.md) for campaign inputs, commands and unresolved reproducibility gaps, and [Colab pipeline](notebooks/colab_pipeline.md) for DS05. Existing outputs should be backed up before rerunning commands that overwrite them.
