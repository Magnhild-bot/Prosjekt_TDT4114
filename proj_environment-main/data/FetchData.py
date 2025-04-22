from Functions_FetchData import*
"""
           ## URL TO FILE ##
csv_url = "https://sdi.eea.europa.eu/webdav/datastore/public/eea_t_national-emissions-reported_p_2024_v01_r00/CSV/UNFCCC_v27.csv"

     ## DOWNLOADING TEMPORARY FILE ##
temp_file = download_temp_file(csv_url)
print(f"Temporary file saved as: {temp_file}")
"""

#AirData=EU_AirPollutantsData(startdate="2025-01-01T00:00:00Z",enddate="2025-12-31T23:00:00Z",pollutants=['PM10','NO2','PM2.5'])

AirData = EU_AirPollutantsData(
    startdate="2024-01-01T00:00:00Z",
    enddate  ="2024-01-31T23:00:00Z",
    pollutants=["PM10", "NO2", "PM2.5"]
)




