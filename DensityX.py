from math import *
import pandas
import numpy
import Tkinter
import tkFileDialog
import sys
import os

##************VERSION**************##
#VERSION 1.1.0
#UPDATED NOVEMBER 2018
#MIT LICENSED

##************DEBUGGING************##
#Make this value True to save all calculated values to the output excel file. Leave as False to omit (default).
debugging = False

#---------DEFINE SOME CONSTANTS----------#
OxideNames = ['SiO2', 'TiO2', 'Al2O3', 'Fe2O3', 'FeO', 'MgO', 'CaO', 'Na2O', 'K2O', 'H2O']

#Molecular Weights
OxideMasses = {'SiO2': 60.0855, 'TiO2': 79.88, 'Al2O3': 101.96, 'Fe2O3': 159.69, 'FeO': 71.85,
                'MgO': 40.3, 'CaO': 56.08, 'Na2O': 61.98, 'K2O': 94.2, 'H2O': 18.02}
MW_SiO2     = 60.0855
MW_TiO2     = 79.88
MW_Al2O3    = 101.96
MW_Fe2O3    = 159.69
MW_FeO      = 71.85
MW_MgO      = 40.3
MW_CaO      = 56.08
MW_Na2O     = 61.98
MW_K2O      = 94.2
MW_H2O      = 18.02

#Partial Molar Volumes
#Volumes for SiO2, Al2O3, MgO, CaO, Na2O, K2O at Tref=1773 K (Lange, 1997; CMP)
#Volume for H2O at Tref=1273 K (Ochs and Lange, 1999)
#Volume for FeO at Tref=1723 K (Guo et al., 2014)
#Volume for Fe2O3 at Tref=1723 K (Liu and Lange, 2006)
#Volume for TiO2 at Tref=1773 K (Lange and Carmichael, 1987)
MolarVolumes = {'SiO2': 26.86, 'TiO2': 28.32, 'Al2O3': 37.42, 'Fe2O3': 41.50, 'FeO': 12.68,
                'MgO': 12.02, 'CaO': 16.90, 'Na2O': 29.65, 'K2O': 47.28, 'H2O': 22.9}
MV_SiO2 = 26.86
MV_TiO2 = 28.32
MV_Al2O3 = 37.42
MV_Fe2O3 = 41.50
MV_FeO = 12.68
MV_MgO = 12.02
MV_CaO = 16.90
MV_Na2O = 29.65
MV_K2O = 47.28
MV_H2O = 22.9

#Partial Molar Volume uncertainties
#value = 0 if not reported
MolarVolumeErrors = {'SiO2': 0.03, 'TiO2': 0.0, 'Al2O3': 0.09, 'Fe2O3': 0.0, 'FeO': 0.0,
                    'MgO': 0.07, 'CaO': 0.06, 'Na2O': 0.07, 'K2O': 0.10, 'H2O': 0.60}
unc_MV_SiO2 = 0.03
unc_MV_TiO2 = 0
unc_MV_Al2O3 = 0.09
unc_MV_Fe2O3 = 0
unc_MV_FeO = 0
unc_MV_MgO = 0.07
unc_MV_CaO = 0.06
unc_MV_Na2O = 0.07
unc_MV_K2O = 0.10
unc_MV_H2O = 0.60

#dV/dT values
#MgO, CaO, Na2O, K2O Table 4 (Lange, 1997)
#SiO2, TiO2, Al2O3 Table 9 (Lange and Carmichael, 1987)
#H2O from Ochs & Lange (1999)
#Fe2O3 from Liu & Lange (2006)
#FeO from Guo et al (2014)
dVdTs = {'SiO2': 0.0, 'TiO2': 0.00724, 'Al2O3': 0.00262, 'Fe2O3': 0.0, 'FeO': 0.00369,
          'MgO': 0.00327, 'CaO': 0.00374, 'Na2O': 0.00768, 'K2O': 0.01208, 'H2O': 0.0095}
dVdT_SiO2 = 0.0
dVdT_TiO2 = 0.00724
dVdT_Al2O3 = 0.00262
dVdT_Fe2O3 = 0.0
dVdT_FeO = 0.00369
dVdT_MgO = 0.00327
dVdT_CaO = 0.00374
dVdT_Na2O = 0.00768
dVdT_K2O = 0.01208
dVdT_H2O = 0.0095

