import numpy as np
import pandas as pd
import surface_temperature
import co2_concentrations
import utils


# Read Dataframes
temperature_df = surface_temperature.dataframe("World")["Value"]
co2_df = co2_concentrations.annual_dataframe("World", 1961, 2022)["Value"]

# Correlation Coeficient
correlation_coeficient = np.corrcoef(temperature_df, co2_df)[0][1]
print(correlation_coeficient)

# Cross-correlation
cross_correlation = np.correlate(temperature_df, co2_df, 'full')
cross_correlation_axis = np.arange(-len(temperature_df) + 1, len(co2_df))
utils.plot(cross_correlation_axis, cross_correlation, "Lag", "Correlation",
           "Cross Correlation - Surface Temperature x Atmospheric CO2", "Temperature x CO2 Correlation")
