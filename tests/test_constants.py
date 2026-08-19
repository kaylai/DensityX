import pytest
from DensityX import constants as cnst

"""
These tests are probably overkill, but they also serve as a simple way to preserve the original
default values in DensityX v1.0, which match those used for calculations in Iacovino and Till (2019)
"""

def test_get_oxides():
    expected_oxides = [
        'SiO2',
        'TiO2',
        'Al2O3',
        'Fe2O3',
        'FeO',
        'MgO',
        'CaO',
        'Na2O',
        'K2O',
        'H2O',
    ]
    
    for exp_oxide in expected_oxides:
        assert exp_oxide in cnst.oxides, f"{exp_oxide} is not in constants.oxides"
    for const_oxide in cnst.oxides:
        assert const_oxide in expected_oxides, f"{const_oxide} was expected but not returned."

def test_default_dicts():
    pass