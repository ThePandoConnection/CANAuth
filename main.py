import serial


def main():
    serV = serial.Serial("COM3", 9600)  # Open Serial Port for Voltage
    serM = serial.Serial("COM6", 115200)  # Open Serial Port for Message content
    print("Opened Voltage serial port")
    print("Opened Message serial port")
    voltList = []
    while True:
        try:
            line = float(serV.readline().decode().strip())  # Take value from Voltage reading
            if line < 25000:  # If voltage less than 25000 start recording
                recording = True
                while recording:  # Keep looping while recording set
                    lineLow = float(serV.readline().decode().strip())  # Record voltage value
                    if (lineLow < 25000):  # If that value goes above 25000 stop recording
                        voltList.append(lineLow)
                    else:
                        recording = False
                ID = serM.readline().decode().strip()
                print(ID)  # Print ID from message
                averageVolt = sum(voltList) / len(voltList)  # Calculate average voltage
                print(averageVolt)  # Print average voltage
                length = (170 * (averageVolt - 22500)) / 167  # Calculate Length from voltage
                print('wire length is: ' + str(length))  # Print length
                voltList = []  # Clear average voltage list
                if not (abs(int(ID[-2:])-int(length)/50) < 0.5):  # ID 1,2,3,4 = 50,100,150,200 so if length/50 != ID then error
                    print("Error: Invalid ID detected")
                    serV.close()
                    serM.close()
                    break



        except ValueError:
            print("Value Error")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
