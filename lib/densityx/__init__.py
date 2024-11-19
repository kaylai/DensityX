"""
DensityX

A python library for calculating the densities of silicate melts.

Published as: Iacovino, K. and Till, C. B. (2019) “DensityX: A program for calculating the
densities of magmatic liquids up to 1,627 °C and 30 kbar”, Volcanica, 2(1), pp. 1-10.
doi: 10.30909/vol.02.01.0110.
"""

__version__ = "1.2.0"
__author__ = "Kayla Iacovino, Christy Till, Felix Boschetty"


import numpy as np
import pandas as pd

molecular_weights = pd.Series({
    "SiO2":     60.0855,
    "TiO2":     79.88,
    "Al2O3":    101.96,
    "Fe2O3":    159.69,
    "FeO":      71.85,
    "MgO":      40.3,
    "CaO":      56.08,
    "Na2O":     61.98,
    "K2O":      94.2,
    "H2O":      18.02,
})

# Volumes for SiO2, Al2O3, MgO, CaO, Na2O, K2O at Tref=1773 K (Lange, 1997; CMP)
# Volume for H2O at Tref=1273 K (Ochs and Lange, 1999)
# Volume for FeO at Tref=1723 K (Guo et al., 2014)
# Volume for Fe2O3 at Tref=1723 K (Liu and Lange, 2006)
# Volume for TiO2 at Tref=1773 K (Lange and Carmichael, 1987)
molar_volume = pd.Series({
    "SiO2":     26.86,
    "TiO2":     28.32,
    "Al2O3":    37.42,
    "Fe2O3":    41.50,
    "FeO":      12.68,
    "MgO":      12.02,
    "CaO":      16.90,
    "Na2O":     29.65,
    "K2O":      47.28,
    "H2O":      22.9,
})

# value = 0 if not reported
uncertainty_molar_volume = pd.Series({
    "SiO2":     0.03,
    "TiO2":     0,
    "Al2O3":    0.09,
    "Fe2O3":    0.,
    "FeO":      0,
    "MgO":      0.07,
    "CaO":      0.06,
    "Na2O":     0.07,
    "K2O":      0.10,
    "H2O":      0.60,
})

# MgO, CaO, Na2O, K2O Table 4 (Lange, 1997)
# SiO2, TiO2, Al2O3 Table 9 (Lange and Carmichael, 1987)
# H2O from Ochs & Lange (1999)
# Fe2O3 from Liu & Lange (2006)
# FeO from Guo et al (2014)
dVdT = pd.Series(data={
    "SiO2":     0.0,
    "TiO2":     0.00724,
    "Al2O3":    0.00262,
    "Fe2O3":    0.0,
    "FeO":      0.00369,
    "MgO":      0.00327,
    "CaO":      0.00374,
    "Na2O":     0.00768,
    "K2O":      0.01208,
    "H2O":      0.0095,
})

# value = 0 if not reported
uncertainty_dVdT = pd.Series(data={
    "SiO2":     0,
    "TiO2":     0,
    "Al2O3":    0,
    "Fe2O3":    0,
    "FeO":      0,
    "MgO":      0,
    "CaO":      0,
    "Na2O":     0,
    "K2O":      0,
    "H2O":      0.00080,
})

# Anhydrous component data from Kess and Carmichael (1991)
# H2O data from Ochs & Lange (1999)
dVdP = pd.Series(data={
    "SiO2":     -0.000189,
    "TiO2":     -0.000231,
    "Al2O3":    -0.000226,
    "Fe2O3":    -0.000253,
    "FeO":      -0.000045,
    "MgO":       0.000027,
    "CaO":       0.000034,
    "Na2O":     -0.00024,
    "K2O":      -0.000675,
    "H2O":      -0.00032,
})

uncertainty_dVdP = pd.Series({
    "SiO2":     0.000002,
    "TiO2":     0.000006,
    "Al2O3":    0.000009,
    "Fe2O3":    0.000009,
    "FeO":      0.000003,
    "MgO":      0.000007,
    "CaO":      0.000005,
    "Na2O":     0.000005,
    "K2O":      0.000014,
    "H2O":      0.000060,
})

reference_temperature = pd.Series(data={
    "SiO2":     1773,
    "TiO2":     1773,
    "Al2O3":    1773,
    "Fe2O3":    1723,
    "FeO":      1723,
    "MgO":      1773,
    "CaO":      1773,
    "Na2O":     1773,
    "K2O":      1773,
    "H2O":      1273,
})

oxide_columns = ["SiO2", "TiO2", "Al2O3", "Fe2O3", "FeO", "MgO", "CaO", "Na2O", "K2O", "H2O"]

