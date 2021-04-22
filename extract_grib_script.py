#/Users/caramelo/anaconda3/envs/test_xesmf/bin/python
import xarray as xr
import xesmf as xe
import pandas as pd
import os
import glob
import geopandas as gpd
from distributed import Client
import matplotlib.pyplot as plt
from datetime import datetime

#Heure d'arrivée des modèles régionaux du CMC au 8 avril 2021 (00Z -4):
#Standard time zone:	UTC/GMT -5 hours
#Daylight saving time:	+1 hour
#Current time zone offset:	UTC/GMT -4 hours
#Time zone abbreviation:	EDT
#00z: 20 PM
#06z: 2 AM
#12z: 8 AM
#18z: 14 PM

#Lorsqu'on vérifie les heures d'arrivée du datamart, alors on voit que les prévisions arrivent environ trois heures plus tard que l'heure d'émission donc:

#00z: 11h00 heure locale
#06z: 5h00 heure locale
#12z: 11h00 heure locale
#18z: 17h00 heure locale

#client = Client(n_workers=2, threads_per_worker=2, memory_limit='1GB')
#client #this is optional, it's good to have a dashboard to follow the computations


sysDate = datetime.now()
#CMC_reg_WIND_TGL_10_ps10km_2021042106_P000
os.chdir('/Users/caramelo/Documents/00_HQ/01_Prevision_Demande/scribe_download/gem/RDPS/WIND/')#ce code peut être utilisé dans n'importe quel dossier, le if à la fin peut traiter les variables
grib_list_total=sorted(glob.glob('*06_P*.grib2'))#il faut regarder pour avoir l'heure d'émission en entrée
ds=xr.open_mfdataset(grib_list_total,concat_dim='valid_time',engine='cfgrib',combine='nested',parallel=True)#ai-je besoin de faire les chunk?
#Faire un if pour le vent
# Convert m/s to km/h
si10 = ds.si10*3.6 
# copy attributes to get nice figure labels and change Kelvin to Celsius
si10.attrs = ds.si10.attrs
si10.attrs["units"] = "km/h"#pas pareil que GRIB_units
ds = si10.rename({'latitude': 'lat', 'longitude': 'lon'})
#ds
ds_out = xe.util.grid_global(0.1, 0.1)
#ds_out  # contains lat/lon values of cell centers and boundaries.
regridder = xe.Regridder(ds, ds_out, 'bilinear')
regridder
dr_out = regridder(ds)
dr_out.where(dr_out>0).plot()
dr_out['lat'] = dr_out.lat[:,0].drop('lon')
dr_out['lon'] = dr_out.lon[0,:].drop('lat')
dr_out = dr_out.sortby(['x','y'])
dr_out = dr_out.rename({'x':'longitude',
                        'y':'latitude',
                        'lon':'longitude',
                        'lat':'latitude'})
dr_out = dr_out.where(dr_out>0) # remplacer 0 par nan


coords_stations=pd.read_csv('/Users/caramelo/Documents/GitHub/cmc/Stations matrice scribe.csv')

def calcul_par_station(lat, lon, nomstn, oaci):    
    si101d = dr_out.sel(latitude=lat, longitude=lon,method='nearest')
    df = si101d.reset_coords(drop=True).to_dataframe()
    df=df.rename(columns={"si10": nomstn+'_'+oaci})
    #df = pd.concat(result,axis=1).sort_values('valid_time')
    return df

result = [calcul_par_station(x, y, nomstn, oaci) for x, y, nomstn, oaci in zip(coords_stations['LAT'], coords_stations['LON'],coords_stations['NOMSTN'],coords_stations['OACI'])]
df = pd.concat(result,axis=1).sort_values('valid_time')

df.to_csv(sysDate+'06_.csv')

#to run: 
# chmod +x extract_grib_script.py  
# /Users/caramelo/anaconda3/envs/test_xesmf/bin/python extract_grib_script.py
#