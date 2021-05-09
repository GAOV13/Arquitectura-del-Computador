"""
Nombre: Funciones de la Memoria RAM.
Autores: Luis Alberto Salazar y Guido Ernesto Salazar.
Fecha: abril/mayo 2021.
"""
import random
import string

# Funciones RAM

def inicializar_ram():
    """
    Se encarga de inicializar toda las posiciones de la memoria RAM con distintos
    valores del alfabeto.
    Entradas:
        ninguna.
    Salidas:
        ninguna.
    """
    f = open("RAM.txt", "w")
    letters = string.ascii_lowercase
    palabra = ''.join(random.choice(letters) for i in range(8))
    for i in range(0, 2048):
        f.write(palabra + '\n')
        palabra = ''.join(random.choice(letters) for i in range(8))
    f.write(palabra)
    f.close()

def modificar_ram(index, tag, data):
    """
    Se encarga de aplicar la política de Right-Back en la memoria RAM, cambiando
    los valores que tiene la posición indicada, en este caso cambia los valores
    del rango de datos que tiene asignado.
    Entradas:
        el índice de la memoria caché, el tag del bloque y el rango de datos que
        tiene arraigado.
    Salidas:
        ninguna.
    """
    f = open("RAM.txt", "r")
    lista = f.readlines()
    f.close()
    index = bin(index)[2:].zfill(4)
    tag = bin(int(tag, 16))[2:].zfill(9)
    numero1 = tag + index + "000"
    numero2 = tag + index + "111"
    numero1, numero2 = int(numero1, 2), int(numero2, 2)
    dato = 0
    f = open("RAM.txt", "w")
    for i in range(len(lista)):
        if i < numero1 or i > numero2: f.write(lista[i])
        else:
            if i != len(lista) - 1: f.write(str(data[dato]) + "\n")
            elif i != len(lista) - 1: f.write(str(data[dato]))
            dato += 1
    f.close()

def traer_datos_ram(index, tag):
    """
    Se encarga de almacenar la información que hay en un bloque de memoria
    en una lista.
    Entradas:
        index: es el numero de conjunto en donde deberia ir la información
        tag: es el identificador del bloque.
        (Juntos crean el Block Adrres (BA))
    Salida:
        M: una lista de los datos del bloque que hacen referencia al BA
    """
    f = open("RAM.txt", "r")
    ver = False
    index = bin(index)[2:].zfill(4)
    tag = bin(int(tag, 16))[2:].zfill(9)
    numero1 = tag + index + "000"
    numero2 = tag + index + "111"
    numero1, numero2 = int(numero1, 2), int(numero2, 2)
    M = []
    pos = 0
    for i in f:
        if pos == numero1:
            M.append(i.strip())
            ver = True
        elif ver and pos != numero2: M.append(i.strip())
        elif pos == numero2:
            M.append(i.strip())
            ver = False
            break
        pos += 1
    f.close()
    return M