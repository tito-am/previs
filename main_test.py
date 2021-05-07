from previs.download.grib_download import cmc_download
from previs.transform.extract_grib import lecture_grib, calcul_par_station
import requests
import urllib.request
from urllib.error import HTTPError
import time
from bs4 import BeautifulSoup
import os
import glob
import pandas as pd


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


#CMC_reg_WIND_TGL_10_ps10km_2021042106_P000
folder = '/Users/caramelo/Documents/00_HQ/01_Prevision_Demande/scribe_download/gem/RDPS/GRIBS/'+d1

for filename in os.listdir(folder):
    #print(filename)
    infilename = os.path.join(folder, filename)
    print(infilename)
    x=glob.glob(infilename+"/*/")
    list_stations_meteo=[]
    coords_stations=pd.read_csv('/Users/caramelo/Documents/GitHub/cmc/Stations matrice scribe.csv')
    for path in x:
        print(path)
        os.chdir(infilename+path.split(infilename)[1])
        var=path.split('/')[-2]
        dr_out=lecture_grib(glob.glob('*'+var+'*.grib2'),var)
        result = [calcul_par_station(dr_out,x, y, nomstn, oaci) for x, y, nomstn, oaci in zip(coords_stations['LAT'], coords_stations['LON'],coords_stations['NOMSTN'],coords_stations['OACI'])] 
        df = pd.concat(result,axis=0).sort_values('valid_time').reset_index().to_csv(var+'.csv')
        print(type(df))
        list_stations_meteo.append(df)


df_final = pd.concat(list_stations_meteo)
df_final.to_csv('final.csv')
#grib_list_total_wind_12=sorted(glob.glob('*_WIND_*.grib2'))#il faut regarder pour avoir l'heure d'émission
#print(grib_list_total_wind_12)
#grib_list_total_tmp_12=sorted(glob.glob('*_TMP_*.grib2'))#il faut regarder pour avoir l'heure d'émission
#print(grib_list_total_tmp_12)
#grib_list_total_wdir_12=sorted(glob.glob('*_WDIR_*.grib2'))#il faut regarder pour avoir l'heure d'émission
#print(grib_list_total_wdir_12)

#d = {}
#for name in companies:
#    d[name] = pd.DataFrame()



#bloc pour voir si les fichiers sont présents

''' if grib_list_total_wind_12:
    #WIND
    dr_out=lecture_grib(grib_list_total_wind_12,'WIND')
    result = [calcul_par_station(dr_out,x, y, nomstn, oaci) for x, y, nomstn, oaci in zip(coords_stations['LAT'], coords_stations['LON'],coords_stations['NOMSTN'],coords_stations['OACI'])]
    df_wind = pd.concat(result,axis=0).sort_values('valid_time').reset_index()

if grib_list_total_tmp_12:
    #TMP
    dr_out=lecture_grib(grib_list_total_tmp_12,'TMP')
    result = [calcul_par_station(dr_out,x, y, nomstn, oaci) for x, y, nomstn, oaci in zip(coords_stations['LAT'], coords_stations['LON'],coords_stations['NOMSTN'],coords_stations['OACI'])]
    df_tmp = pd.concat(result,axis=0).sort_values('valid_time').reset_index()

if grib_list_total_wdir_12:
    #WDIR
    print(grib_list_total_wdir_12)
    dr_out=lecture_grib(grib_list_total_wdir_12,'WDIR')
    result = [calcul_par_station(dr_out,x, y, nomstn, oaci) for x, y, nomstn, oaci in zip(coords_stations['LAT'], coords_stations['LON'],coords_stations['NOMSTN'],coords_stations['OACI'])]
    df_wdir = pd.concat(result,axis=0).sort_values('valid_time').reset_index()

#Concatenation de toutes les previsions 
#df_final = pd.merge(df_wind, df_wdir, on=['valid_time','station'])

#df_final.to_csv(dateStr+'_wdir_tmp_12.csv')#mettre variable
df_wind.to_csv('test.csv') '''