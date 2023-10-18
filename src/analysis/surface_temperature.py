import pandas as pd
import utils
from typing import Optional


def dataframe(region: str) -> pd.DataFrame:
    # Read the CSV file into a DataFrame
    df = utils.read_csv("Annual_Surface_Temperature_Change.csv")

    # Read year columns and convert to datetime
    temp_years = pd.to_datetime(df.columns[10:-1], format="F%Y")

    # Extract values from the world row and cast to float
    temp_values = df.loc[df["Country"] == region].iloc[0][10:-1].astype(float)

    # Create a time series DataFrame
    df = pd.DataFrame({"Date": temp_years, "Value": temp_values})
    df.set_index("Date", inplace=True)

    return df


if __name__ == "__main__":
    df = dataframe("World")
    utils.plot_all(df.index, df["Value"], "Date", "Degree Celsius",
                   "Surface Temperature Change", "Surface Temperature Change")
