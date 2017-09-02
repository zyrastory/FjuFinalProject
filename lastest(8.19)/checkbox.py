from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):      

        self.cb = QCheckBox('Show title', self)
        self.cb.move(20, 20)
        self.cb.toggle()
        #self.cb.stateChanged.connect(self.changeTitle)

        self.cb2 = QCheckBox('title explore',self)
        self.cb2.move(20, 60)
        #self.cb2.stateChanged.connect(self.titleexplore)
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QCheckBox')
        self.haha()
        self.show()
        
    """  
    def changeTitle(self, state):
      
        if state == Qt.Checked:
            self.setWindowTitle('QCheckBox')
        else:
            self.setWindowTitle(' ')

    def titleexplore(self,state):
        if state == Qt.Checked:
            self.setWindowTitle('爆炸炸起來')
        else:
            self.setWindowTitle(' ')
    """
    def haha(self):
        if  self.cb2.isChecked() ==True:
            self.cb.setCheckState(0)
            QTimer.singleShot(10, self.ahah)
        else:
            QTimer.singleShot(10, self.haha)
    
    def ahah(self):
        if self.cb.isChecked()==True:
            self.cb2.setCheckState(0)
            QTimer.singleShot(10, self.haha)
        else:
            QTimer.singleShot(10, self.ahah)
            
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())