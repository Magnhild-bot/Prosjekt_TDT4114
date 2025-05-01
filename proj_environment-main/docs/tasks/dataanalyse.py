import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from retry_requests import retry



#1) Statistikk

median_emission = data['emissions'].median()
std_emission = data['emissions'].std()
mean_emission = data['emissions'].mean()


print("Gjennomsnittlig utslipp:", mean_emission)
print("Median utslipp:", median_emission)
print("Standardavvik utslipp:", std_emission)

#2) Statistisk analyse

# Filtrer data for et land, f.eks. Italia
country = 'Italy'
italy_data = data[data['Country'] == country]

# Fjern rader med manglende verdier
italy_data = italy_data.dropna(subset=['Year', 'emissions'])

# Korrelasjon mellom år og utslipp
correlation = italy_data['Year'].corr(italy_data['emissions'])

print(f"Korrelasjon mellom år og utslipp for {country}: {correlation:.3f}")

# Regresjonsanalyse 
x = italy_data['Year'].values
y = italy_data['emissions'].values

# Estimerer regresjonskoeffisienter, y = ax + b
a, b = np.polyfit(x, y, 1)  # lineær regresjon (grad 1)

print(f"Regresjonslinje: y = {a:.2f} * x + {b:.2f}")

# Plotter med regresjonslinje
plt.figure(figsize=(10, 6))
plt.scatter(x, y, alpha=0.6, label='Utslipp')
plt.plot(x, a * x + b, color='red', label='Regresjonslinje')
plt.title(f'Utslipp over tid – {country}')
plt.xlabel('År')
plt.ylabel('Utslipp (Gg CO₂-ekvivalenter)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()


#3) Håndtere manglende verdier

#Henter data der en ser det er feile verdier
data_f = { 'Year': [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009],
    'Emissions': [300, np.nan, 350, np.nan, 400, 450, 500, np.nan, 550, 600]}
df = pd.DataFrame(data_f)

## Erstatte manglende verdier med gjennomsnittet
df_filled = df.fillna(df['Emissions'].mean())

# Visualisering etter å ha fylt ut manglende verdier
plt.figure(figsize=(10, 6))
plt.plot(df_filled['Year'], df_filled['Emissions'], marker='o', color='green', linestyle='-', label='Utslipp med gjennomsnitt')
plt.title('Utslipp med manglende verdier fylt ut (gjennomsnitt)', fontsize=14)
plt.xlabel('År', fontsize=12)
plt.ylabel('Utslipp (Gg CO₂-ekvivalenter)', fontsize=12)
plt.grid(True)
plt.legend()
plt.show()

## # Erstatte manglende verdier med lineær interpolasjon
df_interpolate = df.interpolate(method='linear')

# Visualisering etter interpolasjon
plt.figure(figsize=(10, 6))
plt.plot(df_interpolate['Year'], df_interpolate['Emissions'], marker='o', color='red', linestyle='-', label='Utslipp med interpolasjon')
plt.title('Utslipp med manglende verdier fylt ut (interpolasjon)', fontsize=14)
plt.xlabel('År', fontsize=12)
plt.ylabel('Utslipp (Gg CO₂-ekvivalenter)', fontsize=12)
plt.grid(True)
plt.legend()
plt.show()


#4) Litt kommentarer

##Regresjonsanalyse er en analyse som ser sammenhenger mellom en avhengig variabel og en eller flere uavhengige variabler, 
#det kan være interessant i denne sammenhengen, der vi kan se på sammenheng mellom utslipp og klima blant annet

##Fylling av tomme kolonner med gjennomsnitt:
#Fordeler: Gir en kontinuerlig linje og gjør dataene lettere å analysere.
#Ulemper: Kan føre til skjevhet, spesielt hvis det er store variasjoner i dataene. Er kanskje ikke representativt for de faktiske utslippene.
#Mulig feilkilde: Å bruke gjennomsnittet kan overskygge virkelige topper eller bunner i dataene, og gi et feil bilde av trenden

#Lineær interpolasjon:
#Fordeler: Gir en mer realistisk fylling basert på eksisterende data, og bevarer trenden på en bedre måte
#Ulemper: Forutsetter at utslippene endrer seg jevnt, og kan gi feil bilde hvis utslippene varierer mer i virkeligheten
#Mulig feilkilde: Hvis dataene har stor variasjon i verdiene, kan interpolasjon da anta at trenden er jevn