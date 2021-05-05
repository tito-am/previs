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




def lecture_grib(grib_list_total,var_meteo):
    ds=xr.open_mfdataset(grib_list_total,concat_dim='valid_time',engine='cfgrib',combine='nested',parallel=True,chunks={"x": -1, "y":-1})#ai-je besoin de faire les chunk?
    #Faire un if pour le vent
    # Convert m/s to km/h
    if var_meteo=='WIND':
        si10 = ds.si10*3.6 
        # copy attributes to get nice figure labels
        si10.attrs = ds.si10.attrs
        si10.attrs["units"] = "km/h"#pas pareil que GRIB_units
        ds = si10.rename({'latitude': 'lat', 'longitude': 'lon'})
    elif var_meteo=='TMP':
        # Convert to celsius
        t2m=ds.t2m-273.15 #passage en celsius
        # copy attributes to get nice figure labels and change Kelvin to Celsius
        t2m.attrs = ds.t2m.attrs
        t2m.attrs["units"] = "deg C"
        ds = t2m.rename({'latitude': 'lat', 'longitude': 'lon'})
    elif var_meteo=='WDIR':
        wdir10=ds.wdir10
        ds = wdir10.rename({'latitude': 'lat', 'longitude': 'lon'})
 
                
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
    return dr_out
    

def calcul_par_station(lat, lon, nomstn, oaci):    
    varmeteo1d = dr_out.sel(latitude=lat, longitude=lon,method='nearest')
    df = varmeteo1d.reset_coords(drop=True).to_dataframe()
    df['nom_station'] = nomstn
    df['station'] = oaci
    return df

def menage_grib():
    for f in grib_list_total_tmp_12:
        os.remove(f)#il ne reste que les idx après
        
    for f in glob.glob("*.idx"):
        os.remove(f)



sysDate = datetime.now()
curSysDate = (str(sysDate))
dateStr = sysDate.strftime("%Y%m%d")

#CMC_reg_WIND_TGL_10_ps10km_2021042106_P000
os.chdir('/Users/caramelo/Documents/00_HQ/01_Prevision_Demande/scribe_download/gem/RDPS/GRIBS/')#ce code peut être utilisé dans n'importe quel dossier, le if à la fin peut traiter les variables

grib_list_total_wind_12=sorted(glob.glob('*_WIND_*12_P*.grib2'))#il faut regarder pour avoir l'heure d'émission
print(grib_list_total_wind_12)
grib_list_total_tmp_12=sorted(glob.glob('*_TMP_*12_P*.grib2'))#il faut regarder pour avoir l'heure d'émission
print(grib_list_total_tmp_12)
grib_list_total_wdir_12=sorted(glob.glob('*_WDIR_*12_P*.grib2'))#il faut regarder pour avoir l'heure d'émission
print(grib_list_total_wdir_12)

coords_stations=pd.read_csv('/Users/caramelo/Documents/GitHub/cmc/Stations matrice scribe.csv')

#bloc pour voir si les fichiers sont présents

if grib_list_total_wind_12:
    #WIND
    dr_out=lecture_grib(grib_list_total_wind_12,'WIND')
    result = [calcul_par_station(x, y, nomstn, oaci) for x, y, nomstn, oaci in zip(coords_stations['LAT'], coords_stations['LON'],coords_stations['NOMSTN'],coords_stations['OACI'])]
    df_wind = pd.concat(result,axis=0).sort_values('valid_time').reset_index()

if grib_list_total_tmp_12:
    #TMP
    dr_out=lecture_grib(grib_list_total_tmp_12,'TMP')
    result = [calcul_par_station(x, y, nomstn, oaci) for x, y, nomstn, oaci in zip(coords_stations['LAT'], coords_stations['LON'],coords_stations['NOMSTN'],coords_stations['OACI'])]
    df_tmp = pd.concat(result,axis=0).sort_values('valid_time').reset_index()

if grib_list_total_wdir_12:
    #WDIR
    print(grib_list_total_wdir_12)
    dr_out=lecture_grib(grib_list_total_wdir_12,'WDIR')
    result = [calcul_par_station(x, y, nomstn, oaci) for x, y, nomstn, oaci in zip(coords_stations['LAT'], coords_stations['LON'],coords_stations['NOMSTN'],coords_stations['OACI'])]
    df_wdir = pd.concat(result,axis=0).sort_values('valid_time').reset_index()

#Concatenation de toutes les previsions 
df_final = pd.merge(df_wind, df_wdir, on=['valid_time','station'])

df_final.to_csv(dateStr+'_wdir_tmp_12.csv')#mettre variable

#Menage

def menage_grib():
    for f in grib_list_total_tmp_12:
        os.remove(f)#il ne reste que les idx après
        
    for f in glob.glob("*.idx"):
        os.remove(f)


#to run: 
# chmod +x extract_grib_script.py  
# /Users/caramelo/anaconda3/envs/test_xesmf/bin/python extract_grib_script.py
#grib download
