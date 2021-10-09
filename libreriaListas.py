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

def eliminarRepetidos(plista):
    """
    Función:    Elimina repetidos de lista empezando por elementos finales
    Entradas:   plista (list) - Lista a analizar
    Salidas:    Retorna lista tras cambios
    """
    index = -1  # Var. de control para indices de derecha a izq.
    for elemento in plista[::-1]: # Analiza lista desde el final
        if plista.count(elemento) != 1: 
            del plista[index]   # Si elemento esta repetido, lo elimina
            index += 1  # Retrocede 1, compensa reposicionamiento al borrar repetidos
        index -= 1 # Pasa al siguiente elemento
    if "" in plista:
        del plista[plista.index("")]
    return plista

def eliminarSignos(pstring):
    """
    Función:    Elimina todo signo de puntuación de un string
    Entradas:   pstring (str) - String de texto extraído
    Salidas:    Retorna mismo string sin signos de puntuación
    """
    index = 0   # Var. de control para posición de elementos
    for char in pstring:            # Busca signos de puntuación
        if char in ",.:;-¿?¡!<>":   # Actualiza pstring, excluyendo caracter
            pstring = pstring[:index] + pstring[index + 1:]
            index -= 1   # Compensa reposicionamiento al excluir un caracter
        elif char == "\n":
            pstring = pstring[:index] + " " + pstring[index + 1:]
        index += 1     # Pasa a la siguiente posición
    return pstring

def incluirToken(plista, ptoken):
    """
    Función:    Incluye token clasificado si no está en sublista
    Entradas:
        plista (list) - Sublista para almacenar categoría de tokens
        ptoken (str) - Token identificado dentro de una categoría
    Salidas:    Retorna sublista tras cambios
    """
    if ptoken not in plista:
        plista.append(ptoken)
    return plista

def clasificarToken(pdocumento, ptokens, plista):
    """
    Función:    Organiza tokens uno a uno por categoría
    Entradas:
        pdocumento (list) - Almacena tokens según categoría
        ptokens (list) - Lista de tokens no categorizados
        plista (list) - Lista con strings para validar en re.match
    Salidas:    Retorna tokens clasificados por sublistas
    """
    while ptokens != []:    # Analiza hasta que no queden más tokens
        token = ptokens[0].lower()  # Copia del token en minúscula
        if re.match(plista[0], token):          # Artículos
            incluirToken(pdocumento[0], token)
        elif re.match(plista[1], token):        # Preposiciones
            incluirToken(pdocumento[1], token)
        elif re.match(plista[2], token):        # Pronombres
            incluirToken(pdocumento[2], token)
        elif re.match(plista[3], token):        # Verbos
            incluirToken(pdocumento[3], token)
        elif re.match(plista[4], token):        # Números
            incluirToken(pdocumento[4], token)
        else:                   # Sin clasificar, agrega token original evitando incluir
            pdocumento[5].append( ptokens[0] ) # posibles nombres propios en minúscula
        del ptokens[0]  # Borra token tras copiarlo en pdocumento
    return pdocumento

def tokenizar(pdocumento, pstring, plista):
    """
    Función:    Convierte contenidos de un str en tokens organizados
    Entradas:
        pdocumento (list) - Lista con sublistas para categorizar tokens
        pstring (str) - String del cuál se extraen tokens
        plista (list) - Lista con strings para re.match()
    Salidas:    Retorna True si tokenizo texto, False si no
    """
    pstring = eliminarSignos(pstring).split(" ") # Tokeniza str por " "
    eliminarRepetidos(pstring)                   # Elimina repetidos
    if pstring == [""] or pstring == []:
        imprimirError("Texto no pudo tokenizarse.")
        return False
    ordenarLista(pstring)
    clasificarToken(pdocumento, pstring, plista) # y los clasifica
    print("", "Texto tokenizado con éxito.".center(50, " "), "", sep="\n")
    input("Continuar <ENTER>".center(50, " "))
    return True

# Ordenamiento de Listas

def cambiarLetras(ppalabra):
    """
    Función:    Complementa ordenarLista para ordenar acentos apropiadamente
    Entradas:   ppalabra (str) - Token a modificar
    Salidas:    Retorna copia modificada para tomar acentos como su caracter no acentuado
    """
    letrasA = ["á","é","í","ó","ú","ñ"] # Letras a reemplazar
    letrasB = ["a","e","i","o","u","n"] # Contrapartes para reemplazar
    ppalabra = ppalabra.lower()     # Toma palabra como si fuese toda en minúscula
    result = ""                     # Acumula caracteres
    for caracter in ppalabra:
        try:    # Si halla un caracter a reemplazar, acumula su contraparte
            result += letrasB[ letrasA.index(caracter) ]
        except ValueError:  # De lo contrario, agrega caracter original
            result += caracter
    return result

def ordenarLista(plista):
    """
    Función:    Ordenamiento burbuja según alfabeto para lista de strings
    Entradas:   plista (list) - Lista de strings para tokens
    Salidas:    Retorna lista con elementos ordenados
    """
    while True:
        index = 0     # Indice para accesar un elemento A
        cambios = 0   # Contador/Var.Control para saber cambios realizados
        for elementoB in plista[1:]:   # Compara elementos A y B de izq a derecha
            # Condicion: Cambia valores si orden es descendente e incrementa contador
            if cambiarLetras( plista[index] ) > cambiarLetras(elementoB):
                plista[index + 1] = plista[index]
                plista[index] = elementoB
                cambios += 1
            index += 1                 # Pasa al siguiente elemento A
        if cambios == 0:
            return plista  # Si no hay cambios, lista ya fue ordenada
