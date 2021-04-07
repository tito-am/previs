def nearest_point_latlon(path,coords):
    """Cette fonction donne les valeurs du point de grille le plus proche des coordonnées données en entrée pour les fichiers grib issus du GDPS

    Args:
        path (str): Chemin du répertoire où se trouvent tous les fichiers grib2.
        coords ([type]): Coordonnées des stations où trouver les points les plus proches. 
    Returns:
        matrice_scribe ([type]): Matrice contenant les prévisions aux stations pour le modèle canadien.
    """
       
    ds=xr.open_mfdataset(grib_list_total,concat_dim='valid_time',parallel=True,engine='cfgrib',combine='nested')