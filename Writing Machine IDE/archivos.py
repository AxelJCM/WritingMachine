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
    # Escribir el codigo correspondiente para poder compilar el codigo contenido en areaTexto
    # Si el codigo compila bien, se muesta un mensaje de "Compilado Correctamente!"
    # Si el codigo no compila de forma correcta, se muestra un mensaje de "Error" segido del error especificando el
    #    numero de linea en el que se encuentra dicho error.

def Ejecutar():
    Compilar()
    print("El codigo se ejecuta!!")
    # Si la compilacion es correcta, Se ejecuta el codigo de areaTexto y se imprimen los mensajes contenidos 
    #   en los "print() dentro del areaPrints"
    