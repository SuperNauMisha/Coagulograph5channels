from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5 import uic
import pyqtgraph as pg
import numpy as np


class GeneralWiev(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        uic.loadUi('general_view.ui', self)
        self.maxTopValue = parent.maxTopValue
        self.setLayout(self.girdMain)
        self.graps = [self.graph1, self.graph2, self.graph3, self.graph4, self.graph5]
        for graph in self.graps:
            # graph.disableAutoRange()
            graph.setLimits(yMin=-10, yMax=100, xMin=0, xMax=parent.maxRightValue)
            graph.setBackground('w')

        self.maxRightValue = parent.maxRightValue
        pen = pg.mkPen(color=(255, 0, 0))