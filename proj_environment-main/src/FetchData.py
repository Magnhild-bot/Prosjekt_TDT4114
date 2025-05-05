import Functions_FetchData as FF
import os
import sys
from pathlib import Path

script_dir=  Path(__file__).resolve().parent #dir til dette scriptet
project_dir=script_dir.parent#dir til hele prosjektmappen
data_dir = project_dir / "data" #dir til excelarkene
sys.path.insert(0, str(project_dir))


AirData = FF.EU_AirPollutantsData(
    startdate="2016-01-01T00:00:00Z",
    enddate  ="2024-12-31T00:00:00Z",
    pollutants=["PM10", "NO2", "PM2.5","O3","SO2","CO"]
)

FF.write_to_excel_by_pollutant(AirData, out_dir=data_dir)






