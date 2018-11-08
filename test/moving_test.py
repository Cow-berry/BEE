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
        self.list = [QGraphicsEllipseItem(250, 250, 100, 100)]
        self.change()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setPen(QColor(Qt.red))
        qp.setBrush(QColor(Qt.blue))
        for l in self.list:
            l.paint(qp, QStyleOptionGraphicsItem())

    def add(self, item):
        self.list = [item]

    def change(self):
        self.update()
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            def animation():
                for i in range(1000):
                    self.add(QGraphicsEllipseItem(g.__next__() + 250, 250, 100, 100))
                    yield self.change()

            anime = animation()
            @pyqtSlot()
            def step():
                anime.__next__()

            self.timer = QTimer(self)
            self.timer.timeout.connect(step)
            for i in range(4):
                self.timer.start(10)

            # for i in range(3):
            #     self.add(QGraphicsEllipseItem(g.__next__() + 250, 250, 100, 100))
            #     self.change()
            #     time.sleep(1)
            # for i in range(3):
            #     self.add(QGraphicsEllipseItem(250, g.__next__() + 250, 100, 100))
            #     self.change()
            #     time.sleep(1)
            # for i in range(3):
            #     self.add(QGraphicsEllipseItem(g.__next__() - 250, g.__next__() - 250, 100, 100))
            #     self.change()
            #     time.sleep(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())