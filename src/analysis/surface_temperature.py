import pandas as pd
import utils
from typing import Optional


def dataframe(region: str, from_year: Optional[int] = None, to_year: Optional[int] = None) -> pd.DataFrame:
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
    if from_year is not None:
        df = df[df.index >= f"{from_year}-01"]
    if to_year is not None:
        df = df[df.index < f"{to_year}-01"]

    return df


if __name__ == "__main__":
    df = dataframe("World")
    utils.plot_all(df.index, df["Value"], "Date", "Degree Celsius",
                   "Surface Temperature Change", "Surface Temperature Change")
