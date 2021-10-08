# Elaborador por: Ignacio García Galagarza, Gabriel Gomez Vega
# Fecha de creación: 21/09/2021, 12:14 AM
# Última edición: 21/09/2021, XX:XX AM
# Versión: 3.9.6

##############################################################
#####              Importación de Librerías              #####
##############################################################

import datetime

##############################################################
#####              Definición de Funciones               #####
##############################################################

def imprimirError(ptexto):
    """
    Función:    Muestra error a usuario antes de continuar el programa
    Entradas:   ptexto (str) - Mensaje de error
    Salidas:    Imprime título y mensaje de error
    """
    print("", "_"*50, "|" + "Error".center(48, ' ') + "|", "-"*50, sep="\n")
    print("\n" + ptexto.center(50, " ") + "\n")
    input("Continuar <ENTER>".center(50, " "))

def crearNombre():
    """
    Función:    Genera string para nombrar archivos HTML y XML
    Entradas:   N/A
    Salidas:    Retorna string de nombre con fecha de creación
    """
    fecha = datetime.datetime.now() # Obtiene fecha y tiempo
    fecha = fecha.strftime("%d-%m-%Y-%H-%M-%S") # Formato a dd-mm-aaaa-hh-mm-ss
    return f"Analisis-{fecha}"