#dV/dT uncertainties
#value = 0 if not reported
dVdTErrors = {'SiO2': 0.0, 'TiO2': 0.0, 'Al2O3': 0.0, 'Fe2O3': 0.0, 'FeO': 0.0,
                'MgO': 0.0, 'CaO': 0.0, 'Na2O': 0.0, 'K2O': 0.0, 'H2O': 0.00080}
unc_dVdT_SiO2 = 0
unc_dVdT_TiO2 = 0
unc_dVdT_Al2O3 = 0
unc_dVdT_Fe2O3 = 0
unc_dVdT_FeO = 0
unc_dVdT_MgO = 0
unc_dVdT_CaO = 0
unc_dVdT_Na2O = 0
unc_dVdT_K2O = 0
unc_dVdT_H2O = 0.00080

#dV/dP values
#Anhydrous component data from Kess and Carmichael (1991)
#H2O data from Ochs & Lange (1999)
dVdPs = {'SiO2': -0.000189, 'TiO2': -0.000231, 'Al2O3': -0.000226, 'Fe2O3': -0.000253, 'FeO': -0.000045,
            'MgO': 0.000027, 'CaO': 0.000034, 'Na2O': -0.00024, 'K2O': -0.000675, 'H2O': -0.00032}
dVdP_SiO2 = -0.000189
dVdP_TiO2 = -0.000231
dVdP_Al2O3 = -0.000226
dVdP_Fe2O3 = -0.000253
dVdP_FeO = -0.000045
dVdP_MgO = 0.000027
dVdP_CaO = 0.000034
dVdP_Na2O = -0.00024
dVdP_K2O = -0.000675
dVdP_H2O = -0.00032

#dV/dP uncertainties
dVdPErros = {'SiO2': 0.000002, 'TiO2': 0.000006, 'Al2O3': 0.000009, 'Fe2O3': 0.000009, 'FeO': 0.000003,
            'MgO': 0.000007, 'CaO': 0.000005, 'Na2O': 0.000005, 'K2O': 0.000014, 'H2O': 0.000060}
unc_dVdP_SiO2 = 0.000002
unc_dVdP_TiO2 = 0.000006
unc_dVdP_Al2O3 = 0.000009
unc_dVdP_Fe2O3 = 0.000009
unc_dVdP_FeO = 0.000003
unc_dVdP_MgO = 0.000007
unc_dVdP_CaO = 0.000005
unc_dVdP_Na2O = 0.000005
unc_dVdP_K2O = 0.000014
unc_dVdP_H2O = 0.000060

#Tref values
Trefs = {'SiO2': 1773, 'TiO2': 1773, 'Al2O3': 1773, 'Fe2O3': 1723, 'FeO': 1723,
            'MgO': 1773, 'CaO': 1773, 'Na2O': 1773, 'K2O': 1773, 'H2O': 1273}
Tref_SiO2 = 1773
Tref_TiO2 = 1773
Tref_Al2O3 = 1773
Tref_Fe2O3 = 1723
Tref_FeO = 1723
Tref_MgO = 1773
Tref_CaO = 1773
Tref_Na2O = 1773
Tref_K2O = 1773
Tref_H2O = 1273



#---------DEFINE SOME UNIVERSAL FUNCTIONS--------#
def open_file_handler():
    Tkinter.Tk().withdraw() # Close the root window
    filePath = tkFileDialog.askopenfilename()
    print(filePath)
    return filePath

if __name__ == "__open_file_handler__":
    open_file_handler()

def handle_file():
    filePath = open_file_handler()
    # handle the file

myfile = open_file_handler()
data = pandas.read_excel(myfile) #import excel file chosen by user

def normalize_sample(sample):
    """Normalizes an input composition to 100%. This is the 'standard' normalization routine.

    Parameters
    ----------
    sample:    pandas Series, dictionary, or pandas DataFrame
        A single composition can be passed as a dictionary or pandas series. Multiple compositions can be passed as 
        a pandas DataFrame. Compositional information as oxides must be present.

    Returns
    -------
    Sample passed as > Returned as
        pandas Series > pandas Series
        dictionary > dictionary
        pandas DataFrame > pandas DataFrame

            Normalized major element oxides.
    """
    def single_normalize(sample):
        single_sample = sample
        return {k: 100.0 * v / sum(single_sample.values()) for k, v in single_sample.items()}

    def multi_normalize(sample):
        multi_sample = sample.copy()
        multi_sample["Sum"] = sum([multi_sample[oxide] for oxide in oxides])
        for column in multi_sample:
            if column in oxides:
                multi_sample[column] = 100.0*multi_sample[column]/multi_sample["Sum"]

        del multi_sample["Sum"]
        return multi_sample

    if isinstance(sample, dict):
        _sample = sample.copy()
        return single_normalize(_sample)
    elif isinstance(sample, pd.core.series.Series):
        _sample = pd.Series(sample.copy())
        sample_dict = sample.to_dict()
        return pd.Series(single_normalize(sample_dict))
    elif isinstance(sample, pd.DataFrame):
        return multi_normalize(sample)

