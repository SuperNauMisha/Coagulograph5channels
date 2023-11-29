import sys
import datetime
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLabel
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from PyQt5 import uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from channel import Channel

# Creating the main window
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.title = "Коагулограф"
        self.left = 500
        self.top = 300
        self.width = 700
        self.height = 500
        self.setWindowTitle(self.title)
        self.maxTopValue = 600
        self.maxRightValue = 2000
        self.chChars = ['@', '#', '$', '%', '^']

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = Channel(self)
        self.tab2 = Channel(self)
        self.tab3 = Channel(self)
        self.tab4 = Channel(self)
        self.tab5 = Channel(self)
        self.tabsList = [self.tab1, self.tab2, self.tab3, self.tab4, self.tab5]

        # Add tabs
        self.tabs.addTab(self.tab1, "Channel 1")
        self.tabs.addTab(self.tab2, "Channel 2")
        self.tabs.addTab(self.tab3, "Channel 3")
        self.tabs.addTab(self.tab4, "Channel 4")
        self.tabs.addTab(self.tab5, "Channel 5")

        self.tabsLayout.addWidget(self.tabs)
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        self.setCentralWidget(self.centralWidget)
        self.show()

        self.strok_data = ''
        self.oldstrok_data = ''
        self.output_rate = 10
        self.counter_rate = 0
        self.setWindowTitle("Коагулограф")
        self.dt_now = datetime.datetime.today()
        self.dateTimeEdit.setDateTime(self.dt_now)
        self.interferences = 0
        self.connectButton.clicked.connect(self.buttonConDis)
        self.saveButton.clicked.connect(self.save)
        self.clearButton.clicked.connect(self.onClear)
        self.importButton.clicked.connect(self.onImport)
        # self.calculateButon.clicked.connect(self.calculate)
        self.serial = QSerialPort()
        self.serial.setBaudRate(9600)
        self.isConnected = False

        self.ports_name_list = []
        self.ports_num_list = []
        ports = QSerialPortInfo().availablePorts()
        for port in ports:
            full_name = port.portName() + " " + port.description()
            print(full_name)
            self.ports_name_list.append(full_name)
            self.ports_num_list.append(port.portName())
            print(full_name)

        self.ports.addItems(self.ports_name_list)
        self.serial.readyRead.connect(self.onRead)

    def buttonConDis(self):
        if self.connectButton.text() == "Начать":
            self.connectButton.setText("Остановить")
            self.onConnect()
        elif self.connectButton.text() == "Остановить":
            self.connectButton.setText("Начать")
            self.onDisconnect()

    def onConnect(self):
        print("connect")
        choose_index = self.ports_name_list.index(self.ports.currentText())
        choose_com_port = self.ports_num_list[choose_index]
        print(choose_com_port)
        self.serial.setPortName(choose_com_port)
        self.serial.open(QIODevice.ReadOnly)
        self.serial.readyRead.connect(self.onRead)

    def onDisconnect(self):
        print("disconnect")
        self.serial.close()


    def onClear(self):

        for tab in self.tabsList:
            tab.cnClear()
        self.onDisconnect()
        self.interferences = 0
        self.oldstrok_data = ''
        self.strok_data = ''
        self.data_list = []
        self.norm_data_list = []
        self.time = []
        self.graph_data = []
        self.nameEdit.setText('')
        self.numEdit.setText('')
        self.diagnosisEdit.clear()
        self.conditionEdit.clear()
        # self.output.clear()
        self.dt_now = datetime.datetime.today()
        self.dateTimeEdit.setDateTime(self.dt_now)
        # self.graph.clear()
        self.fibrinogenEdit.setValue(0)
        self.ptiEdit.setValue(0)
        self.mnoEdit.setValue(0)
        self.actvEdit.setValue(0)
        self.actEdit.setValue(0)
        self.addTimeEdit.setValue(0)
        self.ddimerEdit.setValue(0)
        self.trombEdit.setValue(0)
        # self.beforeClottingSlider.setValue(0)
        # self.afterClottingSlider.setValue(0)
        self.medicationEdit.clear()

    def onRead(self):
        try:
            data = self.serial.readLine()
            self.strok_data = str(data)[2:-1]
            if r"\n" not in self.strok_data:
                self.oldstrok_data += self.strok_data
            else:
                self.oldstrok_data += self.strok_data
                num = self.oldstrok_data[1:-4]
                chChar = self.oldstrok_data[0]
                self.oldstrok_data = ''
                if chChar in self.chChars:
                    self.tabsList[self.chChars.index(chChar)].writeData(round(int(num) / self.maxTopValue * 100))
        except Exception as err:
            print("err", err)

    def save(self):
        print("save")

    def onImport(self):
        print("import")

    def calculate(self):
        self.tab1.chCalculate()
        self.tab2.chCalculate()
        self.tab3.chCalculate()
        self.tab4.chCalculate()
        self.tab5.chCalculate()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
