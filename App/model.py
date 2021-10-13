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
assert cf

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
    catalog["medium"] = mp.newMap(100,maptype='CHAINING',loadfactor=0.5,)
    catalog["country"] = mp.newMap(100,maptype='CHAINING', loadfactor=0.5)
    return catalog
# Funciones para agregar informacion al catalogo
def addArtist(catalog, artist):
    artist["artworks"] = lt.newList("ARRAY_LIST")
    artworksByArtists(catalog,artist)
    lt.addLast(catalog["artists"],artist)
    countryArtworks(catalog,artist)


def addArtwork(catalog,artwork):
    lt.addLast(catalog["artworks"],artwork)
    crtOrcmprMedium(catalog,artwork)

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


    
def artworksByArtists(catalog,artists):
    artwork_lt = catalog["artworks"]
    for artwork in lt.iterator(artwork_lt):
        constId = artwork["ConstituentID"].replace("[", "").replace("]", "").split(",")
        for id in constId:
            if id == artists["ConstituentID"]:
                lt.addLast(artists["artworks"],artwork)
        print(type(id))



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
# Funciones utilizadas para comparar elementos dentro de una lista
def compareratings(book1, book2):
    date1 = book1["Date"]
    date2 = book2["Date"]
    if((date1) < (date2)):
        return 1
    else:
        return 0
# Funciones de ordenamiento
