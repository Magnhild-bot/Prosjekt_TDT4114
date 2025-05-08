import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from pathlib import Path
import sys
from statsmodels.tsa.seasonal import STL
import statsmodels.api as sm
import seaborn as sns

script_dir=  Path(__file__).resolve().parent #dir til dette scriptet
docs_dir=script_dir.parent#dir til hele docs mappen
project_dir=docs_dir.parent #dir til hele prosjektmappen
data_dir = project_dir / "data" #dir til excelarkene og picklen
sys.path.insert(0, str(project_dir))


pkl_dir=data_dir / "mean_air_pollutants.pkl"
with pkl_dir.open( 'rb') as f:
    data = pickle.load(f)
for key,value in data.items():
    print(key)

#--------------------Remove outlaiers--------------------------#

def cap_outliers(data, column):
    """
    Identifiserer tydlige uteliggere, og bytter dem ut med øvre eller nedre kvartil.
    Q1: snittet av de nederste 25% målingene (25% precentile).
    Q3: snittet av de øvre 25% målingene (75% precentile).
    IQR: Differansen mellom nedre og øvre kvartil. Kalles ofte kvartilbredden.
    [Q1 - 1.5*IQR, Q3 + 1.5*IQR]: teoretiske øvre og nedre grense for whiskers.
    """
    def quartiles(df):
        df = df.copy()
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1 #
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df[column]= df[column].clip(lower=lower_bound, upper=upper_bound)
        return df

    NO2=quartiles(data['NO2'])
    #O3=quartiles(data['O3'])
    PM25=quartiles(data['PM2.5'])
    PM10=quartiles(data['PM10'])

    data_w_outliars = [data['NO2']['Value'].values,               #data['O3']['Value'].values,
        data['PM2.5']['Value'].values, data['PM10']['Value'].values]

    data_wo_outliars=[NO2['Value'].values, #O3['Value'].values,
                      PM25['Value'].values, PM10['Value'].values]

    colors=['orange','teal','darkgrey'] #,'plum'

    plt.figure(figsize=(8, 4))
    sns.boxplot(data=data_w_outliars,palette=colors)
    plt.xticks([0, 1, 2],['NO₂',  'PM₂.₅', 'PM₁₀']) #'O₃',
    plt.ylabel("Measure [µg/m^3]")
    plt.title("Deviation of the pollutant measurements")
    plt.show()

    plt.figure(figsize=(8, 4))
    sns.boxplot(data=data_wo_outliars,palette=colors)
    plt.xticks([0, 1, 2], ['NO₂',  'PM₂.₅', 'PM₁₀']) #'O₃',
    plt.ylabel("Pollutant measure [µg/m^3]")
    plt.title("Deviation of the pollutant measurements with outliars removed")
    plt.show()

    return NO2,  PM25, PM10 #O3

NO2,PM25,PM10=cap_outliers(data, 'Value') #O3,

#-------------------------Statistics--------------------------------#

def plot_histogram(df,color,title):
    plt.figure(figsize=(8, 4))
    sns.histplot(data=df, x="Value", bins=20,kde=True,color=color,edgecolor=None,alpha=0.5,shrink=0.8)
    plt.ylabel("Count")
    plt.xlabel("Pollutant measure [µg/m^3] ")
    plt.title(f'Histogram of {title} pollutant measurements')
    plt.grid(axis='y')
    plt.show()

plot_histogram(NO2,'orange','NO2')
#plot_histogram(O3,'teal','O3')
plot_histogram(PM25,'darkgrey','PM2.5')
plot_histogram(PM10,'plum','PM10')



def mean_std_meadin_corr(df):
    """
    Meadian: Det midterste tallet av en stortert tallrekke. Sir noe om hvilket tall som er vanlig.
    Standrard avvik: Hvor langt unna gjennomsnittet ligger 68% av dataene.
    Mean : Gjennomsnittet
    Correlation: Parson korrelasjon leter etter en linær trend på hvordan veskten fra dag til dag ser ut.
                Noen kilder skriver at en bør ha minst en COrrelasjon på +- 0.6 for å kalle det en god korrelasjon.
    """
    median_emission = df['Value'].median() #meadian
    std_emission = df['Value'].std() #standard avvik
    mean_emission = df['Value'].mean() #gjn.snitt
    correlation = df['Time Interval'].corr(NO2['Value'])  # Korrelasjon mellom år og utslipp

    print(f"Gjennomsnittlig utslippsnivå:, {mean_emission:.3f}")
    print(f"Median utslippsnivå: {median_emission:.3f}")
    print(f"Standardavvik utslippsnivå: {std_emission:.3f}")
    print(f"Korrelasjon mellom år og utslipp for NO2: {correlation:.3f}")

    if correlation < 0.6:
        print(' ')
        print(f'Seems like the correlation of your data is close to zero {correlation:.3f} is very low.')
        print('Your has likely season variations.')
        print(' ')

    dict_stats={'Meadian':median_emission,
                'Standard deviation':std_emission,
                'Mean':mean_emission,
                'Correlation':correlation}

    return dict_stats

