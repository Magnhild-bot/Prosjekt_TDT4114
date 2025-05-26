import os
import sys
from pathlib import Path
import pickle

project_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_dir))
#sys.path.insert((0, str(project_dir / 'src'))

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
import pandas as pd
import plotly.express as px

from src.Functions_Dataanalysis import calculate_aqi
#from src.temp_module import Tempdata_manipulering
#from Dataanalyse import NO2_seasonal_raw,PM25_seasonal_raw, PM10_seasonal_raw

#Define directories
data_dir = project_dir / "data"
images_dir = os.path.join(project_dir, 'resources', 'images')

pkl_path = data_dir/ 'mean_air_pollutants.pkl' # load mean_air_pollutants pickle file
with open(pkl_path, 'rb') as f:
    data = pickle.load(f) # loading in mean_pollutant dictionary from data folder

# reading AQI breakpoints, and color ranges
df_breakpoints = pd.read_excel(os.path.join(data_dir, 'aqi_breakpoints.xlsx') )
df_colors = pd.read_excel(os.path.join(data_dir, 'aqi_colors.xlsx'))
Tempdata=pd.read_csv((os.path.join(data_dir,'Temp_oslo_2016_2024.csv')),sep=';')

# AQI breakpoints for different pollutants (in µg/m³)
# Source for AQI breakpoints: https://www.pranaair.com/blog/what-is-air-quality-index-aqi-and-its-calculation/

# Build breakpoints dict
aqi_breakpoints = {}
for _, row in df_breakpoints.iterrows():
    pollutant = row['Pollutant']
    tup = (
        row['Low Concentration'],
        row['High Concentration'],
        row['Low AQI'],
        row['High AQI']
    )
    aqi_breakpoints.setdefault(pollutant, []).append(tup)

# Build color categories
aqi_colors = [
    (row['Category'], row['Color'], row['Low'], row['High'])
    for _, row in df_colors.iterrows()
]


# Plotting the AQI for each pollutant from 2016-2025
fig = plt.figure(figsize=(14, 12))
gs  = gridspec.GridSpec( # divides the figure into a grid
    nrows=3,
    ncols=2,
    width_ratios=[8, 1],
    wspace=0.1,
    hspace=0.35,
    left=0.07,
    right=0.95,
    top=0.92,
    bottom=0.08
)

axes = [fig.add_subplot(gs[i, 0]) for i in range(3)]
legend_ax = fig.add_subplot(gs[:, 1])
legend_ax.axis('off')


fig.suptitle('AQI Levels Over Time', fontsize=18, y=0.97) # global title for all subplots
fig.text(
    0.02, 0.5, 'AQI Value', va='center', rotation='vertical', fontsize=12
)

# Plotting loop
for ax, (pollutant, df) in zip(axes, data.items()):
    df['AQI'] = df['Value'].apply(lambda v: calculate_aqi(v, aqi_breakpoints[pollutant])) # computes AQI from concentration
    ax.plot(df['Time Interval'], df['AQI'], color='black', linewidth=1.5, label=pollutant) #plots AQI over time for each pollutant
    ax.legend(loc='upper right')
    for label, color, low, high in aqi_colors:
        ax.axhspan(low, high, facecolor=color, alpha=1.0) # adds AQI color rectangles across the axes for the pollutants
        # ax.axhspan (ymin, ymax, xmin=0, xmax=1)

    if ax is axes[-1]:
        ax.set_xlabel('Years', fontsize=12) # only bottom plot gets 'Year' axes label
    else:
        ax.set_xticklabels([])
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_ylim(0,500)

patches = [Patch(facecolor=color, label=label) for label, color, *_ in aqi_colors] # Making legend showing the meaning of the AQI colors/intervals
legend_ax.legend(
    patches, [p.get_label() for p in patches], title="AQI Categories", loc='center')

fig.savefig(images_dir, dpi=300, bbox_inches='tight')
plt.show()

####################################

### Plotting the weekly average mean of pollution for each pollutant in one figure with interactive tool to show AQI value

df_list = []
for pollutant, df in data.items():
    df2 = df.copy()
    df2['Time Interval'] = pd.to_datetime(df2['Time Interval'])
    df2.set_index('Time Interval', inplace=True)
    weekly_series = df2['Value'].resample('W-MON').mean().rename(pollutant)
    df_list.append(weekly_series)


df_wide = pd.concat(df_list, axis=1)
df_long = (
    df_wide.reset_index()
    .melt(id_vars ='Time Interval', var_name = 'Pollutant', value_name = 'Concentration')
)

df_long['AQI'] = df_long.apply( # computes the AQI value for each row / day
    lambda row: calculate_aqi(row['Concentration'], aqi_breakpoints[row['Pollutant']]),
    axis=1
)

iso = df_long['Time Interval'].dt.isocalendar()
df_long['Week'], df_long['Year'] = iso.week, iso.year
df_long['Concentration'] = df_long['Concentration'].round(1)
df_long['AQI'] = df_long['AQI'].round(0)


fig2 = px.line(
    df_long, x='Time Interval', y='Concentration', color='Pollutant',
    hover_data={'AQI': ':.0f', 'Concentration': ':.1f', 'Time Interval': False},
    labels={'Concentration': 'µg/m³'},
    title='Mean air pollution per week and AQI value'
)
fig2.update_xaxes(hoverformat='Week %W,%Y')
fig2.update_layout(hovermode='x unified')
fig2.show()



