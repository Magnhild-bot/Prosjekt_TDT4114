import numpy as np
import pandas as pd

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
