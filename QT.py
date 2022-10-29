from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import io
import folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView #erro de biblioteca QtEngineCore
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from random import randint


class Ui_MainWindow(object):
    def __init__(self):
        self.webView = QWebEngineView()
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0, 100) for _ in range(100)]  # 100 data points

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(885, 459)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.map = QVBoxLayout(self.centralwidget)
        self.map.setGeometry(QtCore.QRect(10, 10, 461, 251))
        self.map.setObjectName("map")

        self.graph_rot = pg.PlotWidget(self.centralwidget)
        self.graph_rot.setGeometry(QtCore.QRect(10, 290, 221, 150))
        self.graph_rot.setObjectName("graph_rot")
        self.graph_rot.setBackground('w')
        self.graph_rot.setTitle("RPM", color='r')

        self.graph_vel = pg.PlotWidget(self.centralwidget)
        self.graph_vel.setGeometry(QtCore.QRect(250, 290, 221, 150))
        self.graph_vel.setObjectName("graph_vel")
        self.graph_vel.setBackground('w')
        self.graph_vel.setTitle("Velocidade", color='b')

        font = QtGui.QFont()
        font.setPointSize(16)

        self.acc_x = QtWidgets.QLabel(self.centralwidget)
        self.acc_x.setGeometry(QtCore.QRect(510, 10, 101, 51))
        self.acc_x.setObjectName("acc_x")
        self.acc_x.setFont(font)

        self.acc_y = QtWidgets.QLabel(self.centralwidget)
        self.acc_y.setGeometry(QtCore.QRect(640, 10, 101, 51))
        self.acc_y.setObjectName("acc_y")
        self.acc_y.setFont(font)

        self.acc_z = QtWidgets.QLabel(self.centralwidget)
        self.acc_z.setGeometry(QtCore.QRect(770, 10, 101, 51))
        self.acc_z.setObjectName("acc_z")
        self.acc_z.setFont(font)

        self.fuel = QtWidgets.QLabel(self.centralwidget)
        self.fuel.setGeometry(QtCore.QRect(510, 60, 161, 200))
        self.fuel.setObjectName("fuel")
        self.fuel.setText("")
        self.fuel.setPixmap(QtGui.QPixmap("fuel_empty.jpg"))
        self.fuel.setScaledContents(True)

        self.batt = QtWidgets.QLabel(self.centralwidget)
        self.batt.setGeometry(QtCore.QRect(690, 110, 161, 101))
        self.batt.setObjectName("batt")
        self.batt.setFont(font)

        self.temp_motor = QtWidgets.QLabel(self.centralwidget)
        self.temp_motor.setGeometry(QtCore.QRect(690, 240, 161, 101))
        self.temp_motor.setObjectName("temp_motor")
        self.temp_motor.setFont(font)

        self.temp_cvt = QtWidgets.QLabel(self.centralwidget)
        self.temp_cvt.setGeometry(QtCore.QRect(510, 240, 161, 101))
        self.temp_cvt.setObjectName("temp_cvt")
        self.temp_cvt.setFont(font)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(570, 370, 181, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(770, 370, 101, 31))
        self.pushButton.setObjectName("pushButton")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 885, 19))
        self.menubar.setObjectName("menubar")
        self.menuOp_es = QtWidgets.QMenu(self.menubar)
        self.menuOp_es.setObjectName("menuOp_es")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionStart = QtWidgets.QAction(MainWindow)
        self.actionStart.setObjectName("actionStart")
        self.actionStop = QtWidgets.QAction(MainWindow)
        self.actionStop.setObjectName("actionStop")
        self.menuOp_es.addAction(self.actionStart)
        self.menuOp_es.addAction(self.actionStop)
        self.menubar.addAction(self.menuOp_es.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def update_plots(self, rot_x, rot_y, vel_x, vel_y):
        self.rpm_pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.vel_pen = pg.mkPen(color=(0, 0, 255), width=2)
        self.dataline_rpm = self.graph_rot.plot(rot_x, rot_y, pen=self.rpm_pen)
        self.dataline_vel = self.graph_vel.plot(vel_x, vel_y, pen=self.vel_pen)

    def update_random(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0, 100))  # Add a new random value.

        self.dataline_rpm.setData(self.x, self.y)  # Update the data.
        self.dataline_vel.setData(self.x, self.y)  # Update the data.

    def update_map(self, coordinate):

        self.m = folium.Map(
            tiles='Stamen Terrain',
            zoom_start=15,
            location=coordinate
        )
        folium.Marker(location=coordinate).add_to(self.m)
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)
        self.webView.setFixedWidth(461)
        self.webView.setFixedHeight(251)
        self.webView.setHtml(self.data.getvalue().decode())

        self.map.addWidget(self.webView, 0, QtCore.Qt.AlignTop)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mangue Telemetria"))

        self.update_map((-8.05428, -34.8813))
        self.update_plots([0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4])
        self.acc_x.setText(_translate("MainWindow", "Acc x = 0g"))
        self.acc_y.setText(_translate("MainWindow", "Acc y = 0g"))
        self.acc_z.setText(_translate("MainWindow", "Acc z = 0g"))
        self.batt.setText(_translate("MainWindow", "Bateria = 0%"))
        self.temp_motor.setText(_translate("MainWindow", "Motor = 0ºC"))
        self.temp_cvt.setText(_translate("MainWindow", "CVT = 0ºC"))
        self.comboBox.setItemText(0, _translate("MainWindow", "BOX"))
        self.pushButton.setText(_translate("MainWindow", "Enviar"))
        self.menuOp_es.setTitle(_translate("MainWindow", "Opções"))
        self.actionStart.setText(_translate("MainWindow", "Start"))
        self.actionStop.setText(_translate("MainWindow", "Stop"))
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_random)
        self.timer.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #ui.acc_x.setText('Acc: x = 2g')
    #exemplo: ui.acc_x.setText("Acc x = 2g")
    sys.exit(app.exec_())
