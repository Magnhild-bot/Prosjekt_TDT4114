# Berre ei fil som Magnhild vil testa ulike data i
import pandas as pd
import matplotlib.pyplot as plt
from retry_requests import retry
import datetime
import os
import requests

csv_url = "https://sdi.eea.europa.eu/webdav/datastore/public/eea_t_national-emissions-reported_p_2024_v01_r00/CSV/UNFCCC_v27.csv"

data = pd.read_csv(csv_url)

# 
df_emissions = data[['Country', 'Year', 'emissions']].copy()

# Sjekker / gjer alle verdiar numeriske
df_emissions['emissions'] = pd.to_numeric(df_emissions['emissions'], errors='coerce')

# Drop rows with NaN emissions
df_emissions = df_emissions.dropna(subset=['emissions'])

# Create pivot table (Years vs Countries)
df_pivot = df_emissions.pivot_table(index='Year', columns='Country', values='emissions', aggfunc='sum')

# Plotting emissions per country
plt.figure(figsize=(12, 8))
df_pivot.plot(ax=plt.gca())

# Customize plot
plt.title('Greenhouse Gas Emissions Over Time by Country')
plt.xlabel('Year')
plt.ylabel('Emissions (Gg CO₂ equivalent)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Display plot
plt.show()

##Få oversikt over kor mange rader det er for kvart land

# Tar ut kolonne med land
country_column = data.iloc[:, 1]  # 0-based indexing (second column)

# Returnerer objekt som inneholder 
country_counts = country_column.value_counts()

# Print resultat
for country, count in country_counts.items():
    print(f"{country}: {count} rows")