## Datasett

Denne mappen inneholder koden som laster ned datasett klare for analyse. Målet med 
prosjektet er å lage et program som beregner og viser prognoser for luftkvalitet.

### Luftforurensningsdata

For å analysere luftkvaliteten må data om forurensningskomponentene NO2, PM10 og PM2,5 lastes opp. Ifølge FHI er dette tre av forurensningsstoffene som
forårsaker mest sykdom og død: https://www.fhi.no/he/folkehelserapporten/miljo/luftforureining--i-noreg/?term=#om-luftforurensning. European Environment Agency (EEA) er valgt som kilde, 
og EEA-dokumentasjonen for nedlasting ligger i proj_environment-main\docs\data_documentation. Luftforurensningsdataene lastes ned via API-kall og 
er derfor ikke synlige i denne mappen før du kjører Datainnsamling.py under proj_environment-main\notebooks. 


### Temperaturdata

Temperaturdata for Oslo mellom 2016–2024, er lastet ned som CSV fra Norsk Klimaservicesenter: https://seklima.met.no/. 
Filen Temp_oslo_2016_2024.csv i denne mappen inneholder månedlig middeltemperatur. Ifølge Miljødirektoratet er de viktigste utslippskildene eksos fra biler samt støv fra veislitasje,
bremser og bildekk: https://luftkvalitet.miljodirektoratet.no/artikkel/artikler/kilder-til-luftforurensning/.
 
 

### AQI data
For visualisering av luftforurensning er Air Quality Index (AQI) brukt. aqi_breakpoints.xlsx viser sammenhengen mellom konsentrasjon av hvert stoff og tilhørende AQI-verdi. 
aqi_colors.xlsx knytter AQI-verdier til farger. Verdiene er hentet fra https://www.pranaair.com/blog/what-is-air-quality-index-aqi-and-its-calculation/.



