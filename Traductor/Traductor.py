"""
Nombre: Traductor de Assembly a Binario y Hexadecimal a Assembly.
Autores: Luis Alberto Salazar y Guido Ernesto Salazar.
Fecha: febrero/marzo 2021.
"""

from FuncionesBin import assemblyBin, bin_a_hexa
from FuncionesHexa import hexaAssem

def main():
    ver = True
    while ver:
        print("")
        print("=====================================================================")
        print("Traductor de Assembly a Binario y de Hexadecimal a Assembly")
        print("=====================================================================")
        print("1) Traducir de Assembly a Binario.")
        print("2) Traducir de Hexadeciaml a Assembly.")
        print("3) Salir.")
        print("=====================================================================")
        x = input("Ingrese una opcion: ")
        if(x == "1"): assemblyBin()
        elif(x == "2"): hexaAssem()
        elif(x == "3"):
            ver = False
            print("")
            print("Vuelva pronto!")
        elif(x== "4"): bin_a_hexa()
        else:
            print("=====================================================================")
            print("Error, opcion no valida.")
            print("=====================================================================")

main()