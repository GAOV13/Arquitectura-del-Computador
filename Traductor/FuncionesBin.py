"""
Nombre: Funciones del Traductor de Mips a binario.
Autores: Luis Alberto Salazar y Guido Ernesto Salazar.
Fecha: febrero/marzo 2021.
"""

from os import system
from math import *

### Contantes

#limite de los inm
MAX_LIM_16B = 65535
MAX_LIM_26B = 67108863
MAX_LIM_5B = 31

#Diccionario con la información de las respectivas instrucciones aceptadas por nuestro programa
instruccion_a_formato = {"add": ["R", "rd", "rs", "rt"], "addi": ["I", "rt", "rs", "inm"], 
                         "addiu": ["I", "rt", "rs", "inm"], "addu": ["R", "rd", "rs", "rt"],
                         "and": ["R", "rd", "rs", "rt"], "andi": ["I", "rt", "rs", "inm"],
                         "beq": ["I", "rs", "rt", "inm"], "bne": ["I", "rs", "rt", "inm"],
                         "j": ["J", "inm"], "jal": ["J", "inm"], "jr": ["R", "rs"],
                         "lbu": ["I", "rt", "inm", "rs"], "lhu": ["I", "rt", "inm", "rs"], 
                         "ll": ["I", "rt", "inm", "rs"], "lui": ["I", "rt", "inm"], 
                         "lw": ["I", "rt", "inm", "rs"], "nor": ["R", "rd", "rs", "rt"],
                         "or": ["R", "rd", "rs", "rt"], "ori": ["I", "rt", "rs", "inm"], 
                         "slt": ["R", "rd", "rs", "rt"], "slti": ["I", "rt", "rs", "inm"], 
                         "sltiu": ["I", "rt", "rs", "inm"], "sltu": ["R", "rd", "rs", "rt"],
                         "sll": ["R", "rd", "rt", "shamt"], "srl": ["R", "rd", "rt", "shamt"], 
                         "sb": ["I", "rt", "inm", "rs"], "sc": ["I", "rt", "inm", "rs"],
                         "sh": ["I", "rt", "inm", "rs"], "sw": ["I", "rt", "inm", "rs"],
                         "sub": ["R", "rd", "rs", "rt"], "subu": ["R", "rd", "rs", "rt"],
                         "mfhi": ["R", "rd"], "mflo": ["R", "rd"], "mult": ["R", "rs", "rt"], 
                         "multu": ["R", "rs", "rt"], "div": ["R", "rs", "rt"], "divu": ["R", "rs", "rt"]}

#Diccionario con los respectivos codigos en decimal de las funciones, junto con el parametro de la función para aquellas con tipo R
op_code = {"add": [0, 32], "addi": [8], "addiu": [9], "addu": [0, 33], "and": [0, 36], "andi": [12], "beq": [4], "bne": [5],
           "j": [2], "jal": [3], "jr": [0, 8], "lbu": [36], "lhu": [37],  "ll": [48], "lui": [15], "lw": [35], "nor": [0, 39],
           "or": [0, 37], "ori": [13], "slt": [0, 42], "slti": [10], "sltiu": [11], "sltu": [0, 43], "sll": [0, 0], "srl": [0, 2],
           "sb": [40], "sc": [56], "sh": [41], "sw": [43], "sub": [0, 34], "subu": [0, 35], "mfhi": [0, 16], "mflo": [0, 18], 
           "mult": [0, 24], "multu": [0, 25], "div": [0, 26], "divu": [0, 27]}

#Información del formato por instrucción con sus respectivas cantidad de bits
format_cant_bits = {"I": {"op": 6, "rs": 5, "rt": 5, "inm": 16}, 
                    "R": {"op": 6, "rs": 5, "rt": 5, "rd": 5, "shamt": 5, "funct": 6}, 
                    "J": {"op": 6, "inm": 26}}

#Información de los registros con su representación en decimal
registros = {"$0": 0, "$at": 1, "$v0": 2, "$v1": 3, "$a0": 4, "$a1": 5, "$a2": 6, "$a3": 7, "$t0": 8, "$t1": 9, 
             "$t2": 10, "$t3": 11, "$t4": 12, "$t5": 13, "$t6": 14, "$t7": 15, "$s0": 16, "$s1": 17, "$s2": 18, 
             "$s3": 19, "$s4": 20, "$s5": 21, "$s6": 22, "$s7": 23, "$t8": 24, "$t9": 25, "$k0": 26, "$k1": 27, 
             "$gp": 28, "$sp": 29, "$fp": 30, "$ra": 31} 

#Instrucciones que no modifcan registros de los parametros
no_modifican_valores = ["beq", "bne", "sb", "sc", "sh", "sw", "div", "divu"]

#Instrucciones con formato de escritura distinto
store_y_load = ["lbu", "lhu", "ll", "lw", "sb", "sc", "sh", "sw"]

#Variables globales
instrucciones_correctas = []
instrucciones_erroneas = []

# Funciones de Traducción

