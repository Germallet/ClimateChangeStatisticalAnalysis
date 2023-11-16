import numpy as np
import pandas as pd
import utils
import surface_temperature_change
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from datetime import timedelta
import os

IMG_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../images/forecasting/"

temperature_df = surface_temperature_change.dataframe() # Data from 1850 to 2023

print("PRE-Diff()")
print("Temperature DF")
print("ADF")
print(adfuller(temperature_df)[1])
print("KPSS")
print(kpss(temperature_df)[1])

window_size = 5  # Adjust the window size as needed

aux = temperature_df.diff().rolling(window=window_size, min_periods=0).mean()
temperature_df = temperature_df.diff().fillna(aux)
temperature_df.fillna(method="backfill", inplace=True)

print("-----------------------------------------------------------------------------------------------------")

print("Temperature DF")
print("ADF")
print(adfuller(temperature_df)[1])
print("KPSS")
print(kpss(temperature_df)[1])

ts = temperature_df

# Plot the time series data
plt.figure(figsize=(10, 6))
plt.plot(ts)
plt.title('Generated Time Series Data')
plt.savefig(os.path.join(IMG_DIR, "Monthly Temperature Time Series.png"))
plt.clf()

# Split the data into training and testing sets
train_size = int(len(ts) * 0.8)
train, test = ts[:train_size + 1], ts[train_size:]

# Fit an ARIMA model
order = (15, 0, 15)  # Replace with appropriate order based on your data and analysis
model = ARIMA(train, order=order)
fit_model = model.fit()

# Forecast future values
print("Test Len", len(test))
forecast_steps = len(test)
forecast = fit_model.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=train.index[-2], periods=forecast_steps, freq='M')

# Plot the training data, testing data, and the forecast
plt.figure(figsize=(12, 8))
plt.plot(train, label='Training Data')
plt.plot(test, label='Testing Data')
plt.plot(forecast_index, forecast.predicted_mean, color='red', label='Forecast')
plt.title('ARIMA Model Forecasting')
plt.legend()
plt.savefig(os.path.join(IMG_DIR, "Monthly Temperature Forecasting.png"))
plt.clf()
