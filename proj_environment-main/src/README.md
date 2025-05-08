###########Til "Test_files"###########
This script is used to inspect and preview environmental emissions data from various sources. It leverages the 
`data_reader` and `download_temp_file` functions (imported from Functions_FetchData) to load, display, 
explore and the amount of missing values in the contents of three different datasets.

1. **Air Pollutant Data (PM10.xlsx)**: 
   - A local Excel file containing particulate matter (PM10) pollution data.
   - Loaded from the project’s `/data/` directory.
   - {'Value': 3559} unknown values

2. **CO2 Emissions Data (UNFCCC_v27.csv)**:
   - A CSV file downloaded from the European Environment Agency's public data repository.
   - Temporarily downloaded and passed to `data_reader` for preview.
   - {'emissions': 16031} unknown values
3. **Climate Gas Equivalents (JSON format)**:
   - Structured JSON dataset simulating emissions data by source, component, and year.
   - Written to a local file (`ekvivalenter_data.json`) and then read using `data_reader`.
   - {'dataset': 0} unknown values.
   - 
This script helps verify that the files contain expected structures and values by displaying the top few rows
for quick visual inspection (with the number of rows defined per file). It is primarily used for debugging, data
exploration, or validation purposes in the context of environmental data analysis projects.

Uses SQLite-style SQL to query the df DataFrame.

We choose to continue with the first one since air quality is interesting.

Dependencies:
- pandas
- os
- json
- Functions_FetchData module with `data_reader` and `download_temp_file` functions

(Author: [Your Name]
Last Modified: [Date]
""")


##############Til Function_FetchData########
