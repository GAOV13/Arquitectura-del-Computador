"""
Nombre: Funciones de la Memoria Caché.
Autores: Luis Alberto Salazar y Guido Ernesto Salazar.
Fecha: abril/mayo 2021.
"""

def modificar_ram(index, tag, data):
    f = open("RAM.txt", "r")
    index = bin(index)[2:].zill(4)
    tag = bin(int(tag, 16))[2:].zfill(9)
    numero1 = tag + index + "000"
    numero2 = tag + index + "111"
    numero1, numero2 = int(numero1, 2), int(numero2, 2)
    i = 0
    print(data)
    while(i + numero1 < numero2):
        f[i + numero1] = data[i]
        i += 1

    o = open("RAM.txt", "w")
    o.writelines(f)
    o.close()

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