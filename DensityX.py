from math import *
import pandas
import numpy
import Tkinter
import tkFileDialog
import sys

def open_file_handler():
    Tkinter.Tk().withdraw() # Close the root window
    filePath = tkFileDialog.askopenfilename()
    print filePath
    return filePath

if __name__ == "__open_file_handler__":
    open_file_handler()

def handle_file():
    filePath = open_file_handler()
    # handle the file

data = pandas.read_excel(open_file_handler()) #import excel file chosen by user


#Check to make sure all necessary columns are present in the imported data. If they are not, add them.
if 'SiO2' in data.columns:
    pass
elif 'sio2' in data.columns:
    data = data.rename(columns = {'sio2':'SiO2'})
elif 'Si02' in data.columns:
    data = data.rename(columns = {'Si02':'SiO2'})
else:    
    proceed = raw_input("WARNING: Did not find a column SiO2. Proceed anyways? (y/n)")
    if proceed is "n":
        print "Quitting program."
        sys.exit()
    if proceed is "y":
        data['SiO2'] = 0
    else:
        print "Error."
        sys.exit()


data = data.fillna(value=0) #Replace any empty cells (which read in as NaN) with 0, otherwise Pandas will break

#TODO try to break script, add exceptions, assertions for cases like: no Fe2O3 column exists, user puts in
#wrong file type. Either teach script to deal with it, or make script output a useful error message for the user.

#Save original wt% values
orig_WP_SiO2  	= data["SiO2"]
orig_WP_TiO2  	= data["TiO2"]
orig_WP_Al2O3 	= data["Al2O3"]
orig_WP_Fe2O3 	= data["Fe2O3"]
orig_WP_FeO 	= data["FeO"]
orig_WP_MgO 	= data["MgO"]
orig_WP_CaO 	= data["CaO"]
orig_WP_Na2O  	= data["Na2O"]
orig_WP_K2O 	= data["K2O"]
orig_WP_H2O 	= data["H2O"]

#Molecular Weights
MW_SiO2 	= 60.0855
MW_TiO2 	= 79.88
MW_Al2O3 	= 101.96
MW_Fe2O3 	= 159.69
MW_FeO 		= 71.85
MW_MgO 		= 40.3
MW_CaO 		= 56.08
MW_Na2O 	= 61.98
MW_K2O 		= 94.2
MW_H2O 		= 18.02

#Partial Molar Volumes
#Volumes for SiO2, Al2O3, MgO, CaO, Na2O, K2O at Tref=1773 K (Lange, 1997; CMP)
#Volumes for TiO2, Fe2O3, FeO at Tref=1773 K (Lange and Carmichael, 1987)
#Volume for H2O at Tref=1273 K (Ochs and Lange, 1999)
MV_SiO2 = 26.86
MV_TiO2 = 28.32
MV_Al2O3 = 37.42
MV_Fe2O3 = 42.97
MV_FeO = 13.97
MV_MgO = 12.02
MV_CaO = 16.90
MV_Na2O = 29.65
MV_K2O = 47.28
MV_H2O = 22.9

#dV/dT values
#MgO, CaO, Na2O, K2O Table 4 (Lange, 1997)
#SiO2, TiO2, Al2O3 Table 9 (Lange and Carmichael, 1987)
#H2O from Ochs & Lange (1999)
dVdT_SiO2 = 0.0
dVdT_TiO2 = 0.00724
dVdT_Al2O3 = 0.00262
dVdT_Fe2O3 = 0.00909
dVdT_FeO = 0.00292
dVdT_MgO = 0.00327
dVdT_CaO = 0.00374
dVdT_Na2O = 0.00768
dVdT_K2O = 0.01208
dVdT_H2O = 0.0095

#dV/dP values
#Anhydrous component data from Kess and Carmichael (1991)
#H2O data from Ochs & Lange (1999)
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

#sum original wt% values
data["OriginalSum"] = data["SiO2"] + data["TiO2"] + data["Al2O3"] + data["Fe2O3"] + data["FeO"] + data["MgO"] + data["CaO"] + data["Na2O"] + data["K2O"] + data["H2O"]

