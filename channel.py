import sys
import datetime
import numpy as np
from PyQt5 import uic
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QTabWidget, QLabel


class Channel(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        uic.loadUi('channel.ui', self)
        self.maxTopValue = parent.maxTopValue
        self.setLayout(self.tabsMain)
        self.graph.addLegend()
        self.graph.disableAutoRange()
        self.graph.setLimits(yMin=-10, yMax=100, xMin=0, xMax=parent.maxRightValue)
        self.graph.setBackground('w')
        self.pen = pg.mkPen(color=(255, 0, 0))
        self.calculateButon.clicked.connect(parent.calculate)
        self.chanelData = []
        self.chanelTime = []
        self.norm_data_list = []
        self.now_time = 0
        self.interferences = 0

    def chCalculate(self):
        print("calculate")

    def chClear(self):
        self.chanelData = []
        self.chanelTime = []
        self.norm_data_list = []
        self.now_time = 0
        self.interferences = 0
        self.output.clear()
        self.graph.clear()
        self.beforeClottingSlider.setValue(0)
        self.afterClottingSlider.setValue(0)

    def chImport(self):
        self.graph.plot(self.chanelTime, self.chanelData, pen=self.pen)

    def writeData(self, data):
        self.chanelData.append(data)
        self.chanelTime.append(self.now_time)
        self.now_time += 1
        if self.interferences < 10:
            self.interferences += 1
        else:
            self.interferences = 0
            self.graph.plot(self.chanelTime, self.chanelData, pen=self.pen)