from . import constants as cnst
from .component_volume_terms import ComponentVolumeTerms
import pandas as pd

# TODO make batch method
def calculate_density(composition: dict | pd.Series, pressure: float, temperature: float,
                      component_volume_terms: ComponentVolumeTerms=ComponentVolumeTerms()) -> float:
    """ Calculates the density of the given liquid using the DensityX model of
    Iacovino and Till (2019).

    Parameters
    ----------
    composition:  Magma major element composition in wt% oxides
    pressure: Total pressure in bars
    temperature: Temperature in degrees C
    component_volume_terms: ComponentVolumeTerms() object

    Returns
    -------
    The density of the liquid in g/L, rounded to 3 dp.
    """
    cvt = component_volume_terms
    
    # get only species considered in density calculation
    comp_wtpt = {k: v for k, v in composition.items() if
                    k in cnst.oxides}
    
    # convert wt% oxides to mol fraction
    mol_prop_ox = {
        ox: comp_wtpt[ox] / cvt.molecular_weights[ox] for ox in comp_wtpt.keys()
        }        
    mol_prop_ox_sum = sum(mol_prop_ox.values())
    
    comp_molfrac = {
        ox: mol_prop_ox[ox]/mol_prop_ox_sum for ox in mol_prop_ox.keys()
    }
    
    # convert temperature from C to K
    tempK = temperature + 273.15

    indiv_Vliqs = []
    for k, v in comp_molfrac.items():
        indiv_Vliq = ((cvt.partial_molar_volumes[k] + (cvt.dVdTs[k] * (tempK-cvt.T_refs[k])) +
                      (cvt.dVdPs[k] * (pressure-1))) * v)
        indiv_Vliqs.append(indiv_Vliq)

    Vliq_sum = sum(indiv_Vliqs)
    Sum_X_MW = sum([v*cvt.molecular_weights[k] for k, v in comp_molfrac.items()])

    density_g_per_cm3 = Sum_X_MW/Vliq_sum
    density_g_per_L = density_g_per_cm3*1000

    return round(density_g_per_L, 3)