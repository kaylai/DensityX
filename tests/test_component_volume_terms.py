import pytest
from DensityX import ComponentVolumeTerms as CVT
from DensityX import constants as cnst
from dataclasses import fields
from copy import copy

def test_default_CVT_values():
    """Test that default CVT values pull from those in constants.py"""
    default_CVT_obj = CVT()
    
    assert default_CVT_obj.molecular_weights == pytest.approx(cnst.molecular_weights)
    assert default_CVT_obj.partial_molar_volumes == pytest.approx(cnst.partial_molar_volumes)
    assert default_CVT_obj.dVdTs == pytest.approx(cnst.dVdTs)
    assert default_CVT_obj.dVdPs == pytest.approx(cnst.dVdPs)
    assert default_CVT_obj.T_refs == pytest.approx(cnst.T_refs)

def test_set_CVT_values():
    CVT_obj = CVT() # default
    CVT_obj_preserved = copy(CVT_obj)
    
    new_MW = CVT_obj.set_terms(molecular_weights={"SiO2": 0.02})
    assert new_MW.molecular_weights["SiO2"] == 0.02
    
    new_partial_molar_vols = CVT_obj.set_terms(partial_molar_volumes={"TiO2": 9})
    assert new_partial_molar_vols.molecular_weights["SiO2"] == cnst.molecular_weights["SiO2"]
    assert new_partial_molar_vols.partial_molar_volumes["TiO2"] == 9
    
    new_dVdTs = CVT_obj.set_terms(dVdTs={"Al2O3": 555})
    assert new_dVdTs.dVdTs["Al2O3"] == 555
    
    new_dVdPs = CVT_obj.set_terms(dVdPs={"MgO": 202})
    assert new_dVdPs.dVdPs["MgO"] == 202
    
    new_T_refs = CVT_obj.set_terms(T_refs={"CaO": 40001})
    assert new_T_refs.T_refs["CaO"] == 40001
    
    # assert original CVT_obj object didn't change
    assert CVT_obj.molecular_weights == pytest.approx(CVT_obj_preserved.molecular_weights)
    assert CVT_obj.partial_molar_volumes == pytest.approx(CVT_obj_preserved.partial_molar_volumes)
    assert CVT_obj.dVdTs == pytest.approx(CVT_obj_preserved.dVdTs)
    assert CVT_obj.dVdPs == pytest.approx(CVT_obj_preserved.dVdPs)
    assert CVT_obj.T_refs == pytest.approx(CVT_obj_preserved.T_refs)

def test_unknown_oxide_raises():
    CVT_obj = CVT() # default
    with pytest.raises(ValueError):
        CVT_obj.set_terms(molecular_weights={"F": 0})

def test_wrong_type_raises():
    CVT_obj = CVT() # default
    with pytest.raises(TypeError):
        CVT_obj.set_terms(molecular_weights={"SiO2": "string instead of float"})
