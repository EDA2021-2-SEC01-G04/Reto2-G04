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
import math
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
    catalog["begindate"] = mp.newMap(30448,maptype='PROBING',loadfactor=0.50)
    catalog["artworkcost"] = mp.newMap(160000,maptype='PROBING',loadfactor=0.50)
    catalog["nationality"] = mp.newMap(30448,maptype='PROBING',loadfactor=0.50)
    catalog["exactdate"] = mp.newMap(160000,maptype='PROBING', loadfactor=0.50)
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
    star_time = t.process_time()
    contador = 0
    for artists in lt.iterator(catalog["artists"]):
        if artists["BeginDate"] >= date1 and artists["BeginDate"] <= date2 :
            if mp.contains(catalog["begindate"],artists["BeginDate"]):
                date = mp.get(catalog["begindate"],artists["BeginDate"])
                date = me.getValue(date)
                lt.addLast(date["artist"],artists)
                contador += 1
            else:
                date = artists["BeginDate"]
                artdate = artisByBegindate(date)
                lt.addLast(artdate["artist"],artists)
                mp.put(catalog["begindate"],date,artdate)
                contador += 1
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000
    return (laps_time,contador)

def artisByBegindate(date):
    entry = {"date": "", "artist":None}
    entry["date"] = date
    entry["artist"] = lt.newList("SINGLE_LINKED")
    return entry 

#Punto 2
def artworksByDateRange(date1,date2,catalog):
    star_time = t.process_time()
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
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000
    return laps_time

def listArtworksByDate(date):
    entry = {"date":"","artworks":None}
    entry["date"] = date
    entry["artworks"] = lt.newList("SINGLE_LINKED")
    return entry

def purchase(date1,date2,catalog):
    contador = 0
    purchase = 0
    star_time = t.process_time()
    for artwork in lt.iterator(catalog["artworks"]):
        if artwork["DateAcquired"] != "":
            date_Artwork = datetime.datetime.strptime(artwork["DateAcquired"], '%Y-%m-%d')
            if date_Artwork >= date1 and date_Artwork <= date2:
                contador += 1
                if (artwork["CreditLine"] == "purchase") or (artwork["CreditLine"] == "Purchase") or ("purchase" in artwork["CreditLine"]) or ("Purchase" in artwork["CreditLine"]):
                    purchase += 1
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000
    return (contador,purchase,laps_time)

#Punto 3
def countArtworksOfArtistByMedium(name_artist,catalog):
    ID = ""
    contador = 0
    lst = lt.newList("ARRAY_LIST")
    lista_medios = lt.newList("ARRAY_LIST")
    map = mp.newMap(661,maptype='PROBING',loadfactor=0.50)
    star_time = t.process_time()
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
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000
    return laps_time

def ArtworksOfMedium():
    entry = {"artworks":None,"count":1}
    entry["artworks"] = lt.newList("ARRAY_LIST")
    return entry


#Punto 4
def mapByNationality(catalog):
    star_time = t.process_time()
    for artist in lt.iterator(catalog["artists"]):
        if mp.contains(catalog["nationality"],artist["Nationality"]):
            country = mp.get(catalog["nationality"],artist["Nationality"])
            country = me.getValue(country)
            for artwork in lt.iterator(artist["artworks"]):
                lt.addLast(country["artwork"],artwork)
        else:
            country = artist["Nationality"]
            artCntry = artworkCountry(country)
            for artwork in lt.iterator(artist["artworks"]):
                lt.addLast(artCntry["artwork"],artwork)
            mp.put(catalog["nationality"],country,artCntry)
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000

    return laps_time





