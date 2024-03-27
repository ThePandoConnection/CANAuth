import serial
import time
import threading
from threading import Thread

class voltageThread(threading.Thread):
    def __init__(self, port, baudrate):
        threading.Thread.__init__(self)
        self.port = port
        self.baudrate = baudrate

    def run(self):
        print('Starting Monitoring')
        getVoltage(self.port, self.baudrate)
        print('Monitoring complete')

class messageThread(threading.Thread):
    def __init__(self, port, baudrate):
        threading.Thread.__init__(self)
        self.port = port
        self.baudrate = baudrate

    def run(self):
        print('Starting Monitoring')
        getMessage(self.port, self.baudrate)
        print('Monitoring complete')



def getVoltage(port, baudrate):
    ser = serial.Serial(port, baudrate)
    ser.open()
    print("Opened serial port")
    for line in ser.read():
        print(line)
    ser.close()

def getMessage(port, baudrate):
    ser = serial.Serial(port, baudrate)
    ser.open()
    print("Opened serial port")
    for line in ser.read():
        print(line)
    ser.close()


def main():
    threadVolt = voltageThread("COM13", 9600)
    threadVolt.start()
    threadMessage = messageThread("COM8", 9600)
    threadMessage.start()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
