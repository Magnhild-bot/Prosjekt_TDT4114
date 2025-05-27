# Oppgave 5 - Visualisering

Kodefunksjon   
------------  
Denne oppgaven er løst i skriptet **Visualisering.py**. Det bygger på data som tidligere er hentet og bearbeidet; **mean_air_pollutants.pkl, temperatur_oslo.pkl**

Formålet er å beregne Air Quality Index (AQI) for tre sentrale forurensningskomponenter (NO2, PM2.5 og PM10) og se utviklingen
over tid, samt korrelasjon med lufttemperatur.

* en statisk Matplotlib-figur som viser AQI-nivåer over tid (2016 – 2025).  
* en interaktiv Plotly-figur som viser ukentlig gjennomsnittlig konsentrasjon sammen med tilhørende AQI-verdi.  
* en statisk Matplotlib-figur som viser forurensningskomponenetene sammen med månedlig middeltemperatur.

Funksjonsbeskrivelse  
--------------------  
### 1. **calculate_aqi()**

Denne funksjonen beregner AQI for en enkelt måleverdi av et forurensingsstoff (NO2, PM2.5, PM10).

Den tar inn:
* `value` - selve konsentrasjonen av forureningsstoffet 
* `breakpoints` - en liste med AQI-terksel-tupler.

Den går gjennom breakpoints-listen med en for-løkke. For hvert intervall sjekker den
om `if low_conc <= value <= high_conc:`, når riktig intervall er funnet bruker den lineær interpolasjon
for å plassere verdien på AQI-skalaen. `aqi = ((value - low_conc) / (high_conc - low_conc)) * (high_aqi - low_aqi) + low_aqi`.

### 2. **plot_AQI_leves()**
Denne funksjonen lager en samlet figur som viser hvordan AQI har utviklet seg for flere 
forurensningsstoffer i perioden 2016-2025. Figuren består av tre delplott (ett pr. stoff) pluss en felles fargelegend
som forklarer AQI-kategoriene. Resultatet lagres som en PNG-fil og vises på skjermen.

Den tar inn:
* `data` - dict med forurensningsstoff som nøkkel og verdien er pandas.DataFrame
 med kolonne ``Time Interval`` og ``Value`` (konsentrasjon)
* `aqi_breakpoints` - en liste med AQI-terksel-tupler.
* `aqi_colors` - en liste med fire-tupler `(label, color, low, high)` som definerer
navnet, fargen og y-verdien til hvert AQI-bånd på skalaen 0-500
* `images_dir` - filbanen der ferdig figur skal lagres


Funksjonen oppretter en matplotlib-figur på 14*12 tommer og deler den opp med GridSpec: tre rader i venstre kolonne for selve tidsseriene og en hel høyre kolonne til fargelegenden.
Den setter en hovedtittel, samt en felles vertikal y-akseetikett med teksten AQI Value. For hvert forurensningsstoff i data blir konsentrasjonsverdien omgjort til AQI ved hjelp av calculate_aqi. Resultatet lagres i en ny DataFrame-kolonne kalt AQI, og plottes som en svart linje mot tid.
Samtidig tegnes bakgrunnsrektangler (axhspan) som dekker hele plottområdet i de fargene som beskrives av aqi_colors, slik blir det lett å se hvilke deler av kurven som havner i de ulike helsekateogoriene. 
Kun nederste subplot får x-akseetiketten Years. De andre skjuler x-etikettene for et ryddigere utseende. Alle tre akser får rutenett og y-akse-grense 0–500.
I den høyre kolonnen bygges en egen legend av små fargede rektangler (Patch). Det gjør at figuren får en samlet forklaring uten å stjele plass fra tidsseriene.
Til slutt lagres bildet som PNG ved å kalle fig.savefig(images_dir, dpi=300, bbox_inches='tight'), og plt.show() åpner vinduet (eller viser inline hvis du kjører i Jupyter).


Resultatet er en bildefil som viser AQI-kurven for hvert stoff med klar bakgrunnsfarge som indikerer AQI-kategori, pluss en lettlest legende. Figuren gir et raskt visuelt overblikk over hvor ofte og hvor mye hvert stoff havner i ulike helserelaterte intervaller.



