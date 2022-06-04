from logica_arduino import python_arduino as pa
import time

tiempoPausa = 0.5
color = "black"

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
    global color, tiempoPausa
    print(body)

    pa.inicio()

    for i in body:
        if i[0] == "ContinueDown":
            pa.back(i[1])

        elif i[0] == "ContinueUp":
            pa.front(i[1])

        elif i[0] == "ContinueRight":
            pa.der(i[1])

        elif i[0] == "ContinueLeft":
            pa.izq(i[1])

        elif i[0] == "Pos":
            pa.begin()
            pa.Pos(i[1][0], i[1][1])

        elif i[0] == "PosX":
            pa.begin_espe(x=i[1])
            pa.PosX(i[1])

        elif i[0] == "PosY":
            pa.begin_espe(y=i[1])
            pa.PosY(i[1])

        elif i[0] == "UseColor":
            if i[1] == 1:
                color = "black"

            else:
                color = "red"

        elif i[0] == "Down":
            pa.color(color)

        elif i[0] ==  "Up":
            pa.color("")

        elif i[0] == "Beginning":
            pa.begin()

        elif i[0] == "Speed": #tiempo en milisegundos
            tiempoPausa = i[1] / (1000)

        time.sleep(tiempoPausa)

    pa.reiniciar()