#Normalize original wt% values
data.loc[:,'SiO2'] /= data['OriginalSum']
data.loc[:,'TiO2'] /= data['OriginalSum']
data.loc[:,'Al2O3'] /= data['OriginalSum']
data.loc[:,'Fe2O3'] /= data['OriginalSum']
data.loc[:,'FeO'] /= data['OriginalSum']
data.loc[:,'MgO'] /= data['OriginalSum']
data.loc[:,'CaO'] /= data['OriginalSum']
data.loc[:,'Na2O'] /= data['OriginalSum']
data.loc[:,'K2O'] /= data['OriginalSum']
data.loc[:,'H2O'] /= data['OriginalSum']

data.loc[:,'SiO2'] 	*= 100
data.loc[:,'TiO2'] 	*= 100
data.loc[:,'Al2O3'] *= 100
data.loc[:,'Fe2O3'] *= 100
data.loc[:,'FeO']	*= 100
data.loc[:,'MgO'] 	*= 100
data.loc[:,'CaO'] 	*= 100
data.loc[:,'Na2O'] 	*= 100
data.loc[:,'K2O'] 	*= 100
data.loc[:,'H2O'] 	*= 100

data["NormedSum"] = data["SiO2"] + data["TiO2"] + data["Al2O3"] + data["Fe2O3"] + data["FeO"] + data["MgO"] + data["CaO"] + data["Na2O"] + data["K2O"] + data["H2O"]
#From this point, oxide column values are in normalized wt%


#save normalized wt% values
norm_WP_SiO2  	= data["SiO2"]
norm_WP_TiO2  	= data["TiO2"]
norm_WP_Al2O3 	= data["Al2O3"]
norm_WP_Fe2O3 	= data["Fe2O3"]
norm_WP_FeO 	= data["FeO"]
norm_WP_MgO 	= data["MgO"]
norm_WP_CaO 	= data["CaO"]
norm_WP_Na2O  	= data["Na2O"]
norm_WP_K2O 	= data["K2O"]
norm_WP_H2O 	= data["H2O"]


#divide normalized wt% values by molecular weights
data.loc[:,'SiO2'] 	/= MW_SiO2
data.loc[:,'TiO2'] 	/= MW_TiO2
data.loc[:,'Al2O3'] /= MW_Al2O3
data.loc[:,'Fe2O3'] /= MW_Fe2O3
data.loc[:,'FeO'] 	/= MW_FeO
data.loc[:,'MgO'] 	/= MW_MgO
data.loc[:,'CaO'] 	/= MW_CaO
data.loc[:,'Na2O'] 	/= MW_Na2O
data.loc[:,'K2O'] 	/= MW_K2O
data.loc[:,'H2O'] 	/= MW_H2O

data["MolPropOxSum"] = data["SiO2"] + data["TiO2"] + data["Al2O3"] + data["Fe2O3"] + data["FeO"] + data["MgO"] + data["CaO"] + data["Na2O"] + data["K2O"] + data["H2O"]

