import requests
import tempfile
import time
import os
import zipfile
import io
import pandas as pd
from collections import defaultdict
from datetime import datetime


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
    date_stop = datetime(2023, 1, 1)

    all_dfs: dict[str, pd.DataFrame] = {}

    # To runder: først dataset=2 (verifiserte 2013-2022), deretter dataset=1 (UTD 2023→)
    for dataset, seg_start, seg_end in [
        (2, start_d, min(end_d, datetime(2022, 12, 31, 23, 59, 59))),
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




