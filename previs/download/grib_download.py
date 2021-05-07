#grib download

import requests
import urllib.request
from urllib.error import HTTPError
import time
from bs4 import BeautifulSoup
import os
from datetime import date
import datetime
import socket

timeout = 20
socket.setdefaulttimeout(timeout)

def cmc_download(date,d1,parent_dir,modele='regional',emission='12',variable_level='WIND_TGL_10'):
    #URL = 'https://dd.weather.gc.ca/ensemble/geps/grib2/raw/00/'
    #emission = '12'#00/
    URL = 'https://dd.weather.gc.ca/model_gem_'+modele+'/10km/grib2/'+emission+'/'
    #page = requests.get(URL)
    #soup = BeautifulSoup(page.content, 'html.parser')
    timeout = 20
    socket.setdefaulttimeout(timeout) 
    
    os.chdir(parent_dir+d1)

    try:
        os.mkdir(emission)
    except OSError as error:
        print(error)
    os.chdir(emission)
    
    try:
        os.mkdir(variable_level)
    except OSError as error:
        print(error)
    os.chdir(variable_level)   
    
    
    if date==4:
        for url_b in range(0, 85, 1):
            if url_b < 10:
                url_a='/CMC_reg_'+variable_level+'_ps10km_'+d1+emission+'_P00'
                url_c='.grib2'
                #print(URL+'00'+str(url_b)+url_a+str(url_b)+url_c)
                try:
                    download_url=URL+'00'+str(url_b)+url_a+str(url_b)+url_c
                    urllib.request.urlretrieve(download_url,filename=d1+'_'+emission+str(url_b)+'.grib2')

                except HTTPError as error:
                    print(error)

            elif ((url_b>= 10) and (url_b< 100)):
                url_a='/CMC_reg_'+variable_level+'_ps10km_'+d1+emission+'_P0'
                url_c='.grib2'
                try:
                    download_url=URL+'0'+str(url_b)+url_a+str(url_b)+url_c
                    print(download_url)
                except OSError as error:
                    print(error)
                urllib.request.urlretrieve(download_url,filename='test_reg_wind'+emission+d1+str(url_b)+'.grib2')
            else:
                url_a='/CMC_geps-raw_'+variable_level+'_latlon0p5x0p5_'+d1+emission+'_P'#TMP_TGL_2m
                url_c='_allmbrs.grib2'
                download_url=URL+str(url_b)+url_a+str(url_b)+url_c
                print(download_url)
                urllib.request.urlretrieve(download_url,filename='test_reg'+emission+d1+str(url_b)+'.grib2')
    else:
        for url_b in range(0, 85, 1):
            if url_b < 10:
                url_a='/CMC_reg_'+variable_level+'_ps10km_'+d1+emission+'_P00'
                url_c='.grib2'
                try:
                    download_url=URL+'00'+str(url_b)+url_a+str(url_b)+url_c
                    print(download_url)
                    urllib.request.urlretrieve(download_url,filename='CMC_reg_'+variable_level+'_ps10km_'+d1+emission+'_P00'+str(url_b)+url_c)
                except HTTPError as error:
                    print(error)
            elif ((url_b>= 10) and (url_b< 100)):
                url_a='/CMC_reg_'+variable_level+'_ps10km_'+d1+emission+'_P0'
                url_c='.grib2'
                download_url=URL+'0'+str(url_b)+url_a+str(url_b)+url_c
                print(download_url)
                urllib.request.urlretrieve(download_url,filename='CMC_reg_'+variable_level+'_ps10km_'+d1+emission+'_P0'+str(url_b)+url_c)

            else:
                url_a='/CMC_geps-raw_'+variable_level+'_latlon0p5x0p5_'+d1+emission+'_P'
                url_c='.grib2'
                download_url=URL+str(url_b)+url_a+str(url_b)+url_c
                print(download_url)
                urllib.request.urlretrieve(download_url,filename='test'+d1+str(url_b)+'.grib2')
    
        


#il manque le type et la probabilité de précipitation
#•	La valeur de la colonne matrice scribe  TST (température).
#•	La valeur de la colonne matrice scribe  CLD (nébulosité).
#•	La valeur de la colonne matrice scribe  P06 (probabilités précipitations aux 6 heures).
#•	La valeur de la colonne matrice scribe  QPS (quantités précipitations).
#•	La valeur de la colonne matrice scribe  TYP (types précipitations).
#•	La valeur de la colonne matrice scribe  DD (direction du vent).
#•	La valeur de la colonne matrice scribe  FF (vitesse du vent).
#•	La valeur de la colonne matrice scribe  DPD (écart entre la température et le point de rosée)
