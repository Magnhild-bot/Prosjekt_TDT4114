## Datasets

This folder contains the code where datasets has been downloaded ready to be analyzed.
The goal of this project is to make a program that calculates and shows forecasts of the air quality.

### Air pollutants data
To analyze the air quality, data about the pollutants NO2, PM10, PM2.5 needs to be fetched. 
Accoring to FHI, these are three of the poullutants that causes the most illness and death. https://www.fhi.no/he/folkehelserapporten/miljo/luftforureining--i-noreg/?term=#om-luftforurensning
European Environment Agency (EEA) is chosen as the source to fetch these data, 
and EEA's documentation of downloading this data is uploaded in proj_environment-main\docs\data_documentation.
The EEA Air pollutant data is downloaded by using API request, and is therefore not visable in this folder before running
Datainnsamling.py under the proj_environment-main\notebooks folder. More information about the download in ...

### Temperature data
Further, temperatur data for Oslo between 2016 and 2024 has been downloaded as a csv file from Norsk Klimaservicesenter https://seklima.met.no/.
The file is stored in this folder as Temp_oslo_2016_2024.csv, and contains a monthly mean temperature for each month each year.
According to Miljødirektoratet, the most important source of emissions is exhaust from cars and dust from road wear, brakes and car tires. https://luftkvalitet.miljodirektoratet.no/artikkel/artikler/kilder-til-luftforurensning/
Because seasonal temperature variations strongly influence both vehicle usage and road conditions, incorporating monthly mean temperature into our 
analysis helps capture any relationship with traffic related emissions. 
In winter months when average temperatures drop below freezing, drivers fit studded or winter tires, 
which substantially increase non-exhaust emissions through accelerated road wear and tire abrasion.

### AQI data



