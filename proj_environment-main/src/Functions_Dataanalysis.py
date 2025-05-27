import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import STL
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
import plotly.express as px



class Pollutants_manipulering:

    """
        A class for cleaning and aggregating air quality measurements.

        Given a dictionary of pandas DataFrames—each containing time‐series pollutant
        readings (e.g., NO₂, PM10, PM2.5) from various monitoring stations—this class:

        1. Replaces invalid values (negative readings and extreme outliers) with NaN.
        2. Verifies that each station’s dataset has the expected number of observations,
           and discards any that do not meet the size requirement.
        3. Computes a unified, hourly mean pollutant concentration across all remaining
           stations, linearly interpolating any missing values.

        Call `run_all()` to execute the full pipeline in sequence and return
        a single DataFrame of cleaned, aggregated pollutant levels.
        """

    def __init__(self, dict_file):
        """
        Initializes the pollutant data manipulation instance.

        Args:
            dict_file (dict): A dictionary containing DataFrames for NO2, PM10, and PM2.5 measurements.
        """
        self.dict_file = dict_file

    def negative_to_nan(self):
        print(' ')
        print('Replacing negative values and outliers with NaN')

        # Iterate through the "Value" column in each sheet and replace
        # negative readings and extreme outliers with NaN.
        for sheet, df in self.dict_file.items():
            df.loc[df["Value"] < 0, "Value"] = np.nan
            df.loc[df["Value"] > 430, "Value"] = np.nan  # Highest extreme AQI scale value of PM10, PM25 and NO2 is 430 of PM10.

    def lenght_test(self):
        print(' ')
        print('Checking the size of each data sheet')

        size = {sheet: df.shape for sheet, df in self.dict_file.items()}  # Get the dimensions of each DataFrame.
        unique_sizes = set(size.values())  # Determine how many distinct sizes are present.
        print(' ')
        print('Data sheet   |  Size')
        print('---------------------')
        for sheet, dims in size.items():
            print(f' {sheet}: {dims}')
            if dims[0] < 78000:  # Expected row count is 78887
                print(f'Invalid data size found. Removing {sheet} from dictionary.')
                self.dict_file.pop(sheet)

    def mean_value_pollutant(self):
        print(' ')
        print('Computing the mean pollutant concentration over the stations of Oslo.')
        print('NaN values will be filled by linear interpolation.')

        # Collect all "Value" series from each DataFrame.
        pollutant_data = [df['Value'] for df in self.dict_file.values()]
        pollutant_concat = pd.concat(pollutant_data, axis=1)

        # Compute the row-wise mean, skipping NaN.
        mean_pollutant = pollutant_concat.mean(axis=1, skipna=True)

        # Use the "Start" column from the first sheet for time intervals.
        first_df = next(iter(self.dict_file.values()))
        time_intervals = pd.to_datetime(first_df['Start'])

        result = pd.DataFrame({
            'Time Interval': time_intervals,
            'Value': mean_pollutant.values
        })

        # Linearly interpolate any missing values.
        result['Value'] = result['Value'].interpolate()

        return result

    def run_all(self) -> pd.DataFrame:
        """
        Run all processing steps in the correct order and return the final dataset.
        """
        self.negative_to_nan()
        self.lenght_test()
        return self.mean_value_pollutant()

class Tempdata_manipulering:

    """
    Doing relevant data manipulation for temperature data.

    - Replacing nan values with interpolated value.
    - Replacing comma with dot for descimal delimiters.

    """

    def __init__(self, df):
        """
        Initializes a dict_file instance.

        Args:
            df (Dataframe): Dataframe with information of temperature in oslo between 2016-2024
            """
        self.df = df

    def interpolate_nan(self) -> pd.DataFrame:

        # Replacing comma with dot for descimals.
        self.df['Middeltemperatur (mnd)'] = (
            self.df['Middeltemperatur (mnd)']
            .astype(str)
            .str.replace(',', '.', regex=False)
            .str.extract(r'([-+]?\d*\.?\d+)', expand=False)
        )

        # Finding number of nan.
        nan_vals = self.df['Middeltemperatur (mnd)'].isna().sum()
        print(f"Removing {nan_vals} NaN values")

        # Converting elements from object to float.
        self.df['Middeltemperatur (mnd)'] = (
            pd.to_numeric(self.df['Middeltemperatur (mnd)'], errors='coerce')
        )

        # Interpolating nan values.
        self.df['Middeltemperatur (mnd)'] = (
            self.df['Middeltemperatur (mnd)'].interpolate()
        )

        nan_left = self.df['Middeltemperatur (mnd)'].isna().sum()
        print(f"{nan_left} left")

        return self.df




