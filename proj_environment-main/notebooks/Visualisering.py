import os
import sys
from pathlib import Path
import pickle
import pandas as pd
import matplotlib.pyplot as plt

# Define directories
project_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_dir))
data_dir = project_dir / "data"
images_dir = Path(project_dir) /'resources'/ 'images'
file_path = images_dir/'aqi_levels.png'

from src.Functions_Dataanalysis import plot_AQI_levels,plot_pollutantlevels
from Dataanalyse import NO2_seasonal_raw, PM25_seasonal_raw, PM10_seasonal_raw

# Loading relevant data
mean_air_p_path = data_dir/ 'mean_air_pollutants.pkl'
temp_oslo_path = data_dir/'temperatur_oslo.pkl'

with open(mean_air_p_path, 'rb') as f: # Manipulated pollutant data of Oslo.
    data = pickle.load(f)

with open(temp_oslo_path, 'rb') as f: # Manipulated temperature data of Oslo.
    temp_data = pickle.load(f)


# Reading AQI breakpoints, and color ranges.
df_breakpoints = pd.read_excel(os.path.join(data_dir, 'aqi_breakpoints.xlsx') )
df_colors = pd.read_excel(os.path.join(data_dir, 'aqi_colors.xlsx'))

# Building relevant info of the three different pollutants in three different dataframes, stored in a dict.
aqi_breakpoints = {}
for _, row in df_breakpoints.iterrows():
    pollutant = row['Pollutant']
    tup = (
        row['Low Concentration'],
        row['High Concentration'],
        row['Low AQI'],
        row['High AQI']
    )
    aqi_breakpoints.setdefault(pollutant, []).append(tup)

# Storing the color categories.
aqi_colors = [
    (row['Category'], row['Color'], row['Low'], row['High'])
    for _, row in df_colors.iterrows()
]

# 1. Plotting the AQI data vs the standard AQI categories.
plot_AQI_levels(data,aqi_breakpoints,aqi_colors,file_path)

# 2. Making an interactive plot of the weekly average mean of pollution for each pollutant in one figure.
plot_pollutantlevels(data,aqi_breakpoints)

# 3. Looking at pollutant and temperature correlation
temp = temp_data['Middeltemperatur (mnd)']
temp_NO2index = temp.iloc[:len(NO2_seasonal_raw)].copy()
temp_NO2index.index = NO2_seasonal_raw.index # Indexing temp data with the NO2_seasonal_raw datetimes

plt.figure(figsize=(10,5))
plt.plot(NO2_seasonal_raw.index, NO2_seasonal_raw.values,label='NO2 (seasonal)',color='orange',alpha=0.8)
plt.plot(PM10_seasonal_raw.index, PM10_seasonal_raw.values,label='PM10 (seasonal)',color='plum',alpha=0.8)
plt.plot(PM25_seasonal_raw.index, PM25_seasonal_raw.values,label='PM25 (seasonal)',color='darkgrey',alpha=0.8)
plt.plot(temp_NO2index.index, temp_NO2index.values, label='Temp (mnd)',linestyle='--',color='black')
plt.legend()
plt.show()


