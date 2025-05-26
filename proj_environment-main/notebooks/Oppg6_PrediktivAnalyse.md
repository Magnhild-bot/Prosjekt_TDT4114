# Oppgave 6 – Prediksjon av luftforurensning

## Kodefunksjon

Denne oppgaven er løst i scriptet `Prediktivanalyse.py` og benytter data som tidligere er analysert og bearbeidet i `Dataanalyse.py.`
Dataene er renset for uteliggere og har fått trukket ut trender og sesongkomponenter med funksjoner fra `Functions_Dataanalysis.py.`
Formålet med denne oppgaven er å forutsi utviklingen i luftforurensningsnivåer for tre sentrale komponenter: NO₂, PM₂.₅ og PM₁₀.
Det blir valgt å se på utviklingen for 10 år frem i tid.
Dette gjøres ved hjelp av lineær regresjon fra scikit-learn på de eksisterende trendene som er funnet tidligere.
Scikit-learn benyttes fordi det er enda mer robust enn numpy.polyfit, som også kan brukes til lineær regresjon.

## Funksjonsbeskrivelse

### 1. raw_analysis()
Henter og bearbeider rådata for forurensningskomponentene:

Fjerner uteliggere med `cap_outliers()`.
Bruker `reggresion_analysis()` for å hente ut:
1. Lineær trend over år
2. Generell trend
3. Sesongkomponent

Returverdien er analyserte verdier for hver komponent.


### 2. predict_future()
Denne funksjonen bruker lineær regresjon fra scikit-learn for å lage fremtidige prediksjoner av forurensningsnivåene.

* Inndata:

* x_sorted: Liste med årstall.
* y_fit_sorted: Tilsvarende verdier for den lineære trenden.
* years_ahead: Hvor mange år frem det skal predikeres (velger 10 år).
* label: Navn på komponenten (f.eks. NO₂).
* color: Farge brukt i plottet.


* Utdata:
* Viser et linjediagram med historisk trend og fremtidig prediksjon.
* Returnerer to NumPy-arrays:
1. `future_x_years`: Årstall for fremtidig prediksjon
2. `future_y`: Predikert nivå for de ulike komponentene.


### 3. Lagring av resultater
Prediksjonene for NO₂, PM₂.₅ og PM₁₀ lagres i en pickle-fil, `future_pollutant_predictions.pkl`.

Denne filen lagres i `data_dir`, og inneholder strukturen:
{
    'NO2': (future_x_NO2, future_y_NO2),
    'PM2.5': (future_x_PM25, future_y_PM25),
    'PM10': (future_x_PM10, future_y_PM10)
}

## Tolkning av resultater

### NO₂
NO₂ viser en tydelig nedadgående trend. Prediksjonen indikerer at nivåene vil fortsette å synke. Dette kan indikere redusert biltrafikk og/eller strengere utslippskrav.

### PM₂.₅
PM₂.₅ har en svakere nedgang. Prediksjonen tyder på et forsiktig fall, men med høyere usikkerhet da fallet er mindre enn for eksempel NO₂.

### PM₁₀
PM₁₀-trenden viser en svak økning. Dette kan skyldes andre kilder til svevestøv, som vedfyring eller byggevirksomhet. Endringen er derimot liten og ikke nødvendigvis signifikant.


## Konklusjon

Lineær regresjon brukes til å estimere utviklingen av luftkvalitet fremover.
NO₂ er den komponenten med tydeligst nedgang.
PM-komponentene viser svakere trender og mer usikkerhet.
Resultatene gir et bilde av en mulig fremtidig utvikling, men  dette bør tolkes med forbehold, da de baseres på lineær ekstrapolering uten kontroll på andre eksterne faktorer som kan ha betydning.

Mulige videre forbedringer:
* Bruk av mer avanserte modeller (f.eks. med sesongjustering). 
* Inkludering av variabler som meteorologi og trafikkdata.