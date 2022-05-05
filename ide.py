from tkinter import *
from tkinter import font
from tkinter import messagebox
from turtle import width
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
from tkinter.filedialog import *

from archivos import escribirArchivo, leerArchivo, Compilar, Ejecutar
from numerosLinea import LineNumbers, TextLineNumbers

#Variables
fuente = "Consolas"
tamFuente = 12
fondo = "#1D253C"
guardado = False

def texto(pantalla, mensaje, x, y, color, colorFondo = None):
    if colorFondo == None:
        colorFondo = fondo

    t = Label(pantalla, text=mensaje, font=(fuente, tamFuente), bg = colorFondo, fg= color)
    t.place(x=x, y=y)

# Se abre un archivo compatible con el lenguaje de programacion    
def abrirArchivo():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.readlines()
        areaTexto.delete('1.0', END)
        areaTexto.insert('1.0', code)

# Se guarda el texto que contenga el areaTexto dentro de un archivo .w     
def guardarArchivo():
    path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'w') as file:
        code = areaTexto.get('1.0', END)
        file.write(code)

# Se borran los textos escritos en cada una de las areas de texto del ide    
def borrarTexto():
    areaTexto.delete(1.0, END)   
    areaConsola.delete(1.0, END)
    areaPrint.delete(1.0, END) 

# Creacion de la ventana del ide
ide = Tk()
ide.title('Writing Machine IDE')
ide.iconbitmap('./Imagenes/icono.ico')
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
runMenu.add_command(label='Compilar', command = Compilar)
runMenu.add_command(label='Compilar y Ejecutar', command = Ejecutar)
menu1.add_cascade(label='Compilar', menu=runMenu)
ide.config(menu=menu1)

def prueba(texto):
    print(texto.index())

# Area de trabajo para escritura de codigo
baseIde = Canvas(ide, width = 900, height= 545)
baseIde.place(x=20, y=0)
areaTexto = Text(baseIde, height=34, width=121)
areaTexto.config(bg='#362f2e', fg='#d2ded1')
Percolator(areaTexto).insertfilter(ColorDelegator()) # Hacer algo como esto para cuando se reconozca una palabra
areaTexto.pack()

#lineas = LineNumbers(ide, areaTexto, width=1, height=545)
#lineas.place(x=0,y=0)

lineas = TextLineNumbers(width = 20)
lineas.attach(areaTexto)
lineas.place(x=0,y=0)


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