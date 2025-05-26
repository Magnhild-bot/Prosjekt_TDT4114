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

### Pollutants_manipulering

Pollutants manipulering er en klasse som er laget for å "rense" luftkvaitetsdataen som ble lastet ned med en API request og skjekke at filene er av samme lengde slik at de er sammenlignbare og kan slås sammen til snittverdier over de ulike stasjonene for hver av luftkvalitetsmålingene.
Klassen innholder funksjonene:

1. negative_to_nan()
2. lenght_test()

Fra kjøringen av data_reader() i oppgave 2 ble det oppdaget at datasettet innholdt et par ekstremverdier og negative verdier. Da målinger av luftkvalitet ikke kan være negative, blir disse antatt som feilmålinger.
Et par ekstremverdier som lå oppi 10^3 potens for noen av datafilene som ble lastet ned er også urealistiske, og må dermed filtreres vekk.