def mol_to_wtpercent(sample):
    """
    Takes in a pandas DataFrame containing multi-sample input or a dictionary containing single-sample input
    and returns a pandas DataFrame object with oxide values converted from mole percent to wt percent.

    Parameters
    ----------
    oxides: pandas DataFrame object or dictionary
        Variable name referring to the pandas DataFrame object that contains user-imported data or a dictionary
        for single-sample input.
    """
    data = sample

    if isinstance(sample, pd.DataFrame):
        for key, value in oxideMass.items():
            data.loc[:, key] *= value

        data["MPOSum"] = sum([data[oxide] for oxide in oxides])

        for oxide in oxides:
            data.loc[:, oxide] /= data['MPOSum']
            data.loc[:, oxide] *= 100
        del data['MPOSum']

    elif isinstance(sample, dict):
        for oxide in oxides:
            if oxide in data.keys():
                pass
            else:
                data[oxide] = 0.0

        data = {oxide:  data[oxide] for oxide in oxides}

        for key, value in oxideMass.items():
            data.update({key: (data[key] * value)})
        MPOSum = sum(data.values())
        for key, value in data.items():
            data.update({key: 100 * value / MPOSum})

    return data

def wtpercent_to_molfrac(oxides):
    """ Takes in a pandas Series or dict containing major element oxides in wt%, and converts it
    to molar proportions (normalised to 1).

    Parameters
    ----------
    oxides         dict or pandas Series
        Major element oxides in wt%

    Returns
    -------
    dict or pandas Series
        Molar proportions of major element oxides, normalised to 1.
    """
    molOxides = {}
    _oxides = oxides.copy()
    if type(oxides) == dict or type(oxides) == pd.core.series.Series:
        if type(oxides) == dict:
            oxideslist = list(oxides.keys())
        elif type(oxides) == pd.core.series.Series:
            oxideslist = list(oxides.index)

        for ox in oxideslist:
            molOxides[ox] = _oxides[ox]/oxideMass[ox]

        if type(oxides) == pd.core.series.Series:
            molOxides = pd.Series(molOxides)
            molOxides = molOxides/molOxides.sum()
        else:
            total = np.sum(list(molOxides.values()))
            for ox in oxideslist:
                molOxides[ox] = molOxides[ox]/total

        return molOxides

    elif isinstance(sample, pd.DataFrame):
        data = sample
        for key, value in oxideMass.items():
            data.loc[:, key] /= value

        data["MPOSum"] = sum([data[oxide] for oxide in oxides])

        for oxide in oxides:
            data.loc[:, oxide] /= data['MPOSum']
        del data['MPOSum']

        return data

    else:
        raise InputError("The composition input must be a pandas Series or dictionary.")

#----------PERFORM INPUT CHECKS----------#
#Check to make sure all necessary columns are present in the imported data. If they are not, add them.
for oxide in OxideNames:
    if oxide in data.columns:
        pass
    else:
        proceed = raw_input("WARNING: Did not find a column " + str(oxide) + ". Proceed anyways? (y/n)")
        if proceed is "n":
            print("Quitting program.")
            sys.exit()
        if proceed is "y":
            data[oxide] = 0
        else:
            print("Error.")
            sys.exit()

#Make sure we have T data
if 'T' in data.columns:
    pass
elif 't' in data.columns:
    data = data.rename(columns = {'t':'T'})
else:    
    proceed = raw_input("\n WARNING: Did not find temperature data. Please input temperature value in degrees C to use for all samples. Or type 'n' to quit. \n")
    if proceed is "n":
        print("Quitting program.")
        sys.exit()
    try:
        userT = float(proceed)
        if userT < 1727 and userT > 323:
            data['T'] = userT
        else:
            print("Temperature out of range")
    except ValueError:
        print("Cheeky. That's not a number.")

