import serial
import time
from threading import Thread, Event
from queue import Queue

class voltageThread(Thread):
    def __init__(self, port, baudrate, share):
        Thread.__init__(self)
        self.port = port
        self.baudrate = baudrate
        self.share = share

    def run(self):
        print('Starting Monitoring')
        getVoltage(self.port, self.baudrate, self.share)
        print('Monitoring complete')

class messageThread(Thread):
    def __init__(self, port, baudrate, share):
        Thread.__init__(self)
        self.port = port
        self.baudrate = baudrate
        self.share = share

    def run(self):
        print('Starting Monitoring')
        getMessage(self.port, self.baudrate, self.share)
        print('Monitoring complete')



def getVoltage(port, baudrate):
    return 0




def getMessage(port, baudrate, share):
    ser = serial.Serial(port, baudrate)
    print("Opened message serial port")
    #ser.open()
    while True:
        line = ser.readline().decode().strip(" ")
        print(line)
    ser.close()


def main():
    share = Queue()

    serV = serial.Serial("COM3", 9600)
    serM = serial.Serial("COM6", 115200)
    print("Opened Voltage serial port")
    print("Opened Message serial port")
    voltList = []
    # ser.open()
    while True:
        try:
            line = float(serV.readline().decode().strip())
            if line < 25000:
                recording = True
                while recording:
                    lineLow = float(serV.readline().decode().strip())
                    if lineLow < 25000:
                        voltList.append(lineLow)
                    else:
                        recording = False
                print(serM.readline().decode().strip())
                averageVolt = sum(voltList) / len(voltList)
                length = 170 * (averageVolt - 2.25 * 10 ** 4) / 167
                print('wire length is: ' + str(length), flush=True)
                voltList = []

        except ValueError:
            print("Value Error")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
