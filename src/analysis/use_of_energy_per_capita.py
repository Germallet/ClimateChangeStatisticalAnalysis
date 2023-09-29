import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"
IMG_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../images/"

file = "energy-use-kg-of-oil-per-capita.csv"

# Replace 'your_data.csv' with the path to your CSV file
df = pd.read_csv(os.path.join(DATA_DIR, file))


# Data Cleaning
# Check for missing values
missing_values = df.isnull().sum()

# Extract columns containing data for years
years = df.columns[4:-1]

# Iterate through each country in the DataFrame
for index, row in df.iterrows():
    country_name = row['Country Name']
    
    # Extract energy use data for the current country
    energy_use_data = row[4:-1].astype(float)

    # If all values are missing, skip the current country
    if missing_values.sum() == len(energy_use_data):
        print(f'Skipping {country_name} because all values are missing')
        continue
    
    # Create a line plot for the current country
    plt.figure(figsize=(12, 6))
    plt.plot(years, energy_use_data, marker='o', linestyle='-')
    plt.xlabel('Year')
    plt.xticks(rotation=45)
    plt.ylabel('Energy use (kg of oil equivalent per capita)')
    title = f'Energy Use Per Capita in {country_name} Over Time'
    plt.title(title)
    plt.savefig(os.path.join(IMG_DIR, title))
    plt.close()