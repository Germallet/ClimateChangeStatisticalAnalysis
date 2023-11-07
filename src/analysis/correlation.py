import numpy as np
import pandas as pd
import energy_use_per_capita
import surface_temperature
import co2_concentrations
import co2_emissions
import bitcoin
import meat
import utils

from_year = 2010
to_year = 2021

# Read Dataframes
energy_use = energy_use_per_capita.region_dataframe("World",from_year,to_year)["Value"] # Data from 1971 to 2014
temperature_df = surface_temperature.dataframe("World",from_year,to_year)["Value"] # Data from 1961 to 2022
co2_concentrations_df = co2_concentrations.annual_dataframe("World",from_year,to_year)["Value"] # Data from 1750 to 2021
co2_emissions_df = co2_emissions.dataframe("World","Total",from_year,to_year)["Value"] # Data from 1855 to 2021
bitcoin = bitcoin.annual_dataframe(from_year=from_year,to_year=to_year)["BTCENEMAX"] # Data from 2010 to 2021
meat_df = meat.annual_dataframe(from_year=from_year,to_year=to_year)["Total"] # Data from 1961 to 2020

# Single Correlation Coeficient
correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(energy_use, 1971, 2014),
    utils.dataframe_year_filter(co2_concentrations_df, 1971, 2014)
)[0][1]
print("Correlation Coeficient ENERGY VS CO2 Concentrations")
print(correlation_coeficient)



# Correlation Matrix
correlation_matrix = pd.DataFrame({
    "Energy Use": energy_use,
    "Temperature": temperature_df,
    "CO2 Concentrations": co2_concentrations_df,
    "CO2 Emnissions": co2_emissions_df,
    "Bitcoin Electricity Consumption": bitcoin,
    "Meat Consumption": meat_df
}).corr(method="pearson",min_periods=4)
print(correlation_matrix)


exit(0)

# Cross-correlation
def plot_cross_correlation(serie1: pd.DataFrame, serie2: pd.DataFrame, title1: str, title2: str):
    filtered_serie1, filtered_serie2 = utils.matching_period_dataframes(serie1, serie2)
    cross_correlation = np.correlate(filtered_serie1, filtered_serie2, "full")
    cross_correlation_axis = np.arange(-len(filtered_serie1) + 1, len(filtered_serie2))
    utils.plot(cross_correlation_axis, cross_correlation, "Lag", "Correlation",
            f"Cross Correlation - {title1} x {title2}", f"{title1} x {title2} Correlation")

plot_cross_correlation(temperature_df, co2_concentrations_df, "Surface temperature", "Atmospheric CO2")
plot_cross_correlation(temperature_df, energy_use, "Surface temperature", "Energy use")
plot_cross_correlation(energy_use, co2_concentrations_df, "Energy use", "Atmospheric CO2")
plot_cross_correlation(temperature_df, bitcoin, "Surface temperature", "Bitcoin electricity consumption")
plot_cross_correlation(co2_concentrations_df, bitcoin, "Atmospheric CO2", "Bitcoin electricity consumption")
plot_cross_correlation(energy_use, bitcoin, "Energy use", "Bitcoin electricity consumption")
plot_cross_correlation(temperature_df, meat_df, "Surface temperature", "Meat consumption")
plot_cross_correlation(co2_concentrations_df, meat_df, "Atmospheric CO2", "Meat consumption")
plot_cross_correlation(energy_use, meat_df, "Energy use", "Meat consumption")
plot_cross_correlation(co2_emissions_df, temperature_df, "CO2 Emissions","Surface temperature")
plot_cross_correlation(co2_emissions_df, co2_concentrations_df, "CO2 Emissions","Atmospheric CO2")
plot_cross_correlation(co2_emissions_df, energy_use, "CO2 Emissions","Energy use")
plot_cross_correlation(co2_emissions_df, meat_df, "CO2 Emissions", "Meat consumption")