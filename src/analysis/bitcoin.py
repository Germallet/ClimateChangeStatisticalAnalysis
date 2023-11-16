import pandas as pd
import utils
from typing import Optional


def dataframe() -> pd.DataFrame:
    # Read the CSV file into a DataFrame
    df = utils.read_csv("BTC_Footprints_v1.csv")

    # Convert the "Date" column to a datetime format and set it as the index
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df.set_index("Date", inplace=True)

    # Sort the DataFrame by date in ascending order
    df.sort_index(inplace=True)

    return df


def monthly_dataframe(from_year: Optional[int] = None, to_year: Optional[int] = None) -> pd.DataFrame:
    base_df = dataframe()
    annual_df = base_df.resample("M").mean(numeric_only=True)

    # Date filter
    if from_year is not None:
        annual_df = annual_df[annual_df.index >= f"{from_year}-01"]
    if to_year is not None:
        annual_df = annual_df[annual_df.index < f"{to_year}-01"]

    return annual_df


def annual_dataframe(from_year: Optional[int] = None, to_year: Optional[int] = None) -> pd.DataFrame:
    monthly_df = monthly_dataframe()
    annual_df = monthly_df.resample("Y").mean(numeric_only=True)

    # Date filter
    if from_year is not None:
        annual_df = annual_df[annual_df.index >= f"{from_year}-01"]
    if to_year is not None:
        annual_df = annual_df[annual_df.index < f"{to_year}-01"]

    return annual_df


if __name__ == "__main__":
    # df = dataframe()
    # utils.plot_all(df.index, df["BTCENEMAX"], "Date", "Electricity consumption (kWh)",
    #                "Bitcoin electricity consumption", "Bitcoin electricity consumption")
    # monthly_df = monthly_dataframe()
    # utils.plot_all(monthly_df.index, monthly_df["BTCENEMAX"], "Date", "Month Electricity consumption (kWh)",
    #                "Monthly Bitcoin electricity consumption", "Monthly Bitcoin electricity consumption")
    annual_df = annual_dataframe()
    utils.plot_all(annual_df.index.year, annual_df["BTCENEGUE"]/1000000, "Año", "Consumo eléctrico (Millones de kWh)",
                   "Consumo eléctrico de Bitcoin", "data/Bitcoin electricity consumption")
    # utils.plot_all(annual_df.index.year, annual_df["BTCEMI_GUE"]/1000000, "Año", "Emisiones de CO₂ (Millones de kgCO₂)",
    #                "Emisiones de CO₂ de Bitcoin", "data/Bitcoin CO₂ emissions")