#Make sure we have P data
if 'P' in data.columns:
    pass
elif 'p' in data.columns:
    data = data.rename(columns = {'p':'P'})
else:    
    proceed = raw_input("\n WARNING: Did not find pressure data. Please input pressure value in bars to use for all samples. Or type 'n' to quit. \n Tip: Pressure column header must be called 'P' \n")
    if proceed is "n":
        print("Quitting program.")
        sys.exit()
    try:
        userP = float(proceed)
        if userP < 30000 and userT > 0:
            data['P'] = userP
        else:
            print("Pressure out of range")
    except ValueError:
        print("Cheeky. That's not a number.")

data = data.fillna(value=0) #Replace any empty cells (which read in as NaN) with 0, otherwise Pandas will break

#TODO try to break script, add exceptions, assertions for cases like: no Fe2O3 column exists, user puts in
#wrong file type. Either teach script to deal with it, or make script output a useful error message for the user.

#Save original wt% values
original_input_data = data.copy()

#sum original wt% values
origsum = []
for index, row in data.iterrows():
    origsum.append(sum([row[oxide] for oxide in OxideNames]))
data["OriginalSum"] = origsum

#Normalize original wt% values
data_oxide_norm = normalize(data)

#Convert to mole fraction
data_molfrac = wtpercent_to_molfrac(data_oxide_norm)

#calculating the component density in two equations: one for the denominator, one for the numerator. 
#A new numerator is calculated for each oxide.
data["numerSiO2"] 	= data["SiO2"]  	* MW_SiO2
data["numerTiO2"] 	= data["TiO2"]  	* MW_TiO2
data["numerAl2O3"] 	= data["Al2O3"] 	* MW_Al2O3
data["numerFe2O3"]	= data["Fe2O3"] 	* MW_Fe2O3
data["numerFeO"] 	= data["FeO"]	 	* MW_FeO
data["numerMgO"] 	= data["MgO"]  		* MW_MgO
data["numerCaO"] 	= data["CaO"]  		* MW_CaO
data["numerNa2O"] 	= data["Na2O"]  	* MW_Na2O
data["numerK2O"] 	= data["K2O"]  		* MW_K2O
data["numerH2O"] 	= data["H2O"]  		* MW_H2O

#Caclulate temperature in Kelvin
data["T_K"] 		= data["T"]			+ 273

#A new denominator is calculated for each oxide
data["denomSiO2"] 	=  MV_SiO2 	 + (dVdT_SiO2 	* (data["T_K"] - Tref_SiO2))   + (dVdP_SiO2 	* (data["P"] - 1))
data["denomTiO2"] 	=  MV_TiO2 	 + (dVdT_TiO2 	* (data["T_K"] - Tref_TiO2))   + (dVdP_TiO2 	* (data["P"] - 1))
data["denomAl2O3"]	=  MV_Al2O3  + (dVdT_Al2O3 	* (data["T_K"] - Tref_Al2O3))  + (dVdP_Al2O3 	* (data["P"] - 1))
data["denomFe2O3"]	=  MV_Fe2O3  + (dVdT_Fe2O3 	* (data["T_K"] - Tref_Fe2O3))  + (dVdP_Fe2O3 	* (data["P"] - 1))
data["denomFeO"] 	=  MV_FeO 	 + (dVdT_FeO 	* (data["T_K"] - Tref_FeO))    + (dVdP_FeO 	    * (data["P"] - 1))
data["denomMgO"] 	=  MV_MgO 	 + (dVdT_MgO 	* (data["T_K"] - Tref_MgO))    + (dVdP_MgO 	    * (data["P"] - 1))
data["denomCaO"] 	=  MV_CaO 	 + (dVdT_CaO 	* (data["T_K"] - Tref_CaO))    + (dVdP_CaO 	    * (data["P"] - 1))
data["denomNa2O"] 	=  MV_Na2O 	 + (dVdT_Na2O 	* (data["T_K"] - Tref_Na2O))   + (dVdP_Na2O 	* (data["P"] - 1))
data["denomK2O"] 	=  MV_K2O 	 + (dVdT_K2O 	* (data["T_K"] - Tref_K2O))    + (dVdP_K2O 	    * (data["P"] - 1))
data["denomH2O"] 	=  MV_H2O 	 + (dVdT_H2O 	* (data["T_K"] - Tref_H2O))    + (dVdP_H2O 	    * (data["P"] - 1))

