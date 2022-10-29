from tkinter import *
from struct import unpack
from collections import deque
import matplotlib.pyplot as plt
import threading
import serial
import pandas as pd
from scipy import signal
import sys
import glob

ID = 11
SIZE = 28
FORMAT = '<BHHHHHHHHBBBBBBBLB'

car = deque(200 * [''], 200)
accx = deque(200 * [0], 200)
accy = deque(200 * [0], 200)
accz = deque(200 * [0], 200)
rpm = deque(200 * [0], 200)
speed = deque(200 * [0], 200)
temp_motor = deque(200 * [0], 200)
flags = deque(200 * [0], 200)
soc = deque(200 * [0], 200)
temp_cvt = deque(200 * [0], 200)
volt = deque(200 * [0], 200)
latitude = deque(200 * [0], 200)
longitude = deque(200 * [0], 200)
timestamp = deque(200 * [0], 200)
eixo = deque(200 * [0], 200)

b, a = signal.butter(1, 0.1, analog=False)

car_save = []
accx_save = []
accy_save = []
accz_save = []
rpm_save = []
speed_save = []
temp_motor_save = []
flags_save =[]
soc_save = []
temp_cvt_save = []
volt_save = []
latitude_save = []
longitude_save = []
timestamp_save = []


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class Receiver(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)
        self.com = self.connectSerial(serial_ports())
        print(f'Connected into {self.com}')

    def connectSerial(self, USB_PORT):
        com = []
        for usb in USB_PORT:
            try:
                com = serial.Serial(f'{usb}', 115200)
            except:
                print("Tentativa...")
                com = []
            if com:
                break

        if not com:
            raise Exception("Não há nenhuma porta serial disponível")
        else:
            return com

    def run(self):
        self.com.flush()

        while True:
            try:
                self.checkData()
            except:
                break

    def checkData(self):
        c = 0
        while c != b'\xff':
            c = self.com.read()
            # print(f'trying, {c}')
        msg = self.com.read(SIZE)
        # print(msg)
        pckt = list(unpack(FORMAT, msg))
        # print(pckt)
        # print((pckt[25]/65535)*5000)
        if pckt[0] == 22:
            car.append("MB2")
            accx.append(pckt[1] * 0.061 / 1000)
            accy.append(pckt[2] * 0.061 / 1000)
            accz.append(pckt[3] * 0.061 / 1000)
            rpm.append((pckt[7] / 65535) * 5000)
            speed.append((pckt[8] / 65535) * 60)
            temp_motor.append(pckt[9])
            flags.append(pckt[10])
            soc.append(pckt[11])
            temp_cvt.append(pckt[12])
            volt.append(pckt[13])
            latitude.append(pckt[14])
            longitude.append(pckt[15])
            timestamp.append(pckt[16])

            car_save.append("MB2")
            accx_save.append(pckt[1] * 0.061 / 1000)
            accy_save.append(pckt[2] * 0.061 / 1000)
            accz_save.append(pckt[3] * 0.061 / 1000)
            rpm_save.append((pckt[7] / 65535) * 5000)
            speed_save.append((pckt[8] / 65535) * 60)
            temp_motor_save.append(pckt[9])
            flags_save.append(pckt[10])
            soc_save.append(pckt[11])
            temp_cvt_save.append(pckt[12])
            volt_save.append(pckt[13])
            latitude_save.append(pckt[14])
            longitude_save.append(pckt[15])
            timestamp_save.append(pckt[16])
        if pckt[0] == 11:
            car.append("MB1")
            accx.append(pckt[1] * 0.061 / 1000)
            accy.append(pckt[2] * 0.061 / 1000)
            accz.append(pckt[3] * 0.061 / 1000)
            rpm.append((pckt[7] / 65535) * 5000)
            speed.append((pckt[8] / 65535) * 60)
            temp_motor.append(pckt[9])
            flags.append(pckt[10])
            soc.append(pckt[11])
            temp_cvt.append(pckt[12])
            volt.append(pckt[13])
            latitude.append(pckt[14])
            longitude.append(pckt[15])
            timestamp.append(pckt[16])

            car_save.append("MB1")
            accx_save.append(pckt[1] * 0.061 / 1000)
            accy_save.append(pckt[2] * 0.061 / 1000)
            accz_save.append(pckt[3] * 0.061 / 1000)
            rpm_save.append((pckt[7] / 65535) * 5000)
            speed_save.append((pckt[8] / 65535) * 60)
            temp_motor_save.append(pckt[9])
            flags_save.append(pckt[10])
            soc_save.append(pckt[11])
            temp_cvt_save.append(pckt[12])
            volt_save.append(pckt[13])
            latitude_save.append(pckt[14])
            longitude_save.append(pckt[15])
            timestamp_save.append(pckt[16])

        data = {
            'Tempo': timestamp_save,
            'Carro': car_save,
            'Aceleração X': accx_save,
            'Aceleração Y': accy_save,
            'Aceleração Z': accz_save,
            'RPM': rpm_save,
            'Velocidade': speed_save,
            'Temperatura': temp_motor_save
        }
        csv = pd.DataFrame(data , columns=['Tempo', 'Carro', 'Aceleração X', 'Aceleração Y', 'Aceleração Z', 'RPM',
                                          'Velocidade', 'Temperatura'])
        #csv.to_csv('dados_telemetria.csv')


