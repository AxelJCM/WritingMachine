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




ide = Tk()
ide.title('Writting Machine IDE')
ide.geometry("1000x700")
ide.resizable(False, False)
ide.configure(background='black')


baseIde = Canvas(ide, width = 800, height= 545)
baseIde.place(x=0, y=0)


baseConsola = Canvas(ide, width=490, height=143)
baseConsola.place(x=0, y=550)


basePrint = Canvas(ide, width=490, height=143)
basePrint.place(x=510, y=550)



# Area de trabajo para escritura de codigo
areaTexto = Text(baseIde, height=34, width=100)
areaTexto.pack()

# Area donde se muestran los mensajes de compilador
areaConsola = Text(baseConsola, height=9, width=60)
areaConsola.pack()

# Area donde se muestran los mensajes impresos por parte del codigo
areaPrint = Text(basePrint, height=9, width=60)
areaPrint.pack()

ide.mainloop()


























