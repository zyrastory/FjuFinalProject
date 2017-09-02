from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os
from matplotlib import pyplot as plt 
import matplotlib

from pyalgotrade import plotter  
from pyalgotrade.stratanalyzer import returns, sharpe, drawdown, trades  
from pyalgotrade import strategy  
from pyalgotrade.bar import Frequency  
from pyalgotrade.barfeed.csvfeed import GenericBarFeed  
from pyalgotrade.technical import ma
from pyalgotrade.technical import macd

import importlib
import time



class tab_widget(QTabWidget):
    def __init__(self, parent=None):
        super(tab_widget, self).__init__(parent)
        self.setWindowTitle('績效報表report')
        self.setGeometry(500,300,800,550)
        #self.setStyleSheet("QTabBar{font: bold;}")
        self.setStyleSheet("QTabBar::tab { height: 35px; width: 180px;font-size: 18pt}")
        
        
        self.yoyo=Example()
        self.cookie = Circle()
        self.canvas = App()
        self.addTab(self.yoyo,"績效報表")
        self.addTab(self.canvas,"績效報表圖")
        self.addTab(self.cookie,"勝率圓餅圖")
        self.setCurrentIndex(0)
        self.i = 1
    def keyPressEvent(self, e):
        
        if e.key() == Qt.Key_Space:
            self.setCurrentIndex(self.i)
            self.i+=1
            if self.i == 3:
                self.i = 0
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        quit_msg = "確定要離開嗎?"
        reply = QMessageBox.question(self, 'Message', \
            quit_msg,QMessageBox.Yes , QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class Example(QWidget):         #櫃子
    def __init__(self,parent=None):
        super(Example, self).__init__(parent)

        hhbox = QHBoxLayout()                #横向布局

        self.tableWidget = QTableWidget()

        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(8)      #设置表格有两行五列

        self.table_sitting()

        hhbox.addWidget(self.tableWidget)    #把表格加入布局

        self.setLayout(hhbox)                #创建布局

        self.setWindowTitle("我是一个表格")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(920, 240)
        #self.show()

    def table_sitting(self):
        
        feed = GenericBarFeed(Frequency.DAY, None, None)
        feed.addBarsFromCSV("item", "./cache/8-11.csv")
        f = open("./cache/TSname.txt",'r', encoding = 'utf8')
        u=[]
        line=f.readline()
        while line:            
            u.append(line)
            line = f.readline() 

        a = u[0].replace("\n","")

        if a[:2]=="my":     #使用者寫的策略(不傳參數給策略，已經寫在裡面)
            os.system("rename .\\strategy\\User\\%s.md %s.py"%(a[2:],a[2:]))
            sys.path.append('C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\User')
            #new_module = __import__(a)

            module = importlib.import_module(a[2:], package=None)
            MyStrategy = getattr(importlib.import_module(a[2:]), 'MyStrategy')

            print("啟用使用者策略---"+a[2:])
            myStrategy = MyStrategy(feed, "item")

        elif len(u)==2: #確認非使用者策略，且傳一參數之策略

            os.system("rename .\\strategy\\internal\\%s.md %s.py"%(a,a))

            sys.path.append('C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\internal')
            module = importlib.import_module(a, package=None)   #所有內建策略
            MyStrategy = getattr(importlib.import_module(a), 'MyStrategy')
            print("啟用內建策略---"+a)
            myStrategy = MyStrategy(feed, "item",u[1])

        elif len(u)==4: #確認非使用者策略(macd)，且傳一參數之策略

            os.system("rename .\\strategy\\internal\\%s.md %s.py"%(a,a))

            sys.path.append('C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\internal')
            module = importlib.import_module(a, package=None)   #所有內建策略
            MyStrategy = getattr(importlib.import_module(a), 'MyStrategy')
            print("啟用內建策略---"+a)
            myStrategy = MyStrategy(feed, "item",u[1],u[2],u[3])

        plot = plotter.StrategyPlotter(myStrategy)
        sharpe_ratio = sharpe.SharpeRatio()
        mytrade = trades.Trades() 
        myStrategy.attachAnalyzer(sharpe_ratio)
        myStrategy.attachAnalyzer(mytrade)
        myStrategy.run()
        myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())
        #time.sleep(3)
        plot.plot()

        path = "C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\internal"
        for dirPath, dirNames, fileNames in os.walk (path):
            fileNames = [ fi for fi in fileNames if  fi.endswith(".py") ]
            for f in fileNames:
                os.system("rename .\\strategy\\internal\\%s %s.md"%(f,f.replace(".py","")))
        
        path2 = "C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\User"
        for dirPath, dirNames, fileNames in os.walk (path2):
            fileNames = [ fi for fi in fileNames if  fi.endswith(".py") ]
            for f in fileNames:
                os.system("rename .\\strategy\\User\\%s %s.md"%(f,f.replace(".py","")))     


        self.gotable(myStrategy,mytrade,sharpe_ratio)
        self.circle(myStrategy,mytrade,sharpe_ratio)


    def circle(self,myStrategy,mytrade,sharpe_ratio):
        plt.figure(figsize=(10,8))
        
        try:
            matplotlib.rcParams.update({'font.size': 16})
            explode = None
            b = (mytrade.getProfitableCount()/mytrade.getCount())*100
            #b=float(a)
            if b == 0:
                sizes =[100]
                labels = ['loss rate']
                colors = ['yellowgreen']
                
            elif b == 100:
                sizes =[100]
                labels = ['win rate']
                colors = ['red']
                
            else: 
                sizes =[b,100-b]
                labels = ['win rate','loss rate']
                colors = ['red','yellowgreen']
                explode = (0.05,0.05)
        except ZeroDivisionError:
            sizes = 0
        
        
        if explode == None:
            patches,l_text,p_text = plt.pie(sizes,labels=labels,colors=colors,
                                        labeldistance = 1.1,autopct = '%3.1f%%',shadow = False,
                                        startangle = 180,pctdistance = 0.6)
        else:
            patches,l_text,p_text = plt.pie(sizes,labels=labels,explode=explode,colors=colors,
                                        labeldistance = 1.1,autopct = '%3.1f%%',shadow = False,
                                          startangle = 90,pctdistance = 0.6)
        
        for t in l_text:
            t.set_size=(30)
        for t in p_text:
            t.set_size=(20)
        
        
        plt.axis('equal')
        #labels.move(300,300)
        plt.legend(loc='best')
        plt.savefig("C:\\Users\\user\\Desktop\\lastest(8.19)\\cache\\9487.png"\
            ,dpi=70)
        #self.initUI()


    def gotable(self,myStrategy,mytrade,sharpe_ratio):
        self.setStyleSheet("font-size: 12pt")
        self.tableWidget.setHorizontalHeaderLabels([""])
        self.tableWidget.setVerticalHeaderLabels(["淨利", "毛利","毛損","報酬率","總交易次數","勝率","獲利因子","夏普比率"])


        lb0 = QLabel(str(int(myStrategy.getResult()-1000000)))
        self.tableWidget.setCellWidget(0,0,lb0)

        gross_w =str(mytrade.getProfits().sum())
        lb1 = QLabel(gross_w)
        self.tableWidget.setCellWidget(1,0,lb1)

        gross_l =str(mytrade.getLosses().sum())
        lb2 = QLabel(gross_l)
        self.tableWidget.setCellWidget(2,0,lb2)

        a=str(((myStrategy.getResult()-1000000)/1000000)*100)
        last_a=a[:6]+"(%)"
        lb3 = QLabel(last_a)
        self.tableWidget.setCellWidget(3,0,lb3)

        last_a=str(mytrade.getCount())
        lb4 = QLabel(last_a)
        self.tableWidget.setCellWidget(4,0,lb4)
        try:
            a=str(mytrade.getProfitableCount()/mytrade.getCount()*100)
            last_a=a[:6]+"(%)"
        except ZeroDivisionError:
            last_a=" N/A"

        lb5 = QLabel(last_a)
        self.tableWidget.setCellWidget(5,0,lb5)

        gross_w =(mytrade.getProfits().sum())
        gross_l =(mytrade.getLosses().sum())
        if gross_l != 0:
            w_l= str(abs(gross_w/gross_l))
        else:
            w_l="0.0"
        lb6 = QLabel(w_l[:5])
        self.tableWidget.setCellWidget(6,0,lb6)
        lb7 = QLabel(str(sharpe_ratio.getSharpeRatio(0)))
        self.tableWidget.setCellWidget(7,0,lb7)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        g = open("./cache/fuckfile.txt",'r',encoding = 'utf8')
        gline = g.readline() 
        
        label = QLabel(self)
        pixmap = QPixmap('./cache/8-13.png')
        label.setPixmap(pixmap)

        label2 = QLabel(gline,self)
        label2.move(20,20)


class Circle(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(150, 150, 150, 150)
        label = QLabel(self)
        pixmap = QPixmap('./cache/9487.png')
        label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = tab_widget()
    w.show()
    sys.exit(app.exec_())


