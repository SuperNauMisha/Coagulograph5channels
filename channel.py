from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5 import uic
import pyqtgraph as pg
import numpy as np






class Channel(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        uic.loadUi('channel.ui', self)
        self.maxTopValue = parent.maxTopValue
        self.setLayout(self.tabsMain)
        self.named_graph_data = parent.named_graph_data
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

    def chCalculate(self, parent):
        try:
            self.graph.clear()
            sigma = 0.25 #допуск для "плато" в долях
            period = 20
            data = np.array([np.array(self.chanelTime), np.array(self.chanelData)])
            self.addTime = parent.addTimeEdit.value()
            # (data[0, :] - координата времени, сек; data[1, :] - значение прибора(?), соответсвующий данному моменту времени).
            datanorm = self.contour(data, period) #перестраиваем на верхние и нижние пики. datanorm - четырёхмерный массив (NumPy):
            #(datanorm[0, :] - время верхних пиков, сек; datanorm[1, :] - значение верхних пиков; datanorm[2, :] - время нижних пиков, сек; datanorm[3, :] - значение нижних пиков).
            zeroboard = self.zeropoint(datanorm, np.min(data[1, :])) #граница ухода с начального плато (плато нулей) (одномерный массив (NumPy): [0] - координата границы, сек; [1] - индекс этой точки в datanorm).
            zeroboard[0] = self.beforeClottingSlider.value()

            for i in range(len(datanorm[0, :])):
                if datanorm[0, i] >= zeroboard[0]:
                    zeroboard[1] = i
                    break

            deltamin = self.mindeltapoint(datanorm, zeroboard[1]) # точка с минимальной шириной графика (одномерный массив (NumPy): [0] - ширина; [1] - координата, сек; [2] - индекс точки в datanorm).
            print(deltamin)
            deltamin[1] = self.afterClottingSlider.value()

            for i in range(len(datanorm[0, :])):
                if datanorm[0, i] >= deltamin[1]:
                    deltamin[2] = i
                    deltamin[0] = datanorm[1, i] - datanorm[3, i]
                    break

            plato = self.platopoint(datanorm, zeroboard[1], deltamin, sigma) # границы центрального плато (возле deltamin) plato - двухмерный массив (NumPy):
            #([0/1/2, 0]- координата левой/правой/трёхминутной границы, сек; [0/1/2, 1] - ширина графика в точке левой/правой/трёхминутной границы).
            #трёхминутная граница - точка, отстоящая от правой границы плато на 3 минуты.

            #рисуем график
            # любой из элементоф графика можно отключить, закомментировав его
            # self.graph.plot(data[0,:],data[1,:])



            self.graph.plot(self.chanelTime, self.chanelData, pen=self.pen)
            self.graph.plot(datanorm[0,:],datanorm[1,:], pen=pg.mkPen(color=(0, 0, 255)))
            self.graph.plot(datanorm[2, :], datanorm[3, :], name="Границы", pen=pg.mkPen(color=(0, 0, 255)))
            self.graph.plot([zeroboard[0], zeroboard[0]], [np.min(data[1, :])-10, np.max(data[1, :])+10], name=f'Время до начала свёртывания, t = {zeroboard[0]} сек', pen=pg.mkPen(color=(0, 0, 0), width=2))
            self.graph.plot([deltamin[1], deltamin[1]], [np.min(data[1, :])-10, np.max(data[1, :])+10], name=f'Время до окончания свёртывания, t = {deltamin[1]} сек', pen=pg.mkPen(color=(255, 0, 255), width=2))
            self.graph.plot([plato[0, 0], plato[0, 0]], [np.min(data[1, :])-10, np.max(data[1, :])+10], name=f'Время до начала ретракции, t = {plato[0, 0]} сек', pen=pg.mkPen(color=(255, 100, 166), width=2, style=Qt.DashLine))
            self.graph.plot([plato[1, 0], plato[1, 0]], [np.min(data[1, :])-10, np.max(data[1, :])+10], name=f'Время окончания ретракции, t = {plato[1, 0]} сек', pen=pg.mkPen(color=(255, 165, 0), width=2, style=Qt.DashLine))
            self.graph.plot([plato[2, 0], plato[2, 0]], [np.min(data[1, :])-10, np.max(data[1, :])+10], name=f'Амплитуда на 3 минуте фибринолиза = {plato[2, 1]}', pen=pg.mkPen(color=(0, 100, 100), width=2, style=Qt.DashDotDotLine))
            self.graph.showGrid(x=True, y=True)


            t_clotting = round(plato[0, 0] - zeroboard[0], 2) #Время свёртывания, сек
            v_clotting = round((datanorm[1, zeroboard[1]] - plato[0, 1]) / t_clotting * 60, 2) #Скорость свёртывания, ед/сек
            cof_retr = round((datanorm[1, zeroboard[1]] - deltamin[0]) / datanorm[1, zeroboard[1]] * 100, 2) #Коэффицент ректракции, %
            v_fibrin = round((plato[2, 1] - plato[1, 1]) / 180 * 60, 2) #Скорость нарастания фибринолиза, ед/сек
            cof_fibrin = round((plato[2, 1] - deltamin[0]) / plato[2, 1] * 100, 2) #Коэффицент фибринолиза, %
            act_fibrin = round(plato[2, 1] / (datanorm[1, zeroboard[1]] - deltamin[0]) * 100, 2)

            self.graph_data = [zeroboard[0] + self.addTime, deltamin[1] + self.addTime, t_clotting, plato[0, 0] + self.addTime, plato[1, 0],
                               plato[1, 0] - plato[0, 0], datanorm[1, zeroboard[1]], deltamin[0], plato[2, 1],
                               v_clotting, v_fibrin,
                               cof_retr, cof_fibrin, act_fibrin]


            strok_output = "Время до начала свёртывания, сек" + " " * (40 - len("Время до начала свёртывания, сек")) + str(zeroboard[0] + self.addTime) + " " * (10 - len(str(zeroboard[0] + self.addTime))) + self.secToMin(zeroboard[0] + self.addTime) + "\n"
            strok_output += "Время до окончания свёртывания, сек" + " " * (40 - len("Время до окончания свёртывания, сек")) + str(deltamin[1] + self.addTime) + " " * (10 - len(str(deltamin[1] + self.addTime))) + self.secToMin(deltamin[1] + self.addTime) + "\n"
            strok_output += "Длительность свёртывания, сек" + " " * (40 - len("Длительность свёртывания, сек")) + str(t_clotting) + " " * (10 - len(str(t_clotting))) + self.secToMin(t_clotting) + "\n"
            strok_output += "Время до начала ретракции, сек" + " " * (40 - len("Время до начала ретракции, сек")) + str(plato[0, 0] + self.addTime) + " " * (10 - len(str(plato[0, 0] + self.addTime))) + self.secToMin(plato[0, 0] + self.addTime) + "\n"
            strok_output += "Время до окончания ретракции, сек" + " " * (40 - len("Время до окончания ретракции, сек")) + str(plato[1, 0] + self.addTime) + " " * (10 - len(str(plato[1, 0] + self.addTime))) + self.secToMin(plato[1, 0] + self.addTime) + "\n"
            strok_output += "Длительность ретракции, сек" + " " * (40 - len("Длительность ретракции, сек")) + str(plato[1, 0] - plato[0, 0]) + " " * (10 - len(str(plato[1, 0] - plato[0, 0]))) + self.secToMin(plato[1, 0] - plato[0, 0]) + "\n"

            strok_output += "Максимальная амплитуда, ед" + " " * (40 - len("Максимальная амплитуда, ед")) + str(datanorm[1, zeroboard[1]]) + "\n"
            strok_output += "Минимальная амплитуда, ед" + " " * (40 - len("Минимальная амплитуда, ед")) + str(deltamin[0]) + "\n"
            strok_output += "Амплитуда на 3 минуте фибринолиза, ед" + " " * (40 - len("Амплитуда на 3 минуте фибринолиза, ед")) + str(plato[2, 1]) + "\n"

            strok_output += "Скорость свёртывания, ед/мин" + " " * (40 - len("Скорость свёртывания, ед/мин")) + str(v_clotting) + "\n"
            strok_output += "Скорость нарастания фибринолиза, ед/мин" + " " * (40 - len("Скорость нарастания фибринолиза, ед/мин")) + str(v_fibrin) + "\n"

            strok_output += "Коэффицент ректракции, %" + " " * (40 - len("Коэффицент ректракции, %")) + str(cof_retr) + "\n"
            strok_output += "Коэффицент фибринолиза, %" + " " * (40 - len("Коэффицент фибринолиза, %")) + str(cof_fibrin) + "\n"
            strok_output += "Активность фибринолиза, %" + " " * (40 - len("Активность фибринолиза, %")) + str(act_fibrin) + "\n"

            self.output.setPlainText(strok_output)
        except Exception as err:
            print(err)


    def secToMin(self, sec):
        min = int(sec // 60)
        last_sec = int(sec % 60)
        return f"({str(min)} мин {str(last_sec)} сек)"


    def contour(self, data, period):
        lendata = len(data[1, :])
        datanorm = np.zeros((4, lendata//period+1))


        maxloc = 0
        minloc = 0
        countnorm = 0

        for i in range(0, lendata, period):
            maxloc = np.argmax(data[1, i:i+period])
            minloc = np.argmin(data[1, i:i+period])
            datanorm[0,countnorm] = data[0,i+maxloc]
            datanorm[1,countnorm] = data[1,i+maxloc]
            datanorm[2,countnorm] = data[0,i+minloc]
            datanorm[3,countnorm] = data[1,i+minloc]
            countnorm = countnorm+1
        return datanorm


    def zeropoint(self, datanorm, min_of_data): #min_of_data = np.min(data[1, :])
        zeroboard = np.array([0,0])
        for countnorm in range(len(datanorm[1, :])):
            if (countnorm>2) and (datanorm[3, countnorm] > min_of_data) and (datanorm[3, countnorm-1] > min_of_data) and (datanorm[3, countnorm-2] >= min_of_data):
                zeroboard[0] = datanorm[2, countnorm-2]# + self.addTime
                zeroboard[1] = countnorm-2
                break
        return zeroboard


    def mindeltapoint(self, datanorm, zeroindex): #zeroindex = zeroboard[1]
        height = np.max(datanorm[1,:])-np.min(datanorm[1, :])
        deltamin = np.array([height, 0, 0])
        for countnorm in range(zeroindex,len(datanorm[1, :])):
            delta = datanorm[1, countnorm] - datanorm[3, countnorm]
            if (delta < deltamin[0]):
                deltamin[0] = delta
                deltamin[1] = (datanorm[0, countnorm]+datanorm[2, countnorm])/2
                deltamin[2] = countnorm
        return deltamin


    def platopoint(self, datanorm, zeroindex, deltamin, sigma):
        plato = np.array([[deltamin[1],deltamin[0]], [deltamin[1], deltamin[0]], [0,0]])
        stopper = 0
        rightindex = int(deltamin[2])
        for i in range (int(deltamin[2]), int(zeroindex), -1):
            deltanext = datanorm[1, i] - datanorm[3, i]
            delta = datanorm[1, i-1] - datanorm[3, i-1]
            deltalast = datanorm[1, i-2] - datanorm[3, i-2]
            if (delta <= deltamin[0]*(1+sigma)) and (deltanext <= deltamin[0]*(1+sigma)) and (deltalast <= deltamin[0]*(1+sigma)):
                plato[0,0] = (datanorm[0,i-2]+datanorm[2, i-2])/2# + self.addTime
                plato[0,1] = deltalast

        for i in range (int(deltamin[2]), len(datanorm[1, :])):
            deltanext = datanorm[1, i] - datanorm[3, i]
            delta = datanorm[1, i-1] - datanorm[3, i-1]
            deltalast = datanorm[1, i-2] - datanorm[3, i-2]
            if (delta <= deltamin[0]*(1+sigma)) and (deltanext <= deltamin[0]*(1+sigma)) and (deltalast <= deltamin[0]*(1+sigma)):
                plato[1,0] = (datanorm[0,i]+datanorm[2, i])/2
                plato[1,1] = deltanext
                rightindex = i

        rightindex = np.min([rightindex+18, len(datanorm[1, :])-1])
        plato[2,0] = (datanorm[0,rightindex]+datanorm[2, rightindex])/2 #+3минуты
        plato[2,1] = datanorm[1, rightindex] - datanorm[3, rightindex]
        return plato