import sys
from PyQt5.Qt import QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)
        self.x = 100
        self.y = 100
        self.r = 200
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Alt+F4')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        qp.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        qp.drawEllipse(self.x - self.r / 2, self.y - self.r / 2, 200, 200)

    def mouseMoveEvent(self, event):
        self.x, self.y = event.pos().x(), event.pos().y()
        self.update()
        self.show()

    def moveCircle(self, x, y):
        self.x, self.y = self.x + x, self.y + y
        self.update()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
