import sys
from PyQt5.Qt import QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer,  QRectF, QRect
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsLineItem, QStyleOptionGraphicsItem
import random as rn
import numpy as np

import organism as org
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
        global All_Cells, All_Resources, All_Entities
        All_Cells = []
        All_Resources = [self.resource]
        All_Entities = All_Cells + All_Resources
        self.evolution()

    def evolution(self):
        def fitness_func(x, y): # расстояние до капустки
            return ((x-self.res_x)**2+(y-self.res_y)**2)**(0.5)

        # инициализация первого поколения
        start_distance = 200
        amount = 15
        All_Cells = [Cell(np.cos(2*np.pi*i/amount)*start_distance+self.res_x, np.sin(2*np.pi*i/amount)*start_distance+self.res_y, 10) for i in range(amount)]
        self.change()

        for i in range(1):
            for cell in All_Cells:
                x, y, orient = cell.get_step()
                cell.move(x, y)
                cell.orient = orient
            self.change()


    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setPen(QColor(Qt.red))
        qp.setBrush(QColor(Qt.blue))
        self.resource.paint(qp, QStyleOptionGraphicsItem())
        for cell in All_Cells:
            cell.paint(qp, QStyleOptionGraphicsItem())
            pass

    def change(self):
        self.update()
        self.show()


class Cell(QGraphicsEllipseItem):
    def __init__(self, x, y, r, w = None, b = None, orient = 0):
        super().__init__(x, y, r, r)
        if w is None:
            w = []
            for i in range(layers_count-1):
                w.append(np.array([[rn.uniform(-1, 1) for k in range(neuron_layers[i])] for j in range(neuron_layers[i+1])]))
        self.w = w
        if b is None:
            b = []
            for i in range(layers_count-1):
                b.append(np.array([rn.uniform(-1, 1) for k in range(neuron_layers[i+1])]))
        self.b = b
        self.x = x
        self.y = y
        self.r = r
        self.orient = orient

        self.color = Qt.blue
        self.setBrush(QColor(self.color))

        self.vision_rays = [2*np.pi*(i+orient)/raze_amount for i in range(sector_size)]
        self.ray_length = 20 # длина луча видимости
        self.density = 0.5 # плотность просматриваемых точек на луче

    def set_scales(w, b):
        self.w = w
        self.b = b

    def get_step(self):
        x = self.x
        y = self.y
        Cells_Close = [cell for cell in All_Cells if (x - cell.x)**2 + (y - cell.y)**2 <= self.ray_length**2] # клетки в радиусе видимости
        Resource_Close = [resource for resource in All_Resources if (x - resource.x)**2 + (y - resource.y)**2 <= self.ray_length**2] # еда в радиусе видимости
        Entities_Close = Cells_Close + Resource_Close
        input_data = []
        for angle in self.vision_rays:
            seeing = False
            for i in range(int(self.ray_length//self.density)):
                i_x = np.cos(angle)*i/self.ray_length
                i_y = np.sin(angle)*i/self.ray_length
                for entity in Entities_Close:
                    if (i_x - cell.x)**2 + (i_y - cell.y)**2 <= cell.r**2:
                        input_data.append((i_x**2 + i_y**2)**0.5)
                        seeing = True
                        # TODO 'Завести матрицу отношений'
                        if isinstance(entity, Cell):
                            input_data.append(0)
                        elif isinstance(entity, Resource):
                            input_data.append(1)
                        else:
                            input_data.append(-1)
                        # Для прочих подклассов Cell (особей другого вида) будет делаться проверка типа и передаваться другое число, наверное
                        # TODO переработать структуру классов, определить отношения между видами особей и обобщить код на случай множества разных особей

            if not seeing:
                input_data.append(-1)
                input_data.append(0)
        return org.calc(input_data, self.w, self.b)

    def move(self, x, y):
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
