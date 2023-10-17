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
    total_emissions = df.groupby(by=['Latitude', 'Longitude'])[source].sum().reset_index()

    # Convert emission values to a scale suitable for the heatmap
    max_emission = total_emissions[source].max()
    total_emissions['ScaledEmission'] = total_emissions[source] / max_emission

    map = folium.Map(location=[0, 0], zoom_start=2)

    heat_data = total_emissions[['Latitude', 'Longitude', 'ScaledEmission']].values.tolist()

    heat_map = HeatMap(heat_data,
                       min_opacity=0.2,
                       radius=15, blur=5,
                       max_zoom=1)

    heat_map.add_to(map)

    # Display the map
    map.save(os.path.join(HM_DIR, f'{source}.html'))

