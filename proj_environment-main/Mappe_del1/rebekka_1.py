from datetime import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import pandas as pd
import sys
import time
import requests
import tempfile
import shutil


def download_temp_file(url):
    """
    Laster ned en fil fra URL og lagrer den midlertidig.
    Returnerer banen til den midlertidige filen.
    """
    startTime = time.time()
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(url)[1])
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            # Skriv data i biter for å håndtere store filer
            for chunk in r.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
    finally:
        tmp_file.close()
    endTime = time.time()
    tot_time = endTime - startTime
    print('The download_temp_file code took ', tot_time, ' seconds to run')
    return tmp_file.name


def data_reader(filename, nanlimit):
    startTime = time.time()
    """Leser strukturen og informasjonen til en fil.
    Filen kan være av typen csv, xlsx, json, eller html.
    Dersom filen ikke er lagret lokalt må man bruke funksjonen download_temp_file
    før denne funksjonen kan brukes. Bruk isåfall da tmp_file som filename for denne funksjonen.
    
    Funksjonen printer:
    - Minne informasjon
    - Kolonne navn
    - Antall verdier
    - Kolonne typer
    - Nan verdier
    - Nan prosent (om antall nanverdier overskrider nanlimit)
    """

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
            data = pd.read_html(filename)[0] #Dersom html filen bare har en tabell
        else:
            print('Filetype not valid')
            sys.exit()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"The dataset took: {elapsed_time:.2f} seconds to read")
        print(' ')

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found. Please ensure it exists in the directory.")
        sys.exit()

    #Reading the datastructure:
    try:
        print(f'Following information about the dataset {filename} was found:')
        print('--------------------------------------------------------------------------')

        #Checks the size of the file in kB
        print('Memory information:')
        print('-------------------')
        file_size = os.path.getsize(filename)
        print(f"Filesize: {file_size*10**(-3)} kB")
        mem_usage = data.memory_usage(deep=True).sum()
        print(f"DataFrame size: {mem_usage*10**(-3)} kB")
        print('  ')

        columns_info = pd.DataFrame({
            "Column": data.columns,
            "Count": [len(data[col]) for col in data.columns],
            "Type": [", ".join(data[col].dropna().apply(lambda x: type(x).__name__).unique()) if data[col].dtype == object else str(data[col].dtype)for col in data.columns],
            "First element": [data[col].iloc[0] for col in data.columns]
        })
        print("Available data of the DataFrame:")
        print("-" * 40)
        print(columns_info.to_string(index=False))
        print('   ')

        # Converts objects of type float64 to float 32 to save memory usage
        for col in data.columns:
            if data[col].dtype == np.float64:
                data[col] = data[col].astype(np.float32)
                print(f"Column {col} converted to float32 to save memory")
                print('DataFrame size is now: ', round(data.memory_usage(deep=True).sum() * 10 ** (-3), 2), 'kB')
                print('   ')

        #Tries to convert dataelements in the column to same type if the column consists of more dtypes than one
        for col in data.columns:
            unique_types = data[col].dropna().apply(lambda x: type(x)).unique() #Finsd unique dtypes of column

            if len(unique_types) > 1:
                print(f"Column '{col}' has mixed types: {[t.__name__ for t in unique_types]}")
                try:
                    #Tries to convert all elements to numeric value
                    converted = pd.to_numeric(data[col], errors='raise')
                    data[col] = converted
                    print(f"Column '{col}' successfully converted to {data[col].dtype}")

                except Exception as e:
                    #if it doesnt work, convert all elements to strings
                    print('  ')
                    print(f"Could not convert '{col}' elements to numeric : {e}")
                    # Dersom konvertering til numerisk ikke fungerer, konverter alle verdier til string
                    data[col] = data[col].astype(str)
                    print(f"All elements in '{col}' converted to string")
                    print('   ')


        print('-------------------------------------------------------------')

        #Checks the dataset for nan values
        check_nan = data.isnull().sum()
        print('Number of NaN values found:\n', check_nan)
        nan_prosent=check_nan/len(data)*100

        if (nan_prosent > nanlimit).any():
            print(' ')
            print(f"The following columns exceed the NaN limit of {nanlimit}%")
            print(round(nan_prosent[nan_prosent > nanlimit],2))
            print('WARNING! Please check the quality of your datasource')


    except Exception as e:
        raise Exception(f"An error occurred while processing the data: {e}")

    endTime = time.time()
    tot_time = endTime - startTime
    print(' ')
    print('----------------------------------------------------------------')
    print('The data reader code took ', tot_time, ' seconds to run')
    return data


test=1
                           ###TEST 1 AV FUNKSJONEN HER (der download_temp_file() funksjonen brukes først)###

if test==1:
    # URL til filen
    csv_url = "https://sdi.eea.europa.eu/webdav/datastore/public/eea_t_national-emissions-reported_p_2024_v01_r00/CSV/UNFCCC_v27.csv"

    # Last ned filen lokalt midlertidig:
    temp_file = download_temp_file(csv_url)
    print(f"Temporary file saved as: {temp_file}")

    #Leser informasjon om datasettet
    Data = data_reader(temp_file,10)

    #Sletter den midlertidige filen:
    os.remove(temp_file)
    print(f"Temporary file {temp_file} deleted.")


                            ### TEST 2 AV FUNKSJONEN HER (MED ALLEREDE NEDLASTET CSV FIL)
elif test==2:

    #File path
    file_name = '2010_2020_rainfall.csv'

    # Leser informasjon om datasettet
    Data = data_reader(file_name, 10)

else:
    print('Test doesnt exist')















