from utils import *

df = read_csv("Annual_Surface_Temperature_Change.csv")
years = df.columns[10:-1]
world_surface_temperature_change = df.loc[df["Country"] == "World"].iloc[0][10:-1]
plot_all(years, world_surface_temperature_change, "Date", "Degree Celsius", "Annual Surface Temperature Change", "", "Annual Surface Temperature Change")
