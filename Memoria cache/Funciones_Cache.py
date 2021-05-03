"""
Nombre: Funciones de la Memoria Caché.
Autores: Luis Alberto Salazar y Guido Ernesto Salazar.
Fecha: abril/mayo 2021.
"""

# Total de vias = 2
# Bloques por conjuntos = 32/2 = 16
# Total de bloques = 32
# Offset = 3
# Index = 4
# Tag = 4/9
# Tamaño del bus (antes de preguntarle a maribell) 11 o 16 bits

# Caché

from Funciones_RAM import modificar_ram, traer_datos_ram
import random

miss = 0
cache = [
    #Primer conjunto
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
    #Segundo conjunto
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
]

def transformacion(numero):
    numero = bin(numero)[2:].zfill(16)
    index = int(numero[16-7:16-3], 2) 
    tag = "0x" + hex(int(numero[:16-7], 2))[2:].zfill(3)
    offset = int(numero[16-3:], 2)
    return (index, tag, offset)

def verificarMiss(numero):
    global cache
    index, tag, offset = transformacion(numero)
    ver, pos = False, 0
    if cache[0][index]["validez"] == 0: pos = 0
    elif cache[0][index]["validez"] == 1 and cache[0][index]["tag"] == tag: ver, pos = True, 0
    elif cache[1][index]["validez"] == 0: pos = 1
    elif cache[1][index]["validez"] == 1 and cache[1][index]["tag"] == tag: ver, pos = True, 1
    else: pos = random.randrange(1000) % 2
    return (ver, pos, index, tag, offset)

def traer_cache(pos, index, tag):
    global cache
    print("valore(pos:{}|index:{}|tag:{})".format(pos, index, tag))
    if cache[pos][index]["bit_sucio"] == 1: modificar_ram(index, cache[pos][index]["tag"], cache[pos][index]["data"])
    print("perro")
    cache[pos][index]["bit_sucio"] == 0
    cache[pos][index]["validez"] = 1
    cache[pos][index]["tag"] = tag
    cache[pos][index]["data"] = traer_datos_ram(index, tag)

# Interfaz

def escribir_cache(numero, dato):
    global cache
    pos, index, offset = general(numero)
    cache[pos][index]["data"][offset] = dato
    cache[pos][index]["bit_sucio"] = 1

def leer_cache(numero):
    global cache
    print(type(numero))
    pos, index, offset = general(numero)
    print(cache[pos][index]["data"])
    return cache[pos][index]["data"][offset]

def general(numero):
    global cache
    ver, pos, index, tag, offset = verificarMiss(numero)
    if not ver: traer_cache(pos, index, tag)
    f = open("output.txt", "w")
    for conjunto in cache:
        f.write("Estos son los datos del conjunto\n")
        for posicion in conjunto:
            f.write(str(posicion) + " " + str(conjunto[posicion]) + "\n")
    f.close()
    return pos, index, offset