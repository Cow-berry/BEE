import sys
from PyQt5.Qt import QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer,  QRectF, QRect, QEventLoop
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsLineItem, QStyleOptionGraphicsItem
import random as rn
import numpy as np
import time

circle  = QGraphicsEllipseItem(50, 50, 10, 10)
