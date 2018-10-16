import sys
from PyQt5.Qt import QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer,  QRectF, QRect
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsLineItem, QStyleOptionGraphicsItem
import random as rn
import numpy as np

import organism
from constants import *

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

        self.res_x = 400
        self.res_y = 300
        self.resource = Resource(self.res_x, self.res_y)
        self.All_Cells = []

        self.evolution()

    def evolution(self):
        def fitness_func(x, y): # расстояние до капустки
            return ((x-self.res_x)**2+(y-self.res_y)**2)**(0.5)

        # инициализация первого поколения
        start_distance = 200
        amount = 15
        self.All_Cells = [Cell(np.cos(2*np.pi*i/amount)*start_distance+self.res_x, np.sin(2*np.pi*i/amount)*start_distance+self.res_y, 10) for i in range(amount)]
        self.change()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setPen(QColor(Qt.red))
        qp.setBrush(QColor(Qt.blue))
        self.resource.paint(qp, QStyleOptionGraphicsItem())
        for cell in self.All_Cells:
            cell.paint(qp, QStyleOptionGraphicsItem())
            pass

    def change(self):
        self.update()
        self.show()


class Cell(QGraphicsEllipseItem):
    def __init__(self, x, y, r, w = None, b = None):
        super().__init__(x, y, r, r)
        if w is None:
            w = []
            for i in range(layers_count-1):
                w.append(np.array([[rn.uniform(-1,1) for i in range(neuron_layers[i])] for i in range(neuron_layers[i+1])]))
        self.w = w
        if b is None:
            b = []
            for i in range(layers_count-1):
                b.append(np.array([rn.uniform(-1,1) for i in range(neuron_layers[i])]))
        self.b = b
        self.x = x
        self.y = y
        self.r = r
        self.color = Qt.blue
        self.setBrush(QColor(self.color))

    def set_scales(w, b):
        self.w = w
        self.b = b

    def get_step(self, basic_data): # basic_data -- [x, y, orient, ... (health, stamina) ]
        pass #проверять для каждого существа ксловие, что оно  в поле видимости и на одной из прямых видимости. далее передавать это всё нейронке, пусть решает, шо с этим делать.

    def move(x, y):
        self.x += x
        self.y += y


class Resource(QGraphicsEllipseItem):
    def __init__(self, x, y, r=20):
        super().__init__(x, y, r, r )
        self.x = x
        self.y = y
        self.r = r
        self.setBrush(QColor(Qt.green))
        # self.color = Qt.green

    def getResourceCoords(self):
        return [self.x - self.r / 2, self.y - self.r / 2, self.r, self.r]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
