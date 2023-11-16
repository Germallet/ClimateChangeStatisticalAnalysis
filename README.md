# ClimateChangeStatisticalAnalysis

## Requerimientos

-   Python 3.10.x <

## Setup del ambiente

1. Pararse en el root del repositorio
2. Ejecutar _python -m virtualenv .venv_
3. Ir a la carpeta Scripts en el .venv
4. Ejecutar activate.bat
5. Volver al root
6. Ejecutar _pip install -r requirements.txt_

Para simplificar los pasos se puede ejecutar _setup.bat_

## Fuentes

1. Annual_Surface_Temperature_Change: https://climatedata.imf.org/pages/climatechange-data

2. Monthly_Global_Surface_Temperature_Change: https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series

3. Atmospheric_CO₂_Concentrations: https://climatedata.imf.org/pages/climatechange-data

4. energy-use-kg-of-oil-per-capita: https://data.worldbank.org/indicator/EG.USE.PCAP.KG.OE?end=2015&start=2015&type=shaded&view=map&year=1967

5. per-capita-meat-consumption-by-type-kilograms-per-year: https://ourworldindata.org/grapher/per-capita-meat-consumption-by-type-kilograms-per-year

6. co2-emissions-by-fuel-line.csv: https://ourworldindata.org/grapher/co2-emissions-by-fuel-line

7. Dataset on bitcoin carbon footprint and energy consumption: https://www.sciencedirect.com/science/article/pii/S2352340922004541

## Analisis

En base a la fuente 6. podemos calcular las emisiones de _gas_, _carbon_, _petroleo_ y _CO2_. Hay un ejemplo hecho con el petroleo.

**TODO** replicar con el resto

Con esta misma fuente se puede armar una linea de tiempo, capaz solo de aquellos paises con mas datos. Los 3 que mas emiten. Con el resto o algunos usar un box and whiskers plot.
