import sys
import pickle
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

project_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_dir / 'src'))
sys.path.insert(0, str(project_dir / 'notebooks'))

from Functions_Dataanalysis import reggresion_analysis, cap_outliers, plot_histogram, mean_std_meadin_corr
from Dataanalyse import data, data_dir


# To use the values found and analysed in "Dataanalyse"
def raw_analysis():
    NO2_raw, PM25_raw, PM10_raw = cap_outliers(data, 'Value', plot=False)

    NO2_trend_year_raw, NO2_trend_raw, NO2_seasonal_raw = reggresion_analysis(NO2_raw, 'NO2', 'orange', plot=False)
    PM25_trend_year_raw, PM25_trend_raw, PM25_seasonal_raw = reggresion_analysis(PM25_raw, 'PM25', 'darkgrey', plot=False)
    PM10_trend_year_raw, PM10_trend_raw, PM10_seasonal_raw = reggresion_analysis(PM10_raw, 'PM10', 'plum', plot=False)

    return {
        'NO2': (NO2_raw, NO2_trend_year_raw, NO2_trend_raw, NO2_seasonal_raw),
        'PM25': (PM25_raw, PM25_trend_year_raw, PM25_trend_raw, PM25_seasonal_raw),
        'PM10': (PM10_raw, PM10_trend_year_raw, PM10_trend_raw, PM10_seasonal_raw)
    }


results = raw_analysis()

NO2_raw, NO2_trend_year_raw, NO2_trend_raw, _ = results['NO2']
PM25_raw, PM25_trend_year_raw, PM25_trend_raw, _ = results['PM25']
PM10_raw, PM10_trend_year_raw, PM10_trend_raw, _ = results['PM10']


def predict_future(x_sorted, y_fit_sorted, years_ahead=10, label='NO2', color='orange'):
    # Reshaping for sklearn.
    x_fit_sorted = np.array(x_sorted).reshape(-1, 1)
    y_fit_sorted = np.array(y_fit_sorted)

    # Fitting with the linear regression model.
    model = LinearRegression()
    model.fit(x_fit_sorted, y_fit_sorted)

    # Predicting future years.
    last_year = x_sorted[-1]
    future_x_years = np.linspace(last_year, last_year + years_ahead, num=24)
    future_years_reshape = future_x_years.reshape(-1, 1)
    future_y = model.predict(future_years_reshape)

    plt.figure(figsize=(10, 4))
    plt.plot(x_sorted, y_fit_sorted, label='Historical Trend', color=color)
    plt.plot(future_x_years, future_y, '--', label=f'{label} Prediction ({years_ahead} years)', color='red')
    plt.xlabel("Year")
    plt.ylabel("Pollutant level [µg/m³]")
    plt.title(f"{label} Trend with {years_ahead}-Year Prediction")
    plt.legend()
    plt.grid(True)
    plt.show()

    return future_x_years, future_y

# The pollutants we want to find the future predictions: NO2, PM25, PM10.
# Can choose the years ahead that is wanted, we chose a 10-year prediction.
future_x_NO2, future_y_NO2 = predict_future(
    NO2_trend_year_raw, NO2_trend_raw, years_ahead=10, label='NO₂', color='orange'
    )
future_x_PM25, future_y_PM25 = predict_future(
    PM25_trend_year_raw, PM25_trend_raw, years_ahead=10, label='PM₂.₅', color='darkgrey'
    )
future_x_PM10, future_y_PM10 = predict_future(
    PM10_trend_year_raw, PM10_trend_raw, years_ahead=10, label='PM₁₀', color='plum'
    )

future_predictions = {
    'NO2': (future_x_NO2, future_y_NO2),
    'PM2.5': (future_x_PM25, future_y_PM25),
    'PM10': (future_x_PM10, future_y_PM10)
}

with open(data_dir / "future_pollutant_predictions.pkl", 'wb') as f:
    pickle.dump(future_predictions, f)