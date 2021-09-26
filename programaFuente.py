# Elaborador por: Ignacio García Galagarza, Gabriel Gomez Vega
# Fecha de creación: 21/09/2021, 12:14 AM
# Última edición: 21/09/2021, XX:XX AM
# Versión: 3.9.6

import re

texto = "a! del a560, hola y del, mundo, pedro, copiar, cantando, nosotros y ante contra, el, los"

# Guardar expresiones regulares de tokens aca para mejorar claridad visual de funciones
listaRE = ["^(el|la|los|las|un|una|unos|unas|lo|al|del)$",\

           "^(a|ante|bajo|cabe|con|contra|de|desde|durante|en|" + \
           "entre|hacia|hasta|mediante|para|por|según|sin|so|" + \
           "sobre|tras|versus|vía|cabe|so)$"]

# Por mejorar:
    # 25/09 - Problema de elementos repetidos. Ej. "Ante" y "ante"
    # son diferentes para un computadora y eliminarRepetidos no
    # cubre esos casos. Tampoco se puede tomar todo en minúscula
    # pues nombres propios deben iniciar con mayúscula.
    # Por el momento, solo solucionar repeticiones obvias y terminar
    # de hacer re.matches para otras clasificaciones de tokens

Documento = [[],[],[],[],[],[]] # Maneja clasificacion de tokens

def eliminarRepetidos(plista):
    """
    Función:    Genera lista con elementos únicos a partir de entrada
    Entradas:   plista (list) - Lista a analizar
    Salidas:    Retorna lista generada
    """
    result = []
    for elemento in plista:
        if elemento not in result: # Agrega cada elemento una vez
            result.append(elemento)
    return result

def eliminarSignos(pstring):
    """  """
    nuevo = ""
    for caracter in pstring:
        if caracter not in ",.:;-¿?¡!<>":
            nuevo += caracter
    return nuevo

def tokenizar(pdocumento, pstring, plista):
    """  """
    pstring = eliminarSignos(pstring)
    pstring = pstring.split(" ")
    pstring = eliminarRepetidos(pstring)
    clasificarToken(pdocumento, pstring, plista)

# Documento[0] - Articulos
    # el, la, los, las, un, una, unos, unas, lo, al, del

# Documento[1] - Preposiciones
    # a, ante, bajo, cabe, con, contra, de, desde, durante, en, entre, hacia, hasta, 
    # mediante, para, por, según, sin, so, sobre, tras, versus y vía, cabe y so

# Documento[2] - Pronombres
    # yo, me, mí, conmigo, nosotros, nosotras, nos, tú, te, ti, contigo, vosotros, 
    # vosotras, vos, él, ella, se, consigo, le, les.
    # Mío, mía, míos, mías, nuestro, nuestra, nuestros, nuestras, tuyo, tuya, 
    # tuyos, vuestro, vuestra, vuestros, vuestras, suyo, suya, suyos, suyas. 

# Documento[3] - Verbos
    # Infinitivos = terminados en -ar, -er, -ir
    # Gerundios = terminados en -ando, -iendo
    # Participio = terminados en ado, ido, to, so, cho

# Documento[4] - Números
    # Solo numeros enteros

# Documento[5] - Sin clasificar
    # Lo que sobre

def clasificarToken(pdocumento, ptokens, plista):
    """
    Función:
    Entradas:
        pdocumento (list) - Donde se almacenan tokens según categoría
        ptokens (list) - Lista no categorizada de tokens
        plista (list) - Lista con strings para validar en re.match
    Salidas:
    """
    while len(ptokens) != 0:
        print("Quedan", len(ptokens), "tokens por analizar")
        token = ptokens[0]
        if re.match(plista[0], token):
            print( re.match(plista[0], token) )
            pdocumento[0].append( token )
        elif re.match(plista[1], token):
            print( re.match(plista[1], token) )
            pdocumento[1].append( token )
        del ptokens[0]
    print(pdocumento)
    print(ptokens)

tokenizar(Documento, texto, listaRE)