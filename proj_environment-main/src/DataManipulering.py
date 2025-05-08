import pandas as pd
import os
import numpy as np
import pickle
from Functions_FetchData import data_readerrr

script_dir= os.path.dirname(os.path.abspath(__file__)) #dir til dette scriptet
project_dir=os.path.dirname(script_dir)#dir til hele prosjektmappen
data_dir=os.path.join(project_dir,'data')

#Downloading columns of interest from the dataset
print('     ')
print('-------------------------------------')
print('Reading air pollutant data...........')
NO2_data = pd.read_excel((os.path.join(data_dir, 'NO2.xlsx')),sheet_name=None,usecols=['Value', 'Start', 'End','Pollutant'])
#O3_data= pd.read_excel((os.path.join(data_dir, 'O3.xlsx')),sheet_name=None,usecols=['Value', 'Start', 'End','Pollutant'])
PM25_data= pd.read_excel((os.path.join(data_dir, 'PM2.5.xlsx')),sheet_name=None,usecols=['Value', 'Start', 'End','Pollutant'])
PM10_data=pd.read_excel((os.path.join(data_dir, 'PM10.xlsx')),sheet_name=None,usecols=['Value', 'Start','Pollutant'])

Pullutant_dict= {
    "NO2":  NO2_data,
    #"O3":   O3_data,
    "PM2.5":PM25_data,
    "PM10": PM10_data
}

# In[] Replacing negative numbers with NaN

class Pollutants_manipulering:

    def __init__(self, dict_file):
        """
        Initializes a dict_file instance.

        Args:
            dict_file (dict): A dictionary containing different Dataframes with information of the pollutants NO2, PM10 and PM2.5.
        """
        self.dict_file = dict_file

    def negative_to_nan(self):
        print(' ')
        print('Replacing negative values and outliers with Nan')

        """Itererer gjennom Value kolonnene i alle arkene i excel fila.
            Bytter ut negative verdier med NaN verdier."""
        for sheet,df in self.dict_file.items():
            df.loc[df["Value"] < 0, "Value"] = np.nan
            df.loc[df['Value'] > 748, 'Value']=np.nan #Høyeste O3 verdi på air quality skalaen


    # In[] Making a standarised time interval column

    def lenght_test(self):
        print(' ')
        print('Cheking size of datasheets')

        Size = {sheet: df.shape for sheet, df in self.dict_file.items()} #Finds the size of the dataframes in the dict.
        unique_size = set(Size.values()) #Checks how many different unique dataframe sizes the excel file contains.
        print(' ')
        print('Datasheet   |  Size  ')
        print('---------------------')
        for sheet, size in Size.items():
            print(f' {sheet}: {size}')
            if size[0] < 78000: #Expected size is 78887
                print(f'Unvalid data size found. Removing {sheet} from dict file. ')
                self.dict_file.pop(sheet) #Removing sheet from dict


    def mean_value_pollutant(self):
        print(' ')
        print('Finding the mean pollutants measure of Oslo')
        print('Nan values replaced with interpolated value')

        pollutant_data = [df['Value'] for df in self.dict_file.values()] #Fetching the pollutant measure from all stations
        pollutant_concat = pd.concat(pollutant_data, axis=1)

        mean_pollutant = pollutant_concat.mean(axis=1, skipna=True) #Finding the mean value of all pollutant measures

        first_df = next(iter(self.dict_file.values())) #Using the date time elements from first sheet as the standard.
        time_intervals = pd.to_datetime(first_df['Start'])

        result = pd.DataFrame({
            'Time Interval': time_intervals,
            'Value': mean_pollutant.values
        })

        result['Value'] = result['Value'].interpolate() #Linær interpolerer nan verdier

        return result


    # In[] Checking nan values

    def run_all(self) -> pd.DataFrame:
        """Kjør alle steg i rett rekkefølge og returner sluttresultatet."""
        self.negative_to_nan()
        self.lenght_test()
        return self.mean_value_pollutant()

mean_results = {}
for pollutant, sheets in Pullutant_dict.items():
    print(f'Working on {pollutant.upper()} …')
    manipulator = Pollutants_manipulering(sheets)
    mean_results[pollutant] = manipulator.run_all()



print(f'Storing the data of {mean_results.keys()} in pickle file mean_air_pollutants.pkl')

out_path = os.path.join(data_dir, "mean_air_pollutants.pkl")
with open(out_path, "wb") as f:
    pickle.dump(mean_results, f)

























