﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- ")
    print("3- ")
def initCatalog(type_lyst):
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog(type_lyst)
def getByMedium(catalog,medio):
    return controller.getByMedium(catalog,medio)

def getByCountry(catalog,country):
    return controller.getByCountry(catalog,country)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando Catálogo ....")
        type_lyst = 1
        catalog = initCatalog(type_lyst)
        print("Cargando información de los archivos ....")
        controller.loadData(catalog)
        print(lt.getElement(catalog["artists"],4)["artworks"])
    elif int(inputs[0]) == 2:
        medio = input("Cual medio desea buscar\n")
        lst_m = getByMedium(catalog,medio)

        print("el nuemro de obras encontradas con el medio " + medio + " es " + str(lt.size(lst_m)))

    elif int(inputs[0]) == 3:
        country = input("ibgrese el pais:\n ")
        lst_c = getByCountry(catalog,country)
        print("El numero de obras en la nacinalidad " + country + str(lt.size(lst_c)))
        

    else:
        sys.exit(0)
sys.exit(0)
