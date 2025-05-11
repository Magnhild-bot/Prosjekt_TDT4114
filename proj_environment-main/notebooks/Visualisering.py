# OPPGAVE 5 - VISUALISERING

import pickle
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
import pandas as pd
import os
import plotly.express as px

opg5 = os.path.dirname(__file__)

pkl_path = os.path.abspath(
    os.path.join(opg5, os.pardir, 'data', 'mean_air_pollutants.pkl') # load mean_air_pollutants pickle file
)

project_dir = os.path.abspath(
    os.path.join(opg5, os.pardir)
)
images_dir = os.path.join(project_dir, 'resources', 'images')
out_png = os.path.join(images_dir, 'aqi_levels.png') # path to images, and name of image

aqi_path = os.path.join(project_dir, 'data') # defines path of aqi data in the data folder

with open(pkl_path, 'rb') as f:
    data = pickle.load(f) # loading in mean_pollutant dictionary from data folder

breakpoints_path = os.path.join(aqi_path, 'aqi_breakpoints.xlsx') # loads aqi breakpoints
colors_path = os.path.join(aqi_path, 'aqi_colors.xlsx') # loads aqi colors

df_breakpoints = pd.read_excel(breakpoints_path)
df_colors = pd.read_excel(colors_path)

# AQI breakpoints for different pollutants (in µg/m³)
# Source for AQI breakpoints: https://www.pranaair.com/blog/what-is-air-quality-index-aqi-and-its-calculation/

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

aqi_colors = [
    (row['Category'], row['Color'], row['Low'], row['High'])
    for _, row in df_colors.iterrows()
]


def calculate_aqi(value, breakpoints): # function to calculate AQI for the different pollutants
    for low_conc, high_conc, low_aqi, high_aqi in breakpoints:  #cheks each breakpoint tuple
        if low_conc <= value <= high_conc:
            aqi = ((value - low_conc) / (high_conc - low_conc)) * (high_aqi - low_aqi) + low_aqi
            return aqi


###### Plotting the AQI for each pollutant from 2016-2025
fig = plt.figure(figsize=(14, 12))
gs  = gridspec.GridSpec( # divides the figure into a grid
    nrows=3, ncols=2,
    width_ratios=[8, 1],   # left column 8x wider than right column
    wspace=0.1,            # horizontal spacing between columns
    hspace=0.35,           # vertical spacing between rows
    left=0.07, right=0.95, top=0.92, bottom=0.08
)


axes = [fig.add_subplot(gs[i, 0]) for i in range(3)] # adds the three subplots axes in the left column

legend_ax = fig.add_subplot(gs[:, 1]) # in the second gs column the legend is placed
legend_ax.axis('off')  # no ticks, no frame


fig.suptitle('AQI Levels Over Time', fontsize=18, y=0.97) # global title for all subplots
fig.text(0.02, 0.5, 'AQI Value', va='center', rotation='vertical', fontsize=12) # global y-axis

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

handles = [Patch(facecolor=color, label=label) for label, color, *_ in aqi_colors] # Making legend showing the meaning of the AQI colors/intervals
legend_ax.legend(
    handles,
    [h.get_label() for h in handles],
    title="AQI Categories",
    loc='center',
    frameon=True,
    fontsize=9,
    title_fontsize=11,
    handlelength=1.0,
    handletextpad=0.5
)

fig.savefig(out_png, dpi=300, bbox_inches='tight')
#plt.show()

####################################

### Plotting the weekly average mean of pollution for each pollutant in one plot with interactive tool to show AQI value


weekly_series = []
for pollutant, df in data.items(): #goes through each pollutant and every hour from the dictionary
    data2 = df.copy() # makes a copy to not overwrite the data dictionary

    data2['Time Interval'] = pd.to_datetime(data2['Time Interval']) # makes sure the time interval is Date time object and not string
    data2 = data2.set_index('Time Interval') #makes the timestamp the index

    mean_week_pollution= (
        data2['Value'].resample('W-MON').mean().rename(pollutant)
    )



    weekly_series.append(mean_week_pollution) # adds mean value to daily_series list


df_wide = pd.concat(weekly_series, axis=1) # combines the series to one df, with the date and pollution concentration for each pollutant



df_long = df_wide.reset_index().melt( # converst from wide form in df_wide to long form in df_long
    id_vars='Time Interval', # keep 'Time Interval' fixed
    var_name='Pollutant',# put pollutant column headers into a new column called 'Pollutant'
    value_name='Concentration' # takes value of each cell and put it into a new column called 'Concentration'
)


df_long['AQI'] = df_long.apply( # computes the AQI value for each row / day
    lambda r: calculate_aqi(r['Concentration'], aqi_breakpoints[r['Pollutant']]),
    axis=1
)

#week number
iso = df_long['Time Interval'].dt.isocalendar()
df_long['Week'] = iso.week
df_long['Year'] = iso.year

df_long['Concentration'] = df_long['Concentration'].round(1)
df_long['AQI'] = df_long['AQI'].round(0)


# 5) Interactive Plotly line plot of daily means
fig = px.line(
    df_long,
    x='Time Interval',
    y='Concentration',
    color='Pollutant',
    hover_data={
        'AQI': ':.0f', #integer
        'Concentration': ':.1f',#one decimal
        'Time Interval': False

    },
    labels={
        #'': '',
        'Concentration': 'µg/m³'
    },
    title='Mean air pollution per week and AQI value'
)
fig.update_xaxes(hoverformat='Week %W,%Y')
fig.update_layout(hovermode='x unified')
fig.show()

