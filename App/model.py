"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
import datetime
assert cf
import time as t
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog(type_list):
    if type_list == 1:
            type_list = "ARRAY_LIST"
    else:
        type_list = "LINKED_LIST"

    catalog = {"artworks": None,
               "artists": None,
               "medium":None,
               "country": None}
    catalog["artworks"] = lt.newList(type_list)
    catalog["artists"] = lt.newList(type_list)
    catalog["begindate"] = mp.newMap(661,maptype='PROBING',loadfactor=0.50)
    catalog["department"] = mp.newMap(661,maptype='PROBING',loadfactor=0.50)
    catalog["exactdate"] = mp.newMap(160000,maptype='PROBING', loadfactor=0.80)
    catalog["medium"] = mp.newMap(160000,maptype='PROBING', loadfactor=0.80)
    catalog["country"] = mp.newMap(160000,maptype='PROBING', loadfactor=0.80)
    return catalog
# Funciones para agregar informacion al catalogo
def addArtist(catalog, artist):
    artist["artworks"] = lt.newList("ARRAY_LIST")
    lt.addLast(catalog["artists"],artist)
    

def addArtwork(catalog,artwork):
    lt.addLast(catalog["artworks"],artwork)
    #crtOrcmprMedium(catalog,artwork)
    artists = artwork["ConstituentID"].replace("[", "").replace("]", "").split(",")
    for artist in artists:
        addArtistOfArtwork(catalog,artist,artwork)

def addArtistOfArtwork(catalog,artist_id,artworks):
    for artist in lt.iterator(catalog["artists"]):
        if artist["ConstituentID"] == artist_id:
            lt.addLast(artist["artworks"],artworks)

#--------------------------------------------------LAB6-----------------------------------------------------------------
def loadMediumMap(catalog):
    star_time = t.process_time()
    for artwork in lt.iterator(catalog["artworks"]):
        crtOrcmprMedium(catalog,artwork)
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000
    return laps_time

def loadCountryMap(catalog):
    star_time = t.process_time()
    for artist in lt.iterator(catalog["artists"]):
        countryArtworks(catalog,artist)
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000
    return laps_time

def crtOrcmprMedium(catalog,artwork):
    if mp.contains(catalog["medium"],artwork["Medium"]):
        medio = mp.get(catalog["medium"],artwork["Medium"])
        medio = me.getValue(medio)
        lt.addLast(medio["artwork"],artwork)
    else:
        medio = artwork["Medium"]
        artyear = artworkMedium(medio)
        lt.addLast(artyear["artwork"],artwork)
        mp.put(catalog["medium"],medio,artyear)

def artworkMedium (medio):
    entry = {'medium': "", "artwork": None}
    entry['medium'] = medio
    entry['artwork'] = lt.newList('SINGLE_LINKED')
    return entry

def countryArtworks(catalog,artist):
    if mp.contains(catalog["country"],artist["Nationality"]):
        country = mp.get(catalog["country"],artist["Nationality"])
        country = me.getValue(country)
        for artwork in lt.iterator(artist["artworks"]):
            lt.addLast(country["artwork"],artwork)
    else:
        country = artist["Nationality"]
        artCntry = artworkCountry(country)
        for artwork in lt.iterator(artist["artworks"]):
            lt.addLast(artCntry["artwork"],artwork)
        mp.put(catalog["country"],country,artCntry)
        
def artworkCountry(country):
    entry = {'medium': "", "artwork": None}
    entry['country'] = country
    entry['artwork'] = lt.newList('SINGLE_LINKED')
    return entry


    
#def artworksByArtists(catalog,artists):
    #artwork_lt = catalog["artworks"]
    #for artwork in lt.iterator(artwork_lt):
        #constId = artwork["ConstituentID"].replace("[", "").replace("]", "").split(",")
        #for id in constId:
            #if id == artists["ConstituentID"]:
                #lt.addLast(artists["artworks"],artwork)


