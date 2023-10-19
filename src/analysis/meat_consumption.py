import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"
IMG_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../images/meat_data/"

file = "per-capita-meat-consumption-by-type-kilograms-per-year.csv"

coordinates_file = "countries_codes_and_coordinates.csv"

df = pd.read_csv(os.path.join(DATA_DIR, file))

coords = pd.read_csv(os.path.join(DATA_DIR, coordinates_file))
coords = coords[['Alpha-3 code', 'Latitude (average)', 'Longitude (average)']]
coords.rename(columns={'Alpha-3 code': 'Code', 'Latitude (average)': 'Latitude', 'Longitude (average)': 'Longitude'}, inplace=True)
coords.Code = coords.Code.str.replace('"', '')
coords.Code = coords.Code.str.strip()
coords.Latitude = coords.Latitude.str.replace('"', '')
coords.Longitude = coords.Longitude.str.replace('"', '')
coords.Latitude = coords.Latitude.str.strip()
coords.Longitude = coords.Longitude.str.strip()

df.Year = df.Year.astype(int)
# df = df[df.Year > 2010]

df = df.merge(coords, how='left', on='Code')

df = df.loc[~df.Latitude.isna()]
df = df.loc[~df.Longitude.isna()]
df.Latitude = df.Latitude.astype(float)
df.Longitude = df.Longitude.astype(float)

# Kg per Year
meat_data_by_source = list(df.columns)[3:-2]
df.columns = list(df.columns[:3]) + ['Other', 'Sheep and Goat', 'Beef', 'Pig', 'Poultry'] + list(df.columns[-2:])
df = df[list(df.columns[:3]) + list(df.columns[-2:]) + ['Other', 'Sheep and Goat', 'Beef', 'Pig', 'Poultry']]
df['Total'] = df.iloc[:, 5:].sum(axis=1)
annual_total = df[['Year', 'Total']].copy()
annual_per_meat = df[['Year', 'Other', 'Sheep and Goat', 'Beef', 'Pig', 'Poultry']].copy()
annual_total = annual_total.groupby('Year').sum()
annual_per_meat = annual_per_meat.groupby('Year').sum()
sns.lineplot(data=annual_total).set(title='Cantidad de Kg de carne total consumida por año per cápita')
plt.savefig(os.path.join(IMG_DIR, "annual_total.png"))
plt.clf()
sns.lineplot(data=annual_per_meat).set(title='Cantidad de Kg de carne separada por tipo consumida por año per cápita')
plt.savefig(os.path.join(IMG_DIR, "annual_per_meat.png"))
plt.clf()
# annual_total_by_country = df[['Year', 'Entity', 'Total']].copy()
# print(annual_total_by_country.columns)
# annual_total_by_country = annual_total_by_country.groupby(['Year', 'Entity'], as_index=False).sum()
# annual_total_by_country.sort_values('Total', inplace=True, ascending=False)
# total_by_country = annual_total_by_country[['Entity', 'Total']].copy()
# total_by_country = total_by_country.groupby('Entity', as_index=False).sum()
# total_by_country.sort_values('Total', inplace=True, ascending=False)
# total_by_country = list(total_by_country.head(10).Entity)
# annual_total_by_country = annual_total_by_country[annual_total_by_country.Entity.isin(total_by_country)]
# print(annual_total_by_country.head())
# print(annual_total_by_country.pivot(index='Year', columns='Entity', values='Total').head())
# annual_total_by_country = annual_total_by_country.pivot(index='Year', columns='Entity', values='Total')
# sns.lineplot(data=annual_total_by_country).set(title='Cantidad de Kg de carne total separada por país consumida por año per cápita')
# plt.savefig(os.path.join(IMG_DIR, "annual_total_by_country.png"))
# plt.clf()
