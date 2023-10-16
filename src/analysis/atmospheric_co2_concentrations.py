from utils import *

df = read_csv("Atmospheric_CO₂_Concentrations.csv")
world_co2_concentrations = df.loc[(df["Country"] == "World") & (df["Unit"] == "Parts Per Million")]
plot_all(world_co2_concentrations["Date"], world_co2_concentrations["Value"], "Date", "CO₂ Parts Per Million", "World Atmospheric CO₂ Concentrations", "", "World CO2 Concentrations")
