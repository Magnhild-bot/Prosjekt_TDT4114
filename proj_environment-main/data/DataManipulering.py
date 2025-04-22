import pandas as pd
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pickle

script_dir= os.path.dirname(os.path.abspath(__file__)) #dir til dette scriptet
project_dir=os.path.dirname(script_dir)#dir til hele prosjektmappen
sys.path.insert(0, project_dir)
from Mappe_del1.Datareader import data_reader
data_dir=os.path.join(script_dir,'airdata_excel')


#Cheks what information the file contains by using the data_reader function
file=(os.path.join(data_dir, 'PM10.xlsx'))
data_reader(file,20)


#Downloading columns of interest from the dataset
print('     ')
print('-------------------------------------')
print('Reading air pollutant data...........')
CO_data = pd.read_excel((os.path.join(data_dir, 'CO.xlsx')),sheet_name=None,usecols=['Value', 'Start', 'End','Pollutant'])
NO2_data = pd.read_excel((os.path.join(data_dir, 'NO2.xlsx')),sheet_name=None,usecols=['Value', 'Start', 'End','Pollutant'])
O3_data= pd.read_excel((os.path.join(data_dir, 'O3.xlsx')),sheet_name=None,usecols=['Value', 'Start', 'End','Pollutant'])
PM25_data= pd.read_excel((os.path.join(data_dir, 'PM2.5.xlsx')),sheet_name=None,usecols=['Value', 'Start', 'End','Pollutant'])
PM10_data=pd.read_excel((os.path.join(data_dir, 'PM10.xlsx')),sheet_name=None,usecols=['Value', 'Start','Pollutant'])
SO2_data=pd.read_excel((os.path.join(data_dir, 'SO2.xlsx')),sheet_name=None,usecols=['Value', 'Start', 'End','Pollutant'])

Pullutant_dict= {
    "CO":   CO_data,
    "NO2":  NO2_data,
    "O3":   O3_data,
    "PM2.5":PM25_data,
    "PM10": PM10_data,
    "SO2":  SO2_data,
}

# In[] Replacing negative numbers with NaN

def negative_to_nan(dict_file):
    print(' ')
    print('Replacing negative values with Nan')

    """Itererer gjennom Value kolonnene i alle arkene i excel fila.
        Bytter ut negative verdier med NaN verdier."""
    for sheet,df in dict_file.items():
        df.loc[df["Value"] < 0, "Value"] = np.nan


# In[] Making a standarised time interval column

def lenght_test(dict_file):
    print(' ')
    print('Cheking size of datasheets')

    Size = {sheet: df.shape for sheet, df in dict_file.items()} #Finds the size of the dataframes in the dict.
    unique_size = set(Size.values()) #Checks how many different unique dataframe sizes the excel file contains.
    print(' ')
    print('Datasheet   |  Size  ')
    print('---------------------')
    for sheet, size in Size.items():
        print(f' {sheet}: {size}')
        if size[0] < 35060: #Expected size is 35063
            print(f'Unvalid data size found. Removing {sheet} from dict file. ')
            dict_file.pop(sheet) #Removing sheet from dict




def mean_value_pollutant(dict_file):
    print(' ')
    print('Finding the mean pollutants measure of Oslo')

    pollutant_data = [df['Value'] for df in dict_file.values()] #Fetching the pollutant measure from all stations
    pollutant_concat = pd.concat(pollutant_data, axis=1)

    mean_pollutant = pollutant_concat.mean(axis=1, skipna=True) #Finding the mean value of all pollutant measures

    first_df = next(iter(dict_file.values())) #Using the date time elements from first sheet as the standard.
    time_intervals = pd.to_datetime(first_df['Start'])

    result = pd.DataFrame({
        'Time Interval': time_intervals,
        'Value': mean_pollutant.values
    })

    return result


# In[] Checking nan values

mean_results = {}
for key,datadict in Pullutant_dict.items():
    print('     ')
    print('-----------------------------------------------------------------------------')
    print(f'Checking and filtering the {key} data')
    negative_to_nan(datadict)
    lenght_test(datadict)
    mean_results[key] = mean_value_pollutant(datadict)
    print('-----------------------------------------------------------------------------')


print(f'Storing the data of {mean_results.keys()} in pickle file mean_air_pollutants.pkl')
#Storing da manipulated data as a pickle for later use
out_path   = os.path.join(script_dir, "mean_air_pollutants.pkl")
with open(out_path, "wb") as f:
    pickle.dump(mean_results, f)




















