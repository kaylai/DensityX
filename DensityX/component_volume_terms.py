from . import constants as cnst
from dataclasses import dataclass, field, fields, replace
import numbers

@dataclass
class ComponentVolumeTerms:
    """Defines a set of terms to parameterize the density equation. The default values are those
    from DensityX (Iacovino and Till, 2019). Every attribute is a dict where keys are the oxides in
    ``constants.oxides``.
    
    Use to calculate the density of a silicate melt or glass with custom thermodynamic terms
    parameterizing the density equation.
    
    Attributes
    ----------
    molecular_weights : dict[str, float]
        Molecular weights for all oxides in g/mol.
    partial_molar_volumes : dict[str, float]
        Partial molar volume values, V_i, for all oxides in cc/mol.
    dVdTs : dict[str, float]
        Thermal expansion terms for all oxides in cc/mol-K.
    dVdPs : dict[str, float]
        Compressibility terms for all oxides in cc/mol-bar.
    T_refs : dict[str, float]
        Reference temperatures for all oxides in Kelvin.
    """
    molecular_weights: dict[str, float] = field(
        default_factory=lambda: dict(cnst.molecular_weights))
    partial_molar_volumes: dict[str, float] = field(
        default_factory=lambda: dict(cnst.partial_molar_volumes))
    dVdTs: dict[str, float] = field(default_factory=lambda: dict(cnst.dVdTs))
    dVdPs: dict[str, float] = field(default_factory=lambda: dict(cnst.dVdPs))
    T_refs: dict[str, float] = field(default_factory=lambda: dict(cnst.T_refs))
    
    def __post_init__(self) -> None:
        for f in fields(self):
            # check for unknown oxide names
            unknown_oxides = set(getattr(self, f.name)) - set(cnst.oxides)
            if unknown_oxides:
                raise ValueError(f"{f.name} contains unknown oxide names: {sorted(unknown_oxides)}")
            
            # enforce value types of str and a real number (float, int and np.float, np.int scalars)
            values = getattr(self, f.name)
            for ox, v in values.items():
                if not isinstance(v, numbers.Real):
                    raise TypeError(
                        f"{f.name}['{ox}'] must be a real number, "
                        f"got {type(v).__name__}: {v!r}"
                    )
    
    def _set_term(self, term: str, values: dict[str, float]) -> "ComponentVolumeTerms":
        """Single variant of `set_terms` that genericizes setting each term value one by one. Only
        meant to be used by `set_terms`, which is the user-facing function."""
        
        valid = {f.name for f in fields(self)}
        if term not in valid:
            raise ValueError(f"`term` must be one of {sorted(valid)}, got '{term}'.")
        return replace(self, **{term: {**getattr(self, term), **values}})

    def set_terms(self, **updates: dict[str, float]) -> "ComponentVolumeTerms":
        """Returns a copy of the ComponentVolumeTerms() object with `values` merged into the named
        terms.
                
        Parameters
        ----------
        **updates : dict[str, float]
            Keyword arguments named for any term of :class:`ComponentVolumeTerms` —
            ``molecular_weights``, ``partial_molar_volumes``, ``dVdTs``, ``dVdPs``, ``T_refs``.
            Each value maps oxide names to new values and is merged into the existing term; oxides
            not specified keep their current value. See :class:`ComponentVolumeTerms` for the
            meaning and units of each term.

        Returns
        -------
        ComponentVolumeTerms
            A new ComponentVolumeTerms object. The original is left unchanged (i.e., this function
            is *not* performed "in_place").

        Raises
        ------
        ValueError
            If a keyword does not name a term, or a value dict contains
            an unrecognized oxide.

        Examples
        --------
        >>> terms = ComponentVolumeTerms().set_terms(
        ...     molecular_weights={'SiO2': 55.0},
        ...     dVdTs={'H2O': 0.0},
        ... )
        >>> terms.molecular_weights['SiO2']
        55.0

        See Also
        --------
        ComponentVolumeTerms : Descriptions and units for each term.
        """
        result = self
        for term, values in updates.items():
            result = result._set_term(term, values) 
        return result       
 