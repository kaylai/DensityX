import pytest
from DensityX.density import calculate_density

def test_calculate_partial_molar_volumes():
    comp_wtpt = {
        'SiO2':    47.95,
        'TiO2':    1.67,
        'Al2O3':   17.32,
        'FeO':     10.24,
        'Fe2O3':   0.1,
        'MgO':     5.76,
        'CaO':     10.93,
        'Na2O':    3.45,
        'K2O':     1.99,
        'P2O5':    0.51,
        'MnO':     0.1,
        'H2O':     2.0,
        'CO2':     0.1
        }
    pressure = 1000 # bars
    temperature = 1000 # C
    expected_density = 2620.908
    rho = calculate_density(comp_wtpt, pressure, temperature)
    assert rho == pytest.approx(expected_density)