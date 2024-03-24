from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5 import uic
import pyqtgraph as pg
import numpy as np


class GeneralView(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        uic.loadUi('general_view.ui', self)
        self.maxTopValue = parent.maxTopValue
        self.time = []
        self.setLayout(self.girdMain)
        self.data_all_ch = [[], [], [], [], []]
        self.now_time = 0
        self.interferences = 0
        self.graps = [self.graph1, self.graph2, self.graph3, self.graph4, self.graph5]
        for graph in self.graps:
            # graph.disableAutoRange()
            graph.setLimits(yMin=-10, yMax=100, xMin=0, xMax=parent.maxRightValue)
            graph.setBackground('w')

        self.maxRightValue = parent.maxRightValue
        self.pen = pg.mkPen(color=(255, 0, 0))

    def update_data(self, ind, num):
        self.data_all_ch[ind].append(num)
        self.time.append(self.now_time)
        self.now_time += 0.5
        if self.interferences < 15:
            self.interferences += 1
        else:
            self.interferences = 0
            for graph_ind in range(len(self.graps)):
                self.graps[graph_ind].plot(self.time, self.data_all_ch[graph_ind], pen=self.pen)

    def clear(self):
        self.data_all_ch = [[], [], [], [], []]
        self.time = []
        self.now_time = 0
        self.interferences = 0
        for graph in self.graps:
            graph.clear()