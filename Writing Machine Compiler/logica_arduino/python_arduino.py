
import pyfirmata
from logica_arduino import movimientos

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
    #board = ""
    print("Communication Successfully started")

    servo = board.get_pin('d:11:s')
    servo.write(90)

    def move_x(pos, dis):
        sumarCoordenada(pos, dis)
        if pos == "X-LEFT": #maximo 1500
            board.digital[5].write(1)
            board.digital[6].write(1)

        elif pos == "X-RIGHT":
            board.digital[5].write(0)
            board.digital[6].write(0)

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

        elif pos == "Y-BACK":
            board.digital[5].write(0)
            board.digital[6].write(1)

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

            else:
                board.digital[5].write(0)

            for i in range(dis):
                board.digital[2].write(1)
                board.digital[2].write(0)

        else:
            if tipo == "SO":
                board.digital[6].write(1)

            else:
                board.digital[6].write(0)

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

        elif col == "black":
            servo.write(180)

        else:
            servo.write(90)

    def inicio():
        global analizandoCoordenadas
        move_y("Y-BACK", 500)
        move_x("X-LEFT", 800)
        analizandoCoordenadas = True

    def analizar_Diagonales():
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
        
        analizar_Diagonales()


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
    
    def begin():
        global analizandoCoordenadas, cordenada_x, cordenada_y, analizarDiagonales
        print("----Reiniciando----")
        
        analizar_Diagonales()


        if cordenada_x < 0:
            move_x("X-RIGHT", abs(cordenada_x))

        elif cordenada_x > 0:
            move_x("X-LEFT", abs(cordenada_x))

        if cordenada_y > 0:
            move_y("Y-BACK", abs(cordenada_y))

        elif cordenada_y < 0:
            move_y("Y-FRONT", abs(cordenada_y))

    def begin_espe(x = None, y = None):
        analizar_Diagonales()

        if x != None:
            if cordenada_x < 0:
                move_x("X-RIGHT", abs(x))

            elif cordenada_x > 0:
                move_x("X-LEFT", abs(x))

        else:
            if cordenada_y > 0:
                move_y("Y-BACK", abs(y))

            elif cordenada_y < 0:
                move_y("Y-FRONT", abs(y))
        
    def Pos(x, y):
        if x > 0:
            move_x("X-RIGHT", abs(x))
        
        else:
            move_x("X-LEFT", abs(x))


        if y > 0:
            move_y("Y-FRONT", abs(y))

        else:
            move_y("Y-BACK", abs(y))

    def PosX(x):
        if x > 0:
            move_x("X-RIGHT", abs(x))
        
        else:
            move_x("X-LEFT", abs(x))

    def PosY(y):
        if y > 0:
            move_y("Y-FRONT", abs(y))

        else:
            move_y("Y-BACK", abs(y))

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
    
    def arte():
        color("black")
        izq(300)#cuadrado 1
        back(300)
        der(300)
        front(300)

        color("red")
        front(100)#rectangulo 2
        der(300)
        back(100)
        izq(300)

        color("black") #rombo 3
        diagonal("NE", 500)
        diagonal("NO", 500)
        diagonal("SO", 500)
        diagonal("SE", 500)

        color("") #rombo rectangular 4
        front(100)
        color("red")
        diagonal("NE", 800)
        diagonal("SE", 500)
        diagonal("SO", 800)
        diagonal("NO", 500)

        color("") #rombo rectagular 5
        back(100)
        back(150)
        diagonal("NO", 300)
        diagonal("SO", 150)
        diagonal("SE", 300)
        diagonal("NE", 150)

        #LETRAS TEC
        color("")
        back(250)
        der(300)
        color("black")

        izq(150) #letra T
        color("")
        der(75)
        color("black")
        back(100)
        color("")
        izq(75)
        izq(150)

        color("black") #letra E
        izq(150)
        color("")
        front(33)
        der(75)
        color("black")
        der(75)
        color("")
        back(33)
        color("black")
        front(100)
        izq(150)
        color("")
        izq(150)

        color("black") #letra C
        izq(150)
        color("")
        der(150)
        color("black")
        back(100)
        izq(150)
        color("")

    inicio()
    arte()
    reiniciar()


    #color("black")
    #time.sleep(2)
    #color("red")
    #time.sleep(2)
    #color("")
    #time.sleep(2)