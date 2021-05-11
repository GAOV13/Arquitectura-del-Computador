"""
Nombre: Funciones de la Memoria Caché.
Autores: Luis Alberto Salazar y Guido Ernesto Salazar.
Fecha: abril/mayo 2021.
"""

# Total de vias = 2
# Bloques por conjuntos = 32/2 = #16 conjuntos 
# Total de bloques = 32
# Offset = 3
# Index = 4
# Tag = 4/9

# Caché

from Funciones_RAM import modificar_ram, traer_datos_ram
import random

hits = 0
totales = 0
cache = [
    # Primera vía
    {0: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     1: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0},
     2: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0},
     3: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     4: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     5: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0},
     6: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     7: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0},
     8: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0},
     9: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     10: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     11: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     12: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     13: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     14: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     15: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}},
    # Segundo vía
    {0: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     1: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     2: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     3: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     4: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     5: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     6: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     7: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0},
     8: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0},
     9: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     10: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     11: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     12: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     13: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     14: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}, 
     15: {"validez": 0, "tag": "0x000", "data": [], "bit_sucio": 0}}
]

# Funciones auxiliares

def llamarMiss():
    """
    Se encarga de calcular el Miss ratio en toda la ejecución del sistema.
    Entradas: 
        ninguna.
    Salidas: 
        el miss ratio.
    """
    global totales, hits
    try:
        total = hits / totales
    except:
        total = 0
    hratio = 1 - total
    return hratio

def transformacion(numero):
    """
    Se encarga de transformar el entero a su representación binaria en 16 bits.
    Ademas de separar los parametros de busqueda para identificar su posición.
    en cache.
    Entradas:
        numero es un numero en decimal que representa una posición en memoria.
    Salidas
        index: es la posición del conjunto
        tag: el identificador del bloque de memoria que se trajo a cache
        offset: la posición en la lista de datos que se quiere modificar.
    """
    numero = bin(numero)[2:].zfill(16)
    index = int(numero[16-7:16-3], 2) 
    tag = "0x" + hex(int(numero[:16-7], 2))[2:].zfill(3)
    offset = int(numero[16-3:], 2)
    return (index, tag, offset)

def verificarMiss(numero):
    """
    Se encarga de verificar si en el conjunto indicado existe un miss o un hit.
    Entradas: 
        un número entero.
    Salidas: 
        una tupla con el valor de verdad de la verificación, la vía de
        la caché, el indice del conjunto, la etiqueta del conjunto y por
        último el valor en bits del offset.
    """
    global cache, hits, totales
    totales += 1
    index, tag, offset = transformacion(numero)
    ver, pos = False, 0
    if cache[0][index]["validez"] == 0: pos = 0
    elif cache[0][index]["validez"] == 1 and cache[0][index]["tag"] == tag: ver, pos = True, 0
    elif cache[1][index]["validez"] == 0: pos = 1
    elif cache[1][index]["validez"] == 1 and cache[1][index]["tag"] == tag: ver, pos = True, 1
    else: pos = random.randrange(1000) % 2
    if ver: hits += 1
    return (ver, pos, index, tag, offset)

def traer_cache(pos, index, tag):
    """
    Se encarga de cambiar los valores en la caché según la posición indicada.
    Entradas:
        la vía de la memoria, el índice en la caché y el tag del bloque.
    Salidas:
        ninguna.
    """
    global cache
    if cache[pos][index]["bit_sucio"] == 1: modificar_ram(index, cache[pos][index]["tag"], cache[pos][index]["data"])
    cache[pos][index]["bit_sucio"] = 0
    cache[pos][index]["validez"] = 1
    cache[pos][index]["tag"] = tag
    cache[pos][index]["data"] = traer_datos_ram(index, tag)

# Interfaz

def escribir_cache(numero, dato):
    """
    Procedimiento que se encarga de escribir en la cache.
    Entradas:
        numero: Es la posición en memoria que se quiere escribir
        dato: es la información que se quiere guardar en memoria.
    Salidas:
        ninguna.
    """
    global cache
    pos, index, offset = general(numero)
    cache[pos][index]["data"][offset] = dato
    cache[pos][index]["bit_sucio"] = 1
    ver_cache("escribir el dato={} en la posicion={}".format(dato, numero))

def leer_cache(numero):
    """
    Procedimiento que lee un dato de la cache
    Entradas:
        numero: es la posición de memoria que se quiere leer.
    Salidas:
        el dato que hay en la cache.
    """
    global cache
    pos, index, offset = general(numero)
    ver_cache("Leer la posicion={}".format(numero))
    return cache[pos][index]["data"][offset]

def general(numero):
    """
    Funcion que se encarga de hacer las operaciónes generales sin importar si es
    lectura o escritura.
    Entradas:
        numero: es la posición de memoria con que se va a trabajar.
    Salisas:
        pos: es la via en donde se encuentra el dato.
        index: es el conjunto en donde se encuentra el dato.
        offset: la posición del dato en el bloque.
    """
    global cache
    ver, pos, index, tag, offset = verificarMiss(numero)
    if not ver: traer_cache(pos, index, tag)
    return pos, index, offset

def ver_cache(instruccion):
    """
    Procedimiento que permite visualizar los cambios en cache por instrucción.
    Entradas:
        instruccion: es un string que nos dice la información de lo que se ejecuto.
    Salidas:
        Cache.txt: un archivo de texto en donde se mostrara el cambio a lo largo del 
        tiempo.
    """
    global cache
    f = open("Cache.txt", "a")
    f.write("----------------------------------------------------------------------------------------------------\n")
    f.write("En el numero de consulta {} se hizo la instrucción {} y la cache es:\n".format(totales, instruccion))
    i = 1
    for via in cache:
        f.write("Estos son los datos en la via {}\n".format(i))
        for posicion in via:
            f.write(str(posicion) + " " + str(via[posicion]) + "\n")
        i += 1
    f.close()