#Calculate component density by dividing numerator by denominator
data["ComponentDensity_SiO2"] = data["numerSiO2"] / data["denomSiO2"]
data["ComponentDensity_TiO2"] = data["numerTiO2"] / data["denomTiO2"]
data["ComponentDensity_Al2O3"] = data["numerAl2O3"] / data["denomAl2O3"]
data["ComponentDensity_Fe2O3"] = data["numerFe2O3"] / data["denomFe2O3"]
data["ComponentDensity_FeO"] = data["numerFeO"] / data["denomFeO"]
data["ComponentDensity_MgO"] = data["numerMgO"] / data["denomMgO"]
data["ComponentDensity_CaO"] = data["numerCaO"] / data["denomCaO"]
data["ComponentDensity_Na2O"] = data["numerNa2O"] / data["denomNa2O"]
data["ComponentDensity_K2O"] = data["numerK2O"] / data["denomK2O"]
data["ComponentDensity_H2O"] = data["numerH2O"] / data["denomH2O"]


#Calculate the individual Vliq for each oxide
data["IndivVliq_SiO2"] 	= (MV_SiO2 	+ (dVdT_SiO2 	* (data["T_K"] - Tref_SiO2))  + (dVdP_SiO2 	    * (data["P"]-1))) * data["SiO2"]
data["IndivVliq_TiO2"] 	= (MV_TiO2 	+ (dVdT_TiO2 	* (data["T_K"] - Tref_TiO2))  + (dVdP_TiO2 	    * (data["P"]-1))) * data["TiO2"]
data["IndivVliq_Al2O3"] = (MV_Al2O3 + (dVdT_Al2O3 	* (data["T_K"] - Tref_Al2O3)) + (dVdP_Al2O3 	* (data["P"]-1))) * data["Al2O3"]
data["IndivVliq_Fe2O3"] = (MV_Fe2O3 + (dVdT_Fe2O3 	* (data["T_K"] - Tref_Fe2O3)) + (dVdP_Fe2O3 	* (data["P"]-1))) * data["Fe2O3"]
data["IndivVliq_FeO"] 	= (MV_FeO 	+ (dVdT_FeO 	* (data["T_K"] - Tref_FeO))   + (dVdP_FeO 	    * (data["P"]-1))) * data["FeO"]
data["IndivVliq_MgO"] 	= (MV_MgO 	+ (dVdT_MgO 	* (data["T_K"] - Tref_MgO))   + (dVdP_MgO 	    * (data["P"]-1))) * data["MgO"]
data["IndivVliq_CaO"] 	= (MV_CaO 	+ (dVdT_CaO 	* (data["T_K"] - Tref_CaO))   + (dVdP_CaO 	    * (data["P"]-1))) * data["CaO"]
data["IndivVliq_Na2O"] 	= (MV_Na2O 	+ (dVdT_Na2O 	* (data["T_K"] - Tref_Na2O))  + (dVdP_Na2O 	    * (data["P"]-1))) * data["Na2O"]
data["IndivVliq_K2O"] 	= (MV_K2O 	+ (dVdT_K2O 	* (data["T_K"] - Tref_K2O))   + (dVdP_K2O 	    * (data["P"]-1))) * data["K2O"]
data["IndivVliq_H2O"] 	= (MV_H2O 	+ (dVdT_H2O 	* (data["T_K"] - Tref_H2O))   + (dVdP_H2O 	    * (data["P"]-1))) * data["H2O"]

#Calculate the sum of all Vliq oxides for each sample
data["VliqSum"] = data["IndivVliq_SiO2"] + data["IndivVliq_TiO2"] + data["IndivVliq_Al2O3"] + data["IndivVliq_Fe2O3"] + data["IndivVliq_FeO"] + data["IndivVliq_MgO"] + data["IndivVliq_CaO"] + data["IndivVliq_Na2O"] + data["IndivVliq_K2O"] + data["IndivVliq_H2O"]