def button_press():

    cont = 0
    rpm_plt = plt.subplot2grid((3, 3), (1, 2), rowspan=2)
    speed_plt = plt.subplot2grid((3, 3), (0, 1), colspan=2)
    temp_plt = plt.subplot2grid((3, 3), (0, 0))
    imu_plt = plt.subplot2grid((3, 3), (1, 0), colspan=2, rowspan=2)

    while True:
        rpm_plt.clear()
        speed_plt.clear()
        imu_plt.clear()
        temp_plt.clear()

        cont += 1
        eixo.append(cont)

        sig_rpm = signal.filtfilt(b, a, rpm)
        sig_speed = signal.filtfilt(b, a, speed)
        sig_accx = signal.filtfilt(b, a, accx)
        sig_accy = signal.filtfilt(b, a, accy)
        sig_accz = signal.filtfilt(b, a, accz)

        # print(temp)
        temp_plt.plot(eixo, temp_motor, 'c-', marker="h")
        temp_plt.set_title('Temperatura ' + car[-1])
        temp_plt.set_xlim(-50 + cont, cont)
        temp_plt.set_ylim(0, 90)

        rpm_plt.plot(eixo, sig_rpm, 'c-', marker="h")
        rpm_plt.set_title('Rotação do motor ' + car[-1])
        rpm_plt.set_xlim(-50 + cont, cont)
        rpm_plt.set_ylim(0, 6000)

        speed_plt.plot(eixo, sig_speed, 'k-', marker="h")
        speed_plt.set_title('Velocidade ' + car[-1])
        speed_plt.set_xlim(-50 + cont, cont)
        speed_plt.set_ylim(0, 80)
        plt.grid(True)

        imu_plt.plot(eixo, sig_accx, 'b-', marker="h", label='Eixo X')
        imu_plt.plot(eixo, sig_accy, 'r-', marker="h", label='Eixo Y')
        imu_plt.plot(eixo, sig_accz, 'g-', marker="h", label='Eixo Z')
        imu_plt.set_title('Aceleração ' + car[-1])
        imu_plt.set_xlim(-200 + cont, cont)
        imu_plt.set_ylim(-4, 4)
        imu_plt.legend()

        plt.pause(0.05)

        global stop_threads
        if stop_threads:
            plt.close()
            box.com.close()
            break


def button_press2():
    global stop_threads
    stop_threads = True


window = Tk()
window.title("Telemetria Mangue Baja")
window.geometry('272x75')
flag = False
stop_threads = False

btn1 = Button(window, text="Start", command=button_press)
btn1.grid(column=0, row=0)
btn1.config(height=5, width=21)
btn2 = Button(window, text="Stop", command=button_press2)
btn2.grid(column=1, row=0)
btn2.config(height=5, width=21)

box = Receiver(name='serial_port')
box.start()

window.mainloop()
