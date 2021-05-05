from previs import download

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

cmc_download(date,d1,emission='00',variable_level='WIND_TGL_10')
cmc_download(date,d1,emission='00',variable_level='TMP_TGL_2')
cmc_download(date,d1,emission='00',variable_level='WDIR_TGL_10')
cmc_download(date,d1,emission='00',variable_level='APCP_SFC_0')
cmc_download(date,d1,emission='00',variable_level='TCDC_SFC_0')
cmc_download(date,d1,emission='00',variable_level='DPT_TGL_2')#dewpoint temperatur