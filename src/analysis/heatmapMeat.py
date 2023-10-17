import pandas as pd
import folium
from folium.plugins import HeatMap
import os

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"
HM_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../heatmaps/Meat/"

# Nombre del archivo CSV con los datos de consumo per cápita de carne
file = "per-capita-meat-consumption-by-type-kilograms-per-year.csv"

# Nombre del archivo CSV con las coordenadas geográficas
coordinates_file = "countries_codes_and_coordinates.csv"

# Carga los datos de consumo per cápita de carne y las coordenadas geográficas
df = pd.read_csv(os.path.join(DATA_DIR, file))

coords = pd.read_csv(os.path.join(DATA_DIR, coordinates_file))
coords = coords[['Alpha-3 code', 'Latitude (average)', 'Longitude (average)']]
coords.rename(columns={'Alpha-3 code': 'Code', 'Latitude (average)': 'Latitude', 'Longitude (average)': 'Longitude'},
              inplace=True)
coords.Code = coords.Code.str.replace('"', '')
coords.Code = coords.Code.str.strip()
coords.Latitude = coords.Latitude.str.replace('"', '')
coords.Longitude = coords.Longitude.str.replace('"', '')
coords.Latitude = coords.Latitude.str.strip()
coords.Longitude = coords.Longitude.str.strip()

# Filtra y procesa los datos
df.Year = df.Year.astype(int)
df = df[df.Year > 2010]

df = df.merge(coords, how='left', on='Code')

df = df.loc[~df.Latitude.isna()]
df = df.loc[~df.Longitude.isna()]
df.Latitude = df.Latitude.astype(float)
df.Longitude = df.Longitude.astype(float)

# Obtiene las columnas de consumo de carne por fuente
meat_data_by_source = df.columns[3:-2]

# Genera mapas de calor para cada fuente de carne
for source in meat_data_by_source:
    total_consumption = df.groupby(by=['Latitude', 'Longitude'])[source].sum().reset_index()

    # Convierte los valores de consumo de carne a una escala adecuada para el mapa de calor
    max_consumption = total_consumption[source].max()
    total_consumption['ScaledConsumption'] = total_consumption[source] / max_consumption

    # Crea el mapa y el mapa de calor
    map = folium.Map(location=[0, 0], zoom_start=2)
    heat_data = total_consumption[['Latitude', 'Longitude', 'ScaledConsumption']].values.tolist()
    heat_map = HeatMap(heat_data,
                       min_opacity=0.2,
                       radius=15, blur=5,
                       max_zoom=1)

    heat_map.add_to(map)

    source_name = source.replace("|", "_")

    # Guarda el mapa de calor
    map.save(os.path.join(HM_DIR, f'{source_name}.html'))
