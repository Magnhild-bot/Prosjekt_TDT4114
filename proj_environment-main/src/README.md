# src-Mappen – Funksjoner for Datainnhenting og Dataanalyser

Denne mappen inneholder to script: `Functions_FetchData.py` og `Functions_Dataanalysis.py`. 
Scriptet `Functions_FetchData.py` inneholder funksjoner som behandler og sorterer data, og `Functions_Dataanalysis.py` inneholder klasser og funksjoner for behandling og videre analyse av data.

Alle funksjoner er lagt i mappen `src` for å gjøre det enkelt å gjenbruke funksjonene og klassene, og å holde en oversiktlig struktur ved bruk av funksjonene og klassene i oppgavene. 


## Functions_FetchData.py
Består av funksjonene `download_temp_file`, `eu_air_pollutants_data`, `write_to_excel_by_pollutant` og `data_reader`
Under er de ulike definerte funksjonene i scriptet forklart. De er også forklart i funksjonen i selve scriptet.

### def download_temp_file(url)
* Funksjonen brukes til å laste ned en fil fra en nettadresse og lagre den midlertidig på den lokale maskinen. Filen kan brukes videre i prosjektet.
* Brukes særlig for datasett med stor filstørrelse.
* Printer ut beskjed om hvor lang tid det tok å kjøre den nedlastede filen.

### def eu_air_pollutants_data(startdate, enddate, pollutants)
* Denne funksjonen henter timedata for luftkvalitetsmålinger fra European Environment Agency (EEA) via deres API. Den kan hente både verifiserte og ikke-verifiserte data.
* Data hentes spesifikt for Oslo.
* Returnerer en dictionary med DataFrames for hver stasjon og hver komponent.
* Funksjonen bruker start- og sluttdato i "YYYY-MM-DDTHH:MM:SSZ"-format og en liste med ønskede komponentkoder.

### def write_to_excel_by_pollutant(AirData, out_dir="data")
* Tar dictionaryen med DataFrames og skriver dem til egne Excel-filer for hver luftkomponent
* Excel-arkene blir lagret i mappen `data`
* Mappen `data` blir laget automatisk dersom den ikke eksisterer på forhånd.
* Excel-filene navngis etter den gjeldende utslippskomponenten.


### def data_reader(filename, nanlimit, skiprows=None, usecols=None, nrows=None, sep=None)
* Funksjonen brukes til å lese inn ulike typer datasett, som kan være CSV, Excel, JSON, HTML
* Den kontrollerer også datakvaliteten
* Konverterer `float64 ` til  `float32` for å spare på minnet

* Funksjonen identifiserer prosentandel NaN-verdier, og den gir advarsel dersom det overstiger Nanlimit
* Identifiserer negative verdier i float-kolonner
* Gir visuell oversikt over de første 10 radene og statistikk over numeriske verdier
* Den forsøker å gjøre kolonner som inneholder mixed type til å inneholde samme type
* Den oppgir hvor lang tid funksjonen bruker på å kjøre filen som blir analysert
* Returnerer `data`, som kan blir benyttet til senere oppgaver



## Functions_Dataanalysis.py
Dette scriptet består av klassene `Pollutants_manipulering` og `Tempdata_manipulering`.
Består av funksjonene `cap_outliers`, `plot_histogram`, `mean_std_meadin_corr`,  `reggresion_analysis`, `plot_AQI_leves`, `calculate_aqi` og `plot_pollutantlevels`.
Under er klassene og funksjonene forklart. De er også forklart i selve scriptet.

### `class Pollutants_manipulering`
Gjennomfører analyse av luftkvalitet.
####  negative_to_nan(self)
* Printer at negative verdier og uteliggere blir endret til Nan-verdier
* Høyere verdier enn 430 blir også endret til Nan
#### lenght_test(self)
* Sjekker størrelsen på hvert datasett
* Datasett blir fjernet dersom det er kortere enn 78000 rader
* Derfor blir datasett som er ansett som riktige, beholdt for videre analyse
#### mean_value_pollutant(self)
* Finner gjennomsnittsverdi fra målinger fra ulike stasjoner i Oslo
* `pollutant_concat` viser alle målingene fra de ulike stasjonene side om side
* `mean_pollutant` finner gjennomsnittet for alle målingene
* Missing values blir erstattet med verdier funnet fra lineær interpolasjon
* `result` viser alle målingene sammen med tidsintervaller det er målt ved
#### run_all(self)
* Kjører alle funksjonene i riktig rekkefølge, før den returnerer det datasettet som skal brukes videre



### `class Tempdata_manipulering`.
Gjør analyse av temperaturdata.
#### interpolate_nan(self) -> pd.DataFrame:
* Endrer komma til punktum i datasettet
* `nan_vals` finner antall Nan-verdier
* Sjekker at ale verdier er numeriske
* Verdier blir interpolert til å fylle inn i Nan-verdier
* `nan_left` sjekker hvor mange Nan-verdier som er igjen, og ideelt er det 0
* Returnerer `self.df`, som er interpolert og fikset dataframe


### def cap_outliers(data, column,plot=True)
* Skal finne og identifisere uteliggere i analysen av utslippsdataen. 
* Returnerer utslippsverdier for NO2, PM10 og PM25


### def plot_histogram(df,color,title,bins)
* Visualiserer utslippsdataene


### def mean_std_meadin_corr(df,name)
* Funksjonen finner viktige statistiske sammenhenger i datasettet; gjennomsnitt, standardavvik, median og korrelasjon
* Hvis korrelasjonen er mindre enn 0.6 anses den som veldig lav, og dette blir printet ut som beskjed
* Den statistiske dataen blir lagret i `dict_stats` for å være tilgjengelig ved senere bruk


### def reggresion_analysis(df,name,color,plot=True)
* Gjennomfører lineær regresjon av månedlige målinger, og ser på en lineær trend i årene det gjelder.
* Returnerer `x_sorted`, som er årene analysert i riktig rekkefølge
* Returnerer `y_fit_sorted`, som den lineære trenden for den analyserte utslippsdataen
* Returnerer `seasonal`,  som er sesongbaserte trender for alle årene

### def plot_AQI_leves(data,aqi_breakpoints,aqi_colors,images_dir)
* Plotter AQI-verdiene for alle utslippstypene fra årene 2016 til 2025.
* AQI er luftkvalitetsindeks, som er verdier som viser hvor god/dårlig luftkvaliteten er. Den er fra 0-500, der høyere verdier er verre luftkvalitet

### def calculate_aqi(value, breakpoints)
* Funksjonen regner ut AQI-verdiene for alle utslippstypene
* Lager liste med breakpoints for det aktuelle utslippet
* Finner AQI ved hjelp av formelen  aqi = ((value - low_conc) / (high_conc - low_conc)) * (high_aqi - low_aqi) + low_aqi


### def plot_pollutantlevels(data,aqi_breakpoints)
* Funksjonen lager en graf som viser gjennomsnitt av forurensningsnivåer i µg/m³ over tid og AQI-verdien for den gjeldende utslippstypen
* Denne gjør det mulig å sammenligne forurensingen og AQI-verdien


## Bruk av klassene og funksjonene
* Alle klassene og funksjonene blir benyttet i oppgaven, og er viktige for løsningen av oppgaven og for tolkningen av det endelige resultatet.
* Det var tidkrevende og til tider vanskelig å skape riktige klasser/funksjoner som gjorde det vi hadde som hensikt
* Da de var klare oppfattet vi dem som gode og hensiktsmessige for oppgaven de ble brukt til