import csv
import pandas as pd
from folium.plugins import HeatMap, HeatMapWithTime
import folium
import numpy as np
from datetime import datetime, timedelta
import os


def normalize_and_replace_columns_in_csv_pandas(input_file, columns):
    """
    Normaliza los datos en varias columnas específicas de un archivo CSV en una escala de 0 a 1 y reemplaza el archivo CSV original con los datos normalizados.

    :param input_file: Ruta al archivo CSV de entrada.
    :param columns: Lista de nombres de columna que se deben normalizar.
    """

    try:
        # Cargamos el archivo CSV en un DataFrame de pandas
        DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"
        df = pd.read_csv(os.path.join(DATA_DIR, input_file))

        for column_name in columns:
            if column_name in df.columns:
                # Normalizamos los datos en la columna
                min_value = df[column_name].min()
                max_value = df[column_name].max()
                df[column_name] = 10 * (df[column_name] - min_value) / (max_value - min_value)

        # Reemplazamos el archivo original con el DataFrame modificado
        df.to_csv(input_file, index=False)

    except FileNotFoundError:
        print(f"El archivo '{input_file}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")




def main():

    file = "per-capita-meat-consumption-by-type-kilograms-per-year.csv"

    columns = ['Meat, Other | 00002735 || Food available for consumption | 0645pc || kilograms per year per capita',
               'Meat, sheep and goat | 00002732 || Food available for consumption | 0645pc || kilograms per year per capita',
               'Meat, beef | 00002731 || Food available for consumption | 0645pc || kilograms per year per capita',
               'Meat, pig | 00002733 || Food available for consumption | 0645pc || kilograms per year per capita',
               'Meat, poultry | 00002734 || Food available for consumption | 0645pc || kilograms per year per capita']

    normalize_and_replace_columns_in_csv_pandas(file, columns)


main()
