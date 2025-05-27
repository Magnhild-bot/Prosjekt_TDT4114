# src– Funksjoner for Datainnhenting og Dataanalyser

Denne oppgaven er løst gjennom to sentrale scripts: `Functions_FetchData.py` og `Functions_Dataanalysis.py`. 
Scriptet `Functions_FetchData.py` inneholder funksjoner som laster ned luftkvalitetsdata fra EEA, mens `Functions_Dataanalysis.py` inneholder funksjoner for aggregering og analyse av data over tid.

Alle funksjoner er lagt i mappen src/ for å gjøre det enkelt å gjenbruke funksjonene og strukturere koden. 


## `Functions_FetchData.py`

Under er de ulike definerte funksjonene i scriptet forklart nøyere

### 1. eu_air_pollutants_data(startdate, enddate, pollutants)
Denne funksjonen henter ned timedata for luftkvalitetsmålinger (PM10, NO2, etc.) fra European Environment Agency (EEA) via deres API. Henter både verifiserte og ikke-verifiserte data.

* Data hentes spesifikt for Oslo.
* Funksjonen returnerer en dictionary med DataFrames for hver stasjon og hver komponent.
* Bruker start- og sluttdato i "YYYY-MM-DDTHH:MM:SSZ"-format og en liste med ønskede komponentkoder.

### 2. write_to_excel_by_pollutant(AirData, out_dir="data")
Denne funksjonen tar dictionaryen med DataFrames og skriver dem til separate Excel-filer per luftkomponent (f.eks. PM10.xlsx, NO2.xlsx).
Hvert regneark vil representere en målestasjon.

* Mappen "data" blir laget automatisk dersom den ikke eksisterer.
* Excel-filene navngis etter komponent.


### 3. download_temp_file(url)
Funksjonen brukes til å laste ned en fil fra en nettadresse og lagre den midlertidig på lokal maskin. Filen returneres som en sti og kan brukes videre i prosjektet.

* Brukes primært for datasett med stor filstørrelse.
* Bruker chunked streaming for robusthet.


### 4.data_reader(filename, nanlimit, skiprows=None, usecols=None, nrows=None, sep=None)
Denne funksjonen brukes til å lese inn datasett (CSV, Excel, JSON, HTML) og samtidig kontrollere datakvalitet.

* Konverterer `float64 ` til  `float32` for å spare på minnet.

* Gir oss detaljer om:
* Prosentandel NaN-verdier, og den gir advarsel hvis det overstiger nanlimit)
* Negative verdier i float-kolonner
* Mixed-type kolonner
* Gir visuell oversikt over de første 10 radene og statistikk over numeriske verdier


## Functions_Dataanalysis.py

