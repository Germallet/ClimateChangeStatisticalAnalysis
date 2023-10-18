import pandas as pd
import utils

# Read the CSV file into a DataFrame
temp_df = utils.read_csv("Annual_Surface_Temperature_Change.csv")

# Read year columns
temp_years = pd.to_datetime(temp_df.columns[10:-1], format='F%Y')

# Get world row and extract values from year columns
temp_values = temp_df.loc[temp_df["Country"] == "World"].iloc[0][10:-1]

# Generate timeserie Dataframe
df = pd.DataFrame({"Date": temp_years, "Value": temp_values})
df.set_index('Date', inplace=True)

if __name__ == '__main__':
    utils.plot_all(df.index, df["Value"], "Date", "Degree Celsius", "Annual Surface Temperature Change", "Annual Surface Temperature Change")
