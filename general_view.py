from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5 import uic
import pyqtgraph as pg
import numpy as np


class GeneralView(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        uic.loadUi('general_view.ui', self)
        self.cbCh1.stateChanged.connect(self.ch1Changed)
        self.cbCh2.stateChanged.connect(self.ch2Changed)
        self.cbCh3.stateChanged.connect(self.ch3Changed)
        self.cbCh4.stateChanged.connect(self.ch4Changed)
        self.cbCh5.stateChanged.connect(self.ch5Changed)
        self.maxTopValue = parent.maxTopValue
        self.time = [0.0]
        self.setLayout(self.girdMain)
        self.data_all_ch = [[], [], [], [], []]
        self.check_boxes = [True, True, True, True, True]
        self.now_time = 0
        self.interferences = 0
        self.parent = parent
        self.graps = [self.graph1, self.graph2, self.graph3, self.graph4, self.graph5]
        for graph in self.graps:
            graph.setLimits(yMin=-10, yMax=100, xMin=0, xMax=parent.maxRightValue)
            graph.setBackground('w')

        self.maxRightValue = parent.maxRightValue
        self.pen = pg.mkPen(color=(255, 0, 0))

    def ch1Changed(self):
        if self.cbCh1.isChecked():
            self.graph1.setEnabled(True)
            self.check_boxes[0] = True
            self.graph1.setBackground('w')
        else:
            self.graph1.setEnabled(False)
            self.check_boxes[0] = False
            self.graph1.setBackground('gray')
        self.parent.updateGlobalInfo()

    def ch2Changed(self):
        if self.cbCh2.isChecked():
            self.graph2.setEnabled(True)
            self.check_boxes[1] = True
            self.graph2.setBackground('w')
        else:
            self.graph2.setEnabled(False)
            self.check_boxes[1] = False
            self.graph2.setBackground('gray')
        self.parent.updateGlobalInfo()

    def ch3Changed(self):
        if self.cbCh3.isChecked():
            self.graph3.setEnabled(True)
            self.check_boxes[2] = True
            self.graph3.setBackground('w')
        else:
            self.graph3.setEnabled(False)
            self.check_boxes[2] = False
            self.graph3.setBackground('gray')
        self.parent.updateGlobalInfo()

    def ch4Changed(self):
        if self.cbCh4.isChecked():
            self.graph4.setEnabled(True)
            self.check_boxes[3] = True
            self.graph4.setBackground('w')
        else:
            self.graph4.setEnabled(False)
            self.check_boxes[3] = False
            self.graph4.setBackground('gray')
        self.parent.updateGlobalInfo()

    def ch5Changed(self):
        if self.cbCh5.isChecked():
            self.graph5.setEnabled(True)
            self.check_boxes[4] = True
            self.graph5.setBackground('w')
        else:
            self.graph5.setEnabled(False)
            self.check_boxes[4] = False
            self.graph5.setBackground('gray')
        self.parent.updateGlobalInfo()

    def update_data(self, ind, num):
        try:
            self.data_all_ch[ind].append(num)
            time = [i * 0.5 for i in range(len(self.data_all_ch[ind]))]
            if self.interferences < 15:
                self.interferences += 1
            else:
                self.interferences = 0
                self.graps[ind].plot(time, self.data_all_ch[ind], pen=self.pen)
        except Exception as err:
            print("errr", err)

    def generalImport(self, ind, time, data):
        self.graps[ind].plot(time, data, pen=self.pen)


    def clear(self):
        self.data_all_ch = [[], [], [], [], []]
        self.time = []
        self.now_time = 0
        self.interferences = 0
        for graph in self.graps:
            graph.clear()