import pandas as pd
import utils
from typing import Optional


# Data from 1850 to 2023
def dataframe(from_year: Optional[int] = None, to_year: Optional[int] = None) -> pd.DataFrame:
    # Read the CSV file into a DataFrame
    df = utils.read_csv("Monthly_Global_Surface_Temperature_Change.csv")

    # Read year columns and convert to datetime
    years = pd.to_datetime(df["Year"], format="%Y%m")

    # Extract values and cast to float
    values = df["Anomaly"].astype(float)

    # Create a time series DataFrame
    df = pd.DataFrame({"Date": years, "Value": values})
    df.set_index("Date", inplace=True)

    # Date filter
    if from_year is not None:
        df = df[df.index.year >= from_year]
    if to_year is not None:
        df = df[df.index.year <= to_year]

    return df


# Data from 1961 to 2022
def annual_dataframe(region: str, from_year: Optional[int] = None, to_year: Optional[int] = None) -> pd.DataFrame:
    # Read the CSV file into a DataFrame
    df = utils.read_csv("Annual_Surface_Temperature_Change.csv")

    # Read year columns and convert to datetime
    years = pd.to_datetime(df.columns[10:-1], format="F%Y")

    # Extract values from the region row and cast to float
    values = df.loc[df["Country"] == region].iloc[0][10:-1].astype(float)

    # Create a time series DataFrame
    df = pd.DataFrame({"Date": years, "Value": values})
    df.set_index("Date", inplace=True)

    # Date filter
    df = df.resample("Y").mean(numeric_only=True)
    if from_year is not None:
        df = df[df.index.year >= from_year]
    if to_year is not None:
        df = df[df.index.year < to_year]

    return df


if __name__ == "__main__":
    df = dataframe()
    # Annual Moving Average
    df = df.resample("Y").mean(numeric_only=True)
    # Plot
    utils.plot_all(df.index.year, df["Value"], "Fecha", "Variación de temperatura (Cº)", "Variación de temperatura mundial", "Surface Temperature Change", df.size / 12)
