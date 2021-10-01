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

# Funciones complementarias

def interfazMenu(ptexto, ptoken):
    """
    Función:    Muestra opciones disponibles a usuario en menú de tokenización
    Entradas:
        ptexto (str) - Texto ingresado o cargado de un archivo
        ptoken (bool) - Indica si tokenización fue o no completada
    Salidas:    Imprime título de menú y opciones
    """
    print("_"*50, "|" + "Sistema de Tokenización".center(48, ' ') + "|", "-"*50, sep="\n")
    print("\n1. Ingresar un texto", "2. Cargar archivo de texto", sep="\n")
    if ptexto != "":    # Si hay un texto cargado, imprime opcion tokenizar
        print("3. Tokenizar texto")
    if ptoken:          # Si se logro tokenizar texto, imprime opciones de salida
        print("4. Generar HTML", "5. General XML", "6. Generar Binario", sep="\n")  
    print('0. Salir del Sistema')

def imprimirError(ptexto):
    """
    Función:    Muestra error a usuario antes de continuar el programa
    Entradas:   ptexto (str) - Mensaje de error
    Salidas:    Imprime título y mensaje de error
    """
    print("", "_"*50, "|" + "Error".center(48, ' ') + "|", "-"*50, sep="\n")
    print("\n" + ptexto.center(50, " ") + "\n")
    input("Continuar <ENTER>".center(50, " "))

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
        if contenidos == "":
            imprimirError("El archivo de texto se encuentra vacío.")
        else:
            print("\nArchivo de texto cargado con éxito.\n")
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
    else:
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
        print("Error: No debe ingresar un texto vacío.")
    return entrada


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
    if pstring == [""]:
        return False
    eliminarRepetidos(pstring)                   # Elimina repetidos
    ordenarLista(pstring)
    clasificarToken(pdocumento, pstring, plista) # y los clasifica
    return True

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

# Considerar que ordenamiento de listas no toma en cuenta tildes :(

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
# "hueso", "pincho", "lugar"... Desconocemos si se podrian generar mas falsos positivos al
# prevenir caracteres antes de hacer match con verbos

Documento = [[],[],[],[],[],[]] # Maneja clasificacion de tokens
texto = ""                      # Texto de archivo o usuario para tokenizar
tokenize = False                # Indicador para estado de tokenizacion
while True:
    print('\nDocumento:', Documento) # Borrar prints al final
    print('Texto:', texto)
    print('Tokenize?:', tokenize, '\n')
    interfazMenu(texto, tokenize)   # Imprime interfaz disponible a usuario
    opcion = input("\nDigite una opción: ")
    if opcion == "0":
        print("\n" + "-- Fin del Programa --".center(50, " ") + "\n")
        break
    elif opcion in ['1', '2']: # Si usuario ingresa un texto nuevo...
        Documento =  [[],[],[],[],[],[]]    # Elimina tokens previos
        tokenize= False                     # Reinicia indicador de tokenización
        if opcion == "1":       # Ingresar texto directamente
            texto = ingresarTXT()
        else:                   # Cargar texto desde archivo txt
            texto = revisarTXTAux()
    elif opcion == "3" and texto != "":  # Permite tokenizar si hay un texto no nulo
        tokenize = tokenizar(Documento, texto, listaRE)
    elif tokenize and opcion in ['4','5','6']: # Si se tokenizo texto, permite opciones [4-6]
        if opcion == "4":
            print("Funcion crearHTML")
        elif opcion == "5":
            print("Funcion crearXML")
        elif opcion == "6":
            print("Funcion crearBinario")
    else:                                   # Informa sobre opciones no disponibles
        imprimirError("Digite una opción válida")
        


a0 = ["Luis", "Anabel", "Juan", "Ana"] # Lista de prueba 1
# Lista esperada: ['Ana', 'Anabel', 'Juan', 'Luis']
    # Resultado: ['Ana', 'Anabel', 'Juan', 'Luis']

a1 = ["Luis", "Anabel", "Juan", "Ana", "almacén"] # Lista de prueba 2
# Lista esperada: ['almacén','Ana', 'Anabel', 'Juan', 'Luis']
    # Resultado: ['almacén','Ana', 'Anabel', 'Juan', 'Luis']
    # To-do: Diseñar algoritmo que reemplaze el actual por uno tipo quick sort
   