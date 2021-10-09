# Elaborador por: Ignacio García Galagarza, Gabriel Gomez Vega
# Fecha de creación: 21/09/2021, 12:14 AM
# Última edición: 08/10/2021, 06:00 AM
# Versión: 3.9.6

##############################################################
#####              Importación de Librerías              #####
##############################################################

import re

from libreriaExtra import imprimirError

##############################################################
#####              Definición de Funciones               #####
##############################################################

# Entrada de Datos

def revisarTXT(pnombre):
    """
    Función: Obtiene contenidos de un archivo válido
    Entradas: pnombre(str) - Nombre de archivo
    Salidas: Retorna string de contenidos si los hay, sino retorna uno vacío"""
    try:
        file = open(pnombre + ".txt", "r", encoding="utf-8")
        contenidos = file.read()
        file.close()
        if contenidos == "":
            imprimirError("El archivo de texto se encuentra vacío.")
        else:
            print("", "Archivo de texto cargado con éxito.".center(50, " "), "", sep="\n")
            input("Continuar <ENTER>".center(50, " "))
        return contenidos
    except FileNotFoundError: # Archivo no hallado o no existe
        imprimirError("Archivo indicado no está o no existe.")
    return ""

def revisarTXTAux():
    """
    Función: Valida entrada de función revisarTXT según convención de Windows
    Entradas:
        nombre(str) - Nombre y extensión de archivo
    Salidas:
        Retorna contenidos de archivos válidos. De lo contrario, da string vacío"""
    print("_"*50, "|" + "Manejo de Archivos".center(48, ' ') + "|", "-"*50, sep="\n")
    nombre = input("Nombre del archivo de texto: ")
    # Valida que el archivo no tenga nombre o caractéres reservados en Windows
    if re.match('^(?!CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9]$)[^<>:"/|\?*\\\\]{1,256}$', nombre):
        return revisarTXT(nombre)                    # Revisa si existe dicho archivo TXT
    imprimirError("Nombre inválido de archivo.") # Informa sobre nombre inválido
    return ""

def ingresarTXT():
    """
    Función:    Valida entradas directas de texto en sistema de tokenización
    Entradas:   entrada (str) - Texto que usuario ingrese
    Salidas:    Imprime error si usuario ingresa str nulo
    """
    print("_"*50, "|" + "Entrada de Texto".center(48, ' ') + "|", "-"*50, sep="\n")
    entrada = input("Escriba texto a cargar: ")
    if entrada == "":
        imprimirError("No debe ingresar un texto vacío.")
    else:
        print("", "Texto cargado con éxito.".center(50, " "), "", sep="\n")
        input("Continuar <ENTER>".center(50, " "))
    return entrada
