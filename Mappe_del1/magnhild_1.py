
import openmeteo_requests

import requests_cache
import pandas as pd
import matplotlib.pyplot as plt
from retry_requests import retry
import datetime

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": 62.520032,
	"longitude": 6.15,
	"start_date": "2010-01-01",
	"end_date": "2019-12-31",
	"hourly": ["rain", "snowfall"]
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_rain = hourly.Variables(0).ValuesAsNumpy()
hourly_snowfall = hourly.Variables(1).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["rain"] = hourly_rain
hourly_data["snowfall"] = hourly_snowfall

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)



# Assume hourly_dataframe is already defined from your code.
# Convert 'date' to datetime (if not already) and set as index.
hourly_dataframe['date'] = pd.to_datetime(hourly_dataframe['date'])
hourly_dataframe.set_index('date', inplace=True)

# Aggregate the data by day (summing hourly values).
daily_dataframe = hourly_dataframe.resample('D').sum()

# Create a stacked bar chart
plt.figure(figsize=(12, 6))
plt.bar(daily_dataframe.index, daily_dataframe['rain'], label='Rain')
plt.bar(daily_dataframe.index, daily_dataframe['snowfall'], 
        bottom=daily_dataframe['rain'], label='Snowfall')

plt.xlabel('Date')
plt.ylabel('Precipitation (mm)')
plt.title('Daily Rain and Snowfall')
plt.legend()
plt.tight_layout()
plt.show()

