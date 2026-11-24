import pytest
from regenate.electrical.grounded import grounded_params, eta_at

def test_values_and_provenance():
    params, provenance = grounded_params()
    for key, entry in provenance.items():
        assert 0 < getattr(params, key) <= 1
        assert entry['label'] in {'DATASHEET', 'DERIVED', 'ASSUMED'}
        assert entry['file'] and entry['page']
    assert set(provenance) == {k for k in vars(params) if k.startswith('eta_')}
    assert params.eta_sup_ac == pytest.approx(params.eta_afe_imp * params.eta_sup_dc)
    assert params.eta_rl_ac == pytest.approx(params.eta_rl_dc * params.eta_afe_exp)

def test_curve_interpolation_and_range():
    for name in ('eta_sup_dc', 'eta_rl_dc', 'eta_afe_exp', 'eta_afe_imp', 'eta_sup_ac', 'eta_rl_ac', 'eta_link'):
        assert all(0 < eta_at(name, x) <= 1 for x in (0.2, 0.4, 0.6))
    with pytest.raises(ValueError):
        eta_at('eta_sup_dc', 1.0)
    with pytest.raises(ValueError):
        eta_at('unknown', 0.5)
