# Oppgave 6 – Prediksjon av luftforurensning

## Kodefunksjon

Denne oppgaven er løst i scriptet `Prediktivanalyse.py` og benytter data som tidligere er analysert og bearbeidet i `Dataanalyse.py.`
Dataene er nå renset for uteliggere og har trukket ut trender og sesongkomponenter med funksjoner fra `Functions_Dataanalysis.py.`
Formålet med denne oppgaven er å bruke prediktiv analyse til å forutsi utviklingen i luftforurensningsnivåer for tre komponenter: NO2, PM2.5 og PM10.
Det blir valgt å se på utviklingen for 10 år frem i tid.
Dette gjøres ved hjelp av lineær regresjon fra scikit-learn på de eksisterende trendene som er funnet tidligere.
Scikit-learn benyttes fordi det er enda mer robust enn numpy.polyfit, som også kan brukes til lineær regresjon.

## Funksjonsbeskrivelse

### predict_future()
Denne funksjonen bruker lineær regresjon fra scikit-learn for å lage fremtidige prediksjoner av forurensningsnivåene.
Det blir lagt til en minimimumsverdi på 0 for utslippene, da utslipp ikke kan bli lavere enn 0 µg/m³.

* Inndata:
* x_fit_sorted: Liste med årstall.
* y_fit_sorted: Tilsvarende verdier for utsippene
* years: Hvor mange år frem det skal predikeres, der vi velger 10 år.
* label: Navn på komponenten, for eksempel NO2
* color: Farge som er brukt i plottet.

* Utdata:
* Viser et linjediagram med historisk trend og fremtidig prediksjon.
* Returnerer to NumPy-arrays:
1. `future_x_years`: Årstall for fremtidig prediksjon
2. `future_y`: Predikert verdi for de ulike komponentene.


### 3. Lagring av resultater
Prediksjonene for NO2, PM2.5 og PM10 lagres i en pickle-fil, `future_pollutant_predictions.pkl`.

Denne filen lagres i `data_dir`, og inneholder strukturen:
{
    'NO2': (future_x_NO2, future_y_NO2),
    'PM2.5': (future_x_PM25, future_y_PM25),
    'PM10': (future_x_PM10, future_y_PM10)
}

## Tolkning av resultater

### NO2
NO2 viser en tydelig nedadgående trend. Prediksjonen tyder på at nivåene vil fortsette å synke. Dette kan for eksempel indikere redusert biltrafikk og/eller strengere utslippskrav.

### PM2.5
PM2.5 har en svakere nedgang. Prediksjonen tyder på et forsiktig fall, men med høyere usikkerhet da fallet er mindre enn for eksempel for NO2.

### PM10
PM10-trenden viser en svak økning. Dette kan skyldes andre kilder til svevestøv, som vedfyring eller byggevirksomhet. Endringen er derimot liten, og er ikke nødvendigvis signifikant.


## Konklusjon

Lineær regresjon brukes til å estimere utviklingen frem i tid, og i dette tilfellet er det luftkvalitet frem i tid.
NO2 er den komponenten med tydeligst nedgang.
PM-komponentene viser svakere trender og mer usikkerhet, der PM10 viser en svak økning.
Resultatene gir et bilde av en mulig fremtidig utvikling, men  dette bør tolkes med forbehold, da de baseres på lineær interpolering der andre faktorer som ikke er tatt med i beregningen kan ha betydning.

## Forbedringsmuligheter
Mulige videre forbedringer:
* Bruk av mer avanserte modeller. Vi kunne for eksempel bruk sesongmodeller, da dataen fra oppgave 4 viste en sterk sesongbasert korrelasjon.
* Det er mulig å inkludere flere variabler, som biltrafikk.

Mulige fremtidige gjøremål:
* Analysere årsakene til at utslippene øker/minker.
* Hvilke tiltak som kan gjøres for å minke utslippene i enda større grad.
* Bruke all kode til å analysere flere utslippskomponenter, og deres fremtidige utslipp basert på prediktiv analyse.

## Kjøreveiledning
```bash

# Kjør Prediktivanalyse.py
python Prediktivanalyse.py
