
import pyfirmata
import time

if __name__ == '__main__':
    board = pyfirmata.Arduino('COM3')
    print("Communication Successfully started")

    servo = board.get_pin('d:11:s')
    servo.write(90)

    def move_x(pos, dis):
        if pos == "X-RIGHT":
            board.digital[5].write(1)
            board.digital[6].write(1)
        elif pos == "X-LEFT":
            board.digital[5].write(0)
            board.digital[6].write(0)

        for i in range(dis):
            board.digital[2].write(1)
            board.digital[3].write(1)
            board.digital[2].write(0)
            board.digital[3].write(0)

    def move_y(pos, dis):
        if pos == "Y-FRONT":
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
    move_y("Y-FRONT", 1000)
    '''
    move_x("X-RIGHT", 1000)
    time.sleep(1)

    time.sleep(1)
    move_x("X-LEFT", 1000)
    time.sleep(1)
    move_y("Y-BACK", 1000)
    '''
    def color(col):
        if col == "black":
            servo.write(0)
        elif col == "red":
            servo.write(180)
        else:
            servo.write(90)
    '''
    color("black")
    time.sleep(2)
    color("red")
    time.sleep(2)
    color("")
    time.sleep(2)
    '''