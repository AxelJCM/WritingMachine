from tkinter import *
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from turtle import width
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
from tkinter.filedialog import *

from AnalisisLexico import *
from AnalisisSintactico import *
from AnalisisSemantico import *


#from archivos import escribirArchivo, leerArchivo, Compilar, Ejecutar
from numerosLinea import ScrollText

#Variables
fuente = "Consolas"
tamFuente = 12
fondo = "#1D253C"
guardado = False
codigo = ""
txt = ""
valor = ""

#Listas de Errores y Prints
errores_lexico = []
errores_sintactico = []
lista_prints = []

def mensajeInfo():
    global valor
    valor = messagebox.askquestion("¡Advertencia!","¿Quiere guadar el archivo actual?")
    
def textoModificado():
    global txt
    txt = scroll.get(1.0, END)
    print(len(txt))
    if (len(txt) == 1):
        txt = ""

def texto(pantalla, mensaje, x, y, color, colorFondo = None):
    if colorFondo == None:
        colorFondo = fondo

    t = Label(pantalla, text=mensaje, font=(fuente, tamFuente), bg = colorFondo, fg= color)
    t.place(x=x, y=y)

# Se abre un archivo compatible con el lenguaje de programacion    
def abrirArchivo():
    global codigo, txt, valor
    textoModificado()
    # si se quiere abrir un nuevo archivo y no se ha guardado el que se esta editando
    print(codigo)
    print(txt)
    if (codigo != txt):
        # Se muestra una ventana con el mensaje de si se quiere guardar el archivo actual
        mensajeInfo()
        if (valor == "yes"):
            guardarArchivo()
    
    path = askopenfilename()
    with open(path, 'r') as file:
        code = file.readlines()
        scroll.delete('1.0', END)
        codigoLeido = ''
        for i in range(len(code)):
            codigoLeido += code[i]
        scroll.insert(END, codigoLeido)
        codigo = scroll.get(1.0, END)
        txt = scroll.get(1.0, END)

# Se guarda el texto que contenga el areaTexto dentro de un archivo .w     
def guardarArchivo():
    path = asksaveasfilename(filetypes=[('Writing Machine Files', '*.writ')])
    with open(path, 'w') as file:
        code = scroll.get('1.0', END)
        file.write(code)

# Se borran los textos escritos en cada una de las areas de texto del ide    
def borrarTexto():
    global txt, codigo
    textoModificado()
    if (txt != codigo):
        mensajeInfo()
        if (valor == "yes"):
            txt = ""
            codigo = ""
            guardarArchivo()
    scroll.delete(1.0, END)   
    areaConsola.delete(1.0, END)
    areaPrint.delete(1.0, END) 

#funciones de compilacion


def quitarCom(string):
    lista = string.split('"')
    lista.reverse()
    for i in lista:
        if i != "''":
            areaPrint.insert(1.0, i + " ")

def limpiar_print(string):
    nuevo = ""
    for i in string:
        if i != "{" or i != "}":
            nuevo += i
    return nuevo

def aplanar(lista):
    ret = []
    for elem in lista:
        if isinstance(elem, list):
            ret.extend(aplanar(elem))
        else:
            ret.append(elem)
    return ret
            
def prints(lista):
    x = aplanar(lista)
    x.reverse()
    for i in x:
        if isinstance(i,bool):
            if i == True:
                areaPrint.insert(1.0, "True")
            else:
                areaPrint.insert(1.0, "False")
        elif isinstance(i,int):
            areaPrint.insert(1.0, str(i)+' ')
        else:
            quitarCom(i)


def reiniciarAreas():
    areaConsola.delete(1.0, END)
    areaPrint.delete(1.0, END)

def agregarErrores(lista_errores):
    areaConsola.config(state=NORMAL)
    for i in lista_errores:
        areaConsola.insert(1.0, "-> " + i + "\n" + "\n")
    areaConsola.config(state=DISABLED)

def getTexto(area):
    return area.get(1.0, END)

