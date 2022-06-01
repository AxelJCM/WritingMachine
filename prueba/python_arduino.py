
import pyfirmata
import time
from movimientos import *

listaMovimientos = []
diagonalMov = True

cordenada_x = 0
cordenada_y = 0
analizandoCoordenadas = False

def sumarCoordenada(tipo, cant):
    global cordenada_x, cordenada_y
    if analizandoCoordenadas == True:
        if tipo == "X-LEFT":
            cordenada_x -= cant

        elif tipo == "X-RIGHT":
            cordenada_x += cant

        elif tipo == "Y-FRONT":
            cordenada_y += cant

        else:
            cordenada_y -= cant

        print("Coordenada X = " + str(cordenada_x))
        print("Coordenada Y = " + str(cordenada_y))

if __name__ == '__main__':
    board = pyfirmata.Arduino('COM3')
    print("Communication Successfully started")

    servo = board.get_pin('d:11:s')
    servo.write(90)

    def move_x(pos, dis):
        sumarCoordenada(pos, dis)
        if pos == "X-LEFT": #maximo 1500
            board.digital[5].write(1)
            board.digital[6].write(1)
            time.sleep(1)

        elif pos == "X-RIGHT":
            board.digital[5].write(0)
            board.digital[6].write(0)
            time.sleep(1)

        for i in range(dis):
            board.digital[2].write(1)
            board.digital[3].write(1)
            board.digital[2].write(0)
            board.digital[3].write(0)

    def move_y(pos, dis):
        sumarCoordenada(pos, dis)
        if pos == "Y-FRONT": #maximo 1000
            board.digital[5].write(1)
            board.digital[6].write(0)
            time.sleep(1)

        elif pos == "Y-BACK":
            board.digital[5].write(0)
            board.digital[6].write(1)
            time.sleep(1)

        for i in range(dis):
            board.digital[2].write(1)
            board.digital[3].write(1)
            board.digital[2].write(0)
            board.digital[3].write(0)

    def diagonal(tipo, dis): #SO
        global listaMovimientos
        if diagonalMov == True:
            listaMovimientos += [Movimiento(dis, tipo)]
        if tipo == "NO" or tipo == "SE":
            if tipo == "NO":
                board.digital[5].write(1)
                time.sleep(1)

            else:
                board.digital[5].write(0)
                time.sleep(1)

            for i in range(dis):
                board.digital[2].write(1)
                board.digital[2].write(0)

        else:
            if tipo == "SO":
                board.digital[6].write(1)
                time.sleep(1)

            else:
                board.digital[6].write(0)
                time.sleep(1)

            for i in range(dis):
                board.digital[3].write(1)
                board.digital[3].write(0)
    
    #move_y("Y-FRONT", 500)
    
    #move_x("X-RIGHT", 500)
    #time.sleep(1)

    #time.sleep(1)
    #move_x("X-LEFT", 1000)
    #time.sleep(1)
    #move_y("Y-BACK", 1000)
    
    def color(col):
        if col == "red":
            print("entrando")
            servo.write(0)
            time.sleep(1)

        elif col == "black":
            servo.write(180)
            time.sleep(1)

        else:
            servo.write(90)
            time.sleep(1)

    def inicio():
        global analizandoCoordenadas
        move_y("Y-BACK", 500)
        move_x("X-LEFT", 800)
        analizandoCoordenadas = True

    def analizarDiagonales():
        global listaMovimientos, diagonalMov
        listaMovimientos.reverse()
        diagonalMov = False
        for i in listaMovimientos:
            print(i.get_tipo())
            if i.get_tipo() == "NE":
                diagonal("SO", abs(i.get_x()))

            elif i.get_tipo() == "SO":
                diagonal("NE", abs(i.get_x()))

            elif i.get_tipo() == "NO":
                diagonal("SE", abs(i.get_x()))

            elif i.get_tipo() == "SE":
                diagonal("NO", abs(i.get_x()))

        listaMovimientos = []
        diagonalMov = True

            

    def reiniciar():
        global analizandoCoordenadas, cordenada_x, cordenada_y
        print("----Reiniciando----")
        
        analizarDiagonales()


        if cordenada_x < 0:
            move_x("X-RIGHT", abs(cordenada_x))

        elif cordenada_x > 0:
            move_x("X-LEFT", abs(cordenada_x))

        if cordenada_y > 0:
            move_y("Y-BACK", abs(cordenada_y))

        elif cordenada_y < 0:
            move_y("Y-FRONT", abs(cordenada_y))

        analizandoCoordenadas = False

        move_y("Y-FRONT", 500)
        move_x("X-RIGHT", 800)


    #move_x("X-LEFT", 200)

    def tec():
        
        #LETRA T    
        color("black")
        move_x("X-RIGHT", 100)
        color("")
        move_x("X-LEFT", 100)
        color("black")
        move_y("Y-FRONT", 200)
        color("")
        move_y("Y-BACK", 200)
        color("black")
        move_x("X-LEFT", 100)
        color("")

        #letra E
        move_x("X-LEFT", 100)
        color("red")
        move_y("Y-FRONT", 200)
        move_x("X-LEFT", 200)
        color("")
        move_y("Y-BACK", 100)
        color("red")
        move_x("X-RIGHT", 200)
        color("")
        move_y("Y-BACK", 100)
        color("red")
        move_x("X-LEFT", 200)
        color("")

        #LETRA C
        move_x("X-LEFT", 300)
        color("black")
        move_x("X-RIGHT", 200)
        move_y("Y-FRONT", 200)
        move_x("X-LEFT", 200)
        color("")
        #move_y("Y-BACK", 200)
        #move_x("X-RIGHT", 700)
        

    inicio()
    time.sleep(10)
    color("red")

    move_x("X-RIGHT", 200)
    diagonal("NE", 200)
    move_y("Y-BACK", 200)
    diagonal("SO", 200)
    move_x("X-LEFT", 200)
    diagonal("NO", 200)
    move_y("Y-FRONT", 200)
    diagonal("SE", 200)
    color("")
    reiniciar()


    #color("black")
    #time.sleep(2)
    #color("red")
    #time.sleep(2)
    #color("")
    #time.sleep(2)


def izq(num):
    move_x("X-LEFT", num)

def der(num):
    move_x("X-RIGHT", num)

def front(num):
    move_y("Y-FRONT", num)

def back(num):
    move_y("Y-BACK", num)

def col(clr):
    color(clr)