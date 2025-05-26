import pandas as pd
import pickle
import sys
from pathlib import Path
import os
project_dir = Path(__file__).resolve().parents[1]   #Finner dir til proj_environment-main
sys.path.insert(0, str(project_dir))#Dir til notebooks
data_dir = project_dir / "data" #Dir til excelarkene

from src.Functions_Dataanalysis import Pollutants_manipulering
from src.Functions_Dataanalysis import Tempdata_manipulering
"""
# 1. Loading the Air pollutant files.
print('     ')
print('-------------------------------------')
print('Reading air pollutant data...........')
NO2_data = pd.read_excel((os.path.join(data_dir, 'NO2.xlsx')),sheet_name=None,usecols=['Value', 'Start', 'End','Pollutant'])
PM25_data= pd.read_excel((os.path.join(data_dir, 'PM2.5.xlsx')),sheet_name=None,usecols=['Value', 'Start', 'End','Pollutant'])
PM10_data=pd.read_excel((os.path.join(data_dir, 'PM10.xlsx')),sheet_name=None,usecols=['Value', 'Start','Pollutant'])

Pullutant_dict= {
    "NO2":  NO2_data,
    "PM2.5":PM25_data,
    "PM10": PM10_data
}

# Fixing data of Pullutant_dict. Storing to pkl for later use.
mean_results = {}
for pollutant, sheets in Pullutant_dict.items():
    print(' ')
    print('-'*75)
    print(f'Working on {pollutant.upper()} …')
    manipulator = Pollutants_manipulering(sheets)
    mean_results[pollutant] = manipulator.run_all()

print(f'Storing the data of {mean_results.keys()} in pickle file mean_air_pollutants.pkl')
out_path = os.path.join(data_dir, "mean_air_pollutants.pkl")
with open(out_path, "wb") as f:
    pickle.dump(mean_results, f)
"""

# 2. Loading the temperature data.
print(' ')
print('Working on Temp_Oslo_2016_2024.csv')
temp_data_raw=pd.read_csv(os.path.join(data_dir, "Temp_Oslo_2016_2024.csv"),
                          sep=';',dtype={'Tid(norsk normaltid)': str},
                          parse_dates=False)
temp_data_manipulated=Tempdata_manipulering(temp_data_raw).interpolate_nan()  # Filtering for nan values.

# Storing as a pickle file for later use.
print(f'Storing the data of {temp_data_manipulated} in pickle file temperatur_oslo.pkl')
temp_data_manipulated.to_pickle("temperatur_oslo.pkl")
temp_path = os.path.join(data_dir, "temperatur_oslo.pkl")

with open(temp_path, "wb") as f:
    pickle.dump(temp_data_manipulated, f)




























