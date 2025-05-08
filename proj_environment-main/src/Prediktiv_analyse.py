import os
import pickle
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

##Ikke pushe før spurt de andre
# -- Last inn datasettet fra pickle-filen --
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_dir = os.path.join(project_dir, 'data')
pkl_file = os.path.join(data_dir, "mean_air_pollutants.pkl")

with open(pkl_file, "rb") as f:
    mean_results = pickle.load(f)

# 1. Bruke renset NO2-data
no2_df = mean_results['NO2'].copy()
no2_df['Time Interval'] = pd.to_datetime(no2_df['Time Interval'])

# 2. Lage funksjoner basert på tid
no2_df['Hour'] = no2_df['Time Interval'].dt.hour
no2_df['DayOfWeek'] = no2_df['Time Interval'].dt.dayofweek
no2_df['Month'] = no2_df['Time Interval'].dt.month

# 3. Trene/teste-splitte
X = no2_df[['Hour', 'DayOfWeek', 'Month']]
y = no2_df['Value']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# 4. Trene modeller
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Evaluere modellen
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Modellens MSE: {mse:.2f}")

# 6. Lage fremtidig tidsstempel og forutsi
import pandas as pd
future_date = pd.to_datetime("2025-06-01 12:00:00")
future_features = pd.DataFrame({
    'Hour': [future_date.hour],
    'DayOfWeek': [future_date.dayofweek],
    'Month': [future_date.month]
})
future_prediction = model.predict(future_features)
print(f"Forventet NO2-nivå 1. juni 2025 kl. 12:00: {future_prediction[0]:.2f} µg/m³")