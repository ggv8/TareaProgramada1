# Elaborador por: Ignacio García Galagarza, Gabriel Gomez Vega
# Fecha de creación: 21/09/2021, 12:14 AM
# Última edición: 21/09/2021, XX:XX AM
# Versión: 3.9.6

##############################################
###     Import                             ###
##############################################


##############################################
###    Funciones                           ###
##############################################

def sacarTokens(plista):
    """  """
    result = ""
    for token in plista[:-1]:
        result += token + ', '
    result += plista[-1]
    return result

def crearXML(pnombre, pdocumento):
    """  """
    xml = open(pnombre + ".xml", "w")
    xml.write('<?xml version="1.0" encoding="UTF-8 " ?>\n<Documento>\n')
    partes = ["Artículos", "Preposiciones", "Pronombres", "Verbos", "Números", "Sin clasificar"]
    for num in range(6):
        xml.write(f'    <Parte Seccion="{partes[num]}">\n')
        xml.write(f'        <Contenido>"{sacarTokens(pdocumento[num])}"</Contenido>\n')
        xml.write('    </Parte>\n')
    xml.write('</Documento>\n')
    xml.close()
    return ''

def crearHTML(pnombre, pdocumento, ptexto):
    """  """
    html = open(pnombre + ".html", 'w')
    titularHTML(pnombre, html)
    html.write('    <body>\n        <h1>Archivo Original</h1>'+ \
              f'\n        <p>{ptexto}</p>\n')
    crearTabla(pdocumento, html)
    # funcion para hacer reporte
    html.write('    </body>\n</html>')
    html.close()

def titularHTML(pnombre, parchivo):
    """  """
    string = '<!DOCTYPE html>\n<html>\n    <head>\n        <meta charset="utf-8">\n' + \
            f'        <title>{pnombre}</title>\n    </head>\n'
    parchivo.write(string)
    return ''

def crearTabla(pdocumento, parchivo):
    """  """
    partes = ["Artículos", "Preposiciones", "Pronombres", "Verbos", "Números", "Sin clasificar"]
    parchivo.write('        <table border="1">\n            <tr>\n                ')
    parchivo.write('<th colspan=6 > Análisis del documento </th>\n')
    parchivo.write('            </tr>\n            <tr>\n')
    for num in range(6):
        parchivo.write(f'                <th>{partes[num]}</th>\n')
    parchivo.write('            </tr>\n')
    crearFilas(pdocumento, parchivo)
    parchivo.write('        </table>\n')
    return ''

def crearFilas(pdocumento, parchivo):
    """  """
    cantidad = len(max(pdocumento))
    for num in range(cantidad):
        parchivo.write('            <tr  align="center">\n')
        for lista in pdocumento:
            try:
                parchivo.write(f'                <td>{lista[num]}</td>\n')
            except IndexError:
                parchivo.write(f'                <td> - </td>\n')
        parchivo.write('            </tr>\n')
    return ''

##############################################
###    Principal                           ###
##############################################

ejemplo = [["la", "unos", "del"],["a", "para"],\
           ["ella", "mío"],["comer", "lugar"],\
           ["1234", "36"],["comida", "rancho"]]

crearXML("prueba", ejemplo)

crearHTML('a', ejemplo, 'Texto Original')

# Queda pendiente resolver lo siguiente:
    # Función para hacer reporte final del html
    # Encontrar atributo que permita al html mostrar tildes en navegador
    # Documentar codigo y revisar por mejoras
    # Crear funciones para generar archivo binario