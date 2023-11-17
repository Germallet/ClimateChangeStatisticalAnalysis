import pandas as pd
import utils
import seaborn as sns
import matplotlib.pyplot as plt
import os
from typing import Optional


def dataframe() -> pd.DataFrame:
    # Read the CSV file into a DataFrame
    dataframe = utils.read_csv("energy-use-kg-of-oil-per-capita.csv")

    # Filter rows where some columns have non-null values
    dataframe = dataframe.dropna(subset=dataframe.columns[4:-1], how="all")

    # Extract years and convert them to datetime
    years = pd.to_datetime(dataframe.columns[4:-1], format="%Y")

    # Create a list of DataFrames for each country"s energy data
    country_data_frames = [
        pd.DataFrame({
            "Date": years,
            "Region": country_name,
            "Value": values.astype(float)
        }).set_index("Date")
        # Combine the "Country Name" column with values from columns 4 to second-to-last column
        for country_name, values in zip(dataframe["Country Name"], dataframe.iloc[:, 4:-1].values)
    ]

    # Concatenate the list of DataFrames into a single DataFrame
    combined_energy_data = pd.concat(country_data_frames)

    # Filter rows where Value is not-null
    combined_energy_data = combined_energy_data[pd.notna(combined_energy_data["Value"])]

    return combined_energy_data


def region_dataframe(region: str, from_year: Optional[int] = None, to_year: Optional[int] = None) -> pd.DataFrame:
    df = dataframe()
    df = df.loc[df["Region"] == region]

    # Date filter
    if from_year is not None:
        df = df[df.index >= f"{from_year}-01"]
    if to_year is not None:
        df = df[df.index < f"{to_year}-01"]

    return df


if __name__ == "__main__":
    # Iterate through each region in the DataFrame
    # for region, row in region_dataframe("World", 1961, 2022).groupby("Region"):
    #     utils.plot_all(row.index, row["Value"], "Year", "Energy use (kg of oil equivalent per capita)",
    #                    f"Energy use per capita in {region}", f"Energy use per capita in {region}")
    df = region_dataframe("World", 1961, 2022)
    utils.plot_all(df.index.year, df["Value"], "Año", "Uso de energía (equivalente de kg de petróleo per cápita)",
        f"Uso de energía per cápita", f"data/Energy use")
