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

    start_time = time.time()
    print('Downloading data from given url.....')
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(url)[1])

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            # Skriv data i biter for å håndtere store filer
            for chunk in r.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
    finally:
        tmp_file.close()

    end_time = time.time()
    tot_time = end_time - start_time
    print('The download_temp_file code took ', tot_time, ' seconds to run')

    return tmp_file.name


def eu_air_pollutants_data(startdate: str, enddate: str, pollutants: list[str]) -> dict[str, pd.DataFrame]:

    """
    Fetch hourly air quality data from the EEA API for specified pollutants.

    Given a start and end timestamp (ISO 8601 format) and a list of pollutant
    codes, this function downloads both verified (E2a) and unverified (E1a)
    measurements for Oslo. It returns a dictionary mapping "<Station>_<PollutantName>"
    to a combined DataFrame containing all retrieved parquet data.

    Parameters
    ----------
    startdate : str
        The start of the query interval in "YYYY-MM-DDTHH:MM:SSZ" format.
    enddate : str
        The end of the query interval in "YYYY-MM-DDTHH:MM:SSZ" format.
    pollutants : list[str]
        A list of pollutant codes as defined by the EEA (e.g., "5" for PM10,
        "6001" for PM2.5, "8" for NO2).

    Returns
    -------
    dict[str, pandas.DataFrame]
        A mapping from "<Station>_<PollutantName>" to the corresponding
        pandas DataFrame of hourly measurements.
    """

    # Overview of airpollutant type code from the documentation.
    CODE_TO_NAME = {
        "5": "PM10",
        "6001": "PM2.5",
        "8": "NO2",
    }

    # API request filter based on the documentation description.
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

    # Splitting historic data in verified data (E2a) and unverified data (E1a).
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    start_d = datetime.strptime(startdate, fmt)
    end_d = datetime.strptime(enddate, fmt)
    date_stop = datetime(2024, 1, 1)

    all_dfs: dict[str, pd.DataFrame] = {}

    for dataset, seg_start, seg_end in [
        (2, start_d, min(end_d, datetime(2023, 12, 31, 23, 59, 59))), #Verified (E2a).
        (1, max(start_d, date_stop), end_d) # Unverified (E1a)
    ]:

        if seg_start > seg_end:
            continue

        # Switching to dataset 1 (for E1a) when dataset 2 is finished.
        body["dataset"] = dataset
        body["dateTimeStart"] = seg_start.strftime(fmt)
        body["dateTimeEnd"] = seg_end.strftime(fmt)
        print(f"Downloading data {dataset} from {body['dateTimeStart']} to {body['dateTimeEnd']}")

        r = requests.post(
            "https://eeadmz1-downloads-api-appservice.azurewebsites.net/ParquetFile",
            json=body,
            timeout=300
        )
        r.raise_for_status()

        # Reading the downloaded parquet file and stores as a dataframe.
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            for name in z.namelist():
                with z.open(name) as fp:

                    df = pd.read_parquet(fp)

                # Finding the station name and pollutant type, and sorts based on this.
                parts = name.split('_')
                station       = parts[1] if len(parts) > 1 else "UnknownStation"
                pollutant_code = parts[2] if len(parts) > 2 else "unknown"

                # Switching pollutant code with name.
                pollutant     = ( CODE_TO_NAME.get(pollutant_code, pollutant_code)
                    if pollutant_code.isdigit() else pollutant_code)
                key = f"{station}_{pollutant}"

                # If the key exists, insert data.
                if key in all_dfs:
                    all_dfs[key] = pd.concat([all_dfs[key], df], ignore_index=True)

                else:
                    all_dfs[key] = df

    return all_dfs


def write_to_excel_by_pollutant(AirData, out_dir="data"):

    """
    Writing the station dataframes in the dictionary to sheets
    in different excel files sorted by pollutant type.
    """

    os.makedirs(out_dir, exist_ok=True) # Making data folder C:.......\proj_environment-main\data

    print('Making excel seperate excel files for all air pollutant types.')
    print('--------------------------------------------------------------')
    print('  ')

    # Making seperate excel files for all the air pollutant types.
    grouped = defaultdict(dict) # Empty dict to be filled.
    for key, df in AirData.items():

        try:
            station, pollutant = key.split("_") # Fetching air pollutant type.

        except ValueError:
            print(ValueError)
            continue

        grouped[pollutant][station] = df

    print('Writing stationdata into excel files')
    print('-----------------------------')
    print(' ')

    # Writing the dataframes to seperate excel sheets.
    for pollutant, station_nr in grouped.items():

        file_path = os.path.join(out_dir, f"{pollutant}.xlsx")

        with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
            for station, df in station_nr.items():

                sheet_name = station
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Saved {file_path}")


