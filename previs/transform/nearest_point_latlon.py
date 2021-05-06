def nearest_point_latlon(path,coords):
    """Cette fonction donne les valeurs du point de grille le plus proche des coordonnées données en entrée pour les fichiers grib issus du GDPS

    Args:
        path (str): Chemin du répertoire où se trouvent tous les fichiers grib2.
        coords ([type]): Coordonnées des stations où trouver les points les plus proches. 
    Returns:
        matrice_scribe ([type]): Matrice contenant les prévisions aux stations pour le modèle canadien.
    """
       
    grib_list_total=glob.glob(path)
    ds=xr.open_mfdataset(grib_list_total,concat_dim='valid_time',parallel=True,engine='cfgrib',combine='nested')
    
    #dans le datamart, on download un grib par variable météo, donc on n'a qu'un attribut par fichier grib
  
    
    #passer d'une grille stereographique polaire à lat lon
    ds = ds.rename({'latitude': 'lat', 'longitude': 'lon'})
    ds_out = xe.util.grid_global(0.1, 0.1)
    regridder = xe.Regridder(ds, ds_out, 'bilinear')
    dr_out = regridder(ds)
    dr_out['lat'] = dr_out.lat[:,0].drop('lon')
    dr_out['lon'] = dr_out.lon[0,:].drop('lat')
    dr_out = dr_out.sortby(['x','y'])
    dr_out = dr_out.rename({'x':'longitude',
                        'y':'latitude',
                        'lon':'longitude',
                        'lat':'latitude'})
    dr_out = dr_out.where(dr_out>0) # remplacer 0 par nan


      
    #bloc conditionnel par variable météorologique
    if "si10" in ds:
        ds=dr_out.si10*3.6 #transformer m/s en km/h
        si10=ds.si10
    elif "t2m" in ds:
        ds=dr_out-273.15 #passage en celsius
        t2m = ds.t2m 
    #elif "" ajouter cloud cover
