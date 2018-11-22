import sys
from PyQt5.Qt import QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer,  QRectF, QRect, QEventLoop, pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsLineItem, QStyleOptionGraphicsItem
import random as rn
import numpy as np
import time
import pybrain

import organism as org
from constants import *
import random

class Main(QMainWindow):
    def __init__(self):
        global All_Cells
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
        self.resource = Resource(self.res_x, self.res_y, resource_radius)

        All_Cells = []
        self.first = True
        self.gone = start_distance
        # добавить самое худшее значение и медианное. Рисовать их.

        self.evolution_counter = 0
        self.stop = True
        self.timer_set = False

        self.field_init()

    def field_init(self):
        global All_Resources, All_Entities
        All_Resources = [self.resource]
        All_Entities = All_Cells + All_Resources
        self.evolution()
        self.change()

    def evolution(self):
        global All_Cells
        self.step_count = 0
        def fitness_func(x, y): # расстояние до капустки
            return ((x-self.res_x)**2+(y-self.res_y)**2)**(0.5)

        # инициализация первого поколения
        if not(self.first):
            def fitness_func(cell):  # расстояние до капустки
                return ((cell.x - self.res_x) ** 2 + (cell.y - self.res_y) ** 2) ** (0.5)
            closeness = {fitness_func(cell):cell for cell in All_Cells}
            if self.gone > min(closeness):
                self.gone = min(closeness)
                print('generation %i\nprogress made = %i'%(self.evolution_counter, self.gone))
            worst = [closeness[i] for i in sorted(list(closeness.keys()))[-amount//2:]]
            best = [closeness[i] for i in sorted(list(closeness.keys()))[:-amount//2]]
            [worst[i].brains._setParameters(list(best[i].brains.params)) for i in range(len(worst))]
            [cell.mutate() for cell in worst]
            [cell.change_color(Qt.green) for cell in best]
            [cell.change_color(QtGui.QColor(255,128,0)) for cell in worst]
            All_Cells = best + worst
            random.shuffle(All_Cells)
            for i in range(amount):
                All_Cells[i].x, All_Cells[i].y = (np.cos(2*np.pi*i/amount)*start_distance+self.res_x, np.sin(2*np.pi*i/amount)*start_distance+self.res_y)

        else:
            All_Cells = [Cell(np.cos(2*np.pi*i/amount)*start_distance+self.res_x, np.sin(2*np.pi*i/amount)*start_distance+self.res_y, cell_radius) for i in range(amount)]
        self.change()

    def evolution_step(self):
        global All_Cells
        if self.stop:
            return
        if self.step_count >=step_amount:
            self.first = False
            self.evolution_counter += 1
            self.field_init()
            print('reinitialized!')
            return
        for cell in All_Cells:
            x, y, orient = cell.get_step()
            cell.move(x, y)
            cell.orient = orient
        self.step_count +=1
        self.change()

# 20 шагов
# выбираются лучшие
# репродуцируются
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            self.stop = not(self.stop)
        elif not(self.timer_set):
            self.timer_set = True
            @pyqtSlot()
            def step():
                self.evolution_step()

            self.timer = QTimer(self)
            self.timer.timeout.connect(step)
            self.timer.start(10)
    def paintEvent(self, event):
        global All_Cells
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        gone_circle = Circle(self.res_x, self.res_y, self.gone-cell_radius)
        gone_circle.paint(qp, QStyleOptionGraphicsItem())
        qp.setPen(QColor(Qt.red))
        qp.setBrush(QColor(Qt.blue))
        self.resource.paint(qp, QStyleOptionGraphicsItem())
        for cell in All_Cells:
            qp.setBrush(cell.color)
            cell.paint(qp, QStyleOptionGraphicsItem())
        qp.setPen(QColor(Qt.blue))

    def change(self):
        self.update()
        self.show()

class Circle(QGraphicsEllipseItem):
    def __init__(self, x, y, r):
        super().__init__(x-r, y-r, 2*r, 2*r)

class Cell(Circle):
    def __init__(self, x, y, r, orient=0, n=None, color = None):
        super().__init__(x, y, r)
        self.brains = org.net_init()
        self.coords = [x, y, r, r]
        self.x = x
        self.y = y
        self.r = r
        self.orient = orient
        if color is not None:
            self.color = color
        else:
            self.color = random.choice([Qt.red, Qt.blue, Qt.cyan, Qt.magenta, Qt.yellow, Qt.gray])

        self.setBrush(self.color)

        self.vision_rays = [2*np.pi*(i+orient)/raze_amount for i in range(sector_size)]
        self.ray_length = 105  # длина луча видимости
        self.density = 0.5  # плотность просматриваемых точек на луче

    def mutate(self):
        self.brains._setParameters([i+random.uniform(0, mutation_rate) for i in list(self.brains.params)])

    def get_coords(self):
        return self.coords
    #
    # def set_scales(w, b):
    #     self.w = w
    #     self.b = b

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
                    if (i_x - entity.x)**2 + (i_y - entity.y)**2 <= entity.r**2:
                        # input_data.append((i_x**2 + i_y**2)**0.5)
                        input_data.append(1)
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
        return self.brains.activate(input_data)

    def change_color(self, color):
        self.color = color
        self.setBrush(self.color)

    def move(self, x, y):
        self.x += x
        self.y += y
        self.coords = [x, y, self.r, self.r]
        self.__init__(self.x, self.y, self.r, self.r, color = self.color)


class Resource(Circle):
    def __init__(self, x, y, r):
        super().__init__(x, y, r)
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
