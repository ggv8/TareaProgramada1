# Elaborador por: Ignacio García Galagarza, Gabriel Gomez Vega
# Fecha de creación: 21/09/2021, 12:14 AM
# Última edición: 08/10/2021, 06:00 AM
# Versión: 3.9.6

##############################################################
#####              Importación de Librerías              #####
##############################################################

from libreriaEntradas import ingresarTXT, revisarTXTAux
from libreriaListas import tokenizar
from libreriaArchivos import crearHTML, crearXML
from libreriaBinario import crearBinario
from libreriaExtra import crearNombre, imprimirError

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
    print('', "_"*50, "|" + "Sistema de Tokenización".center(48, ' ') + "|", "-"*50, sep="\n")
    print("\n1. Ingresar un texto", "2. Cargar archivo de texto", sep="\n")
    if ptexto != "":    # Si hay un texto cargado, imprime opcion tokenizar
        print("3. Tokenizar texto")
    if ptoken:          # Si se logro tokenizar texto, imprime opciones de salida
        print("4. Generar HTML", "5. General XML", "6. Generar Binario", sep="\n")  
    print('0. Salir del Sistema')

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
    interfazMenu(texto, tokenize)   # Imprime interfaz disponible a usuario
    opcion = input("\nDigite una opción: ")
    if opcion == "0":
        print("\n" + "-- Gracias por usar el sistema --".center(50, " ") + "\n")
        break
    elif opcion in ['1', '2']: # Si usuario ingresa un texto nuevo...
        Documento =  [[],[],[],[],[],[]]    # Elimina tokens previos
        tokenize = False                     # Reinicia indicador de tokenización
        if opcion == "1":       # Ingresar texto directamente
            texto = ingresarTXT()
        else:                   # Cargar texto desde archivo txt
            texto = revisarTXTAux()
    elif opcion == "3" and texto != "":  # Permite tokenizar si hay un texto no nulo
        tokenize = tokenizar(Documento, texto, listaRE)
    elif tokenize and opcion in ['4','5','6']: # Si se tokenizo texto, permite opciones [4-6]
        if opcion == "4":
            print('\n' + crearHTML( crearNombre(), Documento, texto) + '\n')
            input("<ENTER> Continuar".center(50, " "))
        elif opcion == "5":
            print('\n' + crearXML( crearNombre(), Documento) + '\n')
            input("<ENTER> Continuar".center(50, " "))
        elif opcion == "6":
            crearBinario(Documento)
    else:                                   # Informa sobre opciones no disponibles
        imprimirError("Digite una opción válida")