# Punto 5
def mapByDepartment(catalog,departamento):
    pi = math.pi
    star_time = t.process_time()
    for artwork in lt.iterator(catalog["artworks"]):
        precio1 = 0
        precio2 = 0
        precio3 = 0
        precio4 = 0
        precio5 = 0
        precio6 = 0
        if artwork["Circumference (cm)"] != "":
            circumference = float(artwork["Circumference (cm)"])/100
        else:
            circumference = 0
        if artwork["Depth (cm)"] != "":
            depth = float(artwork["Depth (cm)"])/100
        else:
            depth = 0
        if artwork["Diameter (cm)"] != "":
            diameter = float(artwork["Diameter (cm)"])/100
        else:
            diameter = 0
        if artwork["Height (cm)"] != "":
            height = float(artwork["Height (cm)"])/100
        else:
            height = 0
        if artwork["Length (cm)"] != "":
            length = float(artwork["Length (cm)"])/100
        else:
            length = 0
        if artwork["Weight (kg)"] != "":
            weight = float(artwork["Weight (kg)"])
        else:
            weight = 0
        if artwork["Width (cm)"] != "":
            width = float(artwork["Width (cm)"])/100
        if artwork["Department"] == departamento:
            if circumference != "" and depth != "":
                precio1 = ((circumference)/(4*pi))*depth*72
            if diameter != "" and depth != "":
                precio2 = ((pi*diameter**2)/4)*depth*72
            if height != "" and length != "":
                precio3 = height*length*72
            if weight != "":
                precio4 = weight*72
            if height != "" and length != "" and width != "":
                precio5 = length*width*height*72
            if height != "" and width != "":
                precio6 = height*length*72
            mas_caro = max(precio1,precio2,precio3,precio4,precio5,precio6)
            if mas_caro == 0 or mas_caro < 42:
                precio = 42
            else:
                precio = mas_caro

            artwork["cost"] = precio
            mp.put(catalog["artworkcost"],artwork["ObjectID"],artwork)
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000
    return laps_time
            

def contadores(catalog,departamento):
    pi = math.pi
    peso = 0
    total_obras = 0
    precio_total = 0
    star_time = t.process_time()
    for artwork in lt.iterator(catalog["artworks"]):
        total_obras += 1
        if artwork["Circumference (cm)"] != "":
            circumference = float(artwork["Circumference (cm)"])/100
        else:
            circumference = 0
        if artwork["Depth (cm)"] != "":
            depth = float(artwork["Depth (cm)"])/100
        else:
            depth = 0
        if artwork["Diameter (cm)"] != "":
            diameter = float(artwork["Diameter (cm)"])/100
        else:
            diameter = 0
        if artwork["Height (cm)"] != "":
            height = float(artwork["Height (cm)"])/100
        else:
            height = 0
        if artwork["Length (cm)"] != "":
            length = float(artwork["Length (cm)"])/100
        else:
            length = 0
        if artwork["Weight (kg)"] != "":
            weight = float(artwork["Weight (kg)"])
        else:
            weight = 0
        if artwork["Width (cm)"] != "":
            width = float(artwork["Width (cm)"])/100

        if artwork["Department"] == departamento:
            if circumference != "" and depth != "":
                precio1 = ((circumference)/(4*pi))*depth*72
            if diameter != "" and depth != "":
                precio2 = ((pi*diameter**2)/4)*depth*72
            if height != "" and length != "":
                precio3 = height*length*72
            if weight != "":
                precio4 = weight*72
                peso += weight
            if height != "" and length != "" and width != "":
                precio5 = length*width*height*72
            if height != "" and width != "":
                precio6 = height*length*72
            mas_caro = max(precio1,precio2,precio3,precio4,precio5,precio6)
            if mas_caro == 0 or mas_caro < 42:
                precio = 42
            else:
                precio = mas_caro
            precio_total += precio
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000
    return (peso,total_obras,precio_total,laps_time)

def costOfArtworkByDepartment(catalog):
    mapa1 = mp.valueSet(catalog["artworkcost"])
    mapa1 = sa.sort(mapa1,comparecosts)
    lst = lt.newList()
    lt.addLast(lst,lt.getElement(mapa1,1))
    lt.addLast(lst,lt.getElement(mapa1,2))
    lt.addLast(lst,lt.getElement(mapa1,3))
    lt.addLast(lst,lt.getElement(mapa1,4))
    lt.addLast(lst,lt.getElement(mapa1,5))
    return lst
    