#Punto 1 Reto2
def begindateArtists(date1,date2,catalog):
    
    for artists in lt.iterator(catalog["artists"]):
        if artists["BeginDate"] >= date1 and artists["BeginDate"] <= date2 :
            if mp.contains(catalog["begindate"],artists["BeginDate"]):
                date = mp.get(catalog["begindate"],artists["BeginDate"])
                date = me.getValue(date)
                lt.addLast(date["artist"],artists)
            else:
                date = artists["BeginDate"]
                artdate = artisByBegindate(date)
                lt.addLast(artdate["artist"],artists)
                mp.put(catalog["begindate"],date,artdate)
    return 

def artisByBegindate(date):
    entry = {"date": "", "artist":None}
    entry["date"] = date
    entry["artist"] = lt.newList("SINGLE_LINKED")
    return entry 

#Punto 2
def artworksByDateRange(date1,date2,catalog):
    for artwork in lt.iterator(catalog["artworks"]):
        if artwork["DateAcquired"] != "":
            date_Artwork = datetime.datetime.strptime(artwork["DateAcquired"], '%Y-%m-%d')
            if date_Artwork >= date1 and date_Artwork <= date2:
                if mp.contains(catalog["exactdate"],date_Artwork):
                    lt.addLast(artworkdate["artworks"],artwork)
                else:
                    artworkdate = listArtworksByDate(date_Artwork)
                    lt.addLast(artworkdate["artworks"],artwork)
                    mp.put(catalog["exactdate"],date_Artwork,artworkdate)
    
    return

def listArtworksByDate(date):
    entry = {"date":"","artworks":None}
    entry["date"] = date
    entry["artworks"] = lt.newList("SINGLE_LINKED")
    return entry

def purchase(date1,date2,catalog):
    contador = 0
    purchase = 0
    for artwork in lt.iterator(catalog["artworks"]):
        if artwork["DateAcquired"] != "":
            date_Artwork = datetime.datetime.strptime(artwork["DateAcquired"], '%Y-%m-%d')
            if date_Artwork >= date1 and date_Artwork <= date2:
                contador += 1
                if (artwork["CreditLine"] == "purchase") or (artwork["CreditLine"] == "Purchase") or ("purchase" in artwork["CreditLine"]) or ("Purchase" in artwork["CreditLine"]):
                    purchase += 1
    return (contador,purchase)

#Punto 3
def countArtworksOfArtistByMedium(name_artist,catalog):
    ID = ""
    contador = 0
    lst = lt.newList("ARRAY_LIST")
    lista_medios = lt.newList("ARRAY_LIST")
    map = mp.newMap(661,maptype='PROBING',loadfactor=0.50)
    for artist in lt.iterator(catalog["artists"]):
        if artist["DisplayName"] == name_artist:
            ID = artist["ConstituentID"]
    
    for artwork in lt.iterator(catalog["artworks"]):
        if ID in artwork["ConstituentID"]:
            contador += 1
            lt.addLast(lst,artwork)
    
    for artwork in lt.iterator(lst):
        dict = {"medium": artwork["Medium"],"artwork":artwork}
        lt.addLast(lista_medios,dict)
    for artwork in lt.iterator(lista_medios):
            if mp.contains(catalog["medium"],artwork["medium"]):
                nombre_medio = mp.get(catalog["medium"],artwork["medium"])
                nombre_medio = me.getValue(nombre_medio)
                lt.addLast(nombre_medio["artworks"],artwork["artwork"])
                nombre_medio["count"] += 1
            else:
                counter = ArtworksOfMedium()
                lt.addLast(counter["artworks"],artwork["artwork"])
                mp.put(catalog["medium"],artwork["medium"],counter)
    return

def ArtworksOfMedium():
    entry = {"artworks":None,"count":1}
    entry["artworks"] = lt.newList("ARRAY_LIST")
    return entry


#Punto 4







# Punto 5
def mapByDepartment(catalog,department):
    for artwork in lt.iterator(catalog["artworks"]):
        if artwork["Department"] == department:
            if mp.contains(catalog["department"],artwork["Department"]):
                medio = mp.get(catalog["department"],artwork["Department"])
                medio = me.getValue(medio)
                lt.addLast(medio["artworks"],artwork)
            else:
                medio = artwork["Department"]
                artdep = artworkMedium(medio)
                lt.addLast(artdep["artworks"],artwork)
                mp.put(catalog["department"],medio,artdep)

