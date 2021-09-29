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

# Entrada de Datos

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

# Manejo de Listas

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
    Salidas:    Retorna lista con tokens clasificados en sublistas
    """
    pstring = eliminarSignos(pstring).split(" ") # Tokeniza str por " "
    eliminarRepetidos(pstring)                   # Elimina repetidos
    clasificarToken(pdocumento, pstring, plista) # y los clasifica
    return pdocumento

# Ordenamiento de Listas
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
            if plista[index].lower() > elementoB.lower():          # Cambia valores si orden es
                plista[index + 1] = plista[index]  # descendente e incrementa contador
                plista[index] = elementoB
                cambios += 1
            index += 1                 # Pasa al siguiente elemento A
        if cambios == 0:
            return plista  # Si no hay cambios, lista ya fue ordenada


##############################################################
#####                Programa Principal                  #####
##############################################################

# Guardar expresiones regulares de tokens acá para mejorar claridad visual de funciones
listaRE = ["^(el|la|los|las|un|una|unos|unas|lo|al|del)$",\
           # ^ RE para Articulos
           "^(a|ante|bajo|cabe|con|contra|de|desde|durante|en|entre|hacia|hasta|" + \
           "mediante|para|por|según|sin|so|sobre|tras|versus|vía|cabe|so)$",\
           # ^ RE para Preposiciones
           "^(yo|me|mí|conmigo|nosotros|nosotras|nos|tú|te|ti|contigo|vosotros|" + \
           "vosotras|vos|él|ella|se|consigo|le|les|mío|mía|míos|mías|nuestro|nuestra|" + \
           "nuestros|nuestras|tuyo|tuya|tuyos|vuestro|vuestra|vuestros|vuestras|suyo|" + \
           "suya|suyos|suyas)$",\
           # ^ RE para Pronombres
           "^\w*(ar|er|ir|ando|iendo|ado|ido|to|so|cho)$", "^\d+$"]
           # ^ RE para verbos y luego RE para sólo dígitos

# Por mejorar: RE para verbos participios hace match con textos incorrectos como "texto" o
# "momento". "completo" si aplica (ej "el trabajo esta completo"). En general, queda pendiente
# saber que combinaciones restringir. Otros ejemplos de errores serian "colocho", "tonto", "coso"
# "hueso", "pincho"... Desconocemos si se podrian generar mas falsos positivos al prevenir caracteres
# antes de hacer match con verbos

Documento = [[],[],[],[],[],[]] # Maneja clasificacion de tokens


print(tokenizar(Documento, revisarTXTAux(), listaRE))
a0 = ["Luis", "Anabel", "Juan", "Ana"] # Lista de prueba 1
# Lista esperada: ['Ana', 'Anabel', 'Juan', 'Luis']
    # Resultado: ['Ana', 'Anabel', 'Juan', 'Luis']

a1 = ["Luis", "Anabel", "Juan", "Ana", "almacén"] # Lista de prueba 2
# Lista esperada: ['almacén','Ana', 'Anabel', 'Juan', 'Luis']
    # Resultado: ['almacén','Ana', 'Anabel', 'Juan', 'Luis']
    # To-do: Diseñar algoritmo que reemplaze el actual por uno tipo quick sort

print(ordenarLista(a1))
