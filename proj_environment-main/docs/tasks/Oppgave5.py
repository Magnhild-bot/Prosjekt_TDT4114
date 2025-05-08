import pickle
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
import sys, os
from matplotlib.colors import LinearSegmentedColormap


# Load the pickle file
pollutant_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(pollutant_path))
#pkl_path = os.path.join(project_root, 'data', 'mean_air_pollutants.pkl')
#data = pd.read_pickle(pkl_path)



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

# AQI Colors (EPA Standard Colors)
aqi_colors = [
    ('Good', 'green', 0, 50),  # Green #00E400
    ('Moderate', 'yellow', 51, 100),  # Yellow
    ('Unhealthy for Sensitive Groups', 'orange', 101, 150),  # Orange
    ('Unhealthy', '#FF0000', 151, 200),  # Red
    ('Very Unhealthy', '#8F3F97', 201, 300),  # Purple
    ('Hazardous', '#7E0023', 301, 500)  # Brown
]


# Function to calculate AQI
def calculate_aqi(value, breakpoints):
    for low_conc, high_conc, low_aqi, high_aqi in breakpoints:
        if low_conc <= value <= high_conc:
            aqi = ((value - low_conc) / (high_conc - low_conc)) * (high_aqi - low_aqi) + low_aqi
            return aqi
    return 0  # Out of range


fig = plt.figure(figsize=(14, 12)) # Creating figure
gs  = gridspec.GridSpec(
    nrows=3, ncols=1,
    figure=fig,
    left=0.10,   # 10% of fig width reserved for y‐axis label
    right=0.95,  # up to 95% of fig width for the axes
    bottom=0.08, #  8% of fig height reserved for x‐axis label
    top=0.90,    # 90% of fig height; 10% reserved for suptitle
    hspace=0.35  # space between rows
)

# 2) Make each Axes from the GridSpec
axes = [fig.add_subplot(gs[i,0]) for i in range(3)]

# 3) Put your global decorations
fig.suptitle('AQI Levels Over Time', fontsize=18)
fig.text(0.04, 0.5, 'AQI Value', va='center', rotation='vertical', fontsize=12)

# Loop through pollutants and plot each
for ax, (pollutant, df) in zip(axes, data.items()):
    #if pollutant not in aqi_breakpoints:
     #   print(f"No AQI breakpoints defined for {pollutant}. Skipping...")
     #   continue

    # Calculate AQI and add to the DataFrame
    df['AQI'] = df['Value'].apply(lambda x: calculate_aqi(x, aqi_breakpoints[pollutant]))

    # Plot the pollutant data
    ax.plot(df['Time Interval'], df['AQI'], label=f'{pollutant} AQI', color='black', linewidth=1.5)
    ax.legend(loc='upper right')  # Keep pollutant label in top right

    # Plot the background color for AQI levels with full opacity
    for label, color, low, high in aqi_colors:
        ax.axhspan(low, high, facecolor=color, alpha=1.0)

    # Only set x-label on the last (bottom) subplot
    axes[-1].set_xlabel('Years', fontsize= 12)
    for ax in axes[:-1]:
        ax.set_xticklabels([])

plt.show()

# Global adjustments
# handles, labels = axes[0].get_legend_handles_labels()
# fig.legend(handles, labels, loc='upper right', title="AQI Levels", bbox_to_anchor=(0.9, 0.95))
# plt.tight_layout()
# plt.show()