def data_reader(filename, nanlimit,
                skiprows=None, usecols=None,
                nrows=None, sep=None):

    """Read the structure and information of a file.

    The file can be of type csv, xlsx, json, or html.
    If the file is not stored locally, you must use the download_temp_file
    function before calling this one. In that case, use tmp_file as the filename.

    This function prints:
    - Number of sheets if the file is Excel.
    - Memory usage information.
    - Column names.
    - Number of values per column.
    - Count of NaN values.
    - NaN percentage (for any column exceeding the nanlimit).
    - Count of negative values.
    - Column data types.
    - The first 10 rows of the dataset.
    """

    start_time = time.time()

    filename_only = os.path.basename(filename)

    print(' ')
    print(' ')
    print(f'Following information about the dataset {filename_only} was found:')
    print("-" * 75)

    _, extension = os.path.splitext(filename)  # Splits filename and filetype to read in the data correctly.

    # A test to check if the file exists in the directory. If it exists, the data will be downloaded to a pandas dataframe.
    try:
        if extension.lower() == '.csv':
            if sep is not None:
                data = pd.read_csv(filename, sep=sep)
            else:
                data = pd.read_csv(filename)

        elif extension.lower() == '.xlsx':
            xls = pd.ExcelFile(filename)
            ark_liste = xls.sheet_names  # Reading which sheets the excel file contains.
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
            data = pd.read_html(filename)[0]  # If the html file only has one table.

        else:
            print('Filetype not valid')
            sys.exit()

        print(' ')

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found. Please ensure it exists in the directory.")
        sys.exit()

    try:
        print("Available data of the DataFrame......")
        print(' ')

        # Printing the information found about the dataframe.
        print('Data format information')
        print('-----------------------')
        data.info(memory_usage="deep")

        # Gives warning if there is too many nan values.
        check_nan = data.isnull().sum()
        nan_prosent = check_nan / len(data) * 100
        if (nan_prosent > nanlimit).any():
            print(' ')
            print(f"The following columns exceed the NaN limit of {nanlimit}%")
            print(round(nan_prosent[nan_prosent > nanlimit], 2))
            print('WARNING! Please check the quality of your datasource')

        # Checks the float columns for any negative values.
        negative_values: dict[str, int] = {}
        for col in data.columns:
            if pd.api.types.is_float_dtype(data[col]):
                count = 0
                for val in data[col]:
                    if val < 0:
                        count += 1
                if count > 0:
                    negative_values[col] = count
                    print(' ')
                    print('Negative values was found in the columns:')
                    print(negative_values)
                    print('Check if the values of your data is allowed to be negative')
        print(' ')

        # Iterates through elements of type float64 and converts to float 32 to save memory usage.
        for col in data.columns:
            if data[col].dtype == np.float64:
                data[col] = data[col].astype(np.float32)
                print(f"Column {col} converted to float32 to save memory")
                print('DataFrame size is now: ', round(data.memory_usage(deep=True).sum() * 10 ** (-3), 2), 'kB')
                print(' ')

        # Tries to convert data elements of a column of mixed types to same type.
        for col in data.columns:

            unique_types = data[col].dropna().apply(lambda x: type(x)).unique()  # Finds unique dtypes of column.
            if len(unique_types) > 1:
                print(f"Column '{col}' has mixed types: {[t.__name__ for t in unique_types]}")

                # Tries to convert all elements to numeric value.
                try:
                    converted = pd.to_numeric(data[col], errors='raise')
                    data[col] = converted
                    print(f"Column '{col}' successfully converted to {data[col].dtype}")

                # If error e occurs, try to rather convert all elements to dtype string.
                except Exception as e:
                    print(f"Could not convert '{col}' elements to numeric : {e}")
                    data[col] = data[col].astype(str)
                    print(f"All elements in '{col}' converted to string")
            print('   ')

        print('First 10 rows of the DataFrame:')
        print('-------------------------------')
        print(data.head(10))
        print(' ')

        print('Stats of the DataFrame:')
        print('-----------------------')
        print(data.select_dtypes(include='float').describe()) # Finding stats only for columns of dtype float.
        print(' ')


    except Exception as e:
        raise Exception(f"An error occurred while processing the data: {e}")

    end_time = time.time()
    tot_time = end_time - start_time
    print(' ')
    print('The data reader code took ', tot_time, ' seconds to run')
    print("-" * 75)
    print(' ')
    print(' ')
    return data




