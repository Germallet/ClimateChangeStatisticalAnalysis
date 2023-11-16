import pandas as pd
import utils
from typing import Optional


def dataframe(region: str, value: str = "Total", from_year: Optional[int] = None, to_year: Optional[int] = None) -> pd.DataFrame:
    # Read the CSV file into a DataFrame
    df = utils.read_csv("co2-emissions-by-fuel-line.csv")

    # Read year columns, convert to datetime and rename it
    df["Year"] = pd.to_datetime(df["Year"], format="%Y")
    
    # Calculate Total
    df["Total"] = df["Annual CO₂ emissions from oil"] + df["Annual CO₂ emissions from coal"] + df["Annual CO₂ emissions from cement"] + df["Annual CO₂ emissions from gas"] + df["Annual CO₂ emissions from flaring"] + df["Annual CO₂ emissions from other industry"]
    df["Total"] = df["Total"]/1000000

    # Rename columns and read value as float
    df.rename(columns={"Year": "Date", value: "Value"}, inplace=True)
    df["Value"] = df["Value"].astype(float)

    # Filter region and drop null values
    df = df.loc[(df["Entity"] == region) & (df["Value"] > 0)]

    # Create a time series DataFrame
    df.set_index("Date", inplace=True)

    # Date filter
    if from_year is not None:
        df = df[df.index >= f"{from_year}-01"]
    if to_year is not None:
        df = df[df.index < f"{to_year}-01"]

    return df


if __name__ == "__main__":
    df = dataframe("World")
    utils.plot_all(df.index.year, df["Value"], "Año", "Millones de toneladas",
                   "Emisiones de CO2", "data/CO₂ emissions")
