from python_arduino import *

import time

tiempoPausa = 0.5
color_impr = "black"

def runSemanticAnalizer(parse):
    try:
        inicio(parse[1])
        procedimientos(parse[3])
    except:
        print('error de estructura')


def inicio(body):
    print(body)
    print(1)
    for i in body:
        print(i)
        print('\n')
    print(2)

def procedimientos(body): #[['continuedown', 200], ['begin', None]]
    global color_impr, tiempoPausa
    print("----Iniciando impresion---- ")
    color("")
    inicio_im()

    for i in body:
        if i[0] == "ContinueDown":
            back(i[1])

        elif i[0] == "ContinueUp":
            print("Iniciando el ContinueUp")
            front(i[1])

        elif i[0] == "ContinueRight":
            der(i[1])

        elif i[0] == "ContinueLeft":
            izq(i[1])

        elif i[0] == "Pos":
            begin()
            print("Despues del 00, se mueve")
            Pos(i[1][0], i[1][1])
            print(i[1][0], i[1][1])

        elif i[0] == "PosX":
            begin_espe(x=i[1])
            PosX(i[1])

        elif i[0] == "PosY":
            begin_espe(y=i[1])
            PosY(i[1])

        elif i[0] == "UseColor":
            if i[1] == 1:
                color_impr = "black"

            else:
                color_impr = "red"

        elif i[0] == "Down":
            color(color_impr)

        elif i[0] ==  "Up":
            color("")

        elif i[0] == "Beginning":
            begin()

        elif i[0] == "Speed": #tiempo en milisegundos
            tiempoPausa = i[1] / (1000)

        elif i[0] == "Diagonal":
            diagonal(i[1][0], i[1][1])

        time.sleep(tiempoPausa)
    color("")
    reiniciar()