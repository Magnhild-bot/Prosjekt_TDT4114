import Functions_FetchData as FF
import os
import sys

script_dir= os.path.dirname(os.path.abspath(__file__)) #dir til dette scriptet
project_dir=os.path.dirname(script_dir)#dir til hele prosjektmappen
airdata_dir=os.path.join(script_dir,'airdata_excel') #dir til excelarkene
sys.path.insert(0, project_dir)

from Mappe_del1.Datareader import data_reader


"""
           ## URL TO FILE ##
csv_url = "https://sdi.eea.europa.eu/webdav/datastore/public/eea_t_national-emissions-reported_p_2024_v01_r00/CSV/UNFCCC_v27.csv"

     ## DOWNLOADING TEMPORARY FILE ##
temp_file = download_temp_file(csv_url)
print(f"Temporary file saved as: {temp_file}")
"""


AirData = FF.EU_AirPollutantsData(
    startdate="2020-01-01T00:00:00Z",
    enddate  ="2024-12-31T00:00:00Z",
    pollutants=["PM10", "NO2", "PM2.5","O3","SO2","CO"]
)

FF.write_to_excel_by_pollutant(AirData, out_dir="airdata_excel")
file=os.path.join(airdata_dir,'NO2.xlsx')
data_reader(file,20)



