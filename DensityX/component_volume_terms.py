from . import constants as cnst

class ComponentVolumeTerms(object):
    """Defines a set of terms to parameterize the density equation. The default values are those
    from DensityX (Iacovino and Till, 2019). All attributes are a dict with keys ['SiO2', 'TiO2',
    'Al2O3', 'Fe2O3', 'FeO', 'MgO', 'CaO', 'Na2O', 'K2O', 'H2O'].
    
    Use to calculate the density of a silicate melt or glass with custom thermodynamic terms
    parameterizing the density equation.  
    """

    def __init__(self, molecular_weights: dict = cnst.molecular_weights,
                 partial_molar_volumes: dict = cnst.partial_molar_volumes,
                 dVdTs: dict = cnst.dVdT,
                 dVdPs: dict = cnst.dVdP,
                 T_refs: dict = cnst.T_ref) -> None:
        """ Initializes the ComponentVolumeTerms object. Default values are defined in constants.py
        
        Parameters
        ----------
        molecular_weights   dict
            Molecular weights for all oxides.
        
        partial_molar_volumes   dict
            Partial molar volume values, V_i, in cc/mol for all oxides.
        
        dVdTs   dict
            Thermal expansion terms in cc/mol-K for all oxides.
        
        dVdPs   dict
            Compressibility terms in cc/mol-bar for all oxides.
        
        T_refs  dict
            Reference temperatures, in Kelvin, for all oxides.
        """
        self.molecular_weights = molecular_weights
        self.partial_molar_volumes = partial_molar_volumes
        self.dVdTs = dVdTs
        self.dVdPs = dVdPs
        self.T_refs = T_refs
 