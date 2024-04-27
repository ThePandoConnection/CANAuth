import serial
import time
from threading import Thread, Event
from queue import Queue

class voltageThread(Thread):
    def __init__(self, port, baudrate, record, stop, share):
        Thread.__init__(self)
        self.port = port
        self.baudrate = baudrate
        self.record = record
        self.stop = stop
        self.share = share

    def run(self):
        print('Starting Monitoring')
        getVoltage(self.port, self.baudrate, self.record, self.stop, self.share)
        print('Monitoring complete')

class messageThread(Thread):
    def __init__(self, port, baudrate, record, stop, share):
        Thread.__init__(self)
        self.port = port
        self.baudrate = baudrate
        self.record = record
        self.stop = stop
        self.share = share

    def run(self):
        print('Starting Monitoring')
        getMessage(self.port, self.baudrate, self.record, self.stop, self.share)
        print('Monitoring complete')



def getVoltage(port, baudrate, record, stop, share):
    while True:
        if record.is_set():
            recording = True
            node = share.get()
            print(node)
            ser = serial.Serial(port, baudrate)
            print("Opened voltage serial port")
            domBits = []
            while recording:
                line = ser.readline().decode()
                print(line)
                if float(line) < 25000:
                    domBits.append(line)
                if stop.is_set():
                    recording = False
            ser.close()
            print(domBits)
            average = sum(domBits) / len(domBits)
            length = 170*(average - 2.25 * 10**4)/167
            print('The wire length is: ' + length)

def getMessage(port, baudrate, record, stop, share):
    ser = serial.Serial(port, baudrate)
    print("Opened message serial port")
    #ser.open()
    while True:
        line = int(ser.readline().decode().strip(" "))
        print(line)
        if line == 100:
            print('Stopping Voltage Monitoring')
            stop.set()
            record.clear()
        else:
            share.put(line)
            record.set()
    #ser.close()


def main():
    record = Event()
    stop = Event()
    share = Queue()
    threadMessage = messageThread("COM6", 115200, record, stop, share)
    threadMessage.start()
    threadVolt = voltageThread("COM3", 9600, record, stop, share)
    threadVolt.start()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
