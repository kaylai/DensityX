"""
DensityX

A python library for calculating the densities of silicate liquids.
"""

__version__ = "2.0.0"
__author__ = "Kayla Iacovino"

from .constants import error_fraction
from .density import calculate_density
from .component_volume_terms import ComponentVolumeTerms

__all__ = [
    # Functions
    'calculate_density',
    # Constants
    'error_fraction',
    # Classes
    'ComponentVolumeTerms',
]
