import numpy as np
import pandas as pd
import energy_use_per_capita
import surface_temperature
import co2_concentrations
import bitcoin
import meat
import utils

# Read Dataframes
energy_use = energy_use_per_capita.region_dataframe("World")["Value"] # Data from 1971 to 2014
temperature_df = surface_temperature.dataframe("World")["Value"] # Data from 1961 to 2022
co2_df = co2_concentrations.annual_dataframe("World")["Value"] # Data from 1750 to 2021
bitcoin = bitcoin.annual_dataframe()["BTCENEMAX"] # Data from 2010 to 2021
meat_df = meat.annual_dataframe()["Total"] # Data from 1961 to 2020

# Single Correlation Coeficient
correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(energy_use, 1971, 2014),
    utils.dataframe_year_filter(co2_df, 1971, 2014)
)[0][1]
print(correlation_coeficient)

# Correlation Matrix
correlation_matrix = pd.DataFrame({
    "Energy Use": energy_use,
    "Temperature": temperature_df,
    "CO2 Concentrations": co2_df,
    "Bitcoin Electricity Consumption": bitcoin,
    "Meat Consumption": meat_df
}).corr()
print(correlation_matrix)

# Cross-correlation
def plot_cross_correlation(serie1: pd.DataFrame, serie2: pd.DataFrame, title1: str, title2: str):
    filtered_serie1, filtered_serie2 = utils.matching_period_dataframes(serie1, serie2)
    cross_correlation = np.correlate(filtered_serie1, filtered_serie2, "full")
    cross_correlation_axis = np.arange(-len(filtered_serie1) + 1, len(filtered_serie2))
    utils.plot(cross_correlation_axis, cross_correlation, "Lag", "Correlation",
            f"Cross Correlation - {title1} x {title2}", f"{title1} x {title2} Correlation")

plot_cross_correlation(temperature_df, co2_df, "Surface temperature", "Atmospheric CO2")
plot_cross_correlation(temperature_df, energy_use, "Surface temperature", "Energy use")
plot_cross_correlation(energy_use, co2_df, "Energy use", "Atmospheric CO2")
plot_cross_correlation(temperature_df, bitcoin, "Surface temperature", "Bitcoin electricity consumption")
plot_cross_correlation(co2_df, bitcoin, "Atmospheric CO2", "Bitcoin electricity consumption")
plot_cross_correlation(energy_use, bitcoin, "Energy use", "Bitcoin electricity consumption")
plot_cross_correlation(temperature_df, meat_df, "Surface temperature", "Meat consumption")
plot_cross_correlation(co2_df, meat_df, "Atmospheric CO2", "Meat consumption")
plot_cross_correlation(energy_use, meat_df, "Energy use", "Meat consumption")