### 3. **plot_pollutantlevels()**

Denne funksjonen lager en **interaktiv Plotly-figur** som viser ukentlig gjennomsnitt av konsentrasjon for forurensningsstoffene
samtidig som hvert datapunkt får beregnet og vist sin AQI-verdi en hover-boks.

Den tar inn:
* ``data`` -  dict med forurensningsstoff som nøkkel og verdien er pandas.DataFrame med kolonne Time Interval og Value (konsentrasjon)
* ``aqi_breakpoints`` - en liste med AQI-terksel-tupler.

Den går gjennom forurensningsdataen og og konverterer Time Interval til ekte
datetime64[ns]-objekter og flytter den til DataFrame-ens indeks, som kreves for pandas resample. 
pandas resample grupperer alle rader som faller i samme uke, og .mean() tar så gjenomsnittet av kolonnen ``Value`` for hver uke.

``pandas.concat`` brukes for å sette sammen ukesereiene slik at alle forurensingsstoffene
har samme tidsindeks. ``wide`` lager en kolonne per foruresning og en rad per uke, mens
``long`` lager en rad per uke-stoff par, dette formatet er foretrukket for plotly express .
``melt()`` gjør om den brede tabellen til et oppsett der “variabelnavn blir verdier” og “verdier blir rader”.

`iso.calendar` brukes til å lage en dataframe med kolonner year, week, day basert på ISO ukesystemet.
Disse blir så tildelt kolonnene ``Week`` og `Year ` frå `df_long`.


Resultatet blir et interaktivt plot som viser forurennsingesstoffenes konsentrasjon over tid og 
ved å holde musepekeren langs grafene får man oppgitt uke nummer og AQI-verdi for gitt uke.

Tolkning av resultater  
----------------------  

* **Figur 1**
  * **Fargebåndene** gir et raskt visuelt inntrykk av hvor ofte konsentrasjonene havner i de ulike AQI-kategoriene.
  * Fra dette plottet ser man at det blir uoversiktelig og lite informativt med så store mengder data
    i en figur, det er vanskelig å se trender. Derfor er utslippsdataen i figur nr 2 samlet i ukentlig data istedet, for
    gjøre visualiseringen enklere å tolke og trendene mer synlige. 
  * Her ble GridSpec brukt, da det legend kom i veien for plottene, på denne måten
  kan kolonner og rader i figuren spesifiseres for å ha mer kontroll på layout til figuren.
* **Figur 2**: 
  * **Interaktiv graf** gjør det mulig å ha mer data i samme plot, og visualiseringen mer engasjerende.
  * NO2 viser fallende AQI-topp-verdier over tid, mens PM-komponentene har mindre tydelige endringer.
* **Figur 3**
  * Det er tydelig at lufttempertur og utslipp har en sammenheng. Fra figur 3 er det synlig lavere luftforurensing
  ved høyere temperaturer og omvendt. Dette kan ha sammenheng med
  økt vedforbrenning for oppvarming av hus og bruk av piggdekk, på vinterhavlåret
  som begge bidrar til luftforurensing. I Norge er veitrafikk og vedfyring de viktigste
  kildene til luftforurensning. 
    * https://luftkvalitet.miljodirektoratet.no/artikkel/artikler/kilder-til-luftforurensning/

  
  

## Konklusjon  

Skriptet kombinerer statisk og interaktiv visualisering for å gjøre luftkvalitetsdata både tilgjengelige og intuitive.
Ved å legge AQI-fargebånd bak tidsseriene får brukeren direkte sammenheng med helseeffektskalaen. Med temperaturdata
og luftforurensning i samme figur er det lett å se sammenhengen mellom dem. 


## Forbedringsmuligheter

* Kople vær- og trafikkdata inn i samme visualisering for å finne årsakssammenhenger.  
* Legge inn en alarm som markerer perioder der AQI overstiger “usunn” i mer enn n døgn, for å gi koden 
en mer synlig intensjon.

## Kjøreveildening
```bash
# Kjør Visualisering.py
python Visualisering.py


