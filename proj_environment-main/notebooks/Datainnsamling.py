import os
import sys
from pathlib import Path

# Relevant map paths.
project_dir = Path(__file__).resolve().parents[1]   # Dir to proj_environment-main.
sys.path.insert(0, str(project_dir)) # Dir to notebooks.
data_dir = project_dir / "data" # Dir to the datafiles.

from src.Functions_FetchData import eu_air_pollutants_data, write_to_excel_by_pollutant, download_temp_file, data_reader
"""
# 1: Requesting air pollutant data from EEU database, and checking the data information.

AirData = eu_air_pollutants_data(
    startdate="2016-01-01T00:00:00Z",
    enddate  ="2024-12-31T00:00:00Z",
    pollutants=["PM10", "NO2", "PM2.5"]
)
write_to_excel_by_pollutant(AirData, out_dir=data_dir) # Storing files to \proj_environment-main\data.

PM10_data=(os.path.join(data_dir, 'PM10.xlsx'))
data_reader(PM10_data,20) # PM10 data information.

PM25_data=(os.path.join(data_dir, 'PM2.5.xlsx'))
data_reader(PM25_data,20) # PM2.5 data information.

NO2_data=(os.path.join(data_dir, 'NO2.xlsx'))
data_reader(NO2_data,20) # NO2 data information.



# 2: CO2 data information.
csv_url = "https://sdi.eea.europa.eu/webdav/datastore/public/eea_t_national-emissions-reported_p_2024_v01_r00/CSV/UNFCCC_v27.csv"
CO2_data = download_temp_file(csv_url)
data_reader(CO2_data, 20)

"""
# 3: Temperature data information.
Temprature_Oslo=(os.path.join(data_dir, 'Temp_oslo_2016_2024.csv'))
data_reader(Temprature_Oslo, 20,sep=';')




