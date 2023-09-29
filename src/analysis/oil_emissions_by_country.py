import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"

file = "co2-emissions-by-fuel-line.csv"


df = pd.read_csv(os.path.join(DATA_DIR, file))

# Group the data by 'Entity' (country) and sum the 'Annual CO₂ emissions from oil' column
total_oil_emission = df.groupby('Entity')['Annual CO₂ emissions from oil'].sum().reset_index()

# Rename the columns for clarity
total_oil_emission.columns = ['Entity', 'Total Oil Emission']

# Remove countries in the 10th percentile

total_oil_emission = total_oil_emission[total_oil_emission['Total Oil Emission'] >= 10_000_000_000]


# Print a plot in matplotlib

fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(x='Entity', y='Total Oil Emission', data=total_oil_emission, ax=ax)

ax.set(xlabel='Country', ylabel='Annual CO₂ emissions from oil', title='Annual CO₂ emissions from oil by country')
plt.xticks(rotation=80)
plt.tight_layout()
plt.show()