# Elaborador por: Ignacio García Galagarza, Gabriel Gomez Vega
# Fecha de creación: 21/09/2021, 12:14 AM
# Última edición: 21/09/2021, XX:XX AM
# Versión: 3.9.6

##############################################################
#####              Importación de Librerías              #####
##############################################################



##############################################################
#####              Definición de Funciones               #####
##############################################################

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
            if plista[index] > elementoB:          # Cambia valores si orden es
                plista[index + 1] = plista[index]  # descendente e incrementa contador
                plista[index] = elementoB
                cambios += 1
            index += 1                 # Pasa al siguiente elemento A
        if cambios == 0:
            return plista  # Si no hay cambios, lista ya fue ordenada


##############################################################
#####                Programa Principal                  #####
##############################################################

a0 = ["Luis", "Anabel", "Juan", "Ana"] # Lista de prueba 1
# Lista esperada: ['Ana', 'Anabel', 'Juan', 'Luis']
    # Resultado: ['Ana', 'Anabel', 'Juan', 'Luis']

a1 = ["Luis", "Anabel", "Juan", "Ana", "almacén"] # Lista de prueba 2
# Lista esperada: ['almacén','Ana', 'Anabel', 'Juan', 'Luis']
    # Resultado: ['Ana', 'Anabel', 'Juan', 'Luis', 'almacén']
    # To-do: Resolver condición que ordena correctamente de manera
    #        alfabética sin distinguir entre mayúscula y minúscula


print(ordenarLista(a1))