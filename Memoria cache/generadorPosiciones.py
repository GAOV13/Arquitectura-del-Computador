import random

def generar():
    f = open("Entrada.txt", "w")
    for i in range(1001):
        n = random.randrange(1000) % 2
        f.write(str(n + 1) + "\n")
        pos = random.randrange(0, 2048)
        f.write(str(pos) + "\n")
        if n == 1: f.write(str(random.randrange(10000)) + "\n")
    f.write("4")
    f.close()