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

Oxide components must be input in wt%. P is pressure in bars. T is temperature in degrees C. DensityX outputs a pandas dataframe with columns:
*Sample_ID
*Density (g/cm3)
*Uncertainty on Density (g/cm3)

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

##Example usage

Here is a quick example of how to use DensityX to calculate the density of a set of silicate melts.

```
import densityx
import pandas

#read in an excel file with the correct columns (as specified above)
user_input_data = pandas.read_excel(mydata.xlsx) 

#use library to calculate density
densities = densityx.Density(user_input_data)

#Make a sheet with only the important output data
index = densities["Sample_ID"]
columns = [densities["Sample_ID"], densities["Density_g_per_cm3"], densities["Uncertainty_g_per_cm3"]]
output = pandas.DataFrame(index, columns)

#Save this new data to an Excel spreadsheet
writer = pandas.ExcelWriter('mydata_output.xlsx', engine='xlsxwriter') #Create a Pandas Excel writer using XlsxWriter as the engine.
output.to_excel(writer, sheet_name='Density Data')

writer.save() #Close the Pandas Excel writer and output the Excel file
```

## Authors

* **Kayla Iacovino** - [github](https://github.com/kaylai)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
