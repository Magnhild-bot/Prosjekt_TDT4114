### Datasets

This folder contains the code where datasets has been downloaded ready to be analyzed.
The goal of this project is to make a program that calculates and shows forecasts of the air quality.
To analyze the air quality, data about the pollutants NO2, PM10, PM2.5 needs to be fetched. 
Accoring to FHI, these are three of the poullutants that causes the most illness and death. https://www.fhi.no/he/folkehelserapporten/miljo/luftforureining--i-noreg/?term=#om-luftforurensning
European Environment Agency (EEA) is chosen as the source to fetch these data, 
and EEA's documentation of downloading this data is uploaded in proj_environment-main\docs\data_documentation.
The EEA Air pollutant data is downloaded by using API request, and is therefore not visable in this folder before running
Datainnsamling.py under the proj_environment-main\notebooks folder.

The python file Functions_FetchData.py contains the selfmade functions for downloading data, as well as the data_reader() function.
The function eu_air_pollutants_data() is made with help of the documentation given by EEA (https://eeadmz1-downloads-webapp.azurewebsites.net/content/documentation/How_To_Downloads.pdf)

Further, temperatur data for Oslo between 2016 and 2024 has been downloaded as a csv file from Norsk Klimaservicesenter https://seklima.met.no/.
The file is stored in this folder as Temp_oslo_2016_2024.csv, and contains a monthly mean temperature for each month each year.
According to Miljødirektoratet, the most important source of emissions is exhaust from cars and dust from road wear, brakes and car tires. https://luftkvalitet.miljodirektoratet.no/artikkel/artikler/kilder-til-luftforurensning/

The FetchData.py uses the functions to download the datasets to the folder airdata_excel, that is going to be used further for analyzes.
The Datamanipulering.py is reading the data from the folder airdata_excel, and is giving the user an overview over what the data contains by using the function data_reader().
Further, the data is manipulated to take te mean value over air pollutant measurements from different stations in Oslo. Any negative numbers is also set to NaN, which is later changed to a mean value
for that excact timescale from the past data. The filtered mean data for the 6 different air pollutants is then saved to a Pickle file "mean_air_pollutants.pkl" for later use.

To download and filter data, run first the FetchData.py script and then the DataManipulering.py script.



