# Oppgave 3 -Databehandling

## Kode funksjon
Denne oppgaven er løst i scriptet Databehandling.py. 
Dataen som er analysert er den dataen fra oppgave 2 som gruppen valgte å gå videre med. Både dataen i NO2.xlsx, PM2.5.xlsx, PM10.xlsx og
Temp_oslo_2016_2024.csv innholder både nan-verdier og urealistiske verdier (negative luftkvalitetsmålinger). Gruppen valgte derfor at det var intressant å gå videre med disse dataene
for å utforske måter å manipulere dataen på. I tillegg vil det være interessant å se på sammenhengen mellom temperaturdata og luftkvalitet da disse i følge Miljødirektoratet er korrelert.

For å holde Databehandling.py mest mulig kortfattet er klassene brukt for å manipulere luftkvalitetsdataen og temperaturdataen samlet i Functions_Dataanalyse.py i scr mappen:
Følgende klasser for denne oppgaven er brukt:

1. Pollutants_manipulering
2. Tempdata_manipulering 

Outputtet fra begge klassene er filtrerte dataframes. Outputtet for de ulike luftforrurensningspartikklene fra Pollutants_manipulering er samlet til en dictionary og picklet til mean_air_pollutants.pkl.
Outputtet fra Tempdata_manipulering er picklet til temperatur_oslo.pkl. Begge Pickle filene legges i mappen \data og er klar til å brukes videre for analyser i prosjektet.

### 1. Pollutants_manipulering

Pollutants_manipulering er en klasse som er laget for å "rense" luftkvaitetsdataen som ble lastet ned med en API request og sjekke at filene er av samme lengde slik at de er sammenlignbare og kan slås sammen til snittverdier over de ulike stasjonene for hver av luftkvalitetsmålingene.
Fra kjøringen av data_reader() i oppgave 2 ble det oppdaget at datasettet innholdt et par ekstremverdier og negative verdier. Da målinger av luftkvalitet ikke kan være negative, blir disse antatt som feilmålinger.
Et par ekstremverdier som lå opp i *10^3 for noen av datafilene som ble lastet ned er også urealistiske, og må dermed filtreres vekk.

Klassen innholder funksjonene:

1. negative_to_nan(): Funksjonen henter inn dataframen som skal filtreres, og "markerer" negative verdier og ekstremverdier ved å sette disse til nan.
2. lenght_test(): Sjekker lengden til datasettene. Dersom ingenting mangler skal kolonnene innholde 78887 elementer. Data med feil lengde blir forkastet.
3. mean_value_pollutant(): Funksjonen samler alle luftkvalitetsmålingene fra de ulike stasjonene, slår dem sammen kolonnevis og beregner radvis gjennomsnitt for hvert tidsstempel. 
Deretter brukes tid kolonnen for første stasjon som tidsakse. Eventuelle manglende verdier fylles ved lineær interpolasjon.
Til slutt returneres et DataFrame med tidsintervaller og de interpolerte gjennomsnittsverdiene.


### 2. Tempdata_manipulering

Tempdata_manipulering er en klasse for å filtrere bort eventuelle nan verdier i datasettet fra temp_data_oslo_2016_2020.csv.
Før dette blir gjort blir temperatur verdiene endre desimal separator fra komme til punktum for å tolke dataen riktig.
Dataen blir også sikret å bli lest som tall verdier ved å bruke pd.to_numeric().
Etter dette er gjort ersatttes alle nan verdier med en interpolert verdi ved å bruke pandas sin DataFrame.interpolate().

## Tolking av resultater

Etter å ha kjørt og renset luftkvalitetsdataen innholdt alle filene noen ark med ugylig datalengde, og ble forkastet. Det gyldige dataarkene ble vellykket rensket for det mest ekstreme ekstremverdiene samt negative verdier, og gjennomsnittsmåling for de ulike stasjonene ble funnet.
Oppgave 3 (Dataanalyse.py) vil jobbe videre med å viusualisere eventuelle andre uteliggere/ekstremverdier og rense datasettet for disse.
Tempraturdataen ble sikret for å ikke innholde nan verdier, og komma ble vellykket endret til punktum for desimalskille, som en ser i utskriften fra .head().
## Forbedringsmuligheter

Igjen tar koden veldig lang tid å kjøre på grunn av de store excelfilene for luftkavlitet. Slik som nevnt i Oppg2_Datainnsamling.md kan en i fremditig arbeid se på muligheten for å istede bruke effektive metoder for å skrive til en csv fil.

## Kjøreveiledning
```bash

# Kjør databehandling.py
python Databehandling.py



