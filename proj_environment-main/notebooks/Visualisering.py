# OPPGAVE 5 - VISUALISERING

import pickle
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
import sys, os
from matplotlib.colors import LinearSegmentedColormap

opg5 = os.path.dirname(__file__)
pkl_path = os.path.abspath(
    os.path.join(opg5, os.pardir, 'data', 'mean_air_pollutants.pkl')
)

with open(pkl_path, 'rb') as f:
    data = pickle.load(f)


######### Plotting of AQI values for NO2, PM10, PM2.5 ###

# AQI breakpoints for different pollutants (in µg/m³)
# Source for AQI breakpoints: https://www.pranaair.com/blog/what-is-air-quality-index-aqi-and-its-calculation/






def calculate_aqi(value, breakpoints): # function to calculate AQI for the different pollutants
    for low_conc, high_conc, low_aqi, high_aqi in breakpoints:  #cheks each breakpoint tuple
        if low_conc <= value <= high_conc:
            aqi = ((value - low_conc) / (high_conc - low_conc)) * (high_aqi - low_aqi) + low_aqi
            return aqi




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

plt.show()


