import numpy as np
import pandas as pd
import energy_use_per_capita
import surface_temperature
import co2_concentrations
import utils


# Read Dataframes
energy_use = energy_use_per_capita.region_dataframe("World", 1971, 2014)["Value"]
temperature_df = surface_temperature.dataframe("World", 1971, 2014)["Value"]
co2_df = co2_concentrations.annual_dataframe("World", 1971, 2014)["Value"]

# Single Correlation Coeficient
correlation_coeficient = np.corrcoef(temperature_df, co2_df)[0][1]
print(correlation_coeficient)

# Correlation Matrix
correlation_matrix = pd.DataFrame({
    "Energy Use": energy_use,
    "Temperature": temperature_df,
    "CO2 Concentrations": co2_df
}).corr()
print(correlation_matrix)

# Cross-correlation
def plot_cross_correlation(serie1: pd.DataFrame, serie2: pd.DataFrame, title1: str, title2: str):
    cross_correlation = np.correlate(serie1, serie2, "full")
    cross_correlation_axis = np.arange(-len(serie1) + 1, len(serie2))
    utils.plot(cross_correlation_axis, cross_correlation, "Lag", "Correlation",
            f"Cross Correlation - {title1} x {title2}", f"{title1} x {title2} Correlation")

plot_cross_correlation(temperature_df, co2_df, "Surface temperature", "Atmospheric CO2")
plot_cross_correlation(temperature_df, energy_use, "Surface temperature", "Energy use")
plot_cross_correlation(energy_use, co2_df, "Energy use", "Atmospheric CO2")