def traductorBin():
    """
    Función que hace la traducción de las instrucciones en mips a binario.
    Entradas: 
        instruccion_a_formato: Diccionario con la informacion y formato de la instruccion
        op_code: Diccionario con los codigos de la operación en decimal
        format_cant_bits: Diccionario con las especificaciones de los tipos de formato
        registros: Diccionario con los codigos de los registros en decimal
    Salida:
        retorno: Una lista de diccionarios con los parametros del formato en binario
    """
    retorno = []
    for parametros in instrucciones_correctas:
        operacion = parametros[0] 
        parametros.pop(0) 
        formato, instruccion_operacion = instruccion_a_formato[operacion][0], instruccion_a_formato[operacion][1:] 
        diccionario = format_cant_bits[formato].copy() 
        temp = op_code[operacion] 
        for key in diccionario:
            cant_bits = diccionario[key] 
            numero = 0 
            if key == "op": numero = temp[0]
            elif key == "funct": numero = temp[1]
            elif key == "inm" or key == "shamt":
                if key in instruccion_operacion: #Se hace la verificación si la instrucción tiene como parametro un inmediate o un shamt
                    indice = instruccion_operacion.index(key) #Se guarda la posición en la cual deberia encontrarse el numero segun la instrucción
                    entero = parametros[indice] #Se busca el valor en los parametros de la instrucción
                    try: entero = int(entero) #Se trata traducir el numero a un int en caso de estar en base 10
                    except: entero = int(entero, 16) #De lo contrario se traduce el numero en base 16 a un entero
                    if formato == "R": numero = entero & MAX_LIM_5B #Se corta la cantidad de bits del numero a solo 5 bits si es una operación tipo R
                    elif formato == "I":
                        if(entero < 0):
                            entero *= -1
                            entero = ~int(str(bin(entero)[2:]).zfill(cant_bits), 2)
                            entero += 1
                        numero = entero & MAX_LIM_16B #Se corta la cantidad de bits del numero a solo 16 bits si es una operación tipo I
                    else: numero = entero & MAX_LIM_26B #Se corta la cantidad de bits del numero a solo 26 bits si es una operación tipo J
            else: #Se busca el indice del registro
                if key in instruccion_operacion: #Esto se va a hacer si en la definición de la instrucción se encuentra el registro del formato
                    indice = instruccion_operacion.index(key) #Se busca la ubicación del parametro del formato en la instrucción
                    registro = parametros[indice] #Se busca el identificador del registro en dicha posición
                    numero = registros[registro] #Se trae la representación decimal del registro
            diccionario[key] = str(bin(numero)[2:]).zfill(cant_bits) #Se guarda el numero en binario del parametro del formato en su respectivo lugar
        retorno.append(diccionario)
    # print("Estas son las instrucciones escritas en binario")
    # for elemento in retorno: print(elemento)
    return retorno

# Funciones de Retorno

def salida(informacion):
    f = open("salida.txt", "w")
    
    numero = ""
    i = 0
    while(i < len(informacion)):
        numero = ""
        for dic in informacion[i]: numero += informacion[i][dic]
        f.write(numero)
        f.write("\n")
        i += 1
    
    f.close()

def errores():
    """
    Funcion que devuelve en un archivo con los errores sintacticos y semanticos del
    programa en mips: 
    Entradas: 
        instrucciones_erroneas: Lista con las cadenas que contienen errores
    Salidas: 
        errores.txt: Archivo con la información de los errores
    """
    f = open("errores.txt", "w")
    f.write("=====================================================================\n")
    f.write("Las siguientes entradas tienen errores:\n")
    f.write("=====================================================================\n")
    for (info, cad) in instrucciones_erroneas:
        f.write(info + " " + cad)
    f.write("\n=====================================================================\n")
    f.write("Posibles errores:\n")
    f.write(" - Instrucciones mal escritas.\n")
    f.write(" - Registros inexistentes.\n")
    f.write(" - Mal utilizacion de los registros en espacios no correspondientes.\n")
    f.write(" - Se modifican registros los cuales no se pueden modificar.\n")
    f.write("=====================================================================\n")
    
# Funciones de verificación
    
def verificacion_sintactica(lista_datos, instruccion):
    """
    Funcion  que retorna un valor booleano si la instrucción en codigo assembly esta bien
    sintacticamente
    Entradas:
        lista_datos: una lista con los parametros de la linea de instruccion
        instruccion: operación elemental que se va a ejercer
        instruccion_a_formato: Diccionario con la informacion y formato de la instruccion
        registros: Diccionario con los codigos de los registros en decimal
    Salida:
        ver: Valor booleando que devuelve True si la operación esta bien sintactiacemnte
        o falso de lo contrario
    """
    ver = False
    if(instruccion in instruccion_a_formato):
        if(len(lista_datos) == len(instruccion_a_formato[instruccion])):
            ver2 = True
            i = 1
            while(i < len(lista_datos) and ver2 == True):
                if(lista_datos[i][0] == "$"):
                    if(lista_datos[i] not in registros): ver2 = False
                i += 1
            if(ver2): ver = True
    return ver

