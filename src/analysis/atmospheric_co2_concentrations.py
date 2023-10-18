import pandas as pd
import utils

# Read the CSV file into a DataFrame
df = utils.read_csv("Atmospheric_CO₂_Concentrations.csv")

# Convert the 'Date' column to a datetime format and set it as the index
df['Date'] = pd.to_datetime(df['Date'], format='%YM%m')
df.set_index('Date', inplace=True)

# Get world rows
monthly_df = df.loc[(df["Country"] == "World") & (df["Unit"] == "Parts Per Million")]

# Resample the data to get annual averages
annual_df = monthly_df.resample('Y').mean(numeric_only=True)

def annual_range_df(from_year, to_year):
    return annual_df.loc[(annual_df.index > f'{from_year}-01') & (annual_df.index < f'{to_year}-01')]

if __name__ == '__main__':
    utils.plot_all(monthly_df.index, monthly_df["Value"], "Date", "CO₂ Parts Per Million", "Monthly World Atmospheric CO₂ Concentrations", "Monthly World CO2 Concentrations")
    utils.plot_all(annual_df.index, annual_df["Value"], "Date", "CO₂ Parts Per Million", "Annual World Atmospheric CO₂ Concentrations", "Annual World CO2 Concentrations")
