import pandas as pd
import utils
from typing import Optional


def monthly_dataframe(region: str) -> pd.DataFrame:
    # Read the CSV file into a DataFrame
    df = utils.read_csv("Atmospheric_CO₂_Concentrations.csv")

    # Convert the "Date" column to a datetime format and set it as the index
    df["Date"] = pd.to_datetime(df["Date"], format="%YM%m")
    df.set_index("Date", inplace=True)

    # Filter for the specified region and unit
    df = df.loc[(df["Country"] == region) & (df["Unit"] == "Parts Per Million")]

    # Cast "Value" to float
    df["Value"] = df["Value"].astype(float)

    return df


def annual_dataframe(region: str, from_year: Optional[int] = None, to_year: Optional[int] = None) -> pd.DataFrame:
    monthly_df = monthly_dataframe(region)
    annual_df = monthly_df.resample("Y").mean(numeric_only=True)

    # Date filter
    if from_year is not None:
        annual_df = annual_df[annual_df.index >= f"{from_year}-01"]
    if to_year is not None:
        annual_df = annual_df[annual_df.index < f"{to_year}-01"]

    return annual_df


if __name__ == "__main__":
    monthly_df = monthly_dataframe("World")
    annual_df = annual_dataframe("World")

    utils.plot_all(monthly_df.index, monthly_df["Value"], "Date", "CO₂ ppm",
                   "Monthly World CO₂ Concentrations", "Monthly World CO2 Concentrations")
    utils.plot_all(annual_df.index, annual_df["Value"], "Date", "CO₂ ppm",
                   "Annual World CO₂ Concentrations", "Annual World CO2 Concentrations")