def DateOfArtworkByDepartmentcos(catalog):
    mapa_1 = mp.valueSet(catalog["artworkcost"])
    mapa_1 = sa.sort(mapa_1,compardate)
    lst = lt.newList()
    lt.addLast(lst,lt.getElement(mapa_1,1))
    lt.addLast(lst,lt.getElement(mapa_1,2))
    lt.addLast(lst,lt.getElement(mapa_1,3))
    lt.addLast(lst,lt.getElement(mapa_1,4))
    lt.addLast(lst,lt.getElement(mapa_1,5))
    return lst

def comparecosts(book1,book2):
    cost1 = book1["cost"]
    cost2 = book2["cost"]
    if(cost1) < (cost2):
        return 1
    else:
        return 0
def compardate(book1,book2):
    cost1 = book1["Date"]
    cost2 = book2["Date"]
    if(cost1) > (cost2):
        return 1
    else:
        return 0

def artworkByID(catalog,ID):
    for artwork in lt.iterator(catalog["artworks"]):
        if ID == artwork["ObjectID"]:
            return artwork

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
    star_time = t.process_time()
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
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000
    return (mayor,menor,laps_time)

def getDate(catalog):
    mapa = mp.keySet(catalog["exactdate"])
    mayor = lt.newList()
    menor = lt.newList()
    sort_m = sa.sort(mapa,compareratings3)
    star_time = t.process_time()
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
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000
    return (mayor,menor,laps_time)

def getArtworkMedium(catalog):
    num_obras = 0
    mayor = 0
    mapa = mp.keySet(catalog["medium"])
    num_medios = str(lt.size(mapa))
    star_time = t.process_time()
    for medio in lt.iterator(mapa):
        contador = mp.get(catalog["medium"],medio)
        contador = me.getValue(contador)
        num_obras += contador["count"]
        if contador["count"] > mayor:
            mayor = contador["count"]
            obras_mayor = contador["artworks"]
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000
    return (mayor,num_obras,obras_mayor,num_medios,laps_time)

    

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

def getNationality(catalog):
    nt_artw = {}
    lst = lt.newList("ARRAY_LIST")
    lst_p = lt.newList("ARRAY_LIST")
    star_time = t.process_time()
    for key in lt.iterator(mp.keySet(catalog["nationality"])):
        lst_art = mp.get(catalog["nationality"],key)
        lst_art = me.getValue(lst_art)
        sz = lt.size(lst_art["artwork"])
        nt_artw[key] = sz

    for cntry in nt_artw:
        number = nt_artw[cntry]
        lt.addLast(lst,number)
    lst_sort_num = (sa.sort(lst,compareratings))
    for num in lt.iterator(lst_sort_num):
        for key in nt_artw:
            if nt_artw[key] == num:
                lt.addLast(lst_p,key)
    end_time = t.process_time()
    laps_time = (end_time - star_time)*1000
    info = getArworksnationality(catalog,lst_p)
    return (lst_sort_num,lst_p,info,laps_time)

def getArworksnationality(catalog,lst_key):
    key = lt.getElement(lst_key,1)
    lst_info = lt.newList("ARRAY_LIST")
    lst = mp.get(catalog["nationality"],key)
    lst = me.getValue(lst)
    sz = lt.size(lst["artwork"])
    lt.addLast(lst_info,lt.getElement(lst["artwork"],1))
    lt.addLast(lst_info,lt.getElement(lst["artwork"],2))
    lt.addLast(lst_info,lt.getElement(lst["artwork"],3))
    lt.addLast(lst_info,lt.getElement(lst["artwork"],sz-2))
    lt.addLast(lst_info,lt.getElement(lst["artwork"],sz-1))
    lt.addLast(lst_info,lt.getElement(lst["artwork"],sz))
    return lst_info

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
