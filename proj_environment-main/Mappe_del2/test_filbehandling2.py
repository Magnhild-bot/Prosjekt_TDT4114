#Plotting av EU utslepp forts. frå mappe del 1

csv_url = "https://sdi.eea.europa.eu/webdav/datastore/public/eea_t_national-emissions-reported_p_2024_v01_r00/CSV/UNFCCC_v27.csv"

data = pd.read_csv(csv_url)

import pandas as pd
import matplotlib.pyplot as plt
from retry_requests import retry
import datetime
import os
import requests



# Gjer om alle verdiar i year kolonna til numerisk verdi
# 'coerce' gjer at alle ikkje-numeriske verdiar blir NaN
data['Year'] = pd.to_numeric(data['Year'], errors='coerce')
# Gjer om alle verdiar i emissions kolonna til numerisk verdi
data['emissions'] = pd.to_numeric(data['emissions'], errors='coerce')
# Pandas dropna() dropper dropper rader / kolonner uten verdiar
data.dropna(subset=['Year', 'emissions'], inplace=True)

# Summerer utslepp for kvart land for kvart år
emisson_per_country = data.groupby(['Year', 'Country'])['emissions'].sum().reset_index()

# snur emission_per_country slik at landa blir kolonner
emission_per_country_pivot = emisson_per_country.pivot(index='Year', columns='Country', values='emissions')

# Gjer om indexar til 
emission_per_country_pivot.index = emisson_per_country.index.astype(int)

# Sorterer etter index
emission_per_country_pivot.sort_index(inplace=True)

# Plot data clearly
plt.figure(figsize=(14, 8))
emission_per_country_pivot.plot(ax=plt.gca())

# Enhancements for clarity
plt.xlabel('Year', fontsize=12)
plt.ylabel('Emissions (Gg CO_2 equivalent)', fontsize=12)
plt.title('Greenhouse Gas Emissions Over Time by Country', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Country', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()

plt.show()