def cap_outliers(data, column,plot=True):

    """
    Identify obvious outliers and replace them with the nearest quartile bound.

    Q1: the 25th percentile (mean of the lowest 25% of measurements).
    Q3: the 75th percentile (mean of the highest 25% of measurements).
    IQR: interquartile range, the difference between Q3 and Q1.
    Whisker bounds: [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR], the theoretical lower and upper limits.
    """

    # Function for finding quartiles and the IQR.
    def quartiles(df,name):
        df = df.copy()
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df[column]= df[column].clip(lower=lower_bound, upper=upper_bound)

        if plot:
            print(' ')
            print(f'    - First quartile of {name} is: {Q1}')
            print(f'    - Third quartile of {name} is: {Q3}')
        return df

    # Finding quatriles and IQR of NO2, PM2.5 and PM10.
    NO2=quartiles(data['NO2'],'NO2')
    PM25=quartiles(data['PM2.5'],'PM2.5')
    PM10=quartiles(data['PM10'],'PM10')
    print(' ')

    # Plotting data before and after removing outliars.
    data_w_outliars = [data['NO2']['Value'].values,
        data['PM2.5']['Value'].values, data['PM10']['Value'].values]

    data_wo_outliars=[NO2['Value'].values,
                      PM25['Value'].values, PM10['Value'].values]

    colors=['orange','teal','darkgrey']

    if plot:

        plt.figure(figsize=(8, 4))
        sns.boxplot(data=data_w_outliars,palette=colors)
        plt.xticks([0, 1, 2],['NO₂',  'PM₂.₅', 'PM₁₀'])
        plt.ylabel("Measure [µg/m^3]")
        plt.title("Deviation of the pollutant measurements")
        plt.show()

        plt.figure(figsize=(8, 4))
        sns.boxplot(data=data_wo_outliars,palette=colors)
        plt.xticks([0, 1, 2], ['NO₂',  'PM₂.₅', 'PM₁₀'])
        plt.ylabel("Pollutant measure [µg/m^3]")
        plt.title("Deviation of the pollutant measurements with outliars removed")
        plt.show()

    return NO2,  PM25, PM10


def plot_histogram(df,color,title,bins):

    plt.figure(figsize=(8, 4))
    sns.histplot(data=df, x="Value", bins=bins,kde=True,color=color,edgecolor=None,alpha=0.5,shrink=0.8)
    plt.ylabel("Count")
    plt.xlabel("Pollutant measure [µg/m^3] ")
    plt.title(f'Histogram of {title} pollutant measurements')
    plt.grid(axis='y')
    plt.show()


def mean_std_meadin_corr(df,name):

    """
    Statistical summary metrics used in the analysis.

    - median (float): The middle value of an ordered data set.
    - std_dev (float): Standard deviation; ~68% of data lies within ±1σ of the mean.
    - mean (float): The arithmetic average.
    - correlation (float): Pearson correlation coefficient, indicating linear trend.
      Values ≥|0.6| are often considered strong.
    """

    median_emission = df['Value'].median() # Meadian.
    std_emission = df['Value'].std() # Standard deviation.
    mean_emission = df['Value'].mean() # Mean.
    correlation = df['Time Interval'].corr(df['Value'])  # Correlation between year and pollutant.

    print(' ')
    print(f"    - Mean value of {name}:                   {mean_emission:.3f}")
    print(f"    - Median of {name}:                       {median_emission:.3f}")
    print(f"    - Standard deviation of {name}:           {std_emission:.3f}")
    print(f"    - Correlation of year and {name} measure: {correlation:.3f}")
    print(' ')
    if abs(correlation) < 0.6:
        print(f'Seems like the correlation ({correlation:.3f}) of year and {name} is very low.')
        print(' ')

    # Storing if needed later.
    dict_stats={'Meadian':median_emission,
                'Standard deviation':std_emission,
                'Mean':mean_emission,
                'Correlation':correlation}

    return dict_stats


