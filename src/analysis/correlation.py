import numpy as np
import pandas as pd
import annual_surface_temperature
import atmospheric_co2_concentrations
import utils

normalized_values_1 = annual_surface_temperature.df["Value"].astype(float)
normalized_values_2 = atmospheric_co2_concentrations.annual_range_df(1961, 2022)["Value"].astype(float)

# Correlation Coeficient
correlation_coeficient = np.corrcoef(normalized_values_1, normalized_values_2)[0][1]
print(correlation_coeficient)

# Cross-correlation
cross_correlation = np.correlate(normalized_values_1, normalized_values_2, 'full')
cross_correlation_axis = np.arange(-len(normalized_values_1) + 1, len(normalized_values_2))
utils.plot(cross_correlation_axis, cross_correlation, "Lag", "Correlation", "Cross Correlation: Surface Temperature x Atmospheric CO2", "Temperature x CO2 Correlation")
