import requests
import tempfile
import time
import os
import zipfile
import io
import pandas as pd

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

    # Oppslagstabell:      kode: luftforurensnings‑navn
    # -----------------------------------------------------------
    CODE_TO_NAME = {
        "5": "PM10",
        "8": "PM2.5",
        "6001": "NO2",
        "14": "O3",
        "1": "SO2",
        "7": "CO",
    }

    # API request filteret. Bygd opp slik som nettsiden forklarte (skriv en bedre kommentar her, kanskje vi bør legge inn kilde)
    body = {
        "countries":      ["NO"],
        "cities":         ["Trondheim"],
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

            parts = name.split('_')
            station     = parts[1] if len(parts) > 1 else "UnknownStation"
            code_or_txt = parts[2] if len(parts) > 2 else "unknown"

            # Hvis tredje felt er numerisk → slå opp i CODE_TO_NAME, ellers bruk som er
            pollutant = (
                CODE_TO_NAME.get(code_or_txt, code_or_txt)
                if code_or_txt.isdigit() else code_or_txt
            )

            key = f"{station}_{pollutant}"

            df.attrs.update(station=station, pollutant=pollutant)

            dfs[key] = df

    return dfs




