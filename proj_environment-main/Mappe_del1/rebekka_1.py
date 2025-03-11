from datetime import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import pandas as pd
import sys
import time

"""Fra forelesning: Så langt som mulig, er det lurt å forutse hvilke
deler av programmet som kan feile, og prøve om
vi kan få det til å kræsje der på en planlagt måte"""

#File path
file_name = '2010_2020_rainfall.csv'

def data_reader(filename):
    _, extension = os.path.splitext(filename)

    # A test to check if the file exists in the directory.
    try:
        start_time = time.time()
        if extension.lower()=='.csv':
            data = pd.read_csv(filename)
        elif extension.lower()=='.xlsx':
            data = pd.read_excel(filename)
        elif extension.lower()=='.json':
            data = pd.read_json(filename)
        elif extension.lower()=='.html':
            data = pd.read_html(filename)
        else:
            print('Filetype not valid')
            sys.exit()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"The dataset took: {elapsed_time:.2f} seconds to read")
        print('--------------------------------------------------------------')
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found. Please ensure it exists in the directory.")
        sys.exit()

    try:
        print(f'Following information about the dataset {filename} was found:')
        print('--------------------------------------------------------------')

        #Checks the size of the file
        print('Memory information:')
        file_size = os.path.getsize(filename)
        print(f"Filesize: {file_size*10**(-3)} kB")
        # Skriv ut minnebruk for DataFrame (i bytes)
        mem_usage = data.memory_usage(deep=True).sum()
        print(f"DataFrame size: {mem_usage*10**(-3)} kB")

        print('-------------------------------------------------------------')

        #Skriv ut kolonnenavn (headers)
        print("The DataFrame has the following data avaiable:")
        print(*map(lambda col: f"{col}, with {len(data[col])} objects", data.columns), sep="\n")


        print('-------------------------------------------------------------')
        #Checks the dataset for nan values
        check_nan = data.isnull().sum()
        print('Number of NaN values found:\n', check_nan)

    except AttributeError:
        print('AttributeError: Check if the dataset is converted correctly to a DataFrame')
        sys.exit()

    return data

Data=data_reader(file_name)






"""
#laster inn 2010 data (bruker list comperhensive her)
data_2010_rain = data[data['date'].str.startswith('2010')]['rain'].tolist()
data_2010_snow= data[data['date'].str.startswith('2010')]['snowfall'].tolist()

#Legger sammen regn og snøfalldata for å lage en nedbørsliste
data_2010_nedbor=list(map(lambda x, y: x+y, data_2010_rain, data_2010_snow))
Nedbor_sortert=sorted(data_2010_nedbor)
print(type(Nedbor_sortert))
print(type(data_2010_rain))

plt.plot(Nedbor_sortert, linestyle='-')
plt.xlabel("Time (År)")
plt.ylabel("Nedbør [mm]")
plt.title("Totalt nedbør for Ørsta i 2010")
plt.grid(True)
plt.show()

def Nedbor_data(data_nedbor):
    total_nedbor=sum(data_nedbor)
    nedbor_med_max=max(data_nedbor)
    nedbor_mengde=[]
    for i in data_nedbor:
        if i!=0:
            nedbor_mengde.append(i)
    nedbor_prosent=len(nedbor_mengde)/len(data_nedbor)*100
    nedbor_snitt=total_nedbor/len(data_nedbor)
    print('Tot nebørsmengde i 2010: ', round(total_nedbor,2), 'mm')
    print('Max nedbørmengde per time: ', nedbor_med_max, 'mm')
    print(f'Det regnet {round(nedbor_prosent,2)}% av hele året i 2010 i Ørsta')
    print(f'Snittet på nedbørmengde i 2010 var: {round(nedbor_snitt,2)} mm/h')
    return

Nedbor_data(Nedbor_sortert)

"""











