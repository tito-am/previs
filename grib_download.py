#grib download

import requests
import urllib.request
from urllib.error import HTTPError
import time
from bs4 import BeautifulSoup
import os


#from datetime import date
import datetime

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

parent_dir='/Users/caramelo/Documents/00_HQ/01_Prevision_Demande/scribe_download/gem/RDPS/GRIBS'
os.chdir(parent_dir)
try:
    os.mkdir(d1)
except OSError as error:
    print(error)
os.chdir(d1)
#fonction de téléchargement

def cmc_download(date,d1,modele='regional',emission='12',variable_level='WIND_TGL_10'):
    #URL = 'https://dd.weather.gc.ca/ensemble/geps/grib2/raw/00/'
    #emission = '12'#00/
    URL = 'https://dd.weather.gc.ca/model_gem_'+modele+'/10km/grib2/'+emission+'/'
    #page = requests.get(URL)
    #soup = BeautifulSoup(page.content, 'html.parser')
    
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
                print(URL+'00'+str(url_b)+url_a+str(url_b)+url_c)
                try:
                    download_url=URL+'00'+str(url_b)+url_a+str(url_b)+url_c
                    urllib.request.urlretrieve(download_url,filename=d1+'_'+emission+str(url_b)+'.grib2')

                except HTTPError as error:
                    print(error)

            elif ((url_b>= 10) and (url_b< 100)):
                url_a='/CMC_reg_'+variable_level+'_ps10km_'+d1+emission+'_P0'
                url_c='.grib2'
                print(URL+'0'+str(url_b)+url_a+str(url_b)+url_c)
                try:
                    download_url=URL+'0'+str(url_b)+url_a+str(url_b)+url_c
                except OSError as error:
                    print(error)
                urllib.request.urlretrieve(download_url,filename='test_reg_wind'+emission+d1+str(url_b)+'.grib2')
            else:
                url_a='/CMC_geps-raw_'+variable_level+'_latlon0p5x0p5_'+d1+emission+'_P'#TMP_TGL_2m
                url_c='_allmbrs.grib2'
                print(URL+str(url_b)+url_a+str(url_b)+url_c)
                download_url=URL+str(url_b)+url_a+str(url_b)+url_c
                urllib.request.urlretrieve(download_url,filename='test_reg'+emission+d1+str(url_b)+'.grib2')
    else:
        for url_b in range(0, 85, 1):
            if url_b < 10:
                url_a='/CMC_reg_'+variable_level+'_ps10km_'+d1+emission+'_P00'
                url_c='.grib2'
                print(URL+'00'+str(url_b)+url_a+str(url_b)+url_c)
                try:
                    download_url=URL+'00'+str(url_b)+url_a+str(url_b)+url_c
                    urllib.request.urlretrieve(download_url,filename='CMC_reg_'+variable_level+'_ps10km_'+d1+emission+'_P00'+str(url_b)+url_c)
                except HTTPError as error:
                    print(error)
            elif ((url_b>= 10) and (url_b< 100)):
                url_a='/CMC_reg_'+variable_level+'_ps10km_'+d1+emission+'_P0'
                url_c='.grib2'
                print(URL+'0'+str(url_b)+url_a+str(url_b)+url_c)
                download_url=URL+'0'+str(url_b)+url_a+str(url_b)+url_c
                print(download_url)
                urllib.request.urlretrieve(download_url,filename='CMC_reg_'+variable_level+'_ps10km_'+d1+emission+'_P0'+str(url_b)+url_c)

            else:
                url_a='/CMC_geps-raw_'+variable_level+'_latlon0p5x0p5_'+d1+emission+'_P'
                url_c='.grib2'
                print(URL+str(url_b)+url_a+str(url_b)+url_c)
                download_url=URL+str(url_b)+url_a+str(url_b)+url_c
                urllib.request.urlretrieve(download_url,filename='test'+d1+str(url_b)+'.grib2')
    os.chdir(parent_dir)
    os.chdir(d1)
        
#cmc_download(date,d1,emission='00')
#cmc_download(date,d1,emission='00',variable_level='TMP_TGL_2')
#cmc_download(date,d1,emission='00',variable_level='WDIR_TGL_10')
cmc_download(date,d1,emission='00',variable_level='APCP_SFC_0')
cmc_download(date,d1,emission='00',variable_level='TCDC_SFC_0')
cmc_download(date,d1,emission='00',variable_level='DPT_TGL_2')
