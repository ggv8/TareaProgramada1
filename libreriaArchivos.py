# Elaborador por: Ignacio García Galagarza, Gabriel Gomez Vega
# Fecha de creación: 21/09/2021, 12:14 AM
# Última edición: 21/09/2021, XX:XX AM
# Versión: 3.9.6

##############################################################
#####              Definición de Funciones               #####
##############################################################

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
    for num in range(cantidad):     # Genera filas según mayor de cantidad de tokens
        parchivo.write('            <tr  align="center">\n') # Fila y contenido centrado
        for lista in pdocumento:    # Genera celdas en fila
            try:                        # Reparte tokens por columna
                parchivo.write(f'                <td>{lista[num]}</td>\n')
            except IndexError:          # Si no hay más tokens, muestra "-"
                parchivo.write('                <td> - </td>\n')
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