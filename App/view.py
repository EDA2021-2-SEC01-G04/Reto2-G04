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
    print("2lab- Numero de obras por medio")
    print("3lab- Numero de obras por pais")
    print("4- Listar cronologicamente los artistas")
    print("5- Listar cronologicamente las adquisiciones")
def initCatalog(type_lyst):
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog(type_lyst)

def begindateArtists(date1,date2,catalog):
    return controller.begindateArtists(date1,date2,catalog)

def dateOfArtwork(date1,date2,catalog):
    return controller.dateArtworks(date1,date2,catalog)

def purchase(date1,date2,catalog):
    return controller.purchase(date1,date2,catalog)

def artistofartwork(artwork,catalog):
    return controller.artistsOfAnArtwork(artwork,catalog)

def loadCountryMap(catalog):
    time = controller.loadCountryMap(catalog)
    return time

def loadMediumMap(catalog):
    return controller.loadMediumMap(catalog)
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
        tm_1 = controller.loadData(catalog)
        print("el tiempo de carga de los datos fue de: " + str(tm_1))
    #-------------------------------------LAB6----------------------------------------------
    elif int(inputs[0]) == 2:
        tm_2 = loadMediumMap(catalog)
        medio = input("Cual medio desea buscar\n")
        lst_m = getByMedium(catalog,medio)
        print("tiempo mapa medio: " + str(tm_2))
        print("el nuemro de obras encontradas con el medio " + medio + " es " + str(lt.size(lst_m)))

    elif int(inputs[0]) == 3:
        tm_3 = loadCountryMap(catalog)
        country = input("ingrese el pais:\n")
        lst_c = getByCountry(catalog,country)
        print("tiempo mapa nacionalidad: " + str(tm_3))
        print("El numero de obras en la nacinalidad " + country + " es de: " + str(lt.size(lst_c)))
    #---------------------------------------Reto2------------------------------------------------
    elif int(inputs[0]) == 4:
        date1 = input("ingrese el primer año:\n")
        date2 = input("ingrese el segundo año:\n")
        print("cargando mapa")
        mapa_date = begindateArtists(date1,date2,catalog)
        size = mapa_date[2]
        mayor = mapa_date[0]
        menor = mapa_date[1]
        print("Hay un total de " + str(size) + " artistas entre los años " + date1 + " y " + date2)
        print("Nombre: " + lt.getElement(mayor,1)["DisplayName"],",Fecha de nacimiento: " + lt.getElement(mayor,1)["BeginDate"],",Fecha de muerte: "+ lt.getElement(mayor,1)["EndDate"],",Nacionalidad: "+ lt.getElement(mayor,1)["Nationality"],",Genero: "+ lt.getElement(mayor,1)["Gender"])            
        print("Nombre: " + lt.getElement(mayor,2)["DisplayName"],",Fecha de nacimiento: " + lt.getElement(mayor,2)["BeginDate"],",Fecha de muerte: "+ lt.getElement(mayor,2)["EndDate"],",Nacionalidad: "+ lt.getElement(mayor,2)["Nationality"],",Genero: "+ lt.getElement(mayor,2)["Gender"])
        print("Nombre: " + lt.getElement(mayor,3)["DisplayName"],",Fecha de nacimiento: " + lt.getElement(mayor,3)["BeginDate"],",Fecha de muerte: "+ lt.getElement(mayor,3)["EndDate"],",Nacionalidad: "+ lt.getElement(mayor,3)["Nationality"],",Genero: "+ lt.getElement(mayor,3)["Gender"])
        print("Nombre: " + lt.getElement(menor,1)["DisplayName"],",Fecha de nacimiento: " + lt.getElement(menor,1)["BeginDate"],",Fecha de muerte: "+ lt.getElement(menor,1)["EndDate"],",Nacionalidad: "+ lt.getElement(menor,1)["Nationality"],",Genero: "+ lt.getElement(menor,1)["Gender"])            
        print("Nombre: " + lt.getElement(menor,2)["DisplayName"],",Fecha de nacimiento: " + lt.getElement(menor,2)["BeginDate"],",Fecha de muerte: "+ lt.getElement(menor,2)["EndDate"],",Nacionalidad: "+ lt.getElement(menor,2)["Nationality"],",Genero: "+ lt.getElement(menor,2)["Gender"])
        print("Nombre: " + lt.getElement(menor,3)["DisplayName"],",Fecha de nacimiento: " + lt.getElement(menor,3)["BeginDate"],",Fecha de muerte: "+ lt.getElement(menor,3)["EndDate"],",Nacionalidad: "+ lt.getElement(menor,3)["Nationality"],",Genero: "+ lt.getElement(menor,3)["Gender"])
    elif int(inputs[0]) == 5:
        date1 = input("Ingrese el primer año en formato YYYY-MM-DD:\n")
        date2 = input("ingrese el segundo año en formato YYYY-MM-DD:\n")
        print("Cargando mapa")
        mapa_date = dateOfArtwork(date1,date2,catalog)
        resultados = purchase(date1,date2,catalog)
        size1 = resultados[0]
        compras = resultados[1]
        mayor = mapa_date[0]
        menor = mapa_date[1]
        print("Hay un total de " + str(size1) + " obras entre los años " + date1 + " y " + date2 + ", teniendo un total de " + str(compras) + " obras adquiridas por purchase")
        print("Nombre: " + lt.getElement(mayor,1)["Title"],"Artistas: " + artistofartwork(lt.getElement(mayor,1),catalog) ,"Fecha: " + lt.getElement(mayor,1)["DateAcquired"],",Medio: " + lt.getElement(mayor,1)["Medium"],",Dimensiones: " + lt.getElement(mayor,1)["Dimensions"])
        print("Nombre: " + lt.getElement(mayor,2)["Title"],"Artistas: " + artistofartwork(lt.getElement(mayor,2),catalog) ,",Fecha: " + lt.getElement(mayor,2)["DateAcquired"],",Medio: " + lt.getElement(mayor,2)["Medium"],",Dimensiones: " + lt.getElement(mayor,2)["Dimensions"])
        print("Nombre: " + lt.getElement(mayor,3)["Title"],"Artistas: " + artistofartwork(lt.getElement(mayor,3),catalog) ,",Fecha: " + lt.getElement(mayor,3)["DateAcquired"],",Medio: " + lt.getElement(mayor,3)["Medium"],",Dimensiones: " + lt.getElement(mayor,3)["Dimensions"])
        print("Nombre: " + lt.getElement(menor,1)["Title"],"Artistas: " + artistofartwork(lt.getElement(menor,1),catalog) ,",Fecha: " + lt.getElement(menor,1)["DateAcquired"],",Medio: " + lt.getElement(menor,1)["Medium"],",Dimensiones: " + lt.getElement(menor,1)["Dimensions"])
        print("Nombre: " + lt.getElement(menor,2)["Title"],"Artistas: " + artistofartwork(lt.getElement(menor,2),catalog) ,",Fecha: " + lt.getElement(menor,2)["DateAcquired"],",Medio: " + lt.getElement(menor,2)["Medium"],",Dimensiones: " + lt.getElement(menor,2)["Dimensions"])
        print("Nombre: " + lt.getElement(menor,3)["Title"],"Artistas: " + artistofartwork(lt.getElement(menor,3),catalog) ,",Fecha: " + lt.getElement(menor,3)["DateAcquired"],",Medio: " + lt.getElement(menor,3)["Medium"],",Dimensiones: " + lt.getElement(menor,3)["Dimensions"])
    else:
        sys.exit(0)
sys.exit(0)
