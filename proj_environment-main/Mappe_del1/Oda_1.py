import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import pandas as pd
import sys

"""Fra forelesning: Så langt som mulig, er det lurt å forutse hvilke
deler av programmet som kan feile, og prøve om
vi kan få det til å kræsje der på en planlagt måte"""

#Fil path
file_name = "Grennhouse_gases.csv"

# Skjekker om filen finnes i os pathen
try:
    data = pd.read_csv(file_name)
    check_nan=data.isnull().sum()
    print('Number of NaN values found: \n', check_nan)
except FileNotFoundError:
    print(f"Error: The file '{file_name}' was not found. Please ensure it exists in the directory.")
    sys.exit()


#Obs_value: the numerical value of net greenhouse gas emissions (in Gg CO₂ equivalent) for a specific year, country/region,

#laster inn 2010 data (bruker list comperhensive her)
#data_2010_rain = data[data['date'].str.startswith('2010')]['rain'].tolist()
#data_2010_snow= data[data['date'].str.startswith('2010')]['snowfall'].tolist()

#Legger sammen regn og snøfalldata for å lage en nedbørsliste
#data_2010_nedbor=list(map(lambda x, y: x+y, data_2010_rain, data_2010_snow))
#print(data_2010_nedbor)


## Mean, median, standard deviation, and percentiles of greenhouse gas emissions.
## Minimum and maximum values to identify trends.

file_name = "Grennhouse_gases.csv"

try:
    data = pd.read_csv(file_name)
    
    # Convert the 'time' column to integer and 'obs_value' to float (if necessary)
    data['time'] = data['time'].astype(int)
    data['obs_value'] = data['obs_value'].astype(float)
    
    # Basic statistics
    print(data['obs_value'].describe())

except FileNotFoundError:
    print(f"Error: The file '{file_name}' was not found. Please ensure it exists in the directory.")

## Percentage change in emissions year by year.
data['pct_change'] = data['obs_value'].pct_change() * 100
print(data[['time', 'pct_change']])

## Years with exceptionally high or low emissions.
threshold = data['obs_value'].mean() + 2 * data['obs_value'].std()
anomalies = data[data['obs_value'] > threshold]
print("Anomalies:\n", anomalies)


##Se data about Germany
file_name = "Grennhouse_gases.csv"
data = pd.read_csv(file_name)

country_code = "DE"  # Change this to any country's geo code
country_data = data[data['geo'] == country_code]

print(country_data)

##Liechenstein - have Nan
file_name = "Grennhouse_gases.csv"
data = pd.read_csv(file_name)

country_code = "LI"  
liechtenstein_data = data[data['geo'] == country_code]
print(liechtenstein_data)