def verificacion_semantica(lista_datos):
    """
    Función que me verifica si la linea de codigo esta semanticamente correcta
    Entradas:
        lista_datos: lista con los parametros de la instruccion
        instruccion_a_formato: Diccionario con la informacion y formato de la instruccion
        no_modifican_valores: lista con las instrucciones que no reescriben un registro 
                              de los parametrs
        store_y_load: lista con las instrucciones que tienen una manera diferente de es-
            cribirse
    Salidas:
        ver: valor booleando que retorna true si la instrucción esta correcta semantica-
            mente o falso de lo contrario
    """
    ver = True
    instruccion, lista_datos = lista_datos[0], lista_datos[1:]
    formato, temp = instruccion_a_formato[instruccion][0], instruccion_a_formato[instruccion][1:]
    i = 0
    while i < len(lista_datos) and ver:
        if temp[i] == "inm" or temp[i] == "shamt":
            caract = lista_datos[i]
            try: caract = int(caract)
            except:
                try: caract = int(caract, 16)
                except: caract = caract
            if type(caract) != int: ver = False
            # elif (instruccion in store_y_load) and caract % 4 != 0: ver = False
        elif lista_datos[i][0] != '$': ver = False
        i += 1
    if ver and (instruccion not in no_modifican_valores) and lista_datos[0] == "$0":
        ver = False
    if (instruccion == "div" or instruccion == "divu") and lista_datos[i - 1] == "$0":
        ver = False
    return ver

# Funciones de Lectura

def lectura(cadena):
    """
    Función que lee los parametros de la cadena y retorna los parametors junto con sus
    respectivas verificaciónes
    Entradas:
        cadena: string con la linea del archivo correspondiente
    Salidas:
        temp1: lista con los parametros de la instrucción
        ver: verificación sintactica de la linea, es decir que este bien escrita
        ver2: verificación semantica de la linea, es decir que no haya una operación pro-
            hibida, como modificar el registro 0, que no exista el registro, etc.
    """
    index, temp = cadena.find("#"), cadena
    if index != -1: temp = cadena[:index]
    temp = list(map(str, temp.split()))
    temp1, ver, ver2 = [], False, False
    i = 0
    for elemento in temp:
        c = elemento[len(elemento) - 1]
        if c == ',' and i != len(temp) - 1: 
            elemento = elemento[:len(elemento) - 1]
            temp1.append(elemento)
        elif c == ')' and (temp1[0] in store_y_load) and len(temp) == 3:
            elemento = elemento[:len(elemento) - 1]
            temp2 = list(map(str, elemento.split('(')))
            temp1 = temp1 + temp2
        else: temp1.append(elemento)
        i += 1
    if len(temp1) > 0:
        temp = temp1[0]
        ver = verificacion_sintactica(temp1, temp)
        if(ver): ver2 = verificacion_semantica(temp1)
    return (temp1, ver, ver2)
    
# Funciones Principales

def assemblyBin():
    """
    Procedimiento que se encarga de hacer las respectivas verificación y la traducción
    del programa mips
    """
    global instrucciones_correctas, instrucciones_erroneas
    instrucciones_correctas = []
    instrucciones_erroneas = []
    system("cls")
    ver = True
    print("=====================================================================")
    archivo = str(input("Nombre del archivo (sin la extesion): "))
    try: f = open("{}.txt".format(archivo), "r")
    except: 
        ver = False
        print("=====================================================================")
        print("Hubo un error a la hora de abrir el archivo.")
        print("Volviendo al inicio")
    print("=====================================================================")
    if ver:
        i = 1
        for linea in f:
            instruccion, flag_sintax, flag_sem = lectura(linea)
            flag_comentario = len(instruccion)
            if flag_comentario == 0:
                print("Linea {} trata de un comentario por lo que no se incluyo".format(i))
            elif not flag_sintax: 
                instrucciones_erroneas.append(("Error de sintaxis en linea {}".format(i), linea))
            elif not flag_sem: 
                instrucciones_erroneas.append(("Error semantico en linea {}".format(i), linea))
            else:
                instrucciones_correctas.append(instruccion)
            i += 1

        if(len(instrucciones_erroneas) > 0): errores()
        else:
            informacion = traductorBin()
            salida(informacion)
        f.close()
        
def bin_a_hexa():
    print("=====================================================================")
    archivo = str(input("Nombre del archivo (sin la extesion): "))
    ver = True
    try: f = open("{}.txt".format(archivo), "r")
    except: 
        ver = False
        print("=====================================================================")
        print("Hubo un error a la hora de abrir el archivo.")
        print("Volviendo al inicio")
    print("=====================================================================")
    if ver:
        informacion = []
        for linea in f: informacion.append('0x' + hex(int(linea, 2))[2:].zfill(8))
        f1 = open("salida.txt", "w")
        numero = ""
        for dic in informacion:
            f1.write(dic)
            f1.write("\n")
        
        f1.close()
        f.close()
