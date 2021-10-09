# Elaborador por: Ignacio García Galagarza, Gabriel Gomez Vega
# Fecha de creación: 21/09/2021, 12:14 AM
# Última edición: 08/10/2021, 06:00 AM
# Versión: 3.9.6

##############################################################
#####              Importación de Librerías              #####
##############################################################

import pickle

from libreriaListas import eliminarRepetidos, ordenarLista

##############################################################
#####              Definición de Funciones               #####
##############################################################

# Creacion de BD

def crearBinario(pdocumento):
    """
    Función:    Crea o actualiza archivo binario BD
    Entradas:   pdocumento (list) - Tokens clasificados en sublistas
    Salidas:    Muestra contenidos binarios con funcion auxiliar
    """
    contenido = buscarBD()      # Recupera contenidos de BD si existen
    file = open("BD", 'wb')
    if contenido is None:       # Si no hay contenidos, agrega lista de tokens
        pickle.dump( pdocumento, file )
    else:                       # De lo contrario, actualiza lista de tokens en BD
        pickle.dump( actualizarBD(pdocumento, contenido), file)
    file.close()
    return mostrarBD( buscarBD() )  # Funcion auxiliar para mostrar contenido binario

def buscarBD():
    """
    Función:    Verifica si existe Base de Datos previa
    Entradas:   N/A
    Salidas:    Retorna contenidos de BD. De lo contrario, retorna None
    """
    try:
        file = open('BD', 'rb')
        contenido = pickle.load(file)
        file.close()
        return contenido
    except (EOFError, FileNotFoundError): # None indica BD no existente o vacía
        return None

def actualizarBD(pdocumento, pregistro):
    """
    Función:    Guarda tokens nuevos en contenido binario
    Entradas:
        pdocumento (list) - Tokens clasificados en sublistas
        pregistro (list) - Contenido binario de tokens ya procesados
    Salidas:    Retorna contenido binario con nuevos tokens
    """
    for index in range(6):  # Por cada sublista de tokens
        pregistro[index].extend( pdocumento[index] )  # Agrega nuevos tokens a lista previa
        eliminarRepetidos(pregistro[index])
        ordenarLista(pregistro[index])
    return pregistro

def mostrarBD(pcontenido):
    """
    Función:    Muestra contenido binario ordenado en shell
    Entradas:   pcontenido (list) - Contenido de archivo BD
    Salidas:    Imprime cada parte sección de BD
    """
    # Strings para titular cada parte de impresión en shell
    strings = ["Artículos", "Preposiciones", "Pronombres",\
               "Verbos", "Números", "Sin clasificar"]
    print("_"*80 + "\n|" + "Contenido Binario".center(78, ' ') + "|\n" + "-"*80 )
    for index in range(6):  # Imprime cada subtítulo y lista respectiva
        print(f"Parte Sección: {strings[index]}" + "\n")
        print(pcontenido[index], "\n")
    print('  Fin del contenido binario  '.center(80, "=") + "\n")
    input("<ENTER> Continuar".center(80, " "))
    return ''
