import sys
from pathlib import Path
import os

project_dir = Path(__file__).resolve().parents[1]   #Finner dir til proj_environment-main
sys.path.insert(0, str(project_dir))#Dir til notebooks
data_dir = project_dir / "data" #Dir til excelarkene

from src.Functions_FetchData import EU_AirPollutantsData, write_to_excel_by_pollutant, download_temp_file,data_reader


#------------Importing files from EEU database using API request-----------------------------------#

#Air pollutant data
AirData = EU_AirPollutantsData(
    startdate="2016-01-01T00:00:00Z",
    enddate  ="2024-12-31T00:00:00Z",
    pollutants=["PM10", "NO2", "PM2.5"]
)
write_to_excel_by_pollutant(AirData, out_dir=data_dir)

#CO2 data
#csv_url = "https://sdi.eea.europa.eu/webdav/datastore/public/eea_t_national-emissions-reported_p_2024_v01_r00/CSV/UNFCCC_v27.csv"
#CO2_data = download_temp_file(csv_url)

#------------Cheks what information the file contains by using the data_reader function-------------

#1: Air pollutant data information
Airpollutant_data=(os.path.join(data_dir, 'PM10.xlsx'))
data_reader(Airpollutant_data,20)
print('    ')
print('    ')
print('Tester ny fil...........')
print('    ')


#2: CO2 data information
#data_reader(CO2_data, 30)


#3: Temperature data information
Temprature_Oslo=(os.path.join(data_dir, 'Temp_oslo_2016_2024.csv'))
data_reader(Temprature_Oslo, 30,sep=';')




