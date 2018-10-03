import sys, os
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
    QLabel, QApplication)
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        # hbox = QHBoxLayout(self)
        pixmap = QPixmap("circle.png")
        #pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation)
        pixmap =  pixmap.scaled(720, 405, QtCore.Qt.KeepAspectRatio)
        # print(type(self.pixmap))
        print(dir(pixmap))
        self.lbl = QLabel(self)
        self.lbl.setPixmap(pixmap)

        # hbox.addWidget(lbl)
        # self.setLayout(hbox)

        self.move(300, 200)
        self.resize(pixmap.width(),pixmap.height())
        self.setWindowTitle('Red Rock')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
