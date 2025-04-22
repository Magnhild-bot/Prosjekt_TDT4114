Denne mappen skal innholde svarene på mappe_del2. 
Mappen er ikke fullstendig enda, og mer innhold er under arbeid (spessielt oppgave 5 og 6).

test_filbehandling.py er foreløpig ikke relevant.

dataanalyse.py henter, behandler og analyserer utslippsdata fra EEA (European Environment Agency) 
for de rapporterte nasjonale utslippene (UNFCCC). (Merk at denne dataen kommer til å bli erstattet med dataen i pickle filen under data mappen.)
Hovedfunksjonene er:

1. Statistisk oppsummering

    - Beregner og skriver ut gjennomsnitt, median og standardavvik for kolonnen emissions.

2. Statistisk analyse for enkeltland

    - Filtrerer data for et spesifikt land (f.eks. Italia)
    
    - Fjerner manglende verdier
    
    - Beregner korrelasjon mellom år (Year) og utslipp (emissions)
    
    - Utfører lineær regresjon (y = a · x + b) og skriver ut koeffisientene
    
    - Plotter utslipp over tid sammen med regresjonslinjen

3. Håndtering av manglende verdier

    - Setter opp et eksempel‐datasett med tomme (NaN) utslippsverdier

    - Erstatter manglende verdier med gjennomsnittet i datasettet

    - Plotter fylt‐ut tidsserie

    - Utfører lineær interpolasjon for å fylle NaN og plotter resultatet