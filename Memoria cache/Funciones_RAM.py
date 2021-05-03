"""
Nombre: Funciones de la Memoria RAM.
Autores: Luis Alberto Salazar y Guido Ernesto Salazar.
Fecha: abril/mayo 2021.
"""

# Funciones RAM

# def modificar_ram1(index, tag, data):
#     f = open("RAM.txt", "r")
#     index = bin(index)[2:].zfill(4)
#     tag = bin(int(tag, 16))[2:].zfill(9)
#     numero1 = tag + index + "000"
#     numero2 = tag + index + "111"
#     numero1, numero2 = int(numero1, 2), int(numero2, 2)
#     i = 0
#     while(i + numero1 < numero2):
#         print("error?")
#         f[i + numero1] = data[i]
#         print("error?")
#         i += 1

#     o = open("RAM.txt", "w")
#     o.writelines(f)
#     o.close()

def modificar_ram(index, tag, data):
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
            M.append(int(i))
            ver = True
        elif ver and pos != numero2: M.append(int(i))
        elif pos == numero2:
            M.append(int(i))
            ver = False
            break
        pos += 1
    f.close()
    return M