import pandas as pd
from folium.plugins import HeatMap, HeatMapWithTime
import folium
import numpy as np
from datetime import datetime, timedelta
import os

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"
HM_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../heatmaps/"

file = "co2-emissions-by-fuel-line.csv"

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
df = df[df.Year > 2010]

df = df.merge(coords, how='left', on='Code')

df = df.loc[~df.Latitude.isna()]
df = df.loc[~df.Longitude.isna()]
df.Latitude = df.Latitude.astype(float)
df.Longitude = df.Longitude.astype(float)

co2_data_by_source = list(df.columns)[3:-2]

for source in co2_data_by_source:
    total_oil_emission = df[['Entity', 'Year', 'Latitude', 'Longitude', source]]\
        .groupby(by=['Entity', 'Year', 'Latitude', 'Longitude'], as_index=False)[source].sum()
        
    total_oil_emission = total_oil_emission[total_oil_emission[source] > 0]

    total_oil_emission['Year'] = pd.to_datetime(total_oil_emission['Year'], format='%Y')
    total_oil_emission['Year'] = pd.DatetimeIndex(total_oil_emission['Year']).year

    print(total_oil_emission.head(1))

    # Sort the DataFrame by year
    total_oil_emission.sort_values(by='Year', inplace=True)

    # total_oil_emission.columns = ['Entity', source]

    map = folium.Map(location=[0, 0], zoom_start=2) 
    heat_data = []

    # Iterate through the DataFrame and add data to the list
    # total_oil_emission[source] = 1
    years = list(total_oil_emission['Year'].unique())

    for year in years:
        data = []
        aux = total_oil_emission[total_oil_emission['Year'] == year].copy()
        for index, row in aux.iterrows():
            data.append([row['Latitude'], row['Longitude'], row[source]])
        heat_data.append(data)

    print(len(heat_data))
    print(len(years))

    heat_map = HeatMapWithTime(
        heat_data,
        index=years,
        radius=15,
        auto_play=False,
        max_opacity=0.7,
        scale_radius=True,
        use_local_extrema=True,
        overlay=True,
    ).add_to(map)

    # Display the map
    map.save(os.path.join(HM_DIR, f'{source}.html'))

