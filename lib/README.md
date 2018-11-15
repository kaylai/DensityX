# DensityX

A Python package to calculate the density of a silicate melt up to 3 GPa and  1,627 degrees C, given melt composition in oxides in wt%, pressure, and temperature. DensityX takes a pandas dataframe object with columns named (precisely):
*Sample_ID
*SiO2
*TiO2
*Al2O3
*FeO
*Fe2O3
*MgO
*CaO
*Na2O
*K2O
*H2O
*P
*T

Oxide components must be input in wt%. P is pressure in bars. T is temperature in degrees C. 

Running densityx.Density() returns a pandas dataframe with the columns:
*Sample_ID
*density
*density_unc

Column density is in g/cm3. Column density_unc is uncertainty on the density calculation and is in g/cm3.

## Getting Started

These instructions will get you a copy of DensityX up and running on your local machine for development and testing purposes. 

### Prerequisites

DensityX requires Python pandas. Install this using pip:

```
$ pip install pandas
```

### Installing

You can install DensityX using pip:

```
$ pip install densityx
```

## Example usage

Here is a quick example of how to use DensityX to calculate the density of a set of silicate melts.

```
import pandas
import densityx
import Tkinter
import tkFileDialog
import sys
import os

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

myfile = open_file_handler()
user_input_data = pandas.read_excel(myfile) #import excel file chosen by user

#use library to calculate density
densities = densityx.Density(user_input_data)

#get 100% normalized composition, which is what is used for density calcs
normalized = densityx.NormalizeWtPercentVals(user_input_data)

#Make a sheet with only the important output data
index = densities["Sample_ID"]
columns = [densities["Sample_ID"], densities["Density_g_per_cm3"], densities["Uncertainty_g_per_cm3"]]
output = pandas.DataFrame(index, columns)

#Save this new data to an Excel spreadsheet
filename, file_extension = os.path.splitext(myfile)
writer = pandas.ExcelWriter(filename + '_output' + file_extension, engine='xlsxwriter') #Create a Pandas Excel writer using XlsxWriter as the engine.
output.to_excel(writer, sheet_name='Density Data')
normalized.to_excel(writer, sheet_name='Normalized Data')

writer.save() #Close the Pandas Excel writer and output the Excel file
```

This example script outputs an excel spreadsheet with two sheets. First sheet with columns:
*Sample_ID
*Density (g/cm3)
*Uncertainty on Density (g/cm3)

Second sheet with compositional data in wt%, normalized to 100%. DensityX uses normalized compositions to run density calculations.

### densityx.Density(dataframe, verbose=False)
Determines which output is returned. If False, default values of Sample_ID, density, and density_unc are returned. If True, all calculated values are returned.

Parameters: verbose: boolean, default False

Returns: Pandas dataframe object

### densityx.NormalizeWtPercentVals(dataframe)
Accepts a Pandas dataframe object with same requirements as for densityx.Density(). Returns dataframe with compositional data in wt% normalized to 100%. 

Returns: Pandas dataframe object

### densityx.MoleFraction(dataframe)
Accepts a Pandas dataframe object with same requirements as for densityx.Density(). Returns dataframe with compositional data in mole fraction, normalized to 1.

Returns: Pandas dataframe object

## Authors

* **Kayla Iacovino** - [github](https://github.com/kaylai)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
