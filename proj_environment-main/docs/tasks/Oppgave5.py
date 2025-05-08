import pickle
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
import sys, os
from matplotlib.colors import LinearSegmentedColormap


# Load the pickle file
pollutant_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(pollutant_path))
pkl_path = os.path.join(project_root, 'data', 'mean_air_pollutants.pkl')
data = pd.read_pickle(pkl_path)


######### Plotting of AQI values for NO2, PM10, PM2.5 ###

# Define AQI breakpoints for different pollutants (in µg/m³)
# Source for AQI breakpoints: https://www.pranaair.com/blog/what-is-air-quality-index-aqi-and-its-calculation/
aqi_breakpoints = {
    'NO2': [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 180, 101, 200),
        (181, 280, 201, 300),
        (281, 400, 301, 400),
        (401, float('inf'), 301, 500),
    ],
    'PM10': [
        (0, 54, 0, 50),
        (55, 154, 51, 100),
        (155, 254, 101, 150),
        (255, 354, 151, 200),
        (355, 424, 201, 300),
        (425, float('inf'), 301, 500),
    ],
    'PM2.5': [
        (0, 12, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, float('inf'), 301, 500),
    ]
}

# AQI Colors
aqi_colors = [
    ('Good', 'green', 0, 50),  # Green
    ('Moderate', 'yellow', 51, 100),  # Yellow
    ('Unhealthy for Sensitive Groups', 'orange', 101, 150),  # Orange
    ('Unhealthy', 'red', 151, 200),  # Red
    ('Very Unhealthy', 'purple', 201, 300),  # Purple
    ('Hazardous', 'brown', 301, 500)  # Brown
]


def calculate_aqi(value, breakpoints): # function to calculate AQI for the different pollutants
    for low_conc, high_conc, low_aqi, high_aqi in breakpoints:
        if low_conc <= value <= high_conc:
            aqi = ((value - low_conc) / (high_conc - low_conc)) * (high_aqi - low_aqi) + low_aqi
            return aqi
    return 0  # Out of range



# 1) Set up a Figure + a 2-col GridSpec (3 rows × 2 cols)
fig = plt.figure(figsize=(14, 12))
gs  = gridspec.GridSpec(
    nrows=3, ncols=2,
    width_ratios=[8, 1],   # left col 8× wider than right
    wspace=0.1,            # small gap between cols
    hspace=0.35,           # your existing row spacing
    left=0.07, right=0.95, top=0.92, bottom=0.08
)

# 2) Make your 3 plot axes in the left column
axes = [fig.add_subplot(gs[i, 0]) for i in range(3)]

# 3) Make a single “legend” axes that spans all 3 rows in the right column
legend_ax = fig.add_subplot(gs[:, 1])
legend_ax.axis('off')  # no ticks, no frame

# 4) Global decorations
fig.suptitle('AQI Levels Over Time', fontsize=18, y=0.97)
fig.text(0.02, 0.5, 'AQI Value', va='center', rotation='vertical', fontsize=12)

# 5) Your existing plotting loop
for ax, (pollutant, df) in zip(axes, data.items()):
    df['AQI'] = df['Value'].apply(lambda v: calculate_aqi(v, aqi_breakpoints[pollutant]))
    ax.plot(df['Time Interval'], df['AQI'], color='black', linewidth=1.5, label=pollutant)
    ax.legend(loc='upper right')
    for label, color, low, high in aqi_colors:
        ax.axhspan(low, high, facecolor=color, alpha=1.0)
    # only bottom gets x-labels
    if ax is axes[-1]:
        ax.set_xlabel('Years', fontsize=12)
    else:
        ax.set_xticklabels([])
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_ylim(0,500)

handles = [Patch(facecolor=color, label=label) for label, color, *_ in aqi_colors] # Making ledgend showing the meaning of the AQI colors/intervals
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


