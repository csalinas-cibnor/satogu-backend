# actualizador.py

import os
import requests
import xarray as xr
import pandas as pd
from datetime import datetime, timedelta

# Paso 1: Fecha más reciente disponible
hoy = datetime.utcnow()
ayer = hoy - timedelta(days=1)
fecha = ayer.strftime("%Y%m%d")

# Paso 2: URL del archivo MODIS Aqua L3 SST (resolución 4 km, diario)
url = f"https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A{fecha}.L3m_DAY_SST_sst_4km.nc"

archivo_local = f"sst_{fecha}.nc"

# Paso 3: Descargar el archivo
print(f"Descargando archivo MODIS Aqua: {url}")
r = requests.get(url)
if r.status_code == 200:
    with open(archivo_local, "wb") as f:
        f.write(r.content)
    print(f"Archivo descargado: {archivo_local}")
else:
    raise Exception(f"No se pudo descargar el archivo MODIS: {url}")

# Paso 4: Abrir y procesar el archivo NetCDF
print("Procesando el archivo NetCDF...")
ds = xr.open_dataset(archivo_local)
sst = ds['sst']
lat = ds['lat']
lon = ds['lon']

# Paso 5: Convertir a DataFrame
tsm_min = 10
tsm_max = 35
datos = []
for i in range(len(lat)):
    for j in range(len(lon)):
        tsm = float(sst[0, i, j])
        if tsm_min <= tsm < 18.0:  # el umbral puede cambiarse dinámicamente
            datos.append({'lat': float(lat[i]), 'lon': float(lon[j]), 'tsm_media': tsm})

df = pd.DataFrame(datos)

# Paso 6: Guardar CSV
csv_path = "datos_cuadrantes_frios.csv"
df.to_csv(csv_path, index=False)
print(f"Archivo CSV actualizado: {csv_path}")