#convert to mol fraction
data.loc[:,'SiO2'] /= data['MolPropOxSum']
data.loc[:,'TiO2'] /= data['MolPropOxSum']
data.loc[:,'Al2O3'] /= data['MolPropOxSum']
data.loc[:,'Fe2O3'] /= data['MolPropOxSum']
data.loc[:,'FeO'] /= data['MolPropOxSum']
data.loc[:,'MgO'] /= data['MolPropOxSum']
data.loc[:,'CaO'] /= data['MolPropOxSum']
data.loc[:,'Na2O'] /= data['MolPropOxSum']
data.loc[:,'K2O'] /= data['MolPropOxSum']
data.loc[:,'H2O'] /= data['MolPropOxSum']
#From this point, oxide column values are in mole fraction

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
data["denomSiO2"] 	=  MV_SiO2 	+ (dVdT_SiO2 	* (data["T_K"] - 1773)) + (dVdP_SiO2 	* (data["P"] - 1))
data["denomTiO2"] 	=  MV_TiO2 	+ (dVdT_TiO2 	* (data["T_K"] - 1773)) + (dVdP_TiO2 	* (data["P"] - 1))
data["denomAl2O3"]	=  MV_Al2O3 + (dVdT_Al2O3 	* (data["T_K"] - 1773)) + (dVdP_Al2O3 	* (data["P"] - 1))
data["denomFe2O3"]	=  MV_Fe2O3 + (dVdT_Fe2O3 	* (data["T_K"] - 1773)) + (dVdP_Fe2O3 	* (data["P"] - 1))
data["denomFeO"] 	=  MV_FeO 	+ (dVdT_FeO 	* (data["T_K"] - 1773)) + (dVdP_FeO 	* (data["P"] - 1))
data["denomMgO"] 	=  MV_MgO 	+ (dVdT_MgO 	* (data["T_K"] - 1773)) + (dVdP_MgO 	* (data["P"] - 1))
data["denomCaO"] 	=  MV_CaO 	+ (dVdT_CaO 	* (data["T_K"] - 1773)) + (dVdP_CaO 	* (data["P"] - 1))
data["denomNa2O"] 	=  MV_Na2O 	+ (dVdT_Na2O 	* (data["T_K"] - 1773)) + (dVdP_Na2O 	* (data["P"] - 1))
data["denomK2O"] 	=  MV_K2O 	+ (dVdT_K2O 	* (data["T_K"] - 1773)) + (dVdP_K2O 	* (data["P"] - 1))
data["denomH2O"] 	=  MV_H2O 	+ (dVdT_H2O 	* (data["T_K"] - 1273)) + (dVdP_H2O 	* (data["P"] - 1))

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
data["IndivVliq_SiO2"] 	= (MV_SiO2 	+ (dVdT_SiO2 	* (data["T_K"] - 1773)) + (dVdP_SiO2 	* (data["P"]-1))) * data["SiO2"]
data["IndivVliq_TiO2"] 	= (MV_TiO2 	+ (dVdT_TiO2 	* (data["T_K"] - 1773)) + (dVdP_TiO2 	* (data["P"]-1))) * data["TiO2"]
data["IndivVliq_Al2O3"] = (MV_Al2O3 + (dVdT_Al2O3 	* (data["T_K"] - 1773)) + (dVdP_Al2O3 	* (data["P"]-1))) * data["Al2O3"]
data["IndivVliq_Fe2O3"] = (MV_Fe2O3 + (dVdT_Fe2O3 	* (data["T_K"] - 1773)) + (dVdP_Fe2O3 	* (data["P"]-1))) * data["Fe2O3"]
data["IndivVliq_FeO"] 	= (MV_FeO 	+ (dVdT_FeO 	* (data["T_K"] - 1773)) + (dVdP_FeO 	* (data["P"]-1))) * data["FeO"]
data["IndivVliq_MgO"] 	= (MV_MgO 	+ (dVdT_MgO 	* (data["T_K"] - 1773)) + (dVdP_MgO 	* (data["P"]-1))) * data["MgO"]
data["IndivVliq_CaO"] 	= (MV_CaO 	+ (dVdT_CaO 	* (data["T_K"] - 1773)) + (dVdP_CaO 	* (data["P"]-1))) * data["CaO"]
data["IndivVliq_Na2O"] 	= (MV_Na2O 	+ (dVdT_Na2O 	* (data["T_K"] - 1773)) + (dVdP_Na2O 	* (data["P"]-1))) * data["Na2O"]
data["IndivVliq_K2O"] 	= (MV_K2O 	+ (dVdT_K2O 	* (data["T_K"] - 1773)) + (dVdP_K2O 	* (data["P"]-1))) * data["K2O"]
data["IndivVliq_H2O"] 	= (MV_H2O 	+ (dVdT_H2O 	* (data["T_K"] - 1273)) + (dVdP_H2O 	* (data["P"]-1))) * data["H2O"]

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
data["Density_g-per-cm3"] 	= data["XMW_Sum"] / data["VliqSum"]
data["Density_g-per-L"]		= data["Density_g-per-cm3"] * 1000

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

#Make a sheet with only the important output data
index = data["Sample_ID"]
columns = [data["Sample_ID"], norm_WP_SiO2, data["Density_g-per-cm3"], data["Density_g-per-L"], norm_WP_H2O, data["T"], data["P"]]
output = pandas.DataFrame(index, columns)


#Save this new data to an Excel spreadsheet
writer = pandas.ExcelWriter('Density_output.xlsx', engine='xlsxwriter') #Create a Pandas Excel writer using XlsxWriter as the engine.
output.to_excel(writer, sheet_name='Density Data')
data.to_excel(writer, sheet_name='All Data') #Convert the dataframe to an XlsxWriter Excel object
writer.save() #Close the Pandas Excel writer and output the Excel file