stats_NO2=mean_std_meadin_corr(NO2)


# -----------------Regression analysis-------------------------------------#

def reggresion_analysis(df,name,color):

    """
        .resample() tar inn MS for første dagen hver måned og finner gjennomsnittet for denne måneden.
    """

    df["Time Interval"] = pd.to_datetime(df["Time Interval"]) #Gjør om til datetime, eks: 2020-01-01 00:00:00
    df = df.set_index("Time Interval").sort_index() #Setter datetime som index, feks istede for index 0 er indexen 2020-01-01 00:00:00
    monthly = df["Value"].resample("MS").mean().interpolate("time") #finner månterlig gjennomsnitt for de ulike årene, og interpolerer evt nan verdier

    stl = STL(monthly, period=12, seasonal=25, robust=True)   # 12 måneder per år
    res = stl.fit()
    trend= res.trend           # finner sesongbasert trend
    seasonal= res.seasonal     # finner ut om det er et fast mønster i trenden
    resid= res.resid           # uteliggerene som avviker fra snittet ??

    plt.figure()
    plt.plot(monthly, label="Observation",color=color, alpha=.5)
    plt.plot(trend,   label="Trend (STL)",linestyle='--',color='deeppink')
    plt.plot(seasonal, label="Seasonal (STL)")
    plt.title(f"Monthly STL trends VS observations in {name}")
    plt.legend()
    plt.show()

                  ## Finner årlig trend ##

    x_years = trend.index.year + (trend.index.dayofyear / 365.25) # Lineær trend på utslippsnivå (slope i "verdi per år")
    a, b = np.polyfit(x_years, trend.values, 1)

    print(f"Linear trend is a change of {a:.4f} [µg/m^3] {name} per year")

    y_fit = a * x_years + b

    # Finn sorteringsrekkefølgen
    order = np.argsort(x_years)
    x_sorted = x_years[order]
    y_fit_sorted = y_fit[order]

    plt.figure(figsize=(8,4))
    plt.plot(x_years, trend.values,linestyle='--',color='deeppink', label='Trend-data')
    plt.plot(x_sorted, y_fit_sorted, color=color, linewidth=2,
             label=f'Fit: y = {a:.3f}·x')
    plt.xlabel('Year')
    plt.ylabel('Pollutant measure µg/m^3')
    plt.title(f'Linear reggression of {name} measure between 2016-2024')
    plt.legend()
    plt.show()

reggresion_analysis(NO2,'NO2','orange')
#reggresion_analysis(O3,'O3','teal')
reggresion_analysis(PM25,'PM25','darkgrey')
reggresion_analysis(PM10,'PM10','plum')


#4) Litt kommentarer

##Regresjonsanalyse er en analyse som ser sammenhenger mellom en avhengig variabel og en eller flere uavhengige variabler, 
#det kan være interessant i denne sammenhengen, der vi kan se på sammenheng mellom utslipp og klima blant annet

##Fylling av tomme kolonner med gjennomsnitt:
#Fordeler: Gir en kontinuerlig linje og gjør dataene lettere å analysere.
#Ulemper: Kan føre til skjevhet, spesielt hvis det er store variasjoner i dataene. Er kanskje ikke representativt for de faktiske utslippene.
#Mulig feilkilde: Å bruke gjennomsnittet kan overskygge virkelige topper eller bunner i dataene, og gi et feil bilde av trenden

#Lineær interpolasjon:
#Fordeler: Gir en mer realistisk fylling basert på eksisterende data, og bevarer trenden på en bedre måte
#Ulemper: Forutsetter at utslippene endrer seg jevnt, og kan gi feil bilde hvis utslippene varierer mer i virkeligheten
#Mulig feilkilde: Hvis dataene har stor variasjon i verdiene, kan interpolasjon da anta at trenden er jevn
