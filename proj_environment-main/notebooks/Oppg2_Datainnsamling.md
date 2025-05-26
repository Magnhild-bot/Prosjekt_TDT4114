# Oppgave 2 – Datainnsamling

## 1. Datasources & pålitelighet

I dette prosjektet blir det samlet inn miljødata fra ulike åpne kilder:
- **Luftforurensningsdata** PM10, PM2.5, NO2 fra EEA sitt Parquet-API.  
- **CO₂-utslippsdata** fra UNFCCC-rapporten (CSV).  
- **Månedlig gjennomsnittstemperatur** for Oslo (2016–2024) fra Norsk Klimaservicesenter (Temp_oslo_2016_2024.csv).

Alle dataene skal være åpne og tilgjenglige, og kvaliteten av de blir undersøkt for å vurdere hvilke kilder som skal brukes videre i prosjektet.

| Kilde | Beskrivelse | Autoritet                                                                              |
|---|---|----------------------------------------------------------------------------------------|
| EEA Parquet-API | Timeverdier for PM10, PM2.5, NO₂ i Oslo | EU-byrå; verifiserte (E2a) + uverifiserte (E1a); gratis og tilgjengelig via HTTP-POST. |
| UNFCCC_v27.csv | Nasjonale CO₂-utslipp (reporterte data) | UNFCCC offisiell rapport; stor CSV; kan inneholde NULL-verdier som må håndteres.       |
| Temp_oslo_2016_2024.csv | Månedlig middeltemperatur | Norsk Klimaservicesenter; semikolon-separert csv fil, enkelte manglende verdier.       |


## 2. Kodefunksjoner

For nedlasting og lesing av data kjøres scriptet `Datainnsamling.py` som er et overordnet "hovedscript" for oppgave 2,
og bruker funksjoner som er samlet i scr mappen i scriptet `Functions_FetchData.py`.

### 2.1 `Functions_FetchData.py`  
Implementerer kjernelogikk for datainnsamling og inspeksjon:  
1. **`download_temp_file(url)`**  
   - Laster ned hvilken som helst fil over HTTP som en midlertidig fil.  
   - Håndterer store filer med streaming-chunks.  
2. **`eu_air_pollutants_data(startdate, enddate, pollutants)`**  
   - Henter timeverdier for utvalgte forurensningskomponenter fra EEA API.  
   - Kombinerer verifiserte (E2a) og uverifiserte (E1a) perioder til én DataFrame per stasjon/pollutant.
   - Request funksjonen er skrevet med hjelp av dokumentasjonen til EEA som er lagt ved i mappen **`proj_environment-main\docs\data_documentation\EEA_AQI_data_download.pdf`** 
3. **`write_to_excel_by_pollutant(AirData, out_dir="data")`**  
   - Skriver hver forurensningstype til egne Excel-filer med ett ark per stasjon.  
4. **`data_reader(filename, nanlimit, ...)`**  
   - Leser CSV, Excel, JSON eller HTML.  
   - Skriver ut informasjon om datasettet ved å bruke både egenskrevet kode og de innebygde funksjonene fra pandas miljøet .info(), .describe() og .head().
   - Ved funksjonskall kan man definere en nan limit i prosent, for å sørge for advarsel dersom datasettet har en høyere andel nan verdier enn ønsket.
   
### 2.2 `Datainnsamling.py`  
Koordinerer arbeidsflyten:  
1. Kaller `eu_air_pollutants_data` og `write_to_excel_by_pollutant` for PM10, PM2.5 og NO2 og inspiserer filene med `data_reader`.  
2. Leser inn og inspiserer CO2-CSV via `download_temp_file` + `data_reader`.  
3. Leser inn og inspiserer temperatur-CSV med `data_reader`.

## 4. Teknisk implementasjon
- **HTTP & filhåndtering:** `requests` + `tempfile` + `zipfile` for Parquet-nedlasting.  
- **Dataframes & inspeksjon:** `pandas` – konvertering til `float32`, NaN-sjekk, mixed-type-håndtering via `.pipe()`, list comprehensions og `defaultdict`.  
- **Fil- og katalogadministrasjon:** `pathlib` for plattformuavhengige stier.

## 5. Forbedringsmuligheter
I denne oppgaven ble det startet med å skrive parquet filene fra API requesten for luftkvalitet dataen til excel filer. 
Disse excelfilene ble brukt til å løse videre oppgaver i prosjektet av alle gruppemedlemmene. Etterhvert innsåg gruppen at funksjonen `write_to_excel_by_pollutant(AirData, out_dir="data")` som skriver
dataen til excel er den som gjør at `Datainnsamling.py` tar veldig lang tid å kjøre. Da dette ble oppdaget sent i prosjektet etter at store deler av oppgavene var løst og utformet, 
konkluderte gruppen med at å skrive dataen til feks csv fil, og gjøre om de delene av koden som leser disse filene må bli satt av til fremtidig arbeid.
SQL miljøet kan for framtidig arbeid bli testet ut samt andre metoder for å heller skrive dataen til en csv fil med feks: cython, numpy tofile eller evt Oneliner.

## 6. Kjøreveiledning
```bash

# Kjør datainnsamling
python Datainnsamling.py


