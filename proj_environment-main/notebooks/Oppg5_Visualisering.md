# Oppgave 5 - Visualisering 

## Kode funksjon
Denne oppgaven er løst i i scriptet Visualisering.py. Dataen som er visualisert er den manipulerte Air Pollutants 
dataen lagret i mean_air_pollutants.pkl fra oppgave 3 (Databehandling.py). Nødvendige funksjoner er importert fra src/Functions_Dataanalysis.py. 
Første del av koden definerer Air Quality Index (AQI) verider for de ulike forurensningsstoffene NO2, PM2.5 og PM10. Utslippsmengden i ug/m^3, og 
tilsvarende AQI indeks er tatt fra https://www.pranaair.com/blog/what-is-air-quality-index-aqi-and-its-calculation/. I data mappen ligger excelfilene
aqi_breakpoints.xlsx og aqi_colors. Dictionaryen aqi_breakpoints{} konverterer df_breakpoint til en dictionary med hver key tilsvarende en pollutant 
og value som er en tuple med høy/lav konsentrajon og tilsvarende høy/lav aqi. aqi_colors lager tuples med (kategori, farge, lav aqi verdi, høy aqi verdi).
Siden kommer selve plottingen av AQI veridene. 

# Resonnement 

For det første plottet ble maplotlib klassen gridspec brukt. Grunnen til dette var at for å inkludere legenden som viser AQI-fargene pg betydningen kom
i veien for plottene. Ved å bruke gridspec og sette inn antall rader og kolonner og spesifisere størrelsene på dem, ble det enklere å 'rydde opp' i visualiseringen. 

I plot nummer to var intensjonen å legge til en interaktiv visualisering. I dette plottet blir de tre forskjellige utslippsstoffene samlet i et plot. Siden de ikke
har samme AQI verdi for samme mengde utslipp, ble isteden verktøyet hover label lagt til. 








