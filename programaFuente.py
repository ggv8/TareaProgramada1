# Elaborador por: Ignacio García Galagarza, Gabriel Gomez Vega
# Fecha de creación: 21/09/2021, 12:14 AM
# Última edición: 21/09/2021, XX:XX AM
# Versión: 3.9.6

##############################################################
#####              Importación de Librerías              #####
##############################################################

import re

##############################################################
#####              Definición de Funciones               #####
##############################################################

def revisarTXT(pnombre):
    """ 
    Función: Obtiene contenidos de un archivo válido
    Entradas: pnombre(str) - Nombre de archivo
    Salidas: Retorna contenidos de archivos existentes y no vacios"""
    try:
        file = open(pnombre, "r")
        if file.read() != "":      # Retorna contenidos si los tiene
            return file.read()
        print("\nError: El archivo se encuentra vacío.") # Archivo vacío
    except FileNotFoundError:
        print("\nError: El archivo indicado no existe.") # Archivo no encontrado

def revisarTXTAux():
    """ 
    Función: Valida entrada de función revisarTXT
    Entradas:
        nombre(str) - Nombre y extensión de archivo
    Salidas:
        Retorna contenidos de archivos válidos"""
    nombre = input("Nombre completo de archivo de texto: ")
    if re.match("[\w,\W]+?.txt", nombre): # Valida por lo menos un caracter y extensión txt
        return revisarTXT(nombre)
    else:
        print("\nError: Extensión inválida, ingrese nombre de archivo .txt")
    return ""


##############################################################
#####                Programa Principal                  #####
##############################################################

revisarTXTAux()