#Calculate Indiv X*MW
data.loc[:,'SiO2'] 	*= MW_SiO2
data.loc[:,'TiO2'] 	*= MW_TiO2
data.loc[:,'Al2O3'] *= MW_Al2O3
data.loc[:,'Fe2O3'] *= MW_Fe2O3
data.loc[:,'FeO'] 	*= MW_FeO
data.loc[:,'MgO'] 	*= MW_MgO
data.loc[:,'CaO'] 	*= MW_CaO
data.loc[:,'Na2O'] 	*= MW_Na2O
data.loc[:,'K2O'] 	*= MW_K2O
data.loc[:,'H2O'] 	*= MW_H2O
#From this point, oxide column values are in X*MW

#Calculate the sume of X*MW oxides
data["XMW_Sum"]		= data["SiO2"] + data["TiO2"] + data["Al2O3"] + data["Fe2O3"] + data["FeO"] + data["MgO"] + data["CaO"] + data["Na2O"] + data["K2O"] + data["H2O"]


#Calculate the density of the melt in g/cm3 and in g/L
data["Density_g_per_cm3"] 	= data["XMW_Sum"] / data["VliqSum"]
data["Density_g_per_L"]		= data["Density_g_per_cm3"] * 1000

#Translate oxide column values back into wt% for the output spreadsheet
data.loc[:,'SiO2'] 	= norm_WP_SiO2
data.loc[:,'TiO2'] 	= norm_WP_TiO2
data.loc[:,'Al2O3'] = norm_WP_Al2O3
data.loc[:,'Fe2O3'] = norm_WP_Fe2O3
data.loc[:,'FeO'] 	= norm_WP_FeO
data.loc[:,'MgO'] 	= norm_WP_MgO
data.loc[:,'CaO'] 	= norm_WP_CaO
data.loc[:,'Na2O'] 	= norm_WP_Na2O
data.loc[:,'K2O'] 	= norm_WP_K2O
data.loc[:,'H2O'] 	= norm_WP_H2O

#Uncertainty Calculations
#Partial Molar Volume,
error_MV = {'SiO2'   : (unc_MV_SiO2   / MV_SiO2),
            'TiO2'   : (unc_MV_TiO2   / MV_TiO2),
            'Al2O3'  : (unc_MV_Al2O3  / MV_Al2O3),
            'Fe2O3'  : (unc_MV_Fe2O3  / MV_Fe2O3),
            'FeO'    : (unc_MV_FeO    / MV_FeO),
            'MgO'    : (unc_MV_MgO    / MV_MgO),
            'CaO'    : (unc_MV_CaO    / MV_CaO),
            'Na2O'   : (unc_MV_Na2O   / MV_Na2O),
            'K2O'    : (unc_MV_K2O    / MV_K2O),
            'H2O'    : (unc_MV_H2O    / MV_H2O)}

#dVdT values
error_dVdT = {
            'SiO2'   : (unc_dVdT_SiO2   / 1),
            'TiO2'   : (unc_dVdT_TiO2   / dVdT_TiO2),
            'Al2O3'  : (unc_dVdT_Al2O3  / dVdT_Al2O3),
            'Fe2O3'  : 0,
            'FeO'    : (unc_dVdT_FeO    / dVdT_FeO),
            'MgO'    : (unc_dVdT_MgO    / dVdT_MgO),
            'CaO'    : (unc_dVdT_CaO    / dVdT_CaO),
            'Na2O'   : (unc_dVdT_Na2O   / dVdT_Na2O),
            'K2O'    : (unc_dVdT_K2O    / dVdT_K2O),
            'H2O'    : (unc_dVdT_H2O    / dVdT_H2O)}

#dVdP values
error_dVdP = {
            'SiO2'  : (unc_dVdP_SiO2   / dVdP_SiO2),
            'TiO2'  : (unc_dVdP_TiO2   / dVdP_TiO2),
            'Al2O3' : (unc_dVdP_Al2O3  / dVdP_Al2O3),
            'Fe2O3' : (unc_dVdP_Fe2O3  / dVdP_Fe2O3),
            'FeO'   : (unc_dVdP_FeO    / dVdP_FeO),
            'MgO'   : (unc_dVdP_MgO    / dVdP_MgO),
            'CaO'   : (unc_dVdP_CaO    / dVdP_CaO),
            'Na2O'  : (unc_dVdP_Na2O   / dVdP_Na2O),
            'K2O'   : (unc_dVdP_K2O    / dVdP_K2O),
            'H2O'   : (unc_dVdP_H2O    / dVdP_H2O)}

