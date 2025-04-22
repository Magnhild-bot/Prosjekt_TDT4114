import requests
import tempfile
import time
import os
import zipfile
import io
import pandas as pd
from collections import defaultdict


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
    enddate:   str,
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
        "countries":      ["NO"],
        "cities":         ["Oslo"],
        "pollutants":     pollutants,
        "dataset":        1,
        "dateTimeStart":  startdate,
        "dateTimeEnd":    enddate,
        "aggregationType":"hour",
    }

    r = requests.post(
        "https://eeadmz1-downloads-api-appservice.azurewebsites.net/ParquetFile",
        json=body,
        timeout=300
    )
    r.raise_for_status()

    # --- Les ZIP‑en direkte i minnet og bygg et dict med nøkler basert på type pollutant og stasjonsnavn ---
    dfs: dict[str, pd.DataFrame] = {}

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        for name in z.namelist():          # ett parquet‑fil per stasjon - pollutant
            with z.open(name) as fp:
                df = pd.read_parquet(fp)


            #Finner stasjonsnavn og type pollutant fra dataen som ble lastet ned
            parts = name.split('_')
            station     = parts[1] if len(parts) > 1 else "UnknownStation" 
            pollutant_type = parts[2] if len(parts) > 2 else "unknown"

           #Hvis pullutant type er beskrevet med tall, erstatt tallet med riktig navn:
            pollutant = (
                CODE_TO_NAME.get(pollutant_type, pollutant_type)
                if pollutant_type.isdigit() else pollutant_type
            )

            key = f"{station}_{pollutant}"

            df.attrs.update(station=station, pollutant=pollutant)

            dfs[key] = df

    return dfs


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




