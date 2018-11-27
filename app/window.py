import sys
from PyQt5.Qt        import QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp
from PyQt5           import QtGui
from PyQt5.QtGui     import QPainter, QBrush, QPen
from PyQt5.QtCore    import Qt, QTimer,  QRectF, QRect, QEventLoop, pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsLineItem, QStyleOptionGraphicsItem
import random as rn
import numpy as np
import datetime
import pybrain
from pybrain.tools.customxml.networkwriter import NetworkWriter
from pybrain.tools.customxml.networkreader import NetworkReader
import random
import os

import organism as org
from constants import *


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

        def fitness_func(x, y):  # расстояние до капустки
            return (x - self.res_x) ** 2 + (y - self.res_y) ** 2

        All_Cells = []
        self.first = True
        self.gone = start_distance
        self.last_gone = start_distance

        # TODO добавить самое худшее значение и медианное. Рисовать их.

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
        # инициализация первого поколения
        if not(self.first):
            def distance(x, y):  # расстояние
                return ((x - self.res_x) ** 2 + (y - self.res_y) ** 2)**0.5

            def fitness_func(x, y):  # функция приспособленности
                return (x - self.res_x) ** 2 + (y - self.res_y) ** 2
            closeness = {distance(cell.x, cell.y): cell for cell in All_Cells}
            self.last_gone = min(closeness)
            if self.gone > min(closeness):
                self.gone = min(closeness)
                print('%i: progress made = %i'%(self.evolution_counter, self.gone))
            else:
                print('%i: generation of dovns %i'%(self.evolution_counter, self.last_gone))

            best = [closeness[i] for i in sorted(list(closeness.keys()))[:-amount // 2]]
            random.shuffle(best)
            pairs = [(best[2*i], (best[2*i+1])) for i in range(len(best)//2)]
            All_Cells = []
            for i in range(4):
                All_Cells += [(pair[0].__add__(pair[1])).__copy__() for pair in pairs]
            [cell.mutate() for cell in All_Cells]
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
        global All_Cells
        if e.key() == Qt.Key_Space:
            self.stop = not(self.stop)
        elif e.key() == Qt.Key_W:
            today = '%i%02i%02i%02i%02i%02i'%(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day, datetime.datetime.today().hour, datetime.datetime.today().minute, datetime.datetime.today().second)
            os.mkdir('../data/%s' % today)
            for i in range(len(All_Cells)):
                NetworkWriter.writeToFile(All_Cells[i].brain, '../data/%s/%02i.xml' % (today, i))
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
    def __init__(self, x, y, r, orient=0, params = None, color = None):
        super().__init__(x, y, r)
        self.brain = org.net_init()
        if params is not None:
            self.brain._setParameters(params)
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

        self.vision_rays = [2 * np.pi*(orient + (i / raze_amount)) for i in range(sector_size)]
        self.ray_length = 105  # длина луча видимости
        self.density = 2  # плотность просматриваемых точек на луче

    def __add__(self, cell):
        self.brain._setParameters([(self.brain.params[i] + cell.brain.params[i])/2 for i in range(len(self.brain.params))])
        self.color = random.choice([self.color, cell.color])
        return self

    def __copy__(self):
        return Cell(self.x,self.y, self.r, self.orient, self.brain.params, self.color)

    def mutate(self):
        self.brain._setParameters([i+random.uniform(-mutation_rate, mutation_rate) for i in list(self.brain.params)])

    def get_coords(self):
        return self.coords


    def get_step(self):
        x = self.x
        y = self.y

        Cells_Close = [cell for cell in All_Cells if (x - cell.x)**2 + (y - cell.y)**2 <= self.ray_length**2 and (cell != self)]  # клетки в радиусе видимости
        Resource_Close = [resource for resource in All_Resources if (x - resource.x)**2 + (y - resource.y)**2 <= self.ray_length**2]  # еда в радиусе видимости
        Entities_Close = Resource_Close + Cells_Close
        input_data = []
        for angle in self.vision_rays:
            seeing = False
            for i in range(self.ray_length*self.density):
                i_x = x+np.cos(angle)*i/self.density
                i_y = y+np.sin(angle)*i/self.density
                for entity in Entities_Close:
                    if (i_x - entity.x)**2 + (i_y - entity.y)**2 <= entity.r**2:
                        input_data.append((i_x-x)**2 + (i_y - y)**2)
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
                if seeing:
                    break
            if not seeing:
                input_data.append(-1)
                input_data.append(0)
        return self.brain.activate(input_data)

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
