import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *   
     
class dateWrong(QWidget):
    def __init__(self,judgment):
        QWidget.__init__(self)
 
        self.setMinimumSize(QSize(200, 80))    
        self.setWindowTitle("錯誤訊息") 
        
        if judgment=="NE":
        	pybutton = QPushButton('沒選擇商品\n請重新選擇', self)
        elif judgment=="T":
        	pybutton = QPushButton('起始時間大於等於結束時間\n請重新選擇', self)
        #pybutton.clicked.connect(self.close)
        pybutton.resize(150,80)
        pybutton.move(150, 100)

