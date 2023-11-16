import pandas as pd
import utils
from typing import Optional

def annual_dataframe(from_year: Optional[int] = None, to_year: Optional[int] = None) -> pd.DataFrame:
    # Read the CSV file into a DataFrame
    df = utils.read_csv("per-capita-meat-consumption-by-type-kilograms-per-year.csv")

    # Convert the "Date" column to a datetime format
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')

    # Rename columns and create Total column
    df.columns = list(df.columns[:3]) + ['Otros', 'Oveja y Cabra', 'Res', 'Cerdo', 'Aves de corral']
    df['Total'] = df.iloc[:, 3:].sum(axis=1)

    # Group Total by Year and set Year as index
    annual_total = df[['Year', 'Total']].copy()
    annual_total = annual_total.groupby('Year').sum()

    # Sort the DataFrame by date in ascending order
    annual_total.sort_index(inplace=True)

    # Date filter
    if from_year is not None:
        annual_total = annual_total[annual_total.index >= f"{from_year}-01"]
    if to_year is not None:
        annual_total = annual_total[annual_total.index < f"{to_year}-01"]

    return annual_total


if __name__ == "__main__":
    annual_df = annual_dataframe()
    utils.plot_all(annual_df.index.year, annual_df["Total"], "Año", "Consumo de carne (kg per capita)",
                   "Consumo de carne", "data/Meat consumption")
