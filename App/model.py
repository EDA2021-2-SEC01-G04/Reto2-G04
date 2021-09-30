﻿"""
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
               "medium":None}
    catalog["artworks"] = lt.newList(type_list)
    catalog["artists"] = lt.newList(type_list)
    catalog["medium"] = mp.newMap(500,maptype='CHAINING',loadfactor=4.0,)

    return catalog
# Funciones para agregar informacion al catalogo
def addArtist(catalog, artist):
    artist["artworks"] = lt.newList("ARRAY_LIST")
    lt.addLast(catalog["artists"],artist)


def addArtwork(catalog,artwork):
    lt.addLast(catalog["artworks"],artwork)
    mp.put(catalog["medium"],artwork["Medium"],artwork)
    artists = artwork["ConstituentID"].replace("[", "").replace("]", "").split(",")
def getByMedium(catalog,medio):
    mapa = mp.get(catalog["medium"],medio)
    values = me.getValue(mapa)
    return values

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def compareratings(book1, book2):
    date1 = book1["Date"]
    date2 = book2["Date"]
    if((date1) < (date2)):
        return 1
    else:
        return 0
# Funciones de ordenamiento