def artworkByDepartment(department):
    entry = {"department": "", "artist":None}
    entry["department"] = department
    entry["artworks"] = lt.newList("SINGLE_LINKED")
    return entry

# Funciones para creacion de datos

# Funciones de consulta
def getByMedium(catalog,medio):
    mapa = mp.get(catalog["medium"],medio)
    mapa = me.getValue(mapa)
    if mapa != None:
        return mapa["artwork"]   
    else:
        return "No se encntro ningun artwork vinculado a este medio"
def getByCountry(catalog,country):
    mapa = mp.get(catalog["country"],country)
    mapa = me.getValue(mapa)
    if mapa != None:
        return mapa["artwork"]
    else:
        return "No se encntro artwork vinculado a este pais"

def getBegindate(catalog):
    mapa = mp.keySet(catalog["begindate"])
    mayor = lt.newList()
    menor = lt.newList()
    sort_m = sa.sort(mapa,compareratings)

    for fecha in lt.iterator(sort_m):
        f = mp.get(catalog["begindate"],fecha)
        f = me.getValue(f)
        putinfomation(mayor,f["artist"])
        if lt.size(mayor) >= 3:
            break
    sort_men = sa.sort(mapa,compareratings2)   
    for fecha in lt.iterator(sort_men):
        f = mp.get(catalog["begindate"],fecha)
        f = me.getValue(f)
        putinfomation(menor,f["artist"])
        if lt.size(menor) >= 3:
            break
    size = mp.size(catalog["begindate"])
    return (mayor,menor,size)

def getDate(catalog):
    mapa = mp.keySet(catalog["exactdate"])
    mayor = lt.newList()
    menor = lt.newList()
    sort_m = sa.sort(mapa,compareratings3)

    for fecha in lt.iterator(sort_m):
        f = mp.get(catalog["exactdate"],fecha)
        f = me.getValue(f)
        putinfomation(mayor,f["artworks"])
        if lt.size(mayor) >= 3:
            break
    sort_men = sa.sort(mapa,compareratings4)   
    for fecha in lt.iterator(sort_men):
        f = mp.get(catalog["exactdate"],fecha)
        f = me.getValue(f)
        putinfomation(menor,f["artworks"])
        if lt.size(menor) >= 3:
            break
    return (mayor,menor)
def getArtworkMedium(catalog):
    num_obras = 0
    mayor = 0
    mapa = mp.keySet(catalog["medium"])
    num_medios = str(lt.size(mapa))
    for medio in lt.iterator(mapa):
        contador = mp.get(catalog["medium"],medio)
        contador = me.getValue(contador)
        num_obras += contador["count"]
        if contador["count"] > mayor:
            mayor = contador["count"]
            obras_mayor = contador["artworks"]
    return (mayor,num_obras,obras_mayor,num_medios)

    

def putinfomation(lst,lst2):
    for l in lt.iterator(lst2):
        lt.addLast(lst,l)
    
def artistsOfArtwork(artwork,catalog):
    texto = ""
    constId = (artwork["ConstituentID"]).replace("[", "").replace("]", "").replace(" ","").split(",")
    for Id in constId:
        nombre_a = nameArtistsId(catalog,Id)
        if type(nombre_a) == "NoneType":
            nombre_a = ""
        if nombre_a != "":
            texto += (nombre_a + ",") 
        if texto == "":
            texto = "Unknown"
    return texto

def nameArtistsId(catalog,id):
    for artists in lt.iterator(catalog["artists"]):
        if id == artists["ConstituentID"]:
            return artists["DisplayName"]
# Funciones utilizadas para comparar elementos dentro de una lista
def compareratings(date1, date2):
    if((date1) < (date2)):
        return 0
    else:
        return 1
def compareratings2(date1, date2):
    if((date1) < (date2)):
        return 1
    else:
        return 0

def compareratings3(date1, date2):
    if((date1) < (date2)):
        return 0
    else:
        return 1
def compareratings4(date1, date2):
    if((date1) < (date2)):
        return 1
    else:
        return 0
# Funciones de ordenamiento
