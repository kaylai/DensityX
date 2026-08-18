from DensityX.density import calculate_density
from DensityX.component_volume_terms import ComponentVolumeTerms as CVT

comp_wtpt = {
    'SiO2':    50.21,
    'TiO2':    2.59,
    'Al2O3':   13.83,
    'FeO':     10.94,
    'Fe2O3':   0.0,
    'MgO':     7.23,
    'CaO':     10.78,
    'Na2O':    2.32,
    'K2O':     0.47,
    'P2O5':    0.0,
    'MnO':     0.0,
    'H2O':     0.42,
    'CO2':     0.0,
    }
pressure = 1 # bars
temperature = 607 # C

# component volume terms from various sources
dict_of_vol_terms = {
    "Lange Spreadsheet": CVT(
        partial_molar_volumes={
            "SiO2":     27.01,
            "TiO2":     13.21,
            "Al2O3":    37.73,
            "Fe2O3":    29.63,
            "FeO":      10.50,
            "MgO":      8.81,
            "CaO":      13.03,
            "Na2O":     19.88,
            "K2O":      33.63,
            "H2O":      13.93,
        },
        dVdPs={k: 0 for k in comp_wtpt.keys()},
        dVdTs={k: 0 for k in comp_wtpt.keys()},
    ),
    "Lange Spreadsheet w/P and T derivatives": CVT(
            partial_molar_volumes={
                "SiO2":     27.01,
                "TiO2":     13.21,
                "Al2O3":    37.73,
                "Fe2O3":    29.63,
                "FeO":      10.50,
                "MgO":      8.81,
                "CaO":      13.03,
                "Na2O":     19.88,
                "K2O":      33.63,
                "H2O":      13.93,
            },
            T_refs={k: 298 for k in comp_wtpt.keys()},
        ),
    "Lange and Carmichael 1990 RevMin Table 3": CVT( # note: identical to L&C (1987) GCA
        partial_molar_volumes={
            "SiO2":     26.90,
            "TiO2":     23.16,
            "Al2O3":    37.11,
            "Fe2O3":    42.13,
            "FeO":      13.65,
            "MgO":      11.45,
            "CaO":      16.57,
            "Na2O":     28.78,
            "K2O":      45.84,
            "H2O":      22.9, # from Ochs and Lange (1999)
        },
        # dVdP's are the same as DensityX defaults (and don't matter since P=1 in this test)
        dVdTs={
            "SiO2"   : 0.0,
            "TiO2"   : 0.00724,
            "Al2O3"  : 0.00262,
            "Fe2O3"  : 0.00909,
            "FeO"    : 0.00292,
            "MgO"    : 0.00262,
            "CaO"    : 0.00292,
            "Na2O"   : 0.00741,
            "K2O"    : 0.01191,
            "H2O"    : 0.0095, # from Ochs and Lange (1999)
        },
        T_refs={
            "SiO2"   : 1673,
            "TiO2"   : 1673,
            "Al2O3"  : 1673,
            "Fe2O3"  : 1673,
            "FeO"    : 1673,
            "MgO"    : 1673,
            "CaO"    : 1673,
            "Na2O"   : 1673,
            "K2O"    : 1673,
            "H2O"    : 1273, # from Ochs and Lange (1999)
        }
    ),
}

default_rho = calculate_density(comp_wtpt, pressure, temperature)
# externally checked to be 2964.053 g/L
print("----------")
print(f"Pressure: {pressure} bars")
print(f"Temperature: {temperature} °C")
print("----------")
print("DensityX defaults = " + str(default_rho))

for source, cvtobj in dict_of_vol_terms.items():
    print(source + " = " + str(calculate_density(comp_wtpt, pressure, temperature, cvtobj)))

print("----------")