#calculate square values
percent_error_Vliq = {}
for key in error_MV:
    percent_error_Vliq[key] = sqrt(error_MV[key]**2 + error_dVdT[key]**2 + error_dVdP[key]**2)

data["Unc_Vliq_SiO2"]  = data["IndivVliq_SiO2"]     * percent_error_Vliq['SiO2']
data["Unc_Vliq_TiO2"]  = data["IndivVliq_TiO2"]     * percent_error_Vliq['TiO2']
data["Unc_Vliq_Al2O3"] = data["IndivVliq_Al2O3"]    * percent_error_Vliq['Al2O3']
data["Unc_Vliq_Fe2O3"] = data["IndivVliq_Fe2O3"]    * percent_error_Vliq['Fe2O3']
data["Unc_Vliq_FeO"]   = data["IndivVliq_FeO"]      * percent_error_Vliq['FeO']
data["Unc_Vliq_MgO"]   = data["IndivVliq_MgO"]      * percent_error_Vliq['MgO']
data["Unc_Vliq_CaO"]   = data["IndivVliq_CaO"]      * percent_error_Vliq['CaO']
data["Unc_Vliq_Na2O"]  = data["IndivVliq_Na2O"]     * percent_error_Vliq['Na2O']
data["Unc_Vliq_K2O"]   = data["IndivVliq_K2O"]      * percent_error_Vliq['K2O']
data["Unc_Vliq_H2O"]   = data["IndivVliq_H2O"]      * percent_error_Vliq['H2O']

data["unc_VliqSum"] = (  data["Unc_Vliq_SiO2"] +
                    data["Unc_Vliq_TiO2"] +
                    data["Unc_Vliq_Al2O3"]+
                    data["Unc_Vliq_Fe2O3"]+
                    data["Unc_Vliq_FeO"]  +
                    data["Unc_Vliq_MgO"]  +
                    data["Unc_Vliq_CaO"]  +
                    data["Unc_Vliq_Na2O"] +
                    data["Unc_Vliq_K2O"]  +
                    data["Unc_Vliq_H2O"]  )


#calculate error on density value
data['Uncertainty_g_per_cm3'] = data["unc_VliqSum"] / data["VliqSum"]
data['Uncertainty_g_per_L'] = data["Uncertainty_g_per_cm3"] * 1000

#Make a sheet with only the important output data
index = data["Sample_ID"]
columns = [data["Sample_ID"], data["SiO2_(Normalized)"], data["H2O_(Normalized)"], data["T"], data["P"], data["Density_g_per_cm3"], data["Uncertainty_g_per_cm3"], data["Density_g_per_L"], data["Uncertainty_g_per_L"]]
output = pandas.DataFrame(index, columns)

#Make a sheet with original user input data
index = data["Sample_ID"]
columns = [data["Sample_ID"], data["SiO2 (User Input)"], orig_WP_TiO2, orig_WP_Al2O3, orig_WP_Fe2O3, orig_WP_FeO, orig_WP_MgO, orig_WP_CaO, orig_WP_Na2O, orig_WP_K2O, orig_WP_H2O, data["OriginalSum"], data["T"], data["P"]]
original_user_data = pandas.DataFrame(index, columns)

#Make a sheet with normalized user data
index = data["Sample_ID"]
columns = [data["Sample_ID"], data["SiO2_(Normalized)"], norm_WP_TiO2, norm_WP_Al2O3, 
           norm_WP_Fe2O3, norm_WP_FeO, norm_WP_MgO, norm_WP_CaO, norm_WP_Na2O, norm_WP_K2O, 
           norm_WP_H2O, data["T"], data["P"]]
normed_user_data = pandas.DataFrame(index, columns)

#Save this new data to an Excel spreadsheet
filename, file_extension = os.path.splitext(myfile)
writer = pandas.ExcelWriter(filename + '_output' + file_extension, engine='xlsxwriter') #Create a Pandas Excel writer using XlsxWriter as the engine.
output.to_excel(writer, sheet_name='Density Data')
original_user_data.to_excel(writer, sheet_name='User Input')
normed_user_data.to_excel(writer, sheet_name='Normalized Data')
if debugging == True:
    data.to_excel(writer, sheet_name='All Data') #Convert the dataframe to an XlsxWriter Excel object
else:
    pass
writer.save() #Close the Pandas Excel writer and output the Excel file

print("Success!")