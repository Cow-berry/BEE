import sys
from PyQt5.Qt import QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
import organism
import time
import random
import numpy as np

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Alt+F4')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        #########################################


        self.circle = Cell(0, 0, 0)
        self.res_x = 400
        self.res_y = 300
        self.resource = Resource(self.res_x, self.res_y, 20)
        self.All_Cells = []

        self.evolution()
        # self.b = (0, 0)
        # self.e = (0, 0)



    def evolution(self):
        def fitness_func(x, y): # расстояние до капустки
            return ((x-self.res_x)**2+(y-self.res_y)**2)**(0.5)

        # инициализация первого поколения
        start_distance = 250
        amount = 123
        self.All_Cells = [Cell(np.cos(2*np.pi*i/amount)*start_distance+self.res_x, np.sin(2*np.pi*i/amount)*start_distance+self.res_y, 10) for i in range(amount)]
        self.update()
        self.show()
        # for i in range(3):
        #     self.All_Cells = self.All_Cells[:(amount]

# TODO сделать плавную анимацию трёх шагов.


    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        # self.drawCell(qp, circle)
        self.drawResource(qp)
        for cell in self.All_Cells:
            self.drawCell(qp, cell)

    def drawCell(self, qp, cell):
        qp.setBrush(QBrush(cell.color, Qt.SolidPattern))
        qp.drawEllipse(*cell.getEllipseCoords())

    def drawResource(self, qp):
        qp.setBrush(QBrush(self.resource.color, Qt.SolidPattern))
        qp.drawEllipse(*self.resource.getResourceCoords())

    # def mouseMoveEvent(self, event):
    #     self.circle = Cell(event.pos().x(), event.pos().y(), 50)
        # self.update()
        # self.show()

    # def mousePressEvent(self, event):
    #     self.circle = Cell(event.pos().x(), event.pos().y(), 50)
    #     self.update()
    #     self.show()
    #     x = -(event.pos().x() - self.resource.x)
    #     y = -(event.pos().y() - self.resource.y)
    #     v = organism.calc([x, y], self.circle.w, self.circle.b)
    #     # self.circle = Cell(self.circle.x + int(int(v[0])), self.circle.y + int(v[1]), 50)
    #     self.b = (event.pos().x(), event.pos().y())
    #     self.e = (self.circle.x + int(int(v[0])), self.circle.y+ int(v[1]))
    #     self.update()
    #     self.show()


class Cell():
    def __init__(self, x, y, r, w = None, b = None):
        if w is None:
            # матрица весов первого слоя
            w1 = np.array([[random.uniform(-1, 1) for i in range(2)] for j in range(4)])
            w2 = np.array([[random.uniform(-1, 1) for i in range(4)] for j in range(4)])
            w3 = np.array([[random.uniform(-1, 1) for i in range(4)] for j in range(2)])
            self.w = [w1, w2, w3]
        else:
            self.w = w
        if b is None:
            # веса смещения первого и второго слоев
            b1 = np.array([random.uniform(-1, 1) for i in range(4)])
            b2 = np.array([random.uniform(-1, 1) for i in range(4)])
            b3 = np.array([random.uniform(-1, 1) for i in range(2)])
            self.b = [b1, b2, b3]
        else:
            self.b = b
        self.x = x
        self.y = y
        self.r = r
        self.color = Qt.black
    def set_scales(w, b):
        self.w = w
        self.b = b
    def getEllipseCoords(self):
        return [self.x - self.r / 2, self.y - self.r / 2, self.r, self.r]
    def get_step(self, rx, ry):
        return organism.calc([x, y], self.w, self.b)
    def move(x, y):
        self.x += x
        self.y += y

class Resource():
    def __init__(self, x, y, r=10):
        self.x = x
        self.y = y
        self.r = r
        self.color = Qt.green
    def getResourceCoords(self):
        return [self.x - self.r / 2, self.y - self.r / 2, self.r, self.r]



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
