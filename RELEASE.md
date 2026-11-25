# Release: run4-final

## Freeze and evidence

D019?D021 freeze the Chroma 17020-type battery-cycling reference, P0-E1-Peak, and ETA/advisory AI. The reference AFE and bus are 20 kW and 32 kW; the 20/16 kW alternative is a simulated sizing candidate, not a hardware approval (SIM_DATA_PROFILE; `docs/decisions.md`; `MyDrive/semiexpo/ai_runs/run4_rt3/v2_size_afe20_bus16`). Rolling plans use screened nominal MILP and fallback; FIFO on infeasibility is marked `initial_plan=fifo_unscreened`. The planning/scoring AFE limits are 18/20 kW (SIM_DATA_PROFILE; `docs/decisions.md`, `MyDrive/semiexpo/ai_runs/run4/v2_safe_p0`). No further AI training is authorized. AI-BILL is NO-GO; ETA is advisory. Simulation acceptance does not establish site acceptance.

## Environment and inputs

Install Python and `requirements.txt`; no pinned Python or dependency lock is recorded, so exact environment reproduction is NOT_VERIFIED. Colab is used for DS05 processing and historical campaigns; runtime and accelerator versions are not frozen (`docs/handoff_run4.md`, `notebooks/colab_pipeline.md`). Set `PYTHONPATH=src`. Inputs are read-only. DS05 Figshare article 28732490 version 2 and DS07 article 14822256 version 9, both CC BY 4.0: `data/manifests/dataset_registry.json`. Dataset acquisition entry point is `scripts/download_public_data.py`; its exact historical invocation is NOT_VERIFIED. DS05 download and processing commands are recorded in `notebooks/colab_pipeline.md`. DS05 is battery data, not semiconductor-site data. Do not execute downloaded code.

## Reproduction

Commands below are documented invocations, not evidence of historical reproduction. Back up output folders first. From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:PYTHONPATH = 'src'
python -m pytest -q
python -m regenate.evaluation.v2_campaign --proc /content/ds05_proc --models runs/ai/ds05/ai_models.joblib --out runs/v2_ladder --split test --n_jobs 10 --workers 2
streamlit run app/dashboard.py
python scripts/shoot_dashboard.py --out reports/run4/screenshots
```

The v2 command above is the documented Colab example (`notebooks/colab_pipeline.md`); its `/content` paths require Colab. Historical campaign-specific `--prm` and `--plan_prm` values and exact invocations of `facility.py`, `fin_facility.py`, `eta.py`, `facility_load.py --reuse`, `run4_figs` and `colab_collect_run4.py` are NOT_VERIFIED in the named release sources. Do not infer them from output summaries. See `docs/runbook.md` for other documented commands and overwrite cautions. This missing command provenance prevents a complete reproducibility claim.

## Artifacts and demo

Raw results reside under `MyDrive/semiexpo/ai_runs/`; the Drive `drive_manifest.json` and `docs/raw_binding_manifest.md` record SHA-256 bindings, some as prefixes. The manifest flags infeasible cases, time-limited incumbents, production mismatch and violations; check them before comparisons. Availability and current hashes have not been independently verified for this release. Figures are expected at `MyDrive/semiexpo/ai_runs/run4/figures/` and copied to `reports/run4/figures/`; their status is in `reports/final/Run4_Final_Evaluation_Report.md`. Dashboard screenshots and capture notes: `reports/run4/screenshots/README.md`; capture requires Playwright and Chromium in addition to the listed requirements (`scripts/shoot_dashboard.py`). Screenshots show locally available results and do not establish site performance.

## Limitations

Measured DS05 battery profiles feed simulated scheduling; DS07 facility traces are unsynchronised counterfactuals, with geographic tariff assumptions. Some baseline comparisons have unequal tardiness; raw reconciliation and figure availability remain incomplete (`docs/raw_binding_manifest.md`, `reports/final/Run4_Final_Evaluation_Report.md`). Missing site costs, vendor access, independent protection, FPY and shadow data block industrial acceptance. The AI-BILL duplicate-history export defect was fixed with reuse per D021, with NO-GO unchanged; verify the archived output independently (`docs/decisions.md`). Never treat modeled protection as physical safety validation.
