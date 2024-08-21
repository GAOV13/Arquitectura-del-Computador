"""
Nombre: Funciones del Traductor de Hexadecimal a Mips.
Autores: Luis Alberto Salazar y Guido Ernesto Salazar.
Fecha: febrero/marzo 2021.
"""

from os import system
from math import *
from FuncionesBin import lectura

# Diccionario de mondá
op_code = {0: {32: "add", 33: "addu", 36: "and", 8: "jr", 39: "nor", 37: "or",
               42: "slt", 43: "sltu", 0: "sll", 2: "srl", 34: "sub", 35: "subu", 
               16: "mfhi", 18: "mflo", 24: "mult", 25: "multu", 26: "div", 27: "divu"},
           8: "addi", 9: "addiu", 12: "andi", 4: "beq", 5: "bne", 2: "j", 3: "jal", 36: "lbu", 37: "lhu",
           48: "ll", 15: "lui", 35: "lw", 13: "ori", 10: "slti", 11: "sltiu",
           40: "sb", 56: "sc", 41: "sh", 43: "sw"}

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

format_cant_bits = {"I": {"rs": 5, "rt": 5, "inm": 16}, 
                    "R": {"rs": 5, "rt": 5, "rd": 5, "shamt": 5}, 
                    "J": {"inm": 26}}

registros = {0: "$0", 1: "$at", 2: "$v0", 3: "$v1", 4: "$a0", 5: "$a1", 6: "$a2", 7: "$a3", 8: "$t0", 9: "$t1", 
             10: "$t2", 11: "$t3", 12: "$t4", 13: "$t5", 14: "$t6", 15: "$t7", 16: "$s0", 17: "$s1", 18: "$s2", 
             19: "$s3", 20: "$s4", 21: "$s5", 22: "$s6", 23: "$s7", 24: "$t8", 25: "$t9", 26: "$k0", 27: "$k1", 
             28: "$gp", 29: "$sp", 30: "$fp", 31: "$ra"}

instruccion_in_hexa = ["lui", "ori", "jal", "j"]

store_y_load = ["lbu", "lhu", "ll", "lw", "sb", "sc", "sh", "sw"]

instrucciones_correctas = []
instrucciones_erroneas = []

# Funciones de Retorno

def errores():
    f = open("errores.txt", "w")
    f.write("=====================================================================\n")
    f.write("Las siguientes entradas tienen errores:\n")
    f.write("=====================================================================\n")
    for (info, linea) in instrucciones_erroneas:
        f.write(info + " " + linea)
    f.write("\n=====================================================================\n")
    f.write("Posibles errores:\n")
    f.write(" - Instrucciones mal escritas.\n")
    f.write(" - Registros inexistentes.\n")
    f.write(" - Mal utilizacion de los registros en espacios no correspondientes.\n")
    f.write(" - Se modifican registros los cuales no se pueden modificar.\n")
    f.write("=====================================================================\n")

def salida():
    f = open("salida.txt", "w")
    
    for ins in instrucciones_correctas:
        f.write(ins)
        f.write("\n")
    
    f.close()

# Funciones de Traducción

def traduccionHex(traduccion):
    op, traduccion = int(traduccion[:6], 2), traduccion[6:]
    inst = ""
    if op == 0:
        func, traduccion = int(traduccion[len(traduccion) - 6:],2), traduccion[:len(traduccion) - 6]
        inst = op_code[op][func]
    else: inst = op_code[op]

    formato, infor = instruccion_a_formato[inst][0], instruccion_a_formato[inst][1:]
    traduc_info = format_cant_bits[formato].copy()
    for key in traduc_info:
        cant_bits = traduc_info[key]
        num = ""
        if key == "inm" or key == "shamt":
            if inst in instruccion_in_hexa:
                cant_bitst = cant_bits
                if cant_bits == 26: cant_bitst = 28
                num, traduccion = "0x" + hex(int(traduccion[:cant_bits], 2))[2:].zfill(cant_bitst//4), traduccion[cant_bits:]
            else:
                num, traduccion = traduccion[:cant_bits], traduccion[cant_bits:]
                if num[0] == '1':
                    num = int(num,2) - 1
                    num = str(bin(num)[2:]).zfill(cant_bits)
                    temp = ""
                    for i in range(len(num)):
                        if num[i] == '0': temp += '1'
                        else: temp += '0'
                    num = "-" + str(int(temp, 2))
                else:
                    num = str(int(num, 2))
        else:
            num, traduccion = int(traduccion[:cant_bits], 2), traduccion[cant_bits:]
            num = registros[num]
        traduc_info[key] = num
    dev = inst + " "
    dev += traduc_info[infor[0]]
    i = 1
    while i < len(infor):
        dev += ", "
        if inst in store_y_load:
            dev += traduc_info[infor[i]] + "(" + traduc_info[infor[i + 1]] + ")"
            i += 1

        else: dev += traduc_info[infor[i]]
        i += 1
    
    return dev

# Funciones Principales

def hexaAssem():
    global instrucciones_correctas, instrucciones_erroneas
    try:
      instrucciones_correctas = []
      instrucciones_erroneas = [] 
      system("cls")
      ver = True
      print("=====================================================================")
      archivo = str(input("Ingrese el nombre del archivo (sin extension): "))
      try: f = open("{}.txt".format(archivo), "r")
      except:
          ver = False
          print("=====================================================================")
          print("Hubo un error a la hora de abrir el archivo.")
          print("Volviendo al inicio")
      print("=====================================================================")
      if(ver):
          i = 1
          for linea in f:
              traduccion = str(bin(int(linea, 16)))[2:].zfill(32)
              cadena = traduccionHex(traduccion)
              instruccion, flag_sintaxis, flag_semantica = lectura(cadena)
  
              if not flag_sintaxis: 
                  instrucciones_erroneas.append(("Error de sintaxis en linea {}".format(i), linea))
              if not flag_semantica:
                  instrucciones_erroneas.append(("Error semantico en linea {}".format(i), linea))
              else:
                  instrucciones_correctas.append(cadena)
              i += 1
          
          if(len(instrucciones_erroneas) > 0): errores()
          else: salida()
          f.close()
    except:
      print("=====================================================================")
      print("Hubo un fallo en el programa")
      print("=====================================================================")
