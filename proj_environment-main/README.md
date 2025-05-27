# Prosjekt TDT4114
Et Python-prosjekt utviklet i forbindelse med emnet TDT4114. Denne README-filen gir et raskt overblikk over prosjektets struktur, slik at nye bidragsytere lett finner fram.


## Prosjektstruktur

```text
Prosjekt_TDT4114/
|-- proj_environment-main/
|   |-- data/
|   |-- docs/
|   |-- notebooks/ 
|   |-- resources/
|   |-- src/
|   |-- tests/
|   `-- README.md
|-- .gitignore
|-- requirements.txt

```
## Installering
I requirements.txt ligger alle nødvendige pakker for scriptene i prosjektet.

## Oppbygning
Alle funksjoner brukt i de ulike scriptene er samlet under src mappen. Der ligger
Functions_Datanalysis.py som inneholder funksjoner knyttet til dataanalyse, og Functions_FetchData.py
som inneholder funksjoner knyttet til inhenting av data. Dette er gjort
for at scriptene skal være oversiktlige og kortfattet.


## Bruker instruksjon
1. For å hente inn nødvendig data må bruker begynne med å kjøre
Datainnsamling.py.
2. Kjør Databehandling.py som renserer og formaterer innsamlet data, og lagrer det
for videre oppgaver.
3. Kjør Dataanalyse.py for statistiske analyser.
4. Kjør Visualisering.py for visualisering av behandet data.
5. Kjør Prediktivanalyse for prediksjon av luftforurensningsnivå. 

