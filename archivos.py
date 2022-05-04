from tkinter.filedialog import *


def leerArchivo():
    archivo = askopenfilename()
    ar = open(archivo, "r")
    ar = ar.readlines()
    ar.close()
    return ar

def escribirArchivo(data):
    ruta = askdirectory()
    ar = open(ruta, "w")
    ar.write(data)
    ar.close()

def Compilar():
    print("El codigo compila!!")

def Ejecutar():
    print("El codigo se compila y se ejecuta!!")