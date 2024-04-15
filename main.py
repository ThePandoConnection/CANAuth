import serial
import time
import threading
from threading import Thread, Event



class voltageThread(Thread):
    def __init__(self, port, baudrate, record, stop):
        Thread.__init__(self)
        self.port = port
        self.baudrate = baudrate
        self.record = record
        self.stop = stop

    def run(self):
        print('Starting Monitoring')
        getVoltage(self.port, self.baudrate, self.record, self.stop)
        print('Monitoring complete')

class messageThread(Thread):
    def __init__(self, port, baudrate, record, stop):
        Thread.__init__(self)
        self.port = port
        self.baudrate = baudrate
        self.record = record
        self.stop = stop

    def run(self):
        print('Starting Monitoring')
        getMessage(self.port, self.baudrate, self.record, self.stop)
        print('Monitoring complete')



def getVoltage(port, baudrate, record, stop):
    if record.is_set():
        ser = serial.Serial(port, baudrate)
        ser.open()
        print("Opened voltage serial port")
        for line in ser.read():
            print(line)
            if stop.is_set():
                ser.close()
        ser.close()

def getMessage(port, baudrate, record, stop):
    ser = serial.Serial(port, baudrate)
    ser.open()
    print("Opened message serial port")
    for line in ser.read():
        print(line)
        if "__ID" in line:
            print(line)
            record.set()
        if line == " ":
            stop.set()
            record.clear()
    ser.close()


def main():
    record = Event()
    stop = Event()
    threadMessage = messageThread("COM8", 9600, record, stop)
    threadMessage.start()
    threadVolt = voltageThread("COM13", 9600, record, stop)
    threadVolt.start()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
