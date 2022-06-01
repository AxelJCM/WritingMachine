
import pyfirmata
import time

if __name__ == '__main__':
    board = pyfirmata.Arduino('COM3')
    print("Communication Successfully started")

    servo = board.get_pin('d:11:s')
    #servo.write(90)

    def move_x(pos, dis):
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
        if pos == "Y-FRONT": #maximo 1000
            print("Entramos al y")
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


    #move_x("X-LEFT", 200)
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
    move_y("Y-BACK", 200)
    move_x("X-RIGHT", 700)







    #color("black")
    #time.sleep(2)
    #color("red")
    #time.sleep(2)
    #color("")
    #time.sleep(2)
    