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

