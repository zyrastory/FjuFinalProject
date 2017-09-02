import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os

from notepad import Writer, Notepad
from ta_test8_6 import Figure_Canvas
from report import tab_widget
from datewrong import dateWrong


class firstWindow(QWidget):

    def setupUi(self,MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        MainWindow.setStyleSheet("#MainWindow { border-image: url(./icon/trader2.png) 0 0 0 0 stretch stretch; }")
        self.setWindowIcon(QIcon('./icon/icon.png'))
               
        self.show()
        
    def fade(self):

        if self.fileMenu.title()=="商品":
            self.fileMenu.setTitle("Item")
            self.addAction.setText("Add Item")
            self.setAction.setText("Item Setting")
            self.fileMenu2.setTitle("Strategy")
            self.writeAction.setText("Edit")
            self.checkAction.setText("View")
            self.chooseAction.setText("Choose")
            self.fileMenu3.setTitle("Performance Report")
            self.reportAction.setText("Show")
            self.fileMenu4.setTitle("Order")
            self.exchangeAction.setText("Stock Exchange")
            self.orderAction.setText("Make Order")
            self.fileMenu5.setTitle("Advanced")
            self.loginAction.setText("Login")
            self.fileMenu6.setTitle("Language")

    def fadeout(self):
        if self.fileMenu.title()=="Item":
            self.fileMenu.setTitle("商品")
            self.addAction.setText("新增商品")
            self.setAction.setText("設定商品")
            self.fileMenu2.setTitle("交易策略")
            self.writeAction.setText("編寫")
            self.checkAction.setText("查看")
            self.chooseAction.setText("選擇")
            self.fileMenu3.setTitle("檢視績效報告")
            self.reportAction.setText("策略績效報告")
            self.fileMenu4.setTitle("下單接口")
            self.exchangeAction.setText("選擇證券交易所")
            self.orderAction.setText("下單")
            self.fileMenu5.setTitle("進階")
            self.loginAction.setText("登入")
            self.fileMenu6.setTitle("設定語言")
            


    def re(self):
        path = "C:\\Users\\user\\Desktop\\lastest(8.19)\\cache"
        if os.path.exists(path+"\\8-11.csv") and os.path.exists(path+"\\TSname.txt"): 
            self.reportwindow = tab_widget()
            self.reportwindow.show()
        else:
            print("u are out")

    def se(self):
        path = "C:\\Users\\user\\Desktop\\lastest(8.19)\\cache"
        if os.path.exists(path+"\\8-11.csv"): 
            self.choosewindow.show()
        else:
            print("fuck u")

       
    def initUI(self):
     
        self.addAction = QAction(QIcon('./icon/add.png'), '新增商品', self)
        self.addAction.setShortcut('Alt+F1')
        self.addAction.setStatusTip('從內部資料庫新增商品')
        self.addwindow = addWindow()
        self.addAction.triggered.connect(self.addwindow.show)

        self.setAction = QAction(QIcon('./icon/set.png'), '設定商品', self)
        self.setAction.setShortcut('Alt+F2')
        self.setwindow = setWindow()
        self.setAction.triggered.connect(self.setwindow.show)
        self.setAction.setStatusTip('設定目前商品的細項')

        #第二個按鈕裡面的東西  
        self.writeAction = QAction(QIcon('./icon/write.png'), '編寫', self)
        self.writeAction.setShortcut('Alt+W')
        self.writewindow = Writer()
        self.writeAction.triggered.connect(self.writewindow.show)
        self.writeAction.setStatusTip('手動編寫交易策略')

        self.checkAction = QAction(QIcon('./icon/check.png'), '查看', self)
        self.checkAction.setShortcut('Alt+C')
        self.checkwindow = checkWindow()
        self.checkAction.triggered.connect(self.checkwindow.show)
        self.checkAction.setStatusTip('查看內建的交易策略')

        self.chooseAction = QAction(QIcon('./icon/check.png'), '選擇', self)
        self.chooseAction.setShortcut('Alt+C')
        self.choosewindow = chooseWindow()
        self.chooseAction.triggered.connect(self.se)
        self.chooseAction.setStatusTip('查看內建的交易策略')
        #第三個按鈕
        self.reportAction = QAction(QIcon('./icon/report.png'), '策略績效報告', self)
        self.reportAction.setShortcut('Alt+R')
        self.reportAction.setStatusTip('檢視此次交易策略之績效報告')
        self.reportAction.triggered.connect(self.re)        
        #第四個按鈕
        self.exchangeAction = QAction(QIcon('./icon/exchange.png'), '選擇證券交易所', self)
        self.exchangewindow = exchangeWindow()
        self.exchangeAction.setShortcut('Alt+X')
        self.exchangeAction.triggered.connect(self.exchangewindow.show)
        self.exchangeAction.setStatusTip('選擇欲交易之證券交易所')

        self.orderAction = QAction(QIcon('./icon/order.png'), '下單', self)
        self.tradewindow = tradeWindow()
        self.orderAction.setShortcut('Alt+O')
        self.orderAction.triggered.connect(self.tradewindow.show)
        self.orderAction.setStatusTip('與證券交易所進行交易')
        #第五個按鈕
        self.loginAction = QAction(QIcon('./icon/login.png'), '登入', self)
        self.loginwindow = loginWindow()
        self.loginAction.setShortcut('Alt+L')
        self.loginAction.triggered.connect(self.loginwindow.show)
        self.loginAction.setStatusTip('登入')
        
        self.Language = QAction('繁體中文', self)
        self.Language.setShortcut('Alt+8')
        self.Language.triggered.connect(self.fadeout)
        self.Language2 = QAction('English', self)
        self.Language2.setShortcut('Alt+9')
        self.Language2.triggered.connect(self.fade)
        
        
        self.statusBar()
        menubar = self.menuBar()
        menubar.setStyleSheet("font-size: 12pt")
        
        self.fileMenu = menubar.addMenu('商品')
        self.fileMenu2 = menubar.addMenu('交易策略')
        self.fileMenu3 = menubar.addMenu('檢視績效報告')
        self.fileMenu4 = menubar.addMenu('下單接口')
        self.fileMenu5 = menubar.addMenu('進階')
        self.fileMenu6 = menubar.addMenu('設定語言')
        
        self.fileMenu.addAction(self.addAction)
        self.fileMenu.addAction(self.setAction)
        self.fileMenu2.addAction(self.writeAction)
        self.fileMenu2.addAction(self.checkAction)
        self.fileMenu2.addAction(self.chooseAction)
        self.fileMenu3.addAction(self.reportAction)
        self.fileMenu4.addAction(self.exchangeAction)
        self.fileMenu4.addAction(self.orderAction)
        self.fileMenu5.addAction(self.loginAction)
        self.fileMenu6.addActions([self.Language,self.Language2])
        self.setWindowTitle('iTrader ver2.0')
        self.createContextMenu()
        self.show()

    def createContextMenu(self):  

        self.setContextMenuPolicy(Qt.CustomContextMenu)  
        self.customContextMenuRequested.connect(self.showContextMenu)  
  
        self.contextMenu = QMenu(self)  
        self.actionA = self.contextMenu.addAction("新增商品")  
        self.actionB = self.contextMenu.addAction("編寫交易策略")  
        self.actionC = self.contextMenu.addAction("選擇交易策略") 
        self.actionA.triggered.connect(self.addwindow.show)  
        self.actionB.triggered.connect(self.writewindow.show)  
        self.actionC.triggered.connect(self.se)  
  
    def showContextMenu(self, pos):  

        self.contextMenu.move(self.pos() + pos)  
        self.contextMenu.show()  
 

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

class addWindow(QTabWidget):
    def __init__(self, parent = None):
        super(addWindow, self).__init__(parent)
        self.setWindowTitle('新增商品')
        #self.setFixedSize(500, 300)
        self.setGeometry(600,300,700,400) 


        self.listWidget = QListWidget(self)

        item = QtWidgets.QListWidgetItem()          # delimiter
        item.setText('商品'+'\t'*2+'說明\n'+'-'*53)
        item.setFlags(QtCore.Qt.NoItemFlags)        # item should not be selectable
        self.listWidget.addItem(item)
        self.listWidget.addItems(["%-20s%10s"%("中石化","中國石油化工股份有限公司"), \
            "%-20s%10s"%("台泥","台灣水泥1101")])
        self.listWidget.setFixedSize(330,200)

        self.listWidget2 = QListWidget(self)
        self.listWidget2.addItems(["aa","bb"])
        self.listWidget2.setFixedSize(280,200)

        self.listWidget3 = QListWidget(self)

        self.listWidget3.addItems(["cc","dd"])
        self.listWidget3.setFixedSize(280,200)
        
        self.addTab(self.listWidget,"股票")
        self.addTab(self.listWidget2,"期貨")
        self.addTab(self.listWidget3,"選擇權")

        
        self.start = QLabel("起始",self)
        self.end = QLabel("結束",self)
        self.k = QLabel("K線週期",self)
        self.year = QComboBox(self)
        self.month = QComboBox(self)
        self.day = QComboBox(self)
        self.year2 = QComboBox(self)
        self.month2 = QComboBox(self)
        self.day2 = QComboBox(self)
        self.scope = QLineEdit(self)
        self.Tcount = QComboBox(self)


        self.year.addItems([str(x) for x in range(1998,2018)])
        self.month.addItems([str(y) for y in range(1,13)])
        self.day.addItems([str(z) for z in range(1,32)])
        self.year2.addItems([str(a) for a in range(1998,2018)])
        self.month2.addItems([str(b) for b in range(1,13)])
        self.day2.addItems([str(c) for c in range(1,32)])

        self.scope.setPlaceholderText("default:1")  #時間週期輸入框，設定字體大小
        f = self.scope.font()
        f.setPointSize(12) 
        self.scope.setFont(f)

        self.Tcount.addItems(["日","周","月"])
        self.Tcount.resize(40,27.5)


        self.start.move(350,100)    #起始時間標籤
        self.year.move(400, 100)
        self.month.move(500, 100)
        self.day.move(600, 100)

        self.end.move(350,150)  #結束時間標籤
        self.year2.move(400,150)
        self.month2.move(500,150)
        self.day2.move(600,150)
        
        self.k.move(350,200)
        self.scope.move(430,200)
        self.Tcount.move(600,200)

        self.subbutton = QPushButton('確認',self)
        self.subbutton.move(400, 350)

        backbutton = QPushButton('back \n返回 \nリターン \nбуцах',self)
        backbutton.move(550, 300)



        self.lineedit = QLineEdit(self)
        #self.lineedit.setIcon(QIcon(":/icon/search.png"))

        model = QStringListModel()
        model.setStringList(['中石化', '台泥', '竺元','aa','bb','cc'\
            ,'dd'])

        completer = QCompleter()
        completer.setModel(model)
        self.lineedit.setCompleter(completer)
        self.lineedit.setFixedWidth(200)
        self.lineedit.setPlaceholderText("search by name")
        f = self.lineedit.font()
        f.setPointSize(12) 
        self.lineedit.setFont(f)
        self.lineedit.move(350, 50)


        self.subbutton.clicked.connect(lambda:self.compare(self.currentIndex())) # 比較如果時間不符跳警示窗
        backbutton.clicked.connect(self.close)

    def compare(self,index):
        a = None
        itemlist = (['中石化', '台泥', '竺元','aa','bb','cc','dd'])
        if index == 0:
            mylist = self.listWidget
        elif index == 1:
            mylist = self.listWidget2
        elif index == 2:
            mylist = self.listWidget3 
        
        for i in mylist.selectedItems():
            a = i.text()[:3].replace(" ","")

        if a == None and self.lineedit.text() == "":
            self.dwrongmsg = dateWrong("NE") # no enter
            print ("沒選擇啦嫩")
            self.dwrongmsg.show()

        elif a == None and self.lineedit.text() not in itemlist:
            self.dwrongmsg = dateWrong("NI")  #no item
            print("沒有這項產品")
            self.dwrongmsg.show()
        
        elif int(self.year.currentText()) > int(self.year2.currentText()):
            self.dwrongmsg = dateWrong("T")   #time error
            print ("date wrong1")
            self.dwrongmsg.show()
        elif int(self.year.currentText()) == int(self.year2.currentText()) and int(self.month.currentText()) >= \
            int(self.month2.currentText()):
            self.dwrongmsg = dateWrong("T")
            print ("date wrong2")
            self.dwrongmsg.show()


        else:
            print ("date right")
            self.tt(index)
            self.close()
        

    def tt(self,index):
        if index == 0:
            try:
                self.num = str(self.listWidget.selectedItems()[0].text()[:3].replace(" ",""))
            except:
                self.num = self.lineedit.text()
        elif index == 1:
            self.num = str(self.listWidget2.currentItem().text()[:3].replace(" ",""))
        elif index == 2:
            self.num = str(self.listWidget3.currentItem().text()[:3].replace(" ",""))

        file = open("./cache/fuckfile.txt","w",encoding = 'utf8')
        file.write(self.num)
        print("stockcombo is "+self.num)
        if self.scope.text()=="":    #如果沒有輸入時間週期，跑預設的1
            self.num2=1
        else:
            self.num2 = int(self.scope.text())
        self.a = str(self.year.currentText())+"-"+str(self.month.currentText())+"-"+str(self.day.currentText())
        self.b = str(self.year2.currentText())+"-"+str(self.month2.currentText())+"-"+str(self.day2.currentText())
        if self.Tcount.currentText() == "日":
            self.tc = self.num2* 1

        elif self.Tcount.currentText() == "周":
            self.tc = self.num2* 7
        
        else:
            self.tc = self.num2* 30            
        print("self.num="+self.num)
        print("self.a="+self.a)
        print("self.b="+self.b)
        print("self.tc="+str(self.tc))
        self.kline(self.num,self.a,self.b,self.tc)
    
    def main():
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()

    def onActivated(self, text):
      
        self.lbl.setText(text)
        self.lbl.adjustSize()
        

    def kline(self,num,a,b,tc):
        
        self.graphicview = QtWidgets.QGraphicsView()  # 第一步，創建一个QGraphicsView
        self.graphicview.setObjectName("graphicview")
        
        dr = Figure_Canvas()
        #實例化一个FigureCanvas
        dr.test(num,a,b,tc)  # 畫圖
        graphicscene = QtWidgets.QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        graphicscene.addWidget(dr)  # 第四步，把圖形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        self.graphicview.setScene(graphicscene)
        self.graphicview.show()  # 最後，調用show方法呈现图形！Voila!!
        self.graphicview.resize(1100,500) 


class futureWindow(QWidget):
    def __init__(self, parent = None):
        super(futureWindow, self).__init__(parent)
        self.setFixedSize(800, 600)
        self.setWindowTitle('股票清單')
 

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
class chooseWindow(QWidget):
    def __init__(self, parent = None):
        super(chooseWindow, self).__init__(parent)
        self.setFixedSize(600, 300)
        self.setWindowTitle('選擇交易策略')
        self.lbl2 = QLabel("txf2")
        #self.strategycombo = QComboBox(self)
        self.strategylist = QListWidget(self)
        self.strategylist.addItems(["atr","bollinger","cross","cumret","highlow",\
            "hurst","linebreak","linreg","ma","macd","ratio","roc","rsi","stats","stoch",\
            "vwap"])

        self.strategylist.move(100, 50)
        strategybutton = QPushButton('確認',self)
        strategybutton.move(400, 200)
        #self.strategycombo.activated[str].connect(self.onActivated)
        strategybutton.clicked.connect(self.compare)
        strategybutton.clicked.connect(self.close)

    def compare(self):
        a = None
        for i in self.strategylist.selectedItems():
            a = i.text()
        if a == None:
            self.dwrongmsg = dateWrong("NS")
            self.dwrongmsg.show()
        else:
            self.pyalgostrategy(self.strategylist.selectedItems()[0].text())
        

    def main():
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        mainwindow.show()

    def pyalgostrategy(self,strategyname):
        path = "C:\\Users\\user\\Desktop\\lastest(8.19)\\cache"
        if os.path.exists(path+"\\8-11.csv"):
            if strategyname =="ma": 
                f = open("./cache/TSname.txt",'w')
                f.write('ma'+'\n'+'150')
            if strategyname =="macd":
                f = open("./cache/TSname.txt",'w')
                f.write('macd'+'\n'+'12'+'\n'+'26'+'\n'+'9')                
    def onActivated(self, text):
      
        self.lbl2.setText(text)
        self.lbl2.adjustSize()
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
        """
        stockcombo.addItem("Ubuntu")
        stockcombo.addItem("Mandriva")
        stockcombo.addItem("Fedora")
        stockcombo.addItem("Arch")
        stockcombo.addItem("Gentoo")
        """
        stockcombo.addItems(["a","b","c"])

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
        """
        self.graphicview = QtWidgets.QGraphicsView()  # 第一步，创建一个QGraphicsView
        self.graphicview.setObjectName("graphicview")
        dr = Figure_Canvas()
        graphicscene = QtWidgets.QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        graphicscene.addWidget(dr)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        self.graphicview.setScene(graphicscene)  # 第五步，把QGraphicsScene放入QGraphicsView
        self.graphicview.show()  # 最后，调用show方法呈现图形！
        self.setCentralWidget(self.graphicview)
        self.graphicview.resize(1100,500)
        """
        self.setupUi(self)
        self.initUI()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())