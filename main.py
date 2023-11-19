import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLabel
from PyQt5 import uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg

# Creating the main window
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.title = 'Coagulograph'
        self.left = 500
        self.top = 300
        self.width = 700
        self.height = 500
        self.setWindowTitle(self.title)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = MyTab(self)
        self.tab2 = MyTab(self)
        self.tab3 = MyTab(self)
        self.tab4 = MyTab(self)
        self.tab5 = MyTab(self)

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




class MyTab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        uic.loadUi('channel.ui', self)
        # Create first tab
        self.setLayout(self.tabsMain)
        self.graph.addLegend()
        self.graph.disableAutoRange()
        self.graph.setLimits(yMin=-10, yMax=100, xMin=0, xMax=1800)
        self.graph.setBackground('w')
        self.pen = pg.mkPen(color=(255, 0, 0))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