def reggresion_analysis(df,name,color,plot=True):

    """
        Perform STL decomposition on monthly pollutant measurements and fit a
        linear trend across years.

        This function takes a time‐indexed DataFrame of raw pollutant readings,
        resamples it to monthly medians, fills gaps by time‐based interpolation,
        then applies a Seasonal-Trend decomposition (STL). It computes a yearly
        linear regression on the STL trend component and optionally displays a
        two‐panel plot of the decomposition and fitted line.
    """

    # Formating data.
    df["Time Interval"] = pd.to_datetime(df["Time Interval"]) # Converts to datetime of type: 2020-01-01 00:00:00
    df = df.set_index("Time Interval").sort_index() # Putting datetime as index.
    monthly = df["Value"].resample("MS").median().interpolate("time") # Finding monthly mean for the different years, except nans.

    # Finding STL trends.
    stl = STL(monthly, period=12, seasonal=19, robust=True)
    data = stl.fit()
    trend= data.trend           # Year based trends.
    seasonal= data.seasonal     # Season based trends for all years.
    resid= data.resid           # Outliars from the trend stats.

    # Finding linear based reggression trend between years.
    x_years = trend.index.year + (trend.index.dayofyear / 365.25)
    a, b = np.polyfit(x_years, trend.values, 1)

    if plot:
        print(f"Linear trend is a change of {a:.4f} [µg/m^3] {name} per year")

    y_fit = a * x_years + b

    # Sorting by years.
    order = np.argsort(x_years)
    x_sorted = x_years[order]
    y_fit_sorted = y_fit[order]

    if plot:
        fig, (ax1, ax2) = plt.subplots(2, 1)
        fig.suptitle(f'Monthly {name} trend, and linear reggression between 2016-2024')
        ax1.plot(monthly, label="Observation", color=color, alpha=.5)
        ax1.plot(trend, label="Trend (STL)",linestyle='--', color='deeppink')
        ax1.plot(seasonal, label="Seasonal (STL)")
        ax1.legend()

        ax2.plot(x_years, trend,linestyle='--',color='deeppink', label='Trend-data')
        ax2.plot(x_sorted, y_fit_sorted, color=color, linewidth=2,label=f'Fit: y = {a:.3f}·x')
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Pollutant measure µg/m^3')
        ax2.legend()
        plt.show()

    return x_sorted, y_fit_sorted,seasonal


def plot_AQI_levels(data,aqi_breakpoints,aqi_colors,file_path):
    # Plotting the AQI for each pollutant from 2016-2025
    fig = plt.figure(figsize=(14, 12))
    gs  = gridspec.GridSpec(
        nrows=3,
        ncols=2,
        width_ratios=[7, 2],
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

        if ax is axes[-1]:
            ax.set_xlabel('Years', fontsize=12) # only bottom plot gets 'Year' axes label
        else:
            ax.set_xticklabels([])
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_ylim(0,500)

    patches = [Patch(facecolor=color, label=label) for label, color, *_ in aqi_colors] # Making legend showing the meaning of the AQI colors/intervals
    legend_ax.legend(
        patches, [p.get_label() for p in patches], title="AQI Categories", loc='center')

    fig.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.show()


def calculate_aqi(value, breakpoints):

    """
    Function to calculate AQI value for the different pollutants.
    """

    for low_conc, high_conc, low_aqi, high_aqi in breakpoints:  #cheks each breakpoint tuple
        if low_conc <= value <= high_conc:
            aqi = ((value - low_conc) / (high_conc - low_conc)) * (high_aqi - low_aqi) + low_aqi
            return aqi

def plot_pollutantlevels(data,aqi_breakpoints):
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
