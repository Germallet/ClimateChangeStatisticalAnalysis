import energy_use_per_capita
import surface_temperature
import co2_concentrations
import bitcoin
import co2_emissions
import meat


import utils
import numpy as np



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
    utils.dataframe_year_filter(bitcoin, 2010, 2014),
    utils.dataframe_year_filter(temperature_df, 2010, 2014)
)[0][1]
print("Correlation Coeficient Bitcoin VS Temperature")
print(correlation_coeficient)

correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(energy_use,1971,2014),
    utils.dataframe_year_filter(temperature_df,1971,2014)
    )[0][1]
print("Correlation Coeficient Energy Use VS Temperature")
print(correlation_coeficient)


correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(temperature_df, 1961, 2020),
    utils.dataframe_year_filter(meat_df, 1961, 2020)
    )[0][1]
print("Correlation Coeficient Meat VS Temperature")
print(correlation_coeficient)

print("----------------------------------------------------------------")

## the same but with co2_concentrations_df
correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(bitcoin, 2010, 2014),
    utils.dataframe_year_filter(co2_concentrations_df, 2010, 2014)
    )[0][1]
print("Correlation Coeficient Bitcoin VS CO2 Concentrations")
print(correlation_coeficient)

correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(energy_use,1971,2014),
    utils.dataframe_year_filter(co2_concentrations_df,1971,2014)
    )[0][1]
print("Correlation Coeficient Energy Use VS CO2 Concentrations")
print(correlation_coeficient)

correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(meat_df, 1961, 2020),
    utils.dataframe_year_filter(co2_concentrations_df, 1961, 2020)
    )[0][1]
print("Correlation Coeficient Meat  VS CO2 Concentrations")
print(correlation_coeficient)


print("----------------------------------------------------------------")

## now with co2_emissions_df
correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(bitcoin, 2010, 2014),
    utils.dataframe_year_filter(co2_emissions_df, 2010, 2014)
    )[0][1]
print("Correlation Coeficient Bitcoin VS CO2 Emissions")
print(correlation_coeficient)

correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(energy_use,1971,2014),
    utils.dataframe_year_filter(co2_emissions_df,1971,2014)
    )[0][1]
print("Correlation Coeficient Energy Use VS CO2 Emissions")
print(correlation_coeficient)

correlation_coeficient = np.corrcoef(
    utils.dataframe_year_filter(meat_df, 1961, 2020),
    utils.dataframe_year_filter(co2_emissions_df, 1961, 2020)
    )[0][1]
print("Correlation Coeficient Meat VS CO2 Emissions")
print(correlation_coeficient)







