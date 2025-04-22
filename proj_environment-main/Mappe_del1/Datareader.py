from datetime import time
import numpy as np
import pandas as pd
import os
import pandas as pd
import sys
import time



def data_reader(filename, nanlimit):
    startTime = time.time()
    """Leser strukturen og informasjonen til en fil.
    Filen kan være av typen csv, xlsx, json, eller html.
    Dersom filen ikke er lagret lokalt må man bruke funksjonen download_temp_file
    før denne funksjonen kan brukes. Bruk isåfall da tmp_file som filename for denne funksjonen.
    
    Funksjonen printer:
    - Antall ark dersom excel fil
    - Minne informasjon
    - Kolonne navn
    - Antall verdier
    - Kolonne typer
    - 10 første radene av datasettet
    - Nan verdier
    - Nan prosent (om antall nanverdier overskrider nanlimit)
    """

    filename_only = os.path.basename(filename)

    print(' ')
    print(f'Following information about the dataset {filename_only} was found:')
    print('--------------------------------------------------------------------------')



    _, extension = os.path.splitext(filename) #Splits filename and filetype to read in the data correctly

    # A test to check if the file exists in the directory. If it exists, the data will be downloaded to a pandas dataframe.
    try:
        start_time = time.time()
        if extension.lower()=='.csv':
            data = pd.read_csv(filename)
        elif extension.lower()=='.xlsx':
            xls = pd.ExcelFile(filename)
            ark_liste = xls.sheet_names  # Leser hvilke ark excel filen innholder
            print(f'The xlsx file contains {len(ark_liste)} sheets')
            print(f'The sheetnames are {ark_liste}')
            print(' ')
            print('Reading the first sheet...... ')
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
        print(' ')
        print(f"The dataset took: {elapsed_time:.2f} seconds to read")
        print(' ')

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found. Please ensure it exists in the directory.")
        sys.exit()


    #Reading the datastructure:
    try:
        #Checks the size of the file in kB
        print('Memory information:')
        print('-------------------')

        file_size = os.path.getsize(filename)
        print(f"Filesize: {file_size*10**(-3)} kB")

        mem_usage = data.memory_usage(deep=True).sum()
        print(f"DataFrame size: {mem_usage*10**(-3)} kB")
        print('  ')

        #Finding an overview over the dataset
        columns_info = pd.DataFrame({
            "Column": data.columns, #reading the column names
            "Count": [len(data[col]) for col in data.columns], #how many elements does each column contain
            "Type": [", ".join(data[col].dropna().apply(lambda x: type(x).__name__).unique()) if data[col].dtype == object #Using list comperhension to go through each element in each column (except nan elements) and find the UNIQUE datatypes if dtype is object (just to specify which kind of object.
                     else str(data[col].dtype)for col in data.columns], #if not dtype is object, just read the dtype.
            "First element": [data[col].iloc[0] for col in data.columns] #Reads the first element of each object
        })
        print("Available data of the DataFrame:")
        print("-" * 40)
        print(columns_info.to_string(index=False)) #Prints the columns_info dataframe but as a string.
        print('   ')


        # Iterates through elements of type float64 and converts to float 32 to save memory usage
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

                except Exception as e: #if it doesnt work, convert all elements to strings
                    print('  ')
                    print(f"Could not convert '{col}' elements to numeric : {e}")
                    data[col] = data[col].astype(str) #If error e occurs, try to rather convert all elements to dtype string
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


        #Checks the dataset for any negative values

        negative_values: dict[str, int] = {}
        for col in data.columns:
            if pd.api.types.is_float_dtype(data[col]):
                count = 0
                for val in data[col]:
                    if val < 0:
                        count += 1
                if count > 0:
                    negative_values[col] = count
        print('-----------------------------------------')
        print('Negative values was found in the columns:')
        print(negative_values)
        print('Check if the values of your data is allowed to be negative')

    except Exception as e:
        raise Exception(f"An error occurred while processing the data: {e}")

    endTime = time.time()
    tot_time = endTime - startTime
    print(' ')
    print('----------------------------------------------------------------')
    print('The data reader code took ', tot_time, ' seconds to run')
    return data


















