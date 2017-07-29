import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, qApp, QComboBox, QLabel, QLineEdit, QInputDialog
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pymysql
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
style.use('ggplot')
"""
from test import Figure_Canvas

class firstWindow(QWidget):



    def setupUi(self,MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        self.setWindowIcon(QtGui.QIcon('./icon/icon.png'))

        self.button = QPushButton('弹出新窗口',self)
        self.button.move(50, 100)
        self.slavewindow = slaveWindow()
        #dr = Figure_Canvas()
        #self.button.clicked.connect(lambda:dr.test(10))
        self.button.clicked.connect(self.kline)



        self.button2 = QPushButton('彈出第二個視窗',self)
        self.button2.move(150, 100)
        self.slaveWindow2 = slaveWindow2()
        self.button2.clicked.connect(self.slaveWindow2.show)

        self.button3 = QPushButton('Quit', self)
        self.button3.clicked.connect(QCoreApplication.instance().quit)
        self.button3.move(600, 100)

        self.show()


    def kline(self):
        
        dr = Figure_Canvas()
        #实例化一个FigureCanvas
        dr.test(10)  # 画图
        graphicscene = QtWidgets.QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        graphicscene.addWidget(dr)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        self.graphicview.setScene(graphicscene)
        self.graphicview.show()  # 最后，调用show方法呈现图形！Voila!!
        self.setCentralWidget(self.graphicview)
        self.graphicview.resize(1100,500)


        
    def initUI(self):
        '''
        第一個按鈕裡面的東西
        '''
        addAction = QAction(QIcon('./icon/add.png'), '新增商品', self)
        addAction.setShortcut('Alt+F1')
        addAction.setStatusTip('從內部資料庫新增商品')
        self.addwindow = addWindow()
        addAction.triggered.connect(self.addwindow.show)

        setAction = QAction(QIcon('./icon/set.png'), '設定商品', self)
        setAction.setShortcut('Alt+F2')
        self.setwindow = setWindow()
        setAction.triggered.connect(self.setwindow.show)
        setAction.setStatusTip('設定目前商品的細項')

        exitAction = QAction(QIcon('./icon/exit.png'), '離開', self)
        exitAction.setShortcut('Alt+F4')
        exitAction.triggered.connect(QCoreApplication.instance().quit)
        exitAction.setStatusTip('離開程式')
        '''
        第二個按鈕裡面的東西
        '''     
        writeAction = QAction(QIcon('./icon/write.png'), '編寫', self)
        writeAction.setShortcut('Alt+W')
        self.writewindow = writeWindow()
        writeAction.triggered.connect(self.writewindow.show)
        writeAction.setStatusTip('手動編寫交易策略')

        checkAction = QAction(QIcon('./icon/check.png'), '查看', self)
        checkAction.setShortcut('Alt+C')
        self.checkwindow = checkWindow()
        checkAction.triggered.connect(self.checkwindow.show)
        checkAction.setStatusTip('查看內建的交易策略')

        '''
        第三個按鈕裡面的東西
        '''
        reportAction = QAction(QIcon('./icon/report.png'), '策略績效報告', self)
        reportAction.setShortcut('Alt+R')
        reportAction.setStatusTip('檢視此次交易策略之績效報告')
        self.reportwindow = reportWindow()
        reportAction.triggered.connect(self.reportwindow.show)

        '''
        第四個按鈕裡面的東西
        '''
        exchangeAction = QAction(QIcon('./icon/exchange.png'), '選擇證券交易所', self)
        self.exchangewindow = exchangeWindow()
        exchangeAction.setShortcut('Alt+X')
        exchangeAction.triggered.connect(self.exchangewindow.show)
        exchangeAction.setStatusTip('選擇欲交易之證券交易所')

        orderAction = QAction(QIcon('./icon/order.png'), '下單', self)
        self.tradewindow = tradeWindow()
        orderAction.setShortcut('Alt+O')
        orderAction.triggered.connect(self.tradewindow.show)
        orderAction.setStatusTip('與證券交易所進行交易')

        '''
        第五個按鈕
        '''
        loginAction = QAction(QIcon('./icon/login.png'), '登入', self)
        self.loginwindow = loginWindow()
        loginAction.setShortcut('Alt+L')
        loginAction.triggered.connect(self.loginwindow.show)
        loginAction.setStatusTip('登入')

        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('商品')
        fileMenu2 = menubar.addMenu('交易策略')
        fileMenu3 = menubar.addMenu('檢視績效報告')
        fileMenu4 = menubar.addMenu('下單接口')
        fileMenu5 = menubar.addMenu('進階')
        fileMenu.addAction(addAction)
        fileMenu.addAction(setAction)
        fileMenu.addAction(exitAction)
        fileMenu2.addAction(writeAction)
        fileMenu2.addAction(checkAction)
        fileMenu3.addAction(reportAction)
        fileMenu4.addAction(exchangeAction)
        fileMenu4.addAction(orderAction)
        fileMenu5.addAction(loginAction)
        self.setWindowTitle('iTrader v0723')
        self.show()




class slaveWindow(QWidget):
    def __init__(self, parent = None):
        super(slaveWindow, self).__init__(parent)

    def main():
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()

class slaveWindow2(QWidget):
    def __init__(self, parent = None):
        super(slaveWindow2, self).__init__(parent)


    def main():
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()


class addWindow(QWidget):
    def __init__(self, parent = None):
        super(addWindow, self).__init__(parent)
        self.setWindowTitle('addWindow')
        self.setFixedSize(500, 200) 

        stockbutton = QPushButton('股票',self)
        stockbutton.move(100, 100)
        self.stockwindow = stockWindow()
        stockbutton.clicked.connect(self.stockwindow.show)
        stockbutton.clicked.connect(self.close)

        futurebutton = QPushButton('期貨',self)
        futurebutton.move(200, 100)
        self.futurewindow = futureWindow()
        futurebutton.clicked.connect(self.futurewindow.show)
        futurebutton.clicked.connect(self.close)

        optionbutton = QPushButton('選擇權',self)
        optionbutton.move(300, 100)
        self.optionwindow = optionWindow()
        optionbutton.clicked.connect(self.optionwindow.show)
        optionbutton.clicked.connect(self.close)

    def main():
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()

class stockWindow(QWidget):
    def __init__(self, parent = None):
        super(stockWindow, self).__init__(parent)
        self.setFixedSize(200, 200)
        self.setWindowTitle('股票清單')
        self.lbl = QLabel("Ubuntu", self)

        stockcombo = QComboBox(self)
        stockcombo.addItem("Ubuntu")
        stockcombo.addItem("Mandriva")
        stockcombo.addItem("Fedora")
        stockcombo.addItem("Arch")
        stockcombo.addItem("Gentoo")

        stockcombo.move(50, 50)
        self.lbl.move(50, 100)

        stockcombo.activated[str].connect(self.onActivated)

        subbutton = QPushButton('確認',self)
        subbutton.move(50, 150)
        subbutton.clicked.connect(self.kline)
        subbutton.clicked.connect(self.close)

    def main():
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()

    def onActivated(self, text):
      
        self.lbl.setText(text)
        self.lbl.adjustSize()

    def kline(self, parent=None):
        self.graphicview = QtWidgets.QGraphicsView()  # 第一步，创建一个QGraphicsView
        self.graphicview.setObjectName("graphicview")

        dr = Figure_Canvas()
        #实例化一个FigureCanvas
        dr.test(10)  # 画图
        graphicscene = QtWidgets.QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        graphicscene.addWidget(dr)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        self.graphicview.setScene(graphicscene)
        self.graphicview.show()  # 最后，调用show方法呈现图形！Voila!!
        #self.setCentralWidget(self.graphicview)
        self.graphicview.resize(1100,500) 


class futureWindow(QWidget):
    def __init__(self, parent = None):
        super(futureWindow, self).__init__(parent)
        self.setFixedSize(200, 200)
        self.setWindowTitle('期貨清單')
        self.lbl = QLabel("Ubuntu", self)

        futurecombo = QComboBox(self)
        futurecombo.addItem("Ubuntu")
        futurecombo.addItem("Mandriva")
        futurecombo.addItem("Fedora")
        futurecombo.addItem("Arch")
        futurecombo.addItem("Gentoo")

        futurecombo.move(50, 50)
        self.lbl.move(50, 100)

        futurecombo.activated[str].connect(self.onActivated)

        subbutton = QPushButton('確認',self)
        subbutton.move(50, 150)
        subbutton.clicked.connect(self.close)

    def main():
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()

    def onActivated(self, text):
      
        self.lbl.setText(text)
        self.lbl.adjustSize() 

class optionWindow(QWidget):
    def __init__(self, parent = None):
        super(optionWindow, self).__init__(parent)
        self.setFixedSize(200, 200)
        self.setWindowTitle('選擇權清單')
        self.lbl = QLabel("Ubuntu", self)

        optioncombo = QComboBox(self)
        optioncombo.addItem("Ubuntu")
        optioncombo.addItem("Mandriva")
        optioncombo.addItem("Fedora")
        optioncombo.addItem("Arch")
        optioncombo.addItem("Gentoo")

        optioncombo.move(50, 50)
        self.lbl.move(50, 100)

        optioncombo.activated[str].connect(self.onActivated)

        subbutton = QPushButton('確認',self)
        subbutton.move(50, 150)
        subbutton.clicked.connect(self.close)

    def main():
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()

    def onActivated(self, text):
      
        self.lbl.setText(text)
        self.lbl.adjustSize() 


class setWindow(QWidget):
    def __init__(self, parent = None):
        super(setWindow, self).__init__(parent)
        self.setFixedSize(800, 600)
        self.setWindowTitle('設定商品')


    def main():
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()

class writeWindow(QWidget):
    def __init__(self, parent = None):
        super(writeWindow, self).__init__(parent)
        self.setFixedSize(800, 600)
        self.setWindowTitle('編寫交易策略')       

    def main():
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()
'''
        
    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))

        fh = ''

        if QFile.exists(filename):
            fh = QFile(filename)

        if not fh.open(QFile.ReadOnly):
            QtGui.qApp.quit()

        data = fh.readAll()
        codec = QTextCodec.codecForUtfText(data)
        unistr = codec.toUnicode(data)

        tmp = ('Notepad: %s' % filename)
        self.setWindowTitle(tmp)

        self.textEdit.setText(unistr)
'''

class checkWindow(QWidget):
    def __init__(self, parent = None):
        super(checkWindow, self).__init__(parent)
        self.setFixedSize(800, 600)
        self.setWindowTitle('內建交易策略')

    def main():
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()

class reportWindow(QWidget):
    def __init__(self, parent = None):
        super(reportWindow, self).__init__(parent)
        self.setFixedSize(800, 600)
        self.setWindowTitle('策略績效報告')


    def main():
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()

class exchangeWindow(QWidget):
    def __init__(self, parent = None):
        super(exchangeWindow, self).__init__(parent)
        self.setFixedSize(800, 600)
        self.setWindowTitle('選擇證券交易所')
        self.lbl = QLabel("Ubuntu", self)

        stockcombo = QComboBox(self)
        stockcombo.addItem("Ubuntu")
        stockcombo.addItem("Mandriva")
        stockcombo.addItem("Fedora")
        stockcombo.addItem("Arch")
        stockcombo.addItem("Gentoo")

        stockcombo.move(50, 50)
        self.lbl.move(50, 100)

        stockcombo.activated[str].connect(self.onActivated)

        subbutton = QPushButton('確認',self)
        subbutton.move(50, 150)
        subbutton.clicked.connect(self.close)

    def main():
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()

    def onActivated(self, text):
      
        self.lbl.setText(text)
        self.lbl.adjustSize() 

class tradeWindow(QWidget):
    def __init__(self, parent = None):
        super(tradeWindow, self).__init__(parent)
        self.setFixedSize(800, 600)
        self.setWindowTitle('下單交易')


    def main():
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()

class loginWindow(QWidget):
    def __init__(self, parent = None):
        super(loginWindow, self).__init__(parent)

        self.setFixedSize(800, 600)
        self.setWindowTitle('登入')
        self.btn1 = QPushButton('點擊輸入帳號與密碼', self)
        self.btn1.move(20, 20)
        self.btn1.clicked.connect(self.showDialog)
        
        self.account = QLineEdit(self)
        self.account.move(300, 200)      

        self.password = QLineEdit(self)
        self.password.move(300, 300)   

        self.btn2 = QPushButton('確認', self)     
        self.btn2.move(500, 300)
        self.btn2.clicked.connect(self.close)

        

    def showDialog(self):

        text, ok = QInputDialog.getText(self, '帳號', '請輸入帳號：')
        if ok:
            self.account.setText(str(text))

        text, ok = QInputDialog.getText(self, '密碼', '請輸入密碼：')
        if ok:
            self.password.setText(str(text))

    def main():
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()







class MainWindow(QMainWindow, firstWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.graphicview = QtWidgets.QGraphicsView()  # 第一步，创建一个QGraphicsView
        self.graphicview.setObjectName("graphicview")
        
        dr = Figure_Canvas()
        #实例化一个FigureCanvas
        #dr.test(10)  # 画图
        

        graphicscene = QtWidgets.QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        graphicscene.addWidget(dr)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        self.graphicview.setScene(graphicscene)  # 第五步，把QGraphicsScene放入QGraphicsView
        self.graphicview.show()  # 最后，调用show方法呈现图形！Voila!!
        self.setCentralWidget(self.graphicview)
        self.graphicview.resize(1100,500)
        
        self.setupUi(self)
        self.initUI()
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())