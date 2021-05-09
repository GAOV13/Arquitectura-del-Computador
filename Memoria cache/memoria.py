"""
Nombre: Memoria Caché en alto nivel.
Autores: Luis Alberto Salazar y Guido Ernesto Salazar.
Fecha: abril/mayo 2021.
"""

from Funciones_Cache import leer_cache, escribir_cache, llamarMiss
from Funciones_RAM import inicializar_ram
from os import system

def main():
    f = open("Cache.txt", "w")
    f.close()
    x = "3"
    ver = True
    valor = ""
    while ver:
        print("\n")
        print("=====================================================================")
        print("Bienvenido a su Memoria Caché en alto nivel!")
        print("=====================================================================")
        print("¿Qué desea hacer?")
        print("1) Leer la memoria RAM.")
        print("2) Escribir en la memoria RAM.")
        print("3) Limpiar consola.")
        print("4) Salir.")
        print("=====================================================================")
        x = input("Opcion a elegir: ")

        if x == "1":
            valor = input("Escriba una posición de la memoria que quiera leer: ").strip()
            try:
                valor = int(valor)
                if valor >= 0 and valor <= 2048:
                    print("El dato en la posición [{}] es {}".format(valor, leer_cache(valor)))
                else: print("No se ingreso una posición de memoria valida")
            except: print("No ingreso un valor numerico!")
        elif x == "2":
            valor = input("Escriba una posición de la memoria que quiera leer: ")
            dato = input("Ingrese un valor numerico a escribir: ")
            try:
                valor = int(valor)
                if valor >= 0 and valor <= 2048: escribir_cache(valor, dato)
                else: print("No se ingreso una posición de memoria valida")
            except: print("No ingreso un valor numerico!")
        elif x == "3": system("cls")
        elif x == "4":
            ver = False
            print("=====================================================================")
            print("Tasa de desacierto (Miss ratio): {}".format(llamarMiss()))
            print("=====================================================================")
            print("")
            print("Vuelva pronto!")
        elif x == "Drink Torrent":
            inicializar_ram()
        else:
            print("=====================================================================")
            print("Error, opcion no valida.")
            print("=====================================================================")

main()