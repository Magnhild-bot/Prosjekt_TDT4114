import pandas as pd
import os
from Functions_FetchData import data_reader
from Functions_FetchData import download_temp_file

script_dir= os.path.dirname(os.path.abspath(__file__)) #dir til dette scriptet
project_dir=os.path.dirname(script_dir)#dir til hele prosjektmappen
data_dir=os.path.join(project_dir,'data')


#------------Cheks what information the file contains by using the data_reader function-------------


#1:
Airpollutant_data=(os.path.join(data_dir, 'PM10.xlsx'))
data_reader(Airpollutant_data,20)


print('    ')
print('    ')
print('Tester ny fil...........')
print('    ')


#2:
csv_url = "https://sdi.eea.europa.eu/webdav/datastore/public/eea_t_national-emissions-reported_p_2024_v01_r00/CSV/UNFCCC_v27.csv"
CO2_data = download_temp_file(csv_url) #fra test_filbehandling
data_reader(CO2_data, 30)




