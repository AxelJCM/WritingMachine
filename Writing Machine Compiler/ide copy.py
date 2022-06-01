from tkinter import *
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from turtle import width
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
from tkinter.filedialog import *
from AnalisisLexico import lexicalAnalizer, lex_getErrores
from AnalisisSintactico import sintac_getErrores, sintacticAnalizer

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

#Listas de Errores
errores_lexico = []
errores_sintactico = []
errores_semantico = []

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
    
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.readlines()
        scroll.delete('1.0', END)
        scroll.insert('1.0', code)
        codigo = scroll.get(1.0, END)
        txt = scroll.get(1.0, END)

# Se guarda el texto que contenga el areaTexto dentro de un archivo .w     
def guardarArchivo():
    path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'w') as file:
        code = scroll.get('1.0', END)
        file.write(code)

# Se borran los textos escritos en cada una de las areas de texto del ide    
def borrarTexto():
    global txt, codigo
    print (txt + "hola1")
    print (codigo + "hola2")
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
def correr():
    pass


def reiniciarAreas():
    areaConsola.delete(1.0, END)
    areaPrint.delete(1.0, END)

def agregarErrores(lista_errores):
    for i in lista_errores:
        areaConsola.insert(1.0, i)

def getTexto(area):
    return area.get(1.0, END)


def compilar():
    global errores_sintactico, errores_lexico, errores_semantico

    reiniciarAreas()

    if getTexto(scroll) != "\n":

        texto = getTexto(scroll)

        print("---Lexico---")
        lexicalAnalizer(texto) #analisis lexico
        errores_lexico = lex_getErrores()
        agregarErrores(errores_lexico)

        print("---Sintactico---")
        sintacticAnalizer(texto)
        #errores_sintactico = sintac_getErrores()
        #agregarErrores(errores_sintactico)

    else:
        agregarErrores(["Debe Ingresar Codigo..."])
    

# Creacion de la ventana del ide
ide = Tk()
ide.title('Writing Machine IDE')
ide.iconbitmap('./Writing Machine IDE/Imagenes/icono.ico')
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
areaConsola.config(bg='#362f2e', fg='#1dd604')
areaConsola.pack()
# Area donde se muestran los mensajes impresos por parte del codigo
basePrint = Canvas(ide, width=490, height=143)
basePrint.place(x=510, y=550)
areaPrint = Text(basePrint, height=9, width=60)
areaPrint.config(bg='#362f2e', fg='#d2ded1')
areaPrint.pack()

# Loop de la aplicacion
ide.mainloop()
    