def NormalizeWtPercentVals(dataframe: pd.DataFrame) -> pd.DataFrame:
	"""Normalize a dataframe of input weight percent values by 100 wt.% total.

	Args:
		dataframe (pd.DataFrame): input dataframe.

	Returns:
		pd.DataFrame: normalized dataframe.
	"""
	data = dataframe.copy()
	total = data.sum(axis=1)
	normalized = 100. * data.div(total, axis=0)
	normalized["Sum"] = normalized.sum(axis=1)

	return normalized


def MoleFraction(dataframe: pd.DataFrame) -> pd.DataFrame:
	"""Calculate the mole fractions of an input dataframe in oxide wt%.

	Args:
		dataframe (pd.DataFrame): input dataframe in oxide wt.%.

	Returns:
		pd.DataFrame: mole fractions.
	"""
	data = dataframe.copy()
	mole_proportion = data / molecular_weights
	mole_fraction = mole_proportion.div(mole_proportion[oxide_columns].sum(axis=1), axis=0)

	return mole_fraction


def Density(dataframe: pd.DataFrame, verbose: bool = False) -> pd.DataFrame:
	"""Calculate density using model of Lange and Carmicheal 1990.

	Args:
		dataframe (pd.DataFrame): dataframe containing compositions in wt% oxides, Pressure in bar and temperature in celsius.
		verbose (bool, optional): flag, if True returns density and intermediate steps. Defaults to False.

	Raises:
		ValueError: check input contains required columns.

	Returns:
		pd.DataFrame: calculated densities and uncertainty.
	"""
	missing_columns = [
		col for col in oxide_columns+["Sample_ID", "P", "T"]
		if col not in dataframe.columns
		]
	if missing_columns:
		raise ValueError(f"The following columns are missing from the input: {missing_columns}")

	data = dataframe.copy()
	data = data.fillna(value=0)
	data_oxides = data[oxide_columns]

	normalized = NormalizeWtPercentVals(data_oxides)
	mole_fraction = MoleFraction(normalized[oxide_columns])

	# Convert temperatures to Kelvin
	# Ensure P and T are in mole_fraction for subsequent calculations
	mole_fraction["T_K"] = data["T"] + 273.15
	mole_fraction["P"] = data["P"]

	# Calculate component density.
	numerator = mole_fraction * molecular_weights
	denominator = mole_fraction.apply(
		lambda row: molecular_weights + dVdT * (row["T_K"] - reference_temperature) + dVdP * (row["P"] - 1),
		axis=1
		)
	component_density = numerator[oxide_columns] / denominator[oxide_columns]

	# Calculate liquid molar volumes
	Vliq = component_density * mole_fraction.apply(
		lambda row: molar_volume + dVdT * (row["T_K"] - reference_temperature) + dVdP * (row["P"] - 1),
		axis=1
		)
	Vliq["Sum"] = Vliq[oxide_columns].sum(axis=1)

	# Calculate X*MW
	X_MW = mole_fraction[oxide_columns] * molecular_weights
	X_MW["Sum"] = X_MW[oxide_columns].sum(axis=1)

	# Calculate the density of the melt in g/cm3 and in g/L
	density_g_per_cm3 = X_MW["Sum"] / Vliq["Sum"]

	# Calculate relative errors -> replace divide by zero errors by 0.
	rel_error_mv = (uncertainty_molar_volume / molar_volume).fillna(value=0.)
	rel_error_dVdT = (uncertainty_dVdT / dVdT).fillna(value=0.)
	rel_error_dVdP = (uncertainty_dVdP / dVdP).fillna(value=0.)

	relative_error_Vliq = np.sqrt(rel_error_mv**2 + rel_error_dVdT**2 + rel_error_dVdP**2)
	absolute_error_Vliq = relative_error_Vliq * Vliq
	absolute_error_Vliq["Sum"] = absolute_error_Vliq[oxide_columns].sum(axis=1)

	# Calculate error on density value
	uncertainty_g_per_cm3 = absolute_error_Vliq["Sum"] / Vliq["Sum"]

	if verbose:
		data_to_return = pd.concat([
			data,
			normalized.add_prefix(prefix="Norm_"),
			mole_fraction[oxide_columns].add_prefix(prefix="MoleFrac_"),
			component_density.add_prefix(prefix="CompDensity_"),
			Vliq.add_prefix(prefix="VLiq_"),
			X_MW.add_prefix(prefix="XMW_"),
			absolute_error_Vliq.add_prefix(prefix="AbsError_")
			], axis=1
		)
		data_to_return["density_g_per_cm"] = density_g_per_cm3
		data_to_return["density_unc_g_per_cm"] = uncertainty_g_per_cm3
		data_to_return["density_g_per_L"] = density_g_per_cm3 * 1000
		data_to_return["uncertainty_g_per_L"] = uncertainty_g_per_cm3 * 1000

	else:
		data_to_return = pd.DataFrame(data={
		"Sample_ID": data["Sample_ID"],
		"density_g_per_cm": density_g_per_cm3,
		"density_unc_g_per_cm": uncertainty_g_per_cm3
		})

	return data_to_return