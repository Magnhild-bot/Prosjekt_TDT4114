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
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from src.Functions_Dataanalysis import calculate_aqi
#from src.temp_module import Tempdata_manipulering
#from Dataanalyse import NO2_seasonal_raw,PM25_seasonal_raw, PM10_seasonal_raw

#Define directories
data_dir = project_dir / "data"
images_dir = os.path.join(project_dir, 'resources', 'images')

mean_air_p_path = data_dir/ 'mean_air_pollutants.pkl'
temp_oslo_path = data_dir/'temperatur_oslo.pkl'

with open(mean_air_p_path, 'rb') as f, \
    open(temp_oslo_path, 'rb') as temp_f:
    data      = pickle.load(f)
    temp_oslo = pickle.load(temp_f)


# reading AQI breakpoints, and color ranges
df_breakpoints = pd.read_excel(os.path.join(data_dir, 'aqi_breakpoints.xlsx') )
df_colors = pd.read_excel(os.path.join(data_dir, 'aqi_colors.xlsx'))

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
gs  = gridspec.GridSpec(
    nrows=3,
    ncols=2,
    width_ratios=[8, 2],
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
    df['AQI'] = df['Value'].apply(lambda v: calculate_aqi(v, aqi_breakpoints[pollutant]))
    ax.plot(df['Time Interval'], df['AQI'], color='black', linewidth=1.5, label=pollutant)
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
#plt.show()

# Plotting the weekly average mean of pollution for each pollutant in one figure with interactive tool to show AQI values

# 1 – inspect the DataFrame ---------------------------------------------------
print(temp_oslo.columns.tolist())   # see every column name
print(temp_oslo.head())  # see a few rows
print(temp_oslo['Tid(norsk normaltid)'][55])

# 2 – normalise column labels (strip blanks, remove BOMs, etc.)
temp_oslo.columns = temp_oslo.columns.str.strip()

# 3 – rename the two columns we need -----------------------------------------
# Replace the strings below with whatever you saw in step 1
temp_oslo = temp_oslo.rename(
    columns={
        'Tid(norsk normaltid)': 'Period',
        'Middeltemperatur (mnd)': 'Temperature'
    }
)

# 4 – verify the rename worked
assert 'Period' in temp_oslo.columns, 'Date column still not found'
assert 'Temperature' in temp_oslo.columns, 'Temperature column still not found'

# 5 – parse the date strings --------------------------------------------------
periods = temp_oslo['Period'].astype(str)

dt = pd.to_datetime(periods, format='%m.%Y', errors='coerce')   # strict pass 1
mask = dt.isna()                                               # any failures?
if mask.any():
    dt.loc[mask] = pd.to_datetime(periods[mask], dayfirst=True, errors='coerce')

# 6 – final sanity-check
if dt.isna().any():
    bad = periods[dt.isna()].unique()
    raise ValueError(f'Could not parse these period strings: {bad}')

temp_oslo['Time Interval'] = dt






'''
# If Temperature is stored with commas as decimal separators
if temp_oslo['Temperature'].dtype == object:
    temp_oslo['Temperature'] = (
        temp_oslo['Temperature']
        .str.replace(',', '.', regex=False)
        .astype(float)
    )
df_list = []
for pollutant, df in data.items():
    df2 = df.copy()
    df2['Time Interval'] = pd.to_datetime(df2['Time Interval'])
    df2.set_index('Time Interval', inplace=True)
    weekly_series = (df2['Value']
                     .resample('W-MON')
                     .mean().rename(pollutant)
                     )
    df_list.append(weekly_series)


df_wide = pd.concat(df_list, axis=1)
df_long = (
    df_wide.reset_index()
    .melt(id_vars ='Time Interval',
          var_name = 'Pollutant', value_name = 'Concentration')
)

df_long['AQI'] = df_long.apply( # computes the AQI value for each row / day
    lambda row: calculate_aqi(row['Concentration'],
                              aqi_breakpoints[row['Pollutant']]),
    axis=1
)

fig = make_subplots(
    specs = [[{'secondary_y': True}]],
    shared_xaxes=True
)

for pollutant, grp in df_long.groupby('Pollutant'):
    fig.add_trace(
        go.Scatter(
            x=grp['Time Interval'],
            y=grp['Concentration'],
            name = pollutant,
            mode = 'lines'
        ),
        secondary_y = False
    )

fig.add_trace(
    go.Scatter(
        x=temp_oslo['Time Interval'],
        y=temp_oslo['Temperature'],
        name='Temperature (C)',
        mode='lines',
        line=dict(dash='dash')
    ),
    secondary_y = True
)

fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Pollutant concentration (µg/m³)', secondary_y=False)
fig.update_yaxes(title_text='Temperature (°C)', secondary_y=True)

fig.update_layout(
    title='Weekly Mean Air Pollution and Monthly Temperature (Oslo)',
    hovermode='x unified'
)

fig.show()
'''