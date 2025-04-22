
import pandas as pd
import os
import unittest

"""DENNE KODEN ER IKKE HELT FERDIG! Skal bytte ut dataen fra csv_url en med dataen i pickle filen i data mappen.
Koden her skal tilpasses deretter og scriptet skal flyttes til data mappen. Testene skal flyttes til en egen testmappe som ikke
er opprettet enda."""


csv_url = "https://sdi.eea.europa.eu/webdav/datastore/public/eea_t_national-emissions-reported_p_2024_v01_r00/CSV/UNFCCC_v27.csv"
Data = pd.read_csv(csv_url) #fra test_filbehandling

# In[----------------------------2 DATAHANDLING -----------------------------]

                ## FILTERING DATA WITH EMISSIONS ABOVE 500 Mt CO2 ##
print('    ')
print('Data filtering starting.........')
print(' ')
print('Filtering dataset with emissions above 500 CO2 eq')
if "emissions" in Data.columns:
    filtered_data = Data[[x > 500 for x in Data["emissions"]]]
    print(f"The filtered dataset ,filtered_data, has {filtered_data.shape[0]} rows.")
else:
    print("The cloumn 'emissions' does not exist.")


              ## CHANGING ALL COUNTRY NAMES TO HAVE UPPERCASE LETTERS ##
if "Country" in Data.columns:
    Data["Country"] = [val.upper() for val in Data["Country"]]
    print(' ')
    print("Converted 'Country' column to uppercase.")
else:
    print("Column 'Country' not found in dataset.")


            ## MARKING COUNTRIES WITH EMISSIONS ABOVE 1000 Mt CO2 ##
print(' ')
print('Marking countries with high emissions (>1000 CO2 eq)')
if "emissions" in Data.columns:
    Data["High_emissions"] = ["Yes" if x > 1000 else "No" for x in Data["emissions"]]
    print("Added the column 'High_emissions' column based on emission values.")
else:
    print("Column 'emissions' not found in dataset.")
print(Data)

            ## FINDS THE TOTAL EMISSION FOR EACH COUNTRY USING PANDAS SQL ##
print('')
print('Total CO2 emission [Mt] for all countries are:')
print('-----------------------------------------')
pysqldf = lambda q: sqldf(q, {"Data": Data})
query = """
SELECT Country, SUM(emissions)*0.000001 AS total_emission
FROM Data
GROUP BY Country
"""
tot_emissions = pysqldf(query)
print(tot_emissions)


# In[---------Testing if the data comes as expected-------------]
class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        """Set up a sample DataFrame to test with."""
        self.sample_data = pd.DataFrame({
            "Country": ["Norway", "Sweden", "Denmark"],
            "emissions": [1200, 800, 1500],
            "GDP": [50000, 55000, None]  # Contains NaN
        })

    def test_uppercase_country(self):
        """Test if country names are converted to uppercase."""
        self.sample_data["Country"] = [val.upper() for val in self.sample_data["Country"]]
        expected = ["NORWAY", "SWEDEN", "DENMARK"]
        self.assertEqual(list(self.sample_data["Country"]), expected)

    def test_categorize_emission(self):
        """Test if emissions are correctly categorized as 'Yes' or 'No'."""
        self.sample_data["High_Emission"] = ["Yes" if x > 1000 else "No" for x in self.sample_data["emissions"]]
        expected = ["Yes", "No", "Yes"]
        self.assertEqual(list(self.sample_data["High_Emission"]), expected)

if __name__ == "__main__":
    unittest.main()
