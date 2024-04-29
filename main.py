import serial
import time
from threading import Thread, Event
from queue import Queue


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
                length = (170 * (averageVolt - 22526)) / 167 #changed voltage equation for 150 ohms
                print('wire length is: ' + str(length))
                voltList = []

        except ValueError:
            print("Value Error")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
