from PyQt5.QtWidgets import QTabWidget, QApplication, QLineEdit,QVBoxLayout,QWidget,QPushButton,QHBoxLayout,QTableWidget
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class tab_widget(QTabWidget):
    def __init__(self, parent=None):
        super(tab_widget, self).__init__(parent)
        self.setGeometry(100,100,600,300)
        self.setStyleSheet("QTabBar{font: bold;}")

        w = QWidget()
        w.setLayout(QVBoxLayout())
        w.layout().addWidget(QPushButton("click me"))
        w.layout().addWidget(QLineEdit("write me"))
        self.yoyo=aaa()
        self.addTab(self.yoyo,"Tab1")
        self.addTab(QLineEdit("QLineEdit"),"Tab2")
        self.addTab(w,"Tab2")
class aaa(QWidget):

    def __init__(self):
        super().__init__()


        hhbox = QHBoxLayout()           #横向布局

        tableWidget = QTableWidget()    #创建一个表格

        tableWidget.setRowCount(5)
        tableWidget.setColumnCount(1)   #5行4列

        tableWidget.setHorizontalHeaderLabels(['第一行列'])
        tableWidget.setVerticalHeaderLabels(['第一行','第二行','第三行','第四行','第五行'])
                                        #表头

        hhbox.addWidget(tableWidget)    #把表格加入布局

        self.setLayout(hhbox)           #创建布局

        self.setWindowTitle("表格")
        self.resize(600,250)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = aaa()
    w = tab_widget()
    w.show()
    sys.exit(app.exec_())