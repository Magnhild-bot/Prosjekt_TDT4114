# Berre ei fil som Magnhild vil testa ulike data i

#  Total GHG emissions and removals in the EU
# URL: https://www.eea.europa.eu/en/datahub/datahubitem-view/3b7fe76c-524a-439a-bfd2-a6e4046302a2
# National emissions reported to the UNFCCC and to the EU under the Governance Regulation, April 2024
import pandas as pd
import matplotlib.pyplot as plt
from retry_requests import retry
import datetime
import os
import requests

csv_url = "https://sdi.eea.europa.eu/webdav/datastore/public/eea_t_national-emissions-reported_p_2024_v01_r00/CSV/UNFCCC_v27.csv"

data = pd.read_csv(csv_url)

#Få oversikt over kor mange rader det er for kvart land

# Tar ut kolonne med land
country_column = data['Country']
# Returnerer objekt som inneholder unik verdi
country_counts = country_column.value_counts()

# Itererer gjennom kvart land og lagar dict med antalet rader
for country, count in country_counts.items():
    print(f"{country}: {count} rows")

#####
# Filter rows where the emissions value is missing (NaN)
#missing_emissions = df[df['emissions'].isna()]

# Total number of rows missing emissions
#total_missing = missing_emissions.shape[0]

# Define the columns to check for the word "removal"
#columns_to_check = ['Format_name', 'Sector_code', 'Sector_name']

# Create a boolean mask for rows where any of these columns contain "removal" (case insensitive)
#mask_removal = missing_emissions[columns_to_check].apply(
#    lambda row: row.str.lower().str.contains('removal', na=False)
#).any(axis=1)

# Count how many of the rows missing emissions mention "removal"
#removal_count = mask_removal.sum()

#print("Number of rows without emissions:", total_missing)
#print("Number of rows without emissions that mention 'removal':", removal_count)



