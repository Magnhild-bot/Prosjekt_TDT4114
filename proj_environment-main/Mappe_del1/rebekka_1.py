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
file_name = '2010_2020_rainfall.csv'

# Skjekker om filen finnes i os pathen
try:
    data = pd.read_csv(file_name)
    check_nan=data.isnull().sum()
    print('Number of NaN values found: \n', check_nan)
except FileNotFoundError:
    print(f"Error: The file '{file_name}' was not found. Please ensure it exists in the directory.")
    sys.exit()

#laster inn 2010 data (bruker list comperhensive her)
data_2010_rain = data[data['date'].str.startswith('2010')]['rain'].tolist()
data_2010_snow= data[data['date'].str.startswith('2010')]['snowfall'].tolist()

#Legger sammen regn og snøfalldata for å lage en nedbørsliste
data_2010_nedbor=list(map(lambda x, y: x+y, data_2010_rain, data_2010_snow))
Nedbor_sortert=sorted(data_2010_nedbor)
print(type(Nedbor_sortert))
print(type(data_2010_rain))

plt.plot(Nedbor_sortert)













