# Elaborador por: Ignacio García Galagarza, Gabriel Gomez Vega
# Fecha de creación: 21/09/2021, 12:14 AM
# Última edición: 21/09/2021, XX:XX AM
# Versión: 3.9.6

##############################################################
#####              Importación de Librerías              #####
##############################################################

import re, pickle, datetime

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

def crearNombre():
    """
    Función:    Genera string para nombrar archivos HTML y XML
    Entradas:   N/A
    Salidas:    Retorna string de nombre con fecha de creación
    """
    fecha = datetime.datetime.now() # Obtiene fecha y tiempo
    fecha = fecha.strftime("%d-%m-%Y-%H-%M-%S") # Formato a dd-mm-aaaa-hh-mm-ss
    return f"Analisis-{fecha}"

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

# Creación de HTML

def crearHTML(pnombre, pdocumento, ptexto):
    """
    Función:    Genera documento HTML a partir de lista de tokens
    Entradas:
        pnombre (str) - Nombre del documento a generar
        pdocumento (list) - Lista de tokens clasificados en sublistas
        ptexto (str) - Texto de archivo original
    Salidas:    Retorna mensaje al finalizar el HTML
    """
    # Valores para headers de tablas y listado en reporte
    strings = ["Artículos", "Preposiciones", "Pronombres",\
               "Verbos", "Números", "Sin clasificar"]
    html = open(pnombre + ".html", 'w', encoding="utf-8")
    crearParrafo(pnombre, ptexto, html)     # Estructura inicial y parrafo de texto
    crearTabla(pdocumento, html, strings)   # Tabla de analisis del documento
    crearReporte(pdocumento, html, strings) # Reporte de cantidad de tokens
    html.write('    </body>\n</html>')  # Cierra tags de cuerpo y html
    html.close()
    return f'{pnombre}.html ha sido creado con éxito.'

def crearParrafo(pnombre, ptexto, parchivo):
    """
    Función:    Genera tags básicos del html, títulos y texto original
    Entradas:
        pnombre (str) - Nombre del documento
        ptexto (str) - Texto de archivo original
        parchivo - Archivo html abierto para edición
    Salidas:    Tags dentro del archivo html
    """
    parchivo.write(f"""<!DOCTYPE html>\n<html lang="es">\n    <head>\n        <meta charset="utf-8">
        <title>{pnombre}</title>\n    </head>\n    <body>
        <h1>Archivo Original</h1>\n        <p>{ptexto}</p>\n""")
    return ''

def crearTabla(pdocumento, parchivo, pstrings):
    """
    Función:    Genera tags y atributos para tabla de análisis
    Entradas:
        pdocumento (list) - Lista de tokens clasificados en sublistas
        parchivo - Archivo html abierto para edición
        pstrings (list) - Listado con strings para headers en tabla
    Salidas:    Tags dentro del archivo html
    """
    # Tags para iniciar tabla con bordes y su título
    parchivo.write('        <table border="1">\n            <tr>\n                '+\
    '<th colspan=6 > Análisis del documento </th>\n            </tr>\n            <tr>\n')
    for num in range(6):    # Crea headers de clasificacion tokens
        parchivo.write(f'                <th>{pstrings[num]}</th>\n')
    parchivo.write('            </tr>\n')   # Cierra fila de headers
    crearFilas(pdocumento, parchivo)        # Genera filas con tokens ordenados
    parchivo.write('        </table>\n')    # Cierra tag de tabla
    return ''

def crearFilas(pdocumento, parchivo):
    """
    Función:    Genera filas de tokens para tabla de análisis
    Entradas:
        pdocumento (list) - Lista de tokens clasificados en sublistas
        parchivo - Archivo html abierto para edición
    Salidas:    Tags dentro del archivo html
    """
    cantidad = max( contarTokens(pdocumento)[1:] )
    print("Mayor cantidad", cantidad)
    for num in range(cantidad):     # Genera filas según mayor de cantidad de tokens
        parchivo.write('            <tr  align="center">\n') # Fila y contenido centrado
        for lista in pdocumento:    # Genera celdas en fila
            try:                        # Reparte tokens por columna
                parchivo.write(f'                <td>{lista[num]}</td>\n')
            except IndexError:          # Si no hay más tokens, muestra "-"
                parchivo.write(f'                <td> - </td>\n')
        parchivo.write('            </tr>\n')   # Cierra fila
    return ''

