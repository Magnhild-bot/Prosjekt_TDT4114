import Functions_FetchData as FF
import os
import sys

script_dir= os.path.dirname(os.path.abspath(__file__)) #dir til dette scriptet
project_dir=os.path.dirname(script_dir)#dir til hele prosjektmappen
airdata_dir=os.path.join(script_dir,'airdata_excel') #dir til excelarkene
sys.path.insert(0, project_dir)



AirData = FF.EU_AirPollutantsData(
    startdate="2020-01-01T00:00:00Z",
    enddate  ="2024-12-31T00:00:00Z",
    pollutants=["PM10", "NO2", "PM2.5","O3","SO2","CO"]
)

FF.write_to_excel_by_pollutant(AirData, out_dir="airdata_excel")






