from previs.download.grib_download import cmc_download
from previs.transform.extract_grib import lecture_grib
import requests
import urllib.request
from urllib.error import HTTPError
import time
from bs4 import BeautifulSoup
import os
import glob
import pandas as pd
#import multiprocessing
from dask.distributed import Client, LocalCluster 
import multiprocessing.popen_spawn_posix
import matplotlib.pyplot as plt
import datetime
import multiprocessing
import xarray as xr
#import xesmf as xe
import time
start_time = time.time()


def calcul_par_station(dr_out,lat, lon, nomstn, oaci):    
    

    varmeteo1d = dr_out.sel(latitude=lat, longitude=lon,method='nearest')
    df = varmeteo1d.reset_coords(drop=True).to_dataframe()
    df['nom_station'] = nomstn
    df['station'] = oaci
    return df


if __name__ == '__main__':



    today = datetime.date.today()
    print("Today's date:", today)
    #selon le format des fichiers grib
    d1 = today.strftime("%Y%m%d")
    print("d1 =", d1)
    date_time_obj = datetime.datetime.strptime(d1, '%Y%m%d')
    #print(date_time_obj.weekday())
    date=date_time_obj.strftime('%A')
    print(date)

    #creation d'un folder pour tenir les grib

    parent_dir='/Users/caramelo/Documents/00_HQ/01_Prevision_Demande/scribe_download/gem/RDPS/GRIBS/'
    os.chdir(parent_dir)
    try:
        os.mkdir(d1)
    except OSError as error:
        print(error)
    os.chdir(d1)
    #fonction de téléchargement

    #cmc_download(date,d1,emission='00',variable_level='WIND_TGL_10',parent_dir=parent_dir)
    #cmc_download(date,d1,emission='00',variable_level='TMP_TGL_2',parent_dir=parent_dir)
    #cmc_download(date,d1,emission='00',variable_level='WDIR_TGL_10',parent_dir=parent_dir)
    #cmc_download(date,d1,emission='00',variable_level='APCP_SFC_0',parent_dir=parent_dir)
    #cmc_download(date,d1,emission='00',variable_level='TCDC_SFC_0',parent_dir=parent_dir)
    #cmc_download(date,d1,emission='00',variable_level='DPT_TGL_2',parent_dir=parent_dir)#dewpoint temperature

    #####################################
    #Traitement des données téléchargées#
    #####################################

    #pour dates spécifiques
    #d1='20210509'

    folder = '/Users/caramelo/Documents/00_HQ/01_Prevision_Demande/scribe_download/gem/RDPS/GRIBS/'+d1
    #client = Client(n_workers=3,timeout="150s")
    
    
    #cluster = LocalCluster(
    #n_workers=3,
    #processes=True,
    #threads_per_worker=3
    #)
    
    #client=Client(cluster)
    
    coords_stations=pd.read_csv('/Users/caramelo/Documents/GitHub/cmc/Stations matrice scribe.csv')
    lats = xr.DataArray(data=coords_stations.LAT,
                    dims='station',
                   coords=dict(station=coords_stations.NOMSTN)) #'z' is an arbitrary name placeholder


    lons = xr.DataArray(data=coords_stations.LON,
                    dims='station',
                   coords=dict(station=coords_stations.NOMSTN)) #'z' is an arbitrary name placeholder



    
    for filename in os.listdir(folder):
        #print(filename)
        infilename = os.path.join(folder, filename)
        print(infilename)
        x=glob.glob(infilename+"/*/")
        list_stations_meteo=[]

        for path in x:
            print(path)
            os.chdir(infilename+path.split(infilename)[1])
            var=path.split('/')[-2]
            #client = Client(n_workers=int(multiprocessing.cpu_count()))
            
            
            
            #client = Client(n_workers=3)
            cluster = LocalCluster(
            n_workers=3,
            processes=True,
            threads_per_worker=3
            )
            client=Client(cluster)
            print(os.getcwd())
            ds=xr.open_mfdataset(glob.glob(os.getcwd()+'/*'+var+'*.grib2'),concat_dim='valid_time',engine='cfgrib',combine='nested',parallel=True,chunks={"x": -1, "y":-1},coords='minimal',compat='override')#ai-je besoin de faire les chunk?

            dr_out=lecture_grib(ds,var)
            print('jai fini dr_out!')
            
            data = dr_out.sel(latitude = lats, longitude = lons, method = 'nearest')
            print('j''ai fini le nearest')
            
            client.close()
            data.to_dataframe().to_csv('il roule externe du client.csv')
            #df=data.reset_coords(drop=True).to_dataframe()
            #df=data.load()
            #df.to_dataframe().to_csv('il roule lorsquon loade le ds.csv')
            
            #result = [calcul_par_station(dr_out,x, y, nomstn, oaci) for x, y, nomstn, oaci in zip(coords_stations['LAT'], coords_stations['LON'],coords_stations['NOMSTN'],coords_stations['OACI'])] 
            #df = pd.concat(df,axis=0).sort_values('valid_time').reset_index().to_csv(var+'.csv')
            
            #client.submit(data.to_dataframe().to_csv(var+'.csv'))
            
            #data.to_dataframe().to_csv(var+'.csv')
            
            #print(type(df))
            #list_stations_meteo.append(df)
            
  
    print("--- %s seconds ---" % (time.time() - start_time))
 

    #data.to_dataframe().to_csv('il roule externe du client.csv')
    #df_final = pd.concat(list_stations_meteo)
    #df_final.to_csv('final.csv')
    