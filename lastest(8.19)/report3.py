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
        #self.cookie = Circle()
        self.canvas = App()
        self.width()
        self.addTab(self.yoyo,"績效報表")
        self.addTab(self.canvas,"績效報表圖")
        #self.addTab(self.cookie,"勝率圓餅圖")
        self.setCurrentIndex(0)
        self.i = 1

    def width(self):
        path = "C:\\Users\\user\\Desktop\\lastest(8.19)\\cache"
        self.listR = []
        for dirPath, dirNames, fileNames in os.walk (path):
            fileNames = [ fi for fi in fileNames if  fi.endswith(".csv") ]
            for f in fileNames:
                if int(f[0])>=1:
                    self.listR.append(f)
        if len(self.listR) == 2:
            self.setGeometry(500,300,1200,550)
        elif len(self.listR) >= 3:
            self.setGeometry(500,300,1200,1100)

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

        #设置表格有两行五列

        self.table_sitting()

        hhbox.addWidget(self.tableWidget)    #把表格加入布局

        self.setLayout(hhbox)                #创建布局

        self.setWindowTitle("我是一个表格")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(920, 240)

    def table_sitting(self):
        path = "C:\\Users\\user\\Desktop\\lastest(8.19)\\cache"
        self.listR = []
        for dirPath, dirNames, fileNames in os.walk (path):
            fileNames = [ fi for fi in fileNames if  fi.endswith(".csv") ]
            for f in fileNames:
                if int(f[0])>=1:
                    self.listR.append(f)
        print(self.listR)

        """
        style ="QTableView QTableCornerButton::section {\
    background: red;\
    border: 2px outset red;\
    }"
        self.tableWidget.setStyleSheet(style)
        """
        self.tableWidget.setColumnCount(len(self.listR))
        self.tableWidget.setRowCount(8)



        listA=[]
        for r in range(len(self.listR)):

            #print(self.listR[r])
            feed = GenericBarFeed(Frequency.DAY, None, None)
            feed.addBarsFromCSV("item", "./cache/%s"%(self.listR[r]))
            f = open("./cache/%s"%(self.listR[r][2:].replace("csv","txt")),'r', encoding = 'utf8')
            u=[]
            line=f.readline()
            while line:            
                u.append(line)
                line = f.readline() 



            a = u[0].replace("\n","")
            listA.append(a)

            if a[:2]=="my":     #使用者寫的策略(不傳參數給策略，已經寫在裡面)
                os.system("rename .\\strategy\\User\\%s.md %s.py"%(a[2:],a[2:]))
                sys.path.append('C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\User')
                #new_module = __import__(a)

                module = importlib.import_module(a[2:], package=None)
                MyStrategy = getattr(importlib.import_module(a[2:]), 'MyStrategy')

                print("商品為"+self.listR[r])
                print("啟用使用者策略---"+a[2:])
                myStrategy = MyStrategy(feed, "item")

            elif len(u)==2: #確認非使用者策略，且傳一參數之策略

                os.system("rename .\\strategy\\internal\\%s.md %s.py"%(a,a))

                sys.path.append('C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\internal')
                module = importlib.import_module(a, package=None)   #所有內建策略
                MyStrategy = getattr(importlib.import_module(a), 'MyStrategy')
                print("商品為"+self.listR[r])
                print("啟用內建策略---"+a)
                myStrategy = MyStrategy(feed, "item",u[1])

            elif len(u)==3: #確認非使用者策略，且傳兩參數之策略

                os.system("rename .\\strategy\\internal\\%s.md %s.py"%(a,a))

                sys.path.append('C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\internal')
                module = importlib.import_module(a, package=None)   #所有內建策略
                MyStrategy = getattr(importlib.import_module(a), 'MyStrategy')
                print("商品為"+self.listR[r])
                print("啟用內建策略---"+a)
                myStrategy = MyStrategy(feed, "item",u[1],u[2])

            elif len(u)==4: #確認非使用者策略(macd)，且傳一參數之策略

                os.system("rename .\\strategy\\internal\\%s.md %s.py"%(a,a))

                sys.path.append('C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\internal')
                module = importlib.import_module(a, package=None)   #所有內建策略
                MyStrategy = getattr(importlib.import_module(a), 'MyStrategy')
                print("商品為"+self.listR[r])
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
            
            

            path = "C:\\Users\\user\\Desktop\\lastest(8.19)\\cache"
            os.system("del %s\\%s"%(path,self.listR[r][2:].replace("csv","png")))
            os.system("rename %s\\8-13.png %s"%(path,self.listR[r][2:].replace("csv","png")))

            self.gotable(r,myStrategy,mytrade,sharpe_ratio)
            

        listR_set=[]
        for r in range(len(self.listR)):
            self.tableWidget.setColumnWidth(r,200)
            listR_set.append(self.listR[r][2:5]+"*"+listA[r])
            #listR_set.insert(0,"")

        print(listR_set)
        self.tableWidget.setHorizontalHeaderLabels(listR_set)


    def gotable(self,index,myStrategy,mytrade,sharpe_ratio):
        self.setStyleSheet("font-size: 12pt")
        
        self.tableWidget.setVerticalHeaderLabels(["淨利", "毛利","毛損","報酬率","總交易次數","勝率","獲利因子","夏普比率"])
        #self.tableWidget.setHorizontalHeaderLabels(["",self.listR[r][2:]])



        lb0 = QLabel(str(int(myStrategy.getResult()-1000000)))
        self.tableWidget.setCellWidget(0,index,lb0)

        gross_w =str(mytrade.getProfits().sum())
        lb1 = QLabel(gross_w)
        self.tableWidget.setCellWidget(1,index,lb1)

        gross_l =str(mytrade.getLosses().sum())
        lb2 = QLabel(gross_l)
        self.tableWidget.setCellWidget(2,index,lb2)

        a=str(((myStrategy.getResult()-1000000)/1000000)*100)
        last_a=a[:6]+"(%)"
        lb3 = QLabel(last_a)
        self.tableWidget.setCellWidget(3,index,lb3)

        last_a=str(mytrade.getCount())
        lb4 = QLabel(last_a)
        self.tableWidget.setCellWidget(4,index,lb4)
        try:
            a=str(mytrade.getProfitableCount()/mytrade.getCount()*100)
            last_a=a[:6]+"(%)"
        except ZeroDivisionError:
            last_a=" N/A"

        lb5 = QLabel(last_a)
        self.tableWidget.setCellWidget(5,index,lb5)

        gross_w =(mytrade.getProfits().sum())
        gross_l =(mytrade.getLosses().sum())
        if gross_l != 0:
            w_l= str(abs(gross_w/gross_l))
        else:
            w_l="0.0"
        lb6 = QLabel(w_l[:5])
        self.tableWidget.setCellWidget(6,index,lb6)
        lb7 = QLabel(str(sharpe_ratio.getSharpeRatio(0)))
        self.tableWidget.setCellWidget(7,index,lb7)


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        path = "C:\\Users\\user\\Desktop\\lastest(8.19)\\cache"
        self.listR = []
        for dirPath, dirNames, fileNames in os.walk (path):
            fileNames = [ fi for fi in fileNames if  fi.endswith(".csv") ]
            for f in fileNames:
                if int(f[0])>=1:
                    self.listR.append(f)

        h_layout = QHBoxLayout()
        h_layout2 = QHBoxLayout()
        v_layout = QVBoxLayout()
        
        

        label0 = QLabel(self)
        label1 = QLabel(self)
        label2 = QLabel(self)
        label3 = QLabel(self)


        for r in range(len(self.listR)):
            
            pixmap = QPixmap('./cache/%s'%(self.listR[r][2:].replace("csv","png")))
            print(self.listR[r][2:].replace("csv","png"))
            
            if r == 0:
                label0.setPixmap(pixmap)
                h_layout.addWidget(label0)
            elif r == 1:
                label1.setPixmap(pixmap)
                h_layout.addWidget(label1)
            elif r == 2:
                label2.setPixmap(pixmap)
                h_layout2.addWidget(label2)
            elif r == 3:
                label3.setPixmap(pixmap)
                h_layout2.addWidget(label3)
        if len(self.listR)>=3:
            v_layout.addLayout(h_layout)
            v_layout.addLayout(h_layout2)
            self.setLayout(v_layout)
        else:
            v_layout.addLayout(h_layout)
            self.setLayout(v_layout)




        
        

        



