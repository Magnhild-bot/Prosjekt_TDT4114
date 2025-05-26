import sys
import pickle
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

project_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_dir / 'src'))
sys.path.insert(0, str(project_dir / 'notebooks'))
data_dir = project_dir / "data"

# Importing the trend data of the air pollutants from Dataanalyse.py.
from Dataanalyse import NO2_trend_year_raw, NO2_trend_raw,PM25_trend_year_raw, \
                        PM25_trend_raw, PM10_trend_year_raw, PM10_trend_raw

def predict_future(x_sorted, y_fit_sorted, years=10, label='NO2', color='orange'):
    # Reshaping for sklearn.
    x_fit_sorted = np.array(x_sorted).reshape(-1, 1)
    y_fit_sorted = np.array(y_fit_sorted)

    # Fitting with the linear regression model from scikit.
    model = LinearRegression()
    model.fit(x_fit_sorted, y_fit_sorted)

    # Predicting future years.
    last_year = x_sorted[-1]
    future_x_years = np.linspace(last_year, last_year + years, num=24)
    future_years_reshape = future_x_years.reshape(-1, 1)
    future_y = model.predict(future_years_reshape)

    # Makes sure predicted values are not below 0
    future_y = np.clip(future_y, a_min=0, a_max=None)

    plt.figure(figsize=(10, 4))
    plt.plot(x_sorted, y_fit_sorted, label='Historical trend', color=color)
    plt.plot(future_x_years, future_y, '--', label=f'{label} Prediction ({years} years)', color='red')
    plt.xlabel("Year")
    plt.ylabel("Pollutant level [µg/m³]")
    plt.title(f"{label}-Trend with {years} year prediction")
    plt.legend()
    plt.grid(True)
    plt.show()

    return future_x_years, future_y

# The pollutants we want to find the future predictions: NO2, PM25, PM10.
# Can choose the years ahead that is wanted, we chose a 10-year prediction.
future_x_NO2, future_y_NO2 = predict_future(
    NO2_trend_year_raw, NO2_trend_raw, years=10, label='NO2', color='orange'
    )
future_x_PM25, future_y_PM25 = predict_future(
    PM25_trend_year_raw, PM25_trend_raw, years=10, label='PM2', color='darkgrey'
    )
future_x_PM10, future_y_PM10 = predict_future(
    PM10_trend_year_raw, PM10_trend_raw, years=10, label='PM10', color='plum'
    )

future_predictions = {
    'NO2': (future_x_NO2, future_y_NO2),
    'PM2.5': (future_x_PM25, future_y_PM25),
    'PM10': (future_x_PM10, future_y_PM10)
}

with open(data_dir / "future_pollutant_predictions.pkl", 'wb') as f:
    pickle.dump(future_predictions, f)