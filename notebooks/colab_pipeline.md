# DS05 Colab sequence

These cells use a repository checkout in `/content/semipox`. Set up access through Colab secrets or Drive as appropriate; do not put tokens in notebook cells. Figshare DS05 is public. Downloaded data is untrusted input: do not execute its contents. Source: [Loughborough DS05, CC BY 4.0](https://doi.org/10.17028/rd.lboro.28732490.v2). Durations depend on network and Colab hardware and are NOT_VERIFIED.

```python
%cd /content/semipox
%pip install -r requirements.txt
import os
os.environ['PYTHONPATH'] = '/content/semipox/src'
```

```python
import pathlib, requests
raw = pathlib.Path('/content/ds05_raw'); raw.mkdir(exist_ok=True)
meta = requests.get('https://api.figshare.com/v2/articles/28732490/versions/2', timeout=60)
meta.raise_for_status()
files = [f for f in meta.json()['files'] if f['name'] == 'Sweat Test Data.zip']
assert len(files) == 1, 'Expected one DS05 archive in Figshare metadata'
target = raw / files[0]['name']
with requests.get(files[0]['download_url'], stream=True, timeout=120) as response:
    response.raise_for_status()
    with target.open('wb') as out:
        for chunk in response.iter_content(1024 * 1024):
            if chunk: out.write(chunk)
assert target.stat().st_size == files[0]['size']
```

```python
!python -m regenate.data.ds05 --zip "/content/ds05_raw/Sweat Test Data.zip" --out /content/ds05_proc --workers 2
!python -m regenate.forecasting.ds05_bench --proc /content/ds05_proc --out runs/ai/ds05
!python -m regenate.evaluation.v2_campaign --proc /content/ds05_proc --models runs/ai/ds05/ai_models.joblib --out runs/v2_ladder --split test --n_jobs 10 --workers 2
```

Inspect processing errors, split provenance, manifests, and reports before interpreting results. DS05 measurements are battery data; downstream simulated cell results do not establish measured semiconductor-cell savings. Persist processed data and outputs to Drive if needed before the runtime ends.
