import zipfile
from pathlib import Path
import pandas as pd
from streamlit.testing.v1 import AppTest


def test_run4_pages(tmp_path, monkeypatch):
    monkeypatch.setenv('REGENATE_RESULTS', str(tmp_path))
    pd.DataFrame([dict(facility='F', month='2019-03', method=m, md_increment_kw=d, cell_kwh=e, boundary='SIM_DATA_PROFILE') for m, d, e in [('B1', 2, 10), ('P0', 1, 8)]]).to_csv(tmp_path / 'facility_md.csv', index=False)
    pd.DataFrame({'case': ['FIN-A', 'FIN-B', 'FIN-C'], 'annual_net_usd': [10, 20, 30], 'boundary': ['ASSUMED']*3}).to_csv(tmp_path / 'fin_v3_ds06.csv', index=False)
    z = tmp_path / 'ds07.zip'
    with zipfile.ZipFile(z, 'w') as f:
        f.writestr('Data_list/Factories/F.csv', 'time,kw\n' + ''.join(f'2019-03-01 00:{i:02d},10\n' for i in range(60)))
    monkeypatch.setenv('REGENATE_DS07', str(z))
    at = AppTest.from_file(Path('app/dashboard.py').resolve(), default_timeout=30).run()
    for page in ('Facility load', 'Tariff selector', 'Monthly bill', 'FIN comparison'):
        at.sidebar.radio[0].set_value(page).run()
        assert not at.exception, (page, list(at.exception))
        assert at.get('download_button')
        if page == 'FIN comparison':
            result = at.dataframe[1].value
            assert result['DERIVED 3-year CAPEX USD'].tolist() == [30, 60, 90]
            assert result['DERIVED 5-year CAPEX USD'].tolist() == [50, 100, 150]
        if page == 'Monthly bill':
            assert any('NOT_VERIFIED' in w.value for w in at.warning)


def test_missing_facility(tmp_path, monkeypatch):
    monkeypatch.setenv('REGENATE_RESULTS', str(tmp_path))
    monkeypatch.delenv('REGENATE_DS07', raising=False)
    at = AppTest.from_file(Path('app/dashboard.py').resolve()).run()
    at.sidebar.radio[0].set_value('Facility load').run()
    assert any('data not available' in x.value for x in at.info)
