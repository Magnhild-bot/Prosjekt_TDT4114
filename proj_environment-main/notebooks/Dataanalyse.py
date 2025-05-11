
#------------------------Imports of files and functions--------------------#
import pickle
from pathlib import Path
import sys
import pandas as pd
import os
import matplotlib.pyplot as plt

project_dir = Path(__file__).resolve().parents[1]   #Dir to proj_environment-main
sys.path.insert(0, str(project_dir))#Dir to notebooks
data_dir = project_dir / "data" #Dir to data
from src.Functions_Dataanalysis import cap_outliers, plot_histogram,mean_std_meadin_corr,reggresion_analysis

pkl_dir=data_dir / "mean_air_pollutants.pkl" #Importing mean air pollutant data made in task 2 (Databehandling.py)
with pkl_dir.open( 'rb') as f:
    data = pickle.load(f)

#---------------------- RUN STAT ANALYSIS -------------------------#

NO2,PM25,PM10=cap_outliers(data, 'Value') #Remove outlaiers

plot_histogram(NO2,'orange','NO2')
plot_histogram(PM25,'darkgrey','PM2.5')
plot_histogram(PM10,'plum','PM10')

stats_NO2=mean_std_meadin_corr(NO2) #Finding mean, meadian, standard deviation and correlation.

NO2_trend_year,NO2_trend,NO2_seasonal=reggresion_analysis(NO2,'NO2','orange') #Regression analysis NO2
PM25_trend_year,PM25_trend,PM25_seasonal=reggresion_analysis(PM25,'PM25','darkgrey') #Regression analysis PM25
PM10_trend_year,PM10_trend,PM10_seasonal=reggresion_analysis(PM10,'PM10','plum') ##Regression analysis PM10



