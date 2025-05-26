# Oppgave 5 - Visualisering
===================================================

Kodefunksjon  
------------  
Denne oppgaven er løst i skriptet **Visualisering.py**. Det bygger på data som tidligere er hentet og bearbeidet; **mean_air_pollutants.pkl**

Formålet er å beregne Air Quality Index (AQI) for tre sentrale forurensningskomponenter (NO2, PM2.5 og PM10) og presentere resultatene i to figurer:

* en statisk Matplotlib-figur som viser AQI-nivåer over tid (2016 – 2025)  
* en interaktiv Plotly-figur som viser ukentlig gjennomsnittlig konsentrasjon sammen med tilhørende AQI-verdi  

Funksjonsbeskrivelse  
--------------------  
### 1. **calculate_aqi()**

Denne funksjonen beregner AQI for en enkelt måleverdi av et forurensingsstoff (NO2, PM2.5, PM10).

Den tar inn `value` med selve konsentrasjonen av forureningsstoffet og `breakpoints` en liste med AQI-terksel-tupler.

Den går gjennom breakpoints-listen med en for-løkke. For hvert intervall sjekker den
om `if low_conc <= value <= high_conc:`, når riktig intervall er funnet bruker den lineær interpolasjon
for å plassere verdien på AQI-skalaen. `aqi = ((value - low_conc) / (high_conc - low_conc)) * (high_aqi - low_aqi) + low_aqi`.




Tolkning av resultater  
----------------------  

* **Fargebåndene** gir et raskt visuelt inntrykk av hvor ofte konsentrasjonene havner i de ulike AQI-kategoriene.  
* **Trender**: NO2 viser ofte fallende AQI-topp-verdier, mens PM-komponentene har mindre tydelige endringer.  
* **Interaktiv graf** gjør det mulig å ha mer data i samme plot. Med både konsentrasjon, AQI-verdi og tid.

Konklusjon  
----------  
Skriptet kombinerer statisk og interaktiv visualisering for å gjøre luftkvalitetsdata både tilgjengelige og intuitive. Ved å legge AQI-fargebånd bak tidsseriene får brukeren direkte sammenheng mellom råmålinger og helseeffektskalaen.


Mulige fremtidige gjøremål  
--------------------------  

* Kople vær- og trafikkdata inn i samme visualisering for å finne årsakssammenhenger.  
* Legge inn en alarm som markerer perioder der AQI overstiger “usunn” i mer enn n døgn, for å gjøre koden mer






