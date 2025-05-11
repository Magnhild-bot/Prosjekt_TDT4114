import pickle
from pathlib import Path
import sys
project_dir = Path(__file__).resolve().parents[1]   #Finner dir til proj_environment-main
sys.path.insert(0, str(project_dir))#Dir til notebooks
data_dir = project_dir / "data" #Dir til excelarkene

from src.Functions_Dataanalysis import cap_outliers, plot_histogram,mean_std_meadin_corr,reggresion_analysis


pkl_dir=data_dir / "mean_air_pollutants.pkl"
with pkl_dir.open( 'rb') as f:
    data = pickle.load(f)
for key,value in data.items():
    print(key)

#--------------------Remove outlaiers--------------------------#

NO2,PM25,PM10=cap_outliers(data, 'Value')

#-------------------------Statistics--------------------------------#

plot_histogram(NO2,'orange','NO2')
plot_histogram(PM25,'darkgrey','PM2.5')
plot_histogram(PM10,'plum','PM10')

stats_NO2=mean_std_meadin_corr(NO2)

# -----------------Regression analysis-------------------------------------#
reggresion_analysis(NO2,'NO2','orange')
reggresion_analysis(PM25,'PM25','darkgrey')
reggresion_analysis(PM10,'PM10','plum')

