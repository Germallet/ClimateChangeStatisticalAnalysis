import numpy as np
import pandas as pd
import energy_use_per_capita
import surface_temperature
import co2_concentrations
import co2_emissions
import bitcoin
import meat
import utils
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from datetime import timedelta
import os
# import statsmodels.api as sm

IMG_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../images/forecasting/"

# Read Dataframes
energy_use = energy_use_per_capita.region_dataframe("World",1971,2014)["Value"] # Data from 1971 to 2014
temperature_df = surface_temperature.dataframe("World",1961,2021)["Value"] # Data from 1961 to 2022
co2_concentrations_df = co2_concentrations.annual_dataframe("World",1961,2021)["Value"] # Data from 1750 to 2021
co2_emissions_df = co2_emissions.dataframe("World","Total",1961,2021)["Value"] # Data from 1855 to 2021
bitcoin = bitcoin.annual_dataframe(from_year=2010,to_year=2021)["BTCENEMAX"] # Data from 2010 to 2021
meat_df = meat.annual_dataframe(from_year=1961,to_year=2020)["Total"] # Data from 1961 to 2020

# Single Correlation Coeficient
correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(energy_use, 1971, 2014),
    utils.dataframe_year_filter(temperature_df, 1971, 2014)
)[0][1]
print("Correlation Coeficient ENERGY VS Temperature")
print(correlation_coeficient)

correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(co2_concentrations_df, 1961, 2021),
    utils.dataframe_year_filter(temperature_df, 1961, 2021)
)[0][1]
print("Correlation Coeficient CO2 concentrations VS Temperature")
print(correlation_coeficient)

correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(co2_emissions_df, 1971, 2021),
    utils.dataframe_year_filter(temperature_df, 1971, 2021)
)[0][1]
print("Correlation Coeficient CO2 Emissions VS Temperature")
print(correlation_coeficient)

correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(meat_df, 1961, 2020),
    utils.dataframe_year_filter(temperature_df, 1961, 2020)
)[0][1]
print("Correlation Coeficient Meat VS Temperature")
print(correlation_coeficient)

window_size = 5  # Adjust the window size as needed

aux = temperature_df.diff().rolling(window=window_size, min_periods=0).mean()
print(aux)
temperature_df = temperature_df.diff().fillna(aux)
temperature_df.fillna(method="backfill", inplace=True)
aux = energy_use.diff().rolling(window=window_size, min_periods=0).mean()
energy_use = energy_use.diff().fillna(aux)
energy_use.fillna(method="backfill", inplace=True)
aux = co2_emissions_df.diff().rolling(window=window_size, min_periods=0).mean()
co2_emissions_df = co2_emissions_df.diff().fillna(aux)
co2_emissions_df.fillna(method="backfill", inplace=True)
aux = meat_df.diff().rolling(window=window_size, min_periods=0).mean()
meat_df = meat_df.diff().fillna(aux)
meat_df.fillna(method="backfill", inplace=True)

print("Temperature DF")
print("ADF")
print(adfuller(temperature_df)[1])
print("KPSS")
print(kpss(temperature_df)[1])
print("Energy Use DF")
print("ADF")
print(adfuller(energy_use)[1])
print("KPSS")
print(kpss(energy_use)[1])
print("C02 Concentrations DF")
print("ADF")
print(adfuller(co2_concentrations_df.diff().dropna())[1])
print("KPSS")
print(kpss(co2_concentrations_df.diff().dropna())[1])
print("C02 Emissions DF")
print("ADF")
print(adfuller(co2_emissions_df)[1])
print("KPSS")
print(kpss(co2_emissions_df)[1])
print("Meat DF")
print("ADF")
print(adfuller(meat_df)[1])
print("KPSS")
print(kpss(meat_df)[1])
print("temp", energy_use.shape)
print("eng", energy_use.shape)
print("co2_emissions_df", co2_emissions_df.shape)
print("meat_df", meat_df.shape)

# Single Correlation Coeficient
correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(energy_use, 1971, 2014),
    utils.dataframe_year_filter(temperature_df, 1971, 2014)
)[0][1]
print("Correlation Coeficient ENERGY VS Temperature")
print(correlation_coeficient)

correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(co2_concentrations_df, 1961, 2021),
    utils.dataframe_year_filter(temperature_df, 1961, 2021)
)[0][1]
print("Correlation Coeficient CO2 concentrations VS Temperature")
print(correlation_coeficient)

correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(co2_emissions_df, 1971, 2021),
    utils.dataframe_year_filter(temperature_df, 1971, 2021)
)[0][1]
print("Correlation Coeficient CO2 Emissions VS Temperature")
print(correlation_coeficient)

correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(meat_df, 1961, 2020),
    utils.dataframe_year_filter(temperature_df, 1961, 2020)
)[0][1]
print("Correlation Coeficient Meat VS Temperature")
print(correlation_coeficient)

ts = temperature_df

# Plot the time series data
plt.figure(figsize=(10, 6))
plt.plot(ts)
plt.title('Generated Time Series Data')
plt.savefig(os.path.join(IMG_DIR, "Temperature Time Series.png"))
plt.clf()

# Split the data into training and testing sets
train_size = int(len(ts) * 0.8)
train, test = ts[:train_size + 1], ts[train_size:]

# Fit an ARIMA model
order = (3, 0, 5)  # Replace with appropriate order based on your data and analysis
model = ARIMA(train, order=order)
fit_model = model.fit()

# Forecast future values
print("Test Len", len(test))
forecast_steps = len(test)
forecast = fit_model.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=train.index[-2], periods=forecast_steps, freq='Y')

# Plot the training data, testing data, and the forecast
plt.figure(figsize=(12, 8))
plt.plot(train, label='Training Data')
plt.plot(test, label='Testing Data')
plt.plot(forecast_index, forecast.predicted_mean, color='red', label='Forecast')
plt.title('ARIMA Model Forecasting')
plt.legend()
plt.savefig(os.path.join(IMG_DIR, "Temperature Forecasting.png"))
plt.clf()


exit(0)


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