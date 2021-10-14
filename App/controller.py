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
 """

import config as cf
import model
import csv
import time as t

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog(type_list):
    catalog = model.newCatalog(type_list)
    return catalog
# Funciones para la carga de datos
def loadData(catalog):
    time_1 =loadArtists(catalog)
    time_2 = loadArtwork(catalog)
    return (time_1+time_2)

def loadArtists(catalog):
    artistfile = cf.data_dir + "MoMA/Artists-utf8-50pct.csv"
    input_file = csv.DictReader(open(artistfile,encoding="utf-8"))
    star_time = t.process_time()
    for artist in input_file:
        model.addArtist(catalog, artist)
    end_time = t.process_time()
    laps_time = (end_time-star_time)*1000
    return laps_time

def loadArtwork(catalog):
    artworkfile = cf.data_dir + "MoMA/Artworks-utf8-50pct.csv"
    input_file = csv.DictReader(open(artworkfile,encoding="utf-8"))
    star_time = t.process_time()
    for artwork in input_file:
        model.addArtwork(catalog,artwork)
    end_time = t.process_time()
    laps_time = (end_time-star_time)*1000
    return laps_time

def loadCountryMap(catalog):
    time = model.loadCountryMap(catalog)
    return time

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def getByMedium(catalog,medio):
    return model.getByMedium(catalog,medio)

def getByCountry(catalog,country):
    return model.getByCountry(catalog,country)