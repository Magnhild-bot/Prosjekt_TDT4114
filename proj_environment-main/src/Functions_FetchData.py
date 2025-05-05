import requests
import tempfile
import time
import os
import zipfile
import io
import pandas as pd
from collections import defaultdict
from datetime import datetime
import numpy as np
import sys


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


def EU_AirPollutantsData(
        startdate: str,
        enddate: str,
        pollutants: list[str]
) -> dict[str, pd.DataFrame]:

    """
    Henter EEA‑luftkvalitetsdata for angitte *pollutant‑navn* og returnerer
    et dict der nøkkelen er "<Stasjon>_<Pollutant>" og verdien er DataFrame‑en.
    """
    print('Du bruker den nye koden')
    # Oppslagstabell for tallkodekode--> airpollutant type.
    CODE_TO_NAME = {
        "5": "PM10",
        "8": "PM2.5",
        "6001": "NO2",
        "10": "O3",
        "1": "SO2",
        "7": "CO",
    }

    # API request filteret. Bygd opp slik som nettsiden forklarte (skriv en bedre kommentar her, kanskje vi bør legge inn kilde)
    body = {
        "countries": ["NO"],
        "cities": ["Oslo"],
        "pollutants": pollutants,
        "dataset": 1,
        "dateTimeStart": startdate,
        "dateTimeEnd": enddate,
        "aggregationType": "hour",
    }

    print('  ')
    print('Laster ned data med API request....')
    print(' ')

    # ----------------- Splitt historikk (E1a) og UTD (E2a) -----------------#
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    start_d = datetime.strptime(startdate, fmt)
    end_d = datetime.strptime(enddate, fmt)
    date_stop = datetime(2024, 1, 1)

    all_dfs: dict[str, pd.DataFrame] = {}

    # To runder: først dataset=2 (verifiserte 2013-2022), deretter dataset=1 (UTD 2023→)
    for dataset, seg_start, seg_end in [
        (2, start_d, min(end_d, datetime(2023, 12, 31, 23, 59, 59))),
        (1, max(start_d, date_stop), end_d)
    ]:
        if seg_start > seg_end:
            continue

        # Oppdater body for riktig dataset og tidsrom
        body["dataset"] = dataset
        body["dateTimeStart"] = seg_start.strftime(fmt)
        body["dateTimeEnd"] = seg_end.strftime(fmt)
        print(f"Laster ned dataset {dataset} fra {body['dateTimeStart']} til {body['dateTimeEnd']}")

        r = requests.post(
            "https://eeadmz1-downloads-api-appservice.azurewebsites.net/ParquetFile",
            json=body,
            timeout=300
        )
        r.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            for name in z.namelist():
                with z.open(name) as fp:
                    df = pd.read_parquet(fp)

                # Finner stasjonsnavn og type pollutant fra filnavnet
                parts = name.split('_')
                station       = parts[1] if len(parts) > 1 else "UnknownStation"
                pollutant_code = parts[2] if len(parts) > 2 else "unknown"
                pollutant     = (
                    CODE_TO_NAME.get(pollutant_code, pollutant_code)
                    if pollutant_code.isdigit() else pollutant_code
                )
                key = f"{station}_{pollutant}"

                # Hvis nøkkel finnes fra før --> legg til ny data bak eksisterende
                if key in all_dfs:
                    all_dfs[key] = pd.concat([all_dfs[key], df], ignore_index=True)
                else:
                    all_dfs[key] = df
    return all_dfs


def write_to_excel_by_pollutant(AirData, out_dir="airdata_excel"):
    """
    Skriver Dataframsene i dictionarien til ark i ulike excelfiler basert på type pollutant 
    """

    os.makedirs(out_dir, exist_ok=True) #Lager en mappe med pathen C:.......\proj_environment-main\data\airdata_excel

    #-----------Oppretter en excel fil for hver pollutant--------------#
    print('Oppretter excel filer for alle air pollutants')
    print('----------------------------------------------')
    print('  ')
    grouped = defaultdict(dict) #Lager en tom dict, som skal fylles.
    for key, df in AirData.items():
        try:
            station, pollutant = key.split("_") #Henter ut Air pollutant type og stasjonsnavn.

        except ValueError:
            print(ValueError)
            continue
        grouped[pollutant][station] = df

    print('Skriver inn Dataframes i ark i excelfilene')
    print('------------------------------------------')
    print(' ')
    #------------Skriver Dataframene til ulike ark i excelfilene---------#
    for pollutant, station_nr in grouped.items():

        file_path = os.path.join(out_dir, f"{pollutant}.xlsx")

        with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
            for station, df in station_nr.items():
                sheet_name = station
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Lagret {file_path}")