def reiniciarAreas():
    areaConsola.delete(1.0, END)
    areaPrint.delete(1.0, END)

def compilar():
    global errores_sintactico, errores_lexico

    

    reiniciarAreas()
    limpiarErrores()
    limpiarError()
    limpiarNombres()
    limpiarPrints()
    areaConsola.config(state=NORMAL)
    areaConsola.delete("1.0",END)
    areaPrint.config(state=NORMAL)
    areaPrint.delete("1.0",END)

    if getTexto(scroll) != "\n":
        texto = getTexto(scroll)
        

        print("---Lexico---")
        lexicalAnalizer(texto) #analisis lexico
        errores_lexico = lex_getErrores()
        agregarErrores(errores_lexico)

        print("---Sintactico---")#analisis sintactico
        sintacticAnalizer(texto)
        print("Se analizo el sintactico")
        errores_sintactico = sintac_getErrores()
        agregarErrores(errores_sintactico)

        #se procede a imprimir los prints
        lista_prints = sintac_getPrints()
        prints(lista_prints)

        
    else:
        agregarErrores(["Debe Ingresar Codigo..."])
    
    areaConsola.config(state=DISABLED)
    areaPrint.config(state=DISABLED)
    
    limpiarErrores()
    limpiarError()
    limpiarNombres()
    limpiarPrints()

def correr():
    compilar()
    print("()()() Vacio = " + str(lex_getErrores() == []))
    if errores_lexico == [] and errores_sintactico == []:
        print("Procedimientos es: ")
        print(sintac_getArduino())
        procedimientos(sintac_getArduino())

# Creacion de la ventana del ide
ide = Tk()
ide.title('Writing Machine IDE')
#ide.iconbitmap('./Imagenes/icono.ico')
ide.geometry("1000x700")
ide.resizable(False, False)
ide.configure(background='black')

# Creacion de menu de opciones "Archivo" para el manejo de los archivos de codigo
menu1 = Menu(ide)
fileMenu = Menu(menu1, tearoff=0)
fileMenu.add_command(label='Nuevo', command=borrarTexto)
fileMenu.add_command(label='Abrir', command=abrirArchivo)
fileMenu.add_command(label='Guardar', command = guardarArchivo)
menu1.add_cascade(label='Archivo', menu=fileMenu)


# Creacion de menu de opciones "Ejecutar" para el analisis y ejecucion del codigo contenido en el areaTexto
runMenu = Menu(menu1, tearoff=0)
runMenu.add_command(label='Compilar', command = compilar)
runMenu.add_command(label='Compilar y Ejecutar', command = correr)
menu1.add_cascade(label='Compilar', menu=runMenu)
ide.config(menu=menu1)

scroll = ScrollText(ide)
scroll.insert(tk.END,'')
scroll.pack()
scroll.text.focus()
ide.after(200, scroll.redraw())
'''
# Area de trabajo para escritura de codigo
baseIde = Canvas(ide, width = 900, height= 545)
baseIde.place(x=20, y=0)
areaTexto = Text(baseIde, height=34, width=121)
areaTexto.config(bg='#362f2e', fg='#d2ded1')
Percolator(areaTexto).insertfilter(ColorDelegator()) # Identifica palabras reservadas de python # Hacer algo como esto para cuando se reconozca una palabra
areaTexto.pack()
'''
# Area donde se muestran los mensajes de compilador
baseConsola = Canvas(ide, width=490, height=143)
baseConsola.place(x=0, y=550)
areaConsola = Text(baseConsola, height=9, width=60)
areaConsola.config(state=DISABLED)
areaConsola.config(bg='#362f2e', fg='#1dd604')
areaConsola.pack()
# Area donde se muestran los mensajes impresos por parte del codigo
basePrint = Canvas(ide, width=490, height=143)
basePrint.place(x=510, y=550)
basePrint.config(state=DISABLED)
areaPrint = Text(basePrint, height=9, width=60)
areaPrint.config(bg='#362f2e', fg='#d2ded1')
areaPrint.pack()

# Loop de la aplicacion
ide.mainloop()
    
