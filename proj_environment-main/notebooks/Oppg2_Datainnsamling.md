# Oppgave 2 – Datainnsamling

## 1. Datasources & pålitelighet

I dette prosjektet blir det samlet inn miljødata fra ulike åpne kilder:
- **Luftforurensningsdata** PM10, PM2.5, NO2 fra EEA sitt Parquet-API.  
- **CO2-utslippsdata** fra UNFCCC-rapporten (CSV).  
- **Månedlig gjennomsnittstemperatur** for Oslo i perioden 2016–2024 fra Norsk Klimaservicesenter (Temp_oslo_2016_2024.csv).

Alle dataene skal være åpne og tilgjenglige, og kvaliteten av de blir undersøkt for å vurdere hvilke kilder som skal brukes videre i prosjektet.

| Kilde | Beskrivelse                             | Autoritet                                                                              |
|---|-----------------------------------------|----------------------------------------------------------------------------------------|
| EEA Parquet-API | Timeverdier for PM10, PM2.5, NO2 i Oslo | EU-byrå; verifiserte (E2a) + uverifiserte (E1a); gratis og tilgjengelig via HTTP-POST. |
| UNFCCC_v27.csv | Nasjonale CO2-utslipp (reporterte data) | UNFCCC offisiell rapport; stor CSV; kan inneholde NULL-verdier som må håndteres.       |
| Temp_oslo_2016_2024.csv | Månedlig middeltemperatur               | Norsk Klimaservicesenter; semikolon-separert csv fil, enkelte manglende verdier.       |


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
   - Funksjonen plotter til slutt de kolonnene i datasettet som er av typen numeriske/float verdier. Et vanlig plott av rådataen blir gjort, samt et histogram for å se datafordelingen.   

### 2.2 `Datainnsamling.py`  
Koordinerer arbeidsflyten:  
1. Kaller `eu_air_pollutants_data` og `write_to_excel_by_pollutant` for PM10, PM2.5 og NO2 og inspiserer filene med `data_reader`.  
2. Leser inn og inspiserer CO2-CSV via `download_temp_file` + `data_reader`.  
3. Leser inn og inspiserer temperatur-CSV med `data_reader`.

## 4. Teknisk implementasjon
- **HTTP & filhåndtering:** `requests` + `tempfile` + `zipfile` for Parquet-nedlasting.  
- **Dataframes & inspeksjon:** `pandas` – konvertering til `float32`, NaN-sjekk, mixed-type-håndtering via `.pipe()`, list comprehensions og `defaultdict`.  
- **Fil- og katalogadministrasjon:** `pathlib` for plattformuavhengige stier slik at funksjoner fra scr mappen kan hentes inn, og filer lagres til data mappen.

## 5. Tolking av resultater
Etter at data_reader() ble kjørt for alle datasettene fikk gruppen oversikt over hvilken type data vi har med å gjøre, og hvilke kolonner i datasettet som er relevante for videre analyse.

### EEA Pollutant data
Dataen ble lastet ned ved API request, og skrevet videre til excelfiler. Fra brukermanualen til EEA såg gruppen at en kan både laste ned data fra alle stasjonene som er registrert i Oslo, eller velge ut en spesifikk stasjon. Da noen stasjoner hadde hull i datasettene, og det ville vært tidkrevende å manuelt finne hvilke stasjoner som faktisk hadde data fra 2016-2024 for de tre ulike luftkvalitetsmålingene, bestemte gruppen seg for å heller laste ned dataen til alle stasjonene, og forkaste de datasettene som manglet for mye data.
Gruppen ønsker å jobbe med å manipulere manglende data, men for store mangler (hele år) vil være uhensiktsmessig da de historiske dataene skal brukes for å undersøke trender og predikere framtidsscenario.
Excel filene for de tre luftkvalitetsmålingene NO2, MP10 og PM2.5, innholder et ark per stasjon i Oslo, og første arket for alle tre blir lest i data_reader() for å få en rask oversikt over datainnholdet. I oppgave 3 (Databehandling.py) blir hvert av arkene undersøkt nøyere.
Fra første øyekast på informasjonen om 'Column' og 'Non-Null Count' ser det ut til at ingen av datasettetene ikke har manglende verdier. Derimot når man ser på utskriften fra .describe() at blandt annet gjennomsnittet ligger langt over medianen og kvartilene, noe som tyder på store ekstrem verdier.
Det er også veldig stor differanse mellom min og max verdi. Ekstemverdier i datasettet kan bekreftes fra rådata plottene og histogrammene som kommer ut, samt negative målinger. Gruppen konkluderer med at dette datasettet er relevant for oppgaven, og kan gi flere muligheter for å lære om datamanipulering. Gruppen går derfor videre med å bruke EEA sine data på luftkvalitet i Oslo.
Relevante kolonner fra datasettet er kolonnene 'Start' som innholder tid data, og kolonnen 'Value' som innholder selve luftkvalitetsmålingen.

### UNFCC utslippsdata
Slik som for luftkvalitet dataen, ser en også på resultatene fra data_reader() at utslippsdataen fra UNFCC innholder ekstremverdier.
Utskriften viser også at datasettet har flere nan verdier for 'emission' kolonnen. Likevel velger gruppen å ikke gå videre med dette datasettet da det er såpass stor (opp i 400 000 elementer) at det vil ta alt for lang tid å laste ned hele datasettet. For denne oppgaven er datasettet her bare lastet ned som en midlertidig fil for å kunne lese den.
Gruppen går derfor ikke videre med dette datasettet.

### Temperaturdata Norsk Klimaservicesenter
Da gruppen valgte å gå videre med luftkvalitetsdata, ble det drøftet om muligheten for å se på sammenhengen mellom temperatur og luftkvalitet.
Datasettet ser ikke ut til å ha noen manglende verdier eller ekstremverdier, men da EEA dataen skal bli brukt for å jobbe med datamanipulering, konkluderer gruppen med å likevel gå videre med datasettet for å kunne analysere sesongbaserte korrelasjner mellom temperatur og luftkvalitet.
Relevante kolonner fra dette datasettet er 'Tid(norsk normaltid)' og 'Middeltemperatur(mnd)'

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