def data_reader(filename, nanlimit,skiprows=None,usecols=None,nrows=None):
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

    _, extension = os.path.splitext(filename)  # Splits filename and filetype to read in the data correctly

    # A test to check if the file exists in the directory. If it exists, the data will be downloaded to a pandas dataframe.
    try:
        start_time = time.time()
        if extension.lower() == '.csv':
            data = pd.read_csv(filename)
        elif extension.lower() == '.xlsx':
            xls = pd.ExcelFile(filename)
            ark_liste = xls.sheet_names  # Leser hvilke ark excel filen innholder
            print(f'The xlsx file contains {len(ark_liste)} sheets')
            print(f'The sheetnames are {ark_liste}')
            print(' ')
            print('Reading the first sheet...... ')
            if skiprows is not None:
                data=pd.read_excel(filename, skiprows=skiprows, usecols=usecols,nrows=nrows)
            else:
                data = pd.read_excel(filename)
        elif extension.lower() == '.json':
            data = pd.read_json(filename,orient='records')
        elif extension.lower() == '.html':
            data = pd.read_html(filename)[0]  # Dersom html filen bare har en tabell
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

    # Reading the datastructure:
    try:
        # Checks the size of the file in kB
        print('Memory information:')
        print('-------------------')

        file_size = os.path.getsize(filename)
        print(f"Filesize: {file_size * 10 ** (-3)} kB")

        mem_usage = data.memory_usage(deep=True).sum()
        print(f"DataFrame size: {mem_usage * 10 ** (-3)} kB")
        print('  ')

        # Finding an overview over the dataset
        columns_info = pd.DataFrame({
            "Column": data.columns,  # reading the column names
            "Count": [len(data[col]) for col in data.columns],  # how many elements does each column contain
            "Type": [", ".join(data[col].dropna().apply(lambda x: type(x).__name__).unique()) if data[
                                                                                                     col].dtype == object  # Using list comperhension to go through each element in each column (except nan elements) and find the UNIQUE datatypes if dtype is object (just to specify which kind of object.
                     else str(data[col].dtype) for col in data.columns],  # if not dtype is object, just read the dtype.
            "First element": [data[col].iloc[0] for col in data.columns]  # Reads the first element of each object
        })
        print("Available data of the DataFrame:")
        print("-" * 40)
        print(columns_info.to_string(index=False))  # Prints the columns_info dataframe but as a string.
        print('   ')

        # Iterates through elements of type float64 and converts to float 32 to save memory usage
        for col in data.columns:
            if data[col].dtype == np.float64:
                data[col] = data[col].astype(np.float32)
                print(f"Column {col} converted to float32 to save memory")
                print('DataFrame size is now: ', round(data.memory_usage(deep=True).sum() * 10 ** (-3), 2), 'kB')
                print('   ')

        # Tries to convert dataelements in the column to same type if the column consists of more dtypes than one
        for col in data.columns:
            unique_types = data[col].dropna().apply(lambda x: type(x)).unique()  # Finsd unique dtypes of column

            if len(unique_types) > 1:
                print(f"Column '{col}' has mixed types: {[t.__name__ for t in unique_types]}")
                try:
                    # Tries to convert all elements to numeric value
                    converted = pd.to_numeric(data[col], errors='raise')
                    data[col] = converted
                    print(f"Column '{col}' successfully converted to {data[col].dtype}")

                except Exception as e:  # if it doesnt work, convert all elements to strings
                    print('  ')
                    print(f"Could not convert '{col}' elements to numeric : {e}")
                    data[col] = data[col].astype(
                        str)  # If error e occurs, try to rather convert all elements to dtype string
                    print(f"All elements in '{col}' converted to string")
                    print('   ')

        print('-------------------------------------------------------------')

        # Checks the dataset for nan values
        check_nan = data.isnull().sum()
        print('Number of NaN values found:\n', check_nan)
        nan_prosent = check_nan / len(data) * 100

        if (nan_prosent > nanlimit).any():
            print(' ')
            print(f"The following columns exceed the NaN limit of {nanlimit}%")
            print(round(nan_prosent[nan_prosent > nanlimit], 2))
            print('WARNING! Please check the quality of your datasource')

        # Checks the dataset for any negative values

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




