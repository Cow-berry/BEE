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
        self.resize(600, 400)
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Alt+F4')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        self.circle = Cell(0, 0, 0)
        self.resource = Resource(500, 500, 20)
        self.b = (0, 0)
        self.e = (0, 0)

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        self.drawCell(qp)
        self.drawResource(qp)
        qp.drawLine(*self.b, *self.e)

    def drawCell(self, qp):
        qp.setBrush(QBrush(self.circle.color, Qt.SolidPattern))
        qp.drawEllipse(*self.circle.getEllipseCoords())

    def drawResource(self, qp):
        qp.setBrush(QBrush(self.resource.color, Qt.SolidPattern))
        qp.drawEllipse(*self.resource.getResourceCoords())

    # def mouseMoveEvent(self, event):
    #     self.circle = Cell(event.pos().x(), event.pos().y(), 50)
    #     self.update()
    #     self.show()

    def mousePressEvent(self, event):
        self.circle = Cell(event.pos().x(), event.pos().y(), 50)
        self.update()
        self.show()
        x = -(event.pos().x() - self.resource.x)
        y = -(event.pos().y() - self.resource.y)
        v = organism.calc([x, y], self.circle.w, self.circle.b)
        # self.circle = Cell(self.circle.x + int(int(v[0])), self.circle.y + int(v[1]), 50)
        self.b = (event.pos().x(), event.pos().y())
        self.e = (self.circle.x + int(int(v[0])), self.circle.y+ int(v[1]))
        self.update()
        self.show()

    def keyPressedButton(self, event):
        print('работаю')
        # if e.key() == Qt.Key_Escape:
        #     while True:


class Cell():
    def __init__(self, x, y, r):
        # матрица весов первого слоя
        self.w1 = np.array([[random.uniform(-1, 1) for i in range(2)] for j in range(4)])
        self.w2 = np.array([[random.uniform(-1, 1) for i in range(4)] for j in range(4)])
        self.w3 = np.array([[random.uniform(-1, 1) for i in range(4)] for j in range(2)])
        # веса смещения первого и второго слоев
        self.b1 = np.array([random.uniform(-1, 1) for i in range(4)])
        self.b2 = np.array([random.uniform(-1, 1) for i in range(4)])
        self.b3 = np.array([random.uniform(-1, 1) for i in range(2)])

        self.w = [self.w1, self.w2, self.w3]
        self.b = [self.b1, self.b2, self.b3]
        self.x = x
        self.y = y
        self.r = r
        self.color = Qt.black
    def getEllipseCoords(self):
        return [self.x - self.r / 2, self.y - self.r / 2, self.r, self.r]

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

# TODO нарисовать кружок, который можно перемещать
