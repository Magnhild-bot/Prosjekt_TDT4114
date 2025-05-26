# Oppgave 7 - Enhetstesting av funksjoner

## Kode og testbeskrivelse

Denne oppgaven omhandler testing av funksjonene `data_reader` og `predict_future` som er brukt i prosjektet. 
Testene er implementert i scriptet `tests.py`, og bruker `unittest`-rammeverket fra Python.

De funksjonene som testes er hentet fra:

* `Functions_FetchData.py`, der funksjonen `data_reader` blir testet.
* `Prediktivanalyse.py`, der funksjonen `predict_future` blir testet.

For å kunne importere funksjonene riktig, legges `src`-og `notebooks`-mappene til `sys.path` i starten av testscriptet. 
Dette gjør at testene kan kjøres uavhengig av hvilken mappe de kjøres fra.

## Strukturen i testene

Det er to testklasser:

1. `TestDataReader`  
2. `TestPredictFuture`

### 1. `TestDataReader`

Denne klassen tester funksjonen `data_reader`, som brukes til å lese inn og validere datasett fra CSV-filer.

#### a. `test_data_reader_valid_csv`

**Positiv test**  
Sjekker at en gyldig CSV-fil blir riktig lastet inn. CSV-filen inneholder både manglende og negative verdier. Testen sjekker:

- At `data_reader` returnerer et `pandas.DataFrame`
- At datasettet har riktig form (4 rader, 3 kolonner)
- At funksjonen printer en melding som inkluderer teksten (`'The data reader code took '`, output, `' seconds to run'`)

#### b. `test_data_reader_file_not_found`

**Negativ test**  
Sjekker at funksjonen håndterer filnavn som ikke eksisterer. Funksjonen skal avslutte programmet med `SystemExit`.



### 2. `TestPredictFuture`

Denne klassen tester funksjonen `predict_future`, som brukes til å gjøre framtidsprognoser basert på tidligere data.

#### a. `test_predict_future_output`

**Positiv test**  
Sjekker at funksjonen returnerer 24 fremtidige verdier når det ønskes 2 år med månedlige prediksjoner. Testen verifiserer at:

* Antall prediksjoner er 24
* Alle fremtidige årstall er større eller lik siste årstall i input

#### b. `test_predict_future_empty_input`

**Negativ test**  
Tester hvordan funksjonen håndterer tom input (`np.array([])`). Det forventes at funksjonen gir en `ValueError`.

#### c. `test_predict_future_increasing`

**Positiv test**  
Verifiserer at predikerte verdier endres over tid når dataen viser en tydelig lineær vekst. Dette bekrefter da at funksjonen lager en trendlinje som gir mening.


## Resultat
Alle testene passerte på rundt 1.50 sekunder totalt.
Dette betyr at begge funksjonene oppfører seg slik det forventes, og den håndterer vanlige og uvanlige inputs på en korrekt måte.
Dette tyder på robuste funksjoner, noe som er ønskelig da målet er at de skal fungere for mange forskjellige inputs.


## Kjøring av testene

Testene kan kjøres direkte fra terminalen ved å bruke:


```bash
python test_main.py
