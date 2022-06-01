from tkinter import *
from tkinter import messagebox
import sys
from tkinter import filedialog as fd
from AnalisisLexico import *
from AnalisisSintactico import *
#import serial
import time


class Gui:
    
    def __init__(self):
        self.MainWindow = Tk()

        ####################################  Centra la ventana  #######################################################

        w = 1000
        h = 800

        ws = self.MainWindow.winfo_screenwidth()
        hs = self.MainWindow.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        self.MainWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))

        ################################################################################################################

        self.MainWindow.title("TEC Writing Machine")
        self.MainWindow.geometry("1000x800")

        self.MainWindow.configure(bg="#227474")

        # Buttons
        Button(self.MainWindow, text="ABRIR", background = "white", foreground = "black" ,command=self.OpenButtonClick).place(x=5, y=1)
        Button(self.MainWindow, text="GUARDAR", background = "white", foreground = "black" ,command=self.SaveButtonClick).place(x=47.5, y=1)
        Button(self.MainWindow, text="COMPILAR", background = "yellow", foreground = "black" , command=lambda: self.buttonClick(False)).place(x=550, y=1)
        Button(self.MainWindow, text="CORRER", background = "yellow", foreground = "black" , command=lambda: self.buttonClick(True)).place(x=620, y=1)
        Button(self.MainWindow, text="SALIR", background = "red", foreground = "black" ,command=lambda: self.MainWindow.destroy()).place(x=945, y=1)

        # Inserta las dos areas de texto

        self.CodeTextArea = Text(self.MainWindow, font = 14, bg='#227474', fg="white")
        self.CodeTextArea.place(x=40, y=30, width=960, height=500)

        self.OutputTextArea = Text(self.MainWindow, font = 14 ,bg='#227474', fg="white")
        self.OutputTextArea.place(x=40, y=535, width=960, height=260)
        self.OutputTextArea.config(state=DISABLED)

        # Crea el area de numeracion de linea del codigo

        self.linenumbers = TextLineNumbers(self.MainWindow, width=35, bg='#227474')
        self.linenumbers.place(x=0, y=30, height=500)
        self.linenumbers.attach(self.CodeTextArea)

        self.uniscrollbar= Scrollbar(self.MainWindow, orient=VERTICAL, command=self.CodeTextArea.yview)
        self.uniscrollbar.place(x=980, y=30, height=500)

        self.CodeTextArea.config(yscrollcommand=self.uniscrollbar.set)

        self.CodeTextArea.bind("<Key>", self.onPressDelay)
        self.CodeTextArea.bind("<Button-1>", self.linenumbers.redraw)
        self.uniscrollbar.bind("<Button-1>", self.onScrollPress)
        self.CodeTextArea.bind("<MouseWheel>", self.onPressDelay)

        self.MainWindow.after(200,self.redraw) 
        
        self.MainWindow.mainloop()

    def OpenButtonClick(self):
        nombrearch = fd.askopenfilename(initialdir=".", title="Seleccione archivo",
                                        filetypes=(("txt files", "*.txt"), ("todos los archivos", "*.*")))
        if nombrearch != '':
            archi1 = open(nombrearch, "r", encoding="utf-8")
            contenido = archi1.read()
            archi1.close()
            self.setCodeTextArea(contenido)

    def SaveButtonClick(self):
        nombrearch = fd.asksaveasfilename(initialdir=".", title="Guardar como",
                                          filetypes=(("txt files", "*.txt"), ("todos los archivos", "*.*")))
        if nombrearch != '':
            archi1 = open(nombrearch, "w", encoding="utf-8")
            archi1.write(self.CodeTextArea.get("1.0", END))
            archi1.close()

            messagebox.showinfo("Informacion", "Los datos fueron guardados en la siguiente ruta: " + nombrearch + ".")


    def buttonClick(self, compare):
        cadena = self.CodeTextArea.get("1.0", 'end-1c')
        self.OutputTextArea.config(state=NORMAL)
        self.OutputTextArea.delete("1.0",END)
        
        if cadena.strip() != "":
            lexicalAnalizer(cadena)
            sintacticAnalizer(cadena)

            for i in errores:
                self.OutputTextArea.insert(END,errores)
                self.OutputTextArea.insert(END,'\n')
                
            for j in error:
                self.OutputTextArea.insert(END,error)
                self.OutputTextArea.insert(END,'\n')
            if errores == [] and error == []:
                for k in prints:
                    self.OutputTextArea.insert(END,prints)
                    self.OutputTextArea.insert(END,'\n')
            
            self.OutputTextArea.config(state=DISABLED)
        
        else:
            
            messagebox.showwarning("Error","Debes escribir codigo!!")
        
        errores.clear()
        error.clear()

        if compare:
            print("run button")
        else:
            print("compile button")


    def setCodeTextArea(self, output):
        self.CodeTextArea.delete('1.0', END)
        self.CodeTextArea.insert(INSERT, output)

    #def setOutputText(self, output):
        #self.OutputTextArea.insert(INSERT, errores)
        #self.OutputTextArea.insert(INSERT,error)

    #################### Funciones numero de linea del codigo ####################################

    def onScrollPress(self, *args):
        self.uniscrollbar.bind("<B1-Motion>", self.linenumbers.redraw)

    def onScrollRelease(self, *args):
        self.uniscrollbar.unbind("<B1-Motion>", self.linenumbers.redraw)

    def onPressDelay(self, *args):
        self.MainWindow.after(2, self.linenumbers.redraw)

    def get(self, *args, **kwargs):
        return self.CodeTextArea.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.CodeTextArea.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.CodeTextArea.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.CodeTextArea.index(*args, **kwargs)

    def redraw(self):
        self.linenumbers.redraw()
                
class TextLineNumbers(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="#fff", font=14)
            i = self.textwidget.index("%s+1line" % i)      


IDE = Gui()