from tkinter import *
from tkinter import font
from tkinter import messagebox

#Variables
fuente = "Consolas"
tamFuente = 12
fondo = "#1D253C"

def texto(pantalla, mensaje, x, y, color, colorFondo = None):
    if colorFondo == None:
        colorFondo = fondo

    t = Label(pantalla, text=mensaje, font=(fuente, tamFuente), bg = colorFondo, fg= color)
    t.place(x=x, y=y)

# Creacion de la ventana del ide
ide = Tk()
ide.title('Writting Machine IDE')
ide.iconbitmap('C:\\Users\\mario\\Desktop\\GitHub\\WritingMachine\\Imagenes\\icono.ico')
ide.geometry("1000x700")
ide.resizable(False, False)
ide.configure(background='black')

# Area de trabajo para escritura de codigo
baseIde = Canvas(ide, width = 900, height= 545)
baseIde.place(x=0, y=0)
areaTexto = Text(baseIde, height=34, width=112)
areaTexto.pack()
# Area donde se muestran los mensajes de compilador
baseConsola = Canvas(ide, width=490, height=143)
baseConsola.place(x=0, y=550)
areaConsola = Text(baseConsola, height=9, width=60)
areaConsola.pack()
# Area donde se muestran los mensajes impresos por parte del codigo
basePrint = Canvas(ide, width=490, height=143)
basePrint.place(x=510, y=550)
areaPrint = Text(basePrint, height=9, width=60)
areaPrint.pack()

#### PROGRAMAR LAS ACCIONES PARA LOS BOTONES AQUI #########################################################

# Area donde se muestran los botones para compilar, corrrer el codigo ....
baseCompi = Canvas(ide, width=100, height=545)
baseCompi.place(x=905, y=2)
abrirBtn = Button(baseCompi, text ="    ABRIR     ", activebackground='light blue', activeforeground='red')
abrirBtn.pack(ipadx=10, ipady=0, expand=True)

### Boton "NUEVO"  ####

compilarBtn = Button(baseCompi, text ="COMPILAR", activebackground='light blue', activeforeground='red')
compilarBtn.pack(ipadx=10, ipady=0, expand=True)
ejecutarBtn = Button(baseCompi, text =" EJECUTAR ", activebackground='light blue', activeforeground='red')
ejecutarBtn.pack(ipadx=10, ipady=0, expand=True)

# Loop de la aplicacion
ide.mainloop()