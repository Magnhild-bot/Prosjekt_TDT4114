Datasets

This folder contains the code where datasets has been downloaded ready to be analyzed.
The goal of this project is to make a program that calculates and shows forecasts of the air quality. 
The user can put in any health conditions as Astma or Allergies, so the program can give the user relevant warnings.
To analyze tha air quality, data about the pollutants O3, NO2, CO, SO2, PM10, PM2.5 needs to be fetched. EEA is chosen as the source of this data.

The python file Functions_FetchData.py contains the selfmade functions for downloading data, as well as the data_reader() function.
The function EU_AirPollutantsData() is made with help of the documentation given by EEA (https://eeadmz1-downloads-webapp.azurewebsites.net/content/documentation/How_To_Downloads.pdf)

The FetchData.py uses the functions to download the datasets to the folder airdata_excel, that is going to be used further for analyzes.
The Datamanipulering.py is reading the data from the folder airdata_excel, and is giving the user an overview over what the data contains by using the function data_reader().
Further, the data is manipulated to take te mean value over air pollutant measurements from different stations in Oslo. Any negative numbers is also set to NaN, which is later changed to a mean value
for that excact timescale from the past data. The filtered mean data for the 6 different air pollutants is then saved to a Pickle file "mean_air_pollutants.pkl" for later use.

To download and filter data, run first the FetchData.py script and then the DataManipulering.py script.