def contarTokens(pdocumento):
    """
    Función:    Crea lista con datos de cantidad de tokens
    Entradas:   pdocumento (list) - Tokens clasificados en sublistas
    Salidas:    Retorna lista numérica con contadores
    """
    contador = [0]  # Inicia con contador total
    for lista in pdocumento:
        cantidad = len(lista)       # Obtiene cantidad en sublista
        contador[0] += cantidad     # Acumula conteo total
        contador.append(cantidad)   # Agrega conteo de sublista
    return contador

def crearReporte(pdocumento, parchivo, pstrings):
    """
    Función:    Genera título, párrafo y listado para reporte de tokens
    Entradas:
        pdocumento (list) - Tokens clasificados en sublistas
        parchivo - Archivo html abierto para edición
        pstrings (list) - Strings para cantidades en reporte
    Salidas:    Tags dentro del archivo html
    """
    lista = contarTokens(pdocumento)    # Cantidades de tokens
    # Titula reporte y crea párrafo de cantidad total de tokens
    parchivo.write(f"""        <h2>Reporte</h2>
        <p>El texto original tiene {lista[0]} tokens de los cuales hay:</p>
        <ul>\n""")  # Inicia tag de lista no ordenada
    for num in range(1,7):  # Crea listado de cantidades por sublista
        parchivo.write(f'            <li>{lista[num]} {pstrings[num-1]}</li>\n')
    parchivo.write('        </ul>\n')   # Cierra tag de lista
    return ''

# Creacion de XML

def sacarTokens(plista):
    """
    Función:    Obtiene tokens de lista para contenido XML
    Entradas:   plista (list) - Lista de tokens de una parte
    Salidas:    Retorna tokens ordenados en un string
    """
    result = ""     # Acumulador
    if plista != []:
        for token in plista[:-1]:   # Concatena tokens seguido de ', '
            result += token + ', '
        result += plista[-1] # Agrega último token sin ', '
    return result

def crearXML(pnombre, pdocumento):
    """
    Función:    Genera documento XML a partir de lista de tokens
    Entradas:
        pnombre (str) - Nombre del documento a generar
        pdocumento (list) - Lista de tokens clasificados en sublistas
    Salidas:    Retorna mensaje al finalizar el XML
    """
    # Valores para <Parte Seccion=>
    strings = ["Artículos", "Preposiciones", "Pronombres",\
              "Verbos", "Números", "Sin clasificar"]
    xml = open(f"{pnombre}.xml", "w", encoding="utf-8")   # Crea XML con UTF-8 e inicia root
    xml.write('<?xml version="1.0" encoding="UTF-8" ?>\n<Documento>\n')
    for num in range(6):        # Crea elementos respectivos por cada sublista
        xml.write(f'    <Parte Seccion="{strings[num]}">\n')
        xml.write(f'        <Contenido>{sacarTokens(pdocumento[num])}</Contenido>\n')
        xml.write('    </Parte>\n') # Cierra tag de elemento
    xml.write('</Documento>\n') # Cierra root de XML
    xml.close()
    return f'{pnombre}.xml ha sido creado con éxito.'

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
        print("\n" + "-- Gracias por usar el sistema --".center(50, " ") + "\n")
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
            print('\n' + crearHTML( crearNombre(), Documento, texto) + '\n')
        elif opcion == "5":
            print('\n' + crearXML( crearNombre(), Documento) + '\n')
        elif opcion == "6":
            crearBinario(Documento)
    else:                                   # Informa sobre opciones no disponibles
        imprimirError("Digite una opción válida")


# Por mejorar: RE para verbos participios hace match con textos incorrectos como "texto" o
# "momento". "completo" si aplica (ej "el trabajo esta completo"). En general, queda pendiente
# saber que combinaciones restringir. Otros ejemplos de errores serian "colocho", "tonto", "coso"
# "hueso", "pincho", "lugar"... Desconocemos si se podrian generar mas falsos positivos al
# prevenir caracteres antes de hacer match con verbos
