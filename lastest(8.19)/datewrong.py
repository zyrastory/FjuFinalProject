import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *   
     
class dateWrong(QWidget):
    def __init__(self,judgment,*args):
        QWidget.__init__(self)
        self.setFixedSize(320, 100)
        
        if len(args) != 0:
            self.setWindowTitle("Wrong Message")
        else:
            self.setWindowTitle("錯誤訊息") 
        
        if judgment=="NE":
            if len(args) == 0:
               pybutton = QPushButton('沒選擇商品\n請重新選擇', self)
            else:
                pybutton = QPushButton('no item choose\npls choose again', self)
        elif judgment=="NI" and len(args) == 0:
            pybutton = QPushButton('無此項產品\n請重新選擇', self)
        elif judgment=="T" and len(args) == 0:
            pybutton = QPushButton('起始時間大於等於結束時間\n請重新選擇', self)
        elif judgment=="NS" and len(args) == 0:
            pybutton = QPushButton('沒選擇策略\n請重新選擇', self)
        elif judgment=="NI-C" and len(args) == 0:
            pybutton = QPushButton('沒選擇商品\n無法選擇策略', self)
        elif judgment=="NS-C" and len(args) == 0:
            pybutton = QPushButton('沒選擇策略\n顯示個毛績效報表', self)

        pybutton.clicked.connect(self.close)
        QTimer.singleShot(2200, self.close)
        pybutton.resize(160,60)
        pybutton.move(80,20)

