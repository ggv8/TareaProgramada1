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
    Salidas: Retorna string de contenidos si los hay, sino retorna uno vacío"""
    try:
        file = open(pnombre + ".txt", "r")
        contenidos = file.read()
        file.close()
        if contenidos != "":      # Retorna contenidos si los tiene
            return contenidos
        print("\nError: El archivo se encuentra vacío.") # Archivo vacío
    except FileNotFoundError:
        print("\nError: El archivo indicado no existe.") # Archivo no encontrado
    return ""

def revisarTXTAux():
    """ 
    Función: Valida entrada de función revisarTXT según convención de Windows
    Entradas:
        nombre(str) - Nombre y extensión de archivo
    Salidas:
        Retorna contenidos de archivos válidos. De lo contrario, da string vacío"""
    nombre = input("Nombre del archivo de texto: ")
    # Valida que el archivo no tenga nombre o caractéres reservados en Windows
    if re.match('^(?!CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9]$)[^<>:"/|\?*\\\\]{1,256}$', nombre):
        return revisarTXT(nombre)                    # Revisa si existe dicho archivo TXT
    else:
        print("\nError: Nombre inválido de archivo") # Informa sobre nombre inválido
        return ""


##############################################################
#####                Programa Principal                  #####
##############################################################

print(revisarTXTAux()) # Permite probar funciones