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

def gen():
    x = 0
    while True:
        x += 5
        yield x

g = gen()

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
        self.list = [Circle(250, 250, 100, 100)]
        self.change()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setPen(QtGui.QPen(QtGui.QColor(0,0,0)))
        qp.setBrush(QtGui.QBrush(QtGui.QColor(0,255,0)))
        for l in self.list:
            qp.drawEllipse(*l.get_coords())

    def add(self, l):
        self.list = l

    def change(self):
        self.update()
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            def animation():
                while True:
                    self.add([Circle(g.__next__() + 250, 250, 100, 100), Circle(250, g.__next__() + 250, 100, 100)])
                    yield self.change()

            anim= animation()
            @pyqtSlot()
            def step():
                anim.__next__()

            self.timer = QTimer(self)
            self.timer.timeout.connect(step)
            for i in range(4):
                self.timer.start(1)


class Circle(QGraphicsEllipseItem):
    def __init__(self, x, y, a, b):
        super().__init__(x, y, a, b)
        self.coords = [x, y, a, b]
    def get_coords(self):
        return self.coords

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())