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

#Remane some columns for explicit output to excel spreadsheet
densities = densities.rename(columns = {'density':'Density(g/cm3)', 'density_unc':'Uncertainty(g/cm3)'})

#get 100% normalized composition, which is what is used for density calcs
normalized = densityx.NormalizeWtPercentVals(user_input_data)

#Make a sheet with only the important output data
index = densities["Sample_ID"]
columns = [densities["Sample_ID"], densities["Density(g/cm3)"], densities["Uncertainty(g/cm3)"]]
output = pandas.DataFrame(index, columns)

#Save this new data to an Excel spreadsheet
filename, file_extension = os.path.splitext(myfile)
writer = pandas.ExcelWriter(filename + '_output' + file_extension, engine='xlsxwriter') #Create a Pandas Excel writer using XlsxWriter as the engine.
output.to_excel(writer, sheet_name='Density Data')
normalized.to_excel(writer, sheet_name='Normalized Data')

writer.save() #Close the Pandas Excel writer and output the Excel file

print "Success!"