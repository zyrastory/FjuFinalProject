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


class tab_widget(QTabWidget):
    def __init__(self, parent=None):
        super(tab_widget, self).__init__(parent)
        self.setWindowTitle('績效報表report')
        self.setGeometry(100,100,800,550)
        #self.setStyleSheet("QTabBar{font: bold;}")
        self.setStyleSheet("QTabBar::tab { height: 35px; width: 180px;font-size: 18pt}")
        
        self.canvas = App()
        self.cookie = Circle()
        self.yoyo=Example()
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
        #QMessageBox.question(None,'mesage','GoodBye!')
        quit_msg = "確定要離開嗎?"
        reply = QMessageBox.question(self, 'Message', \
            quit_msg,QMessageBox.Yes , QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class Example(QWidget):
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
        self.setStyleSheet("font-size: 12pt")
        feed = GenericBarFeed(Frequency.DAY, None, None)
        path = "C:\\Users\\user\\Desktop\\lastest(8.19)\\cache"
        if os.path.exists(path+"\\8-11.csv") and os.path.exists(path+"\\test.txt"): 
            feed.addBarsFromCSV("item", "./cache/8-11.csv")  
            f = open("./cache/test.txt",'r', encoding = 'utf8')
            u=[]
            line=f.readline()
            while line:
                #print(line)
                u.append(line)
                line = f.readline()


            
            if u[0] == "ma\n":
                myStrategy = MyStrategy(feed, "item",u[0],u[1])
            elif u[0] == "macd\n": 
                myStrategy = MyStrategy(feed, "item",u[0],u[1],u[2],u[3])  
            # 4.設置指標  
            sharpe_ratio = sharpe.SharpeRatio()
            mytrade = trades.Trades() 
            myStrategy.attachAnalyzer(sharpe_ratio)
            myStrategy.attachAnalyzer(mytrade)
            #plt = plotter.StrategyPlotter(myStrategy) 
              
            # 5.運行策略  
            myStrategy.run()
            myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())

            self.tableWidget.setHorizontalHeaderLabels([""])
            self.tableWidget.setVerticalHeaderLabels(["淨利", "毛利","毛損","報酬率","總交易次數","勝率","獲利因子","夏普比率"])
            #设置表头

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
            
class Circle(QWidget):
    def __init__(self):
        super(Circle, self).__init__()



        feed = GenericBarFeed(Frequency.DAY, None, None)

        path = "C:\\Users\\user\\Desktop\\lastest(8.19)\\cache"
        if os.path.exists(path+"\\8-11.csv") and os.path.exists(path+"\\test.txt"): 
            feed.addBarsFromCSV("item", "./cache/8-11.csv")  
            f = open("./cache/test.txt",'r', encoding = 'utf8')
            u=[]
            line=f.readline()
            while line:
            
                u.append(line)
                line = f.readline()
 
            if u[0] == "ma\n":
                myStrategy = MyStrategy(feed, "item",u[0],u[1])
            elif u[0] == "macd\n": 
                myStrategy = MyStrategy(feed, "item",u[0],u[1],u[2],u[3]) 
            mytrade = trades.Trades() 
            myStrategy.attachAnalyzer(mytrade)
            myStrategy.run()
        
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
        #plt.plot()
        self.initUI()

    def initUI(self):
        self.setGeometry(150, 150, 150, 150)
            
        label = QLabel(self)
        pixmap = QPixmap('./cache/9487.png')
        label.setPixmap(pixmap)


class MyStrategy(strategy.BacktestingStrategy):  
    def __init__(self, feed, instrument,name,*args):  
        super(MyStrategy, self).__init__(feed) 

        #self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(),int(args[0]))
        if name == "ma\n":
            print("執行MA")
            self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(),int(args[0]))
        elif name == "macd\n":
            print("執行macd")
            self.__macd = macd.MACD(feed[instrument].getCloseDataSeries(),int(args[0].replace("\n","")),int(args[1].replace("\n","")),int(args[2]))
            self.__macdHistgram=self.__macd.getHistogram()
            self.__macdSignal=self.__macd.getSignal()
        self.__position = None
        self.__instrument = instrument  
        self.getBroker()
        self.a = 0 
    def onEnterOk(self, position):  
        execInfo = position.getEntryOrder().getExecutionInfo()  
        #self.info("BUY at %.2f" % (execInfo.getPrice())) 
        self.a+=1
  
    def onEnterCanceled(self, position):  
        self.__position = None  
  
    def onExitOk(self, position):  
        execInfo = position.getExitOrder().getExecutionInfo()  
        #self.info("SELL at $%.2f" % (execInfo.getPrice()))  
        self.__position = None  
  
    def onExitCanceled(self, position):  
        self.__position.exitMarket()  
  
    def getSMA(self):  
        return self.__sma

    def getMACD(self):  
        return self.__macd   

    def onBars(self, bars):# 每一个数据都会抵达这里   
        try:
            if self.__sma[-1] is not None:
                bar = bars[self.__instrument]
            elif self.__sma[-1] is None:
                return    
            if self.__position is None:  
                if bar.getPrice() > self.__sma[-1]:    
                    self.__position = self.enterLong(self.__instrument, 5000, True)  
            elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive(): 
                self.__position.exitMarket()
            
        
        except AttributeError:
            print("",end="")
        #except Exception as e: print (str(e))
        
        try:
            if self.__macd[-1] is not None: 
                bar = bars[self.__instrument]
            elif self.__macd[-1] is None:
                return 
            if self.__position is None:  
                if self.__macdHistgram[-1] > 0:   
                    self.__position = self.enterLong(self.__instrument,5000, True)  
            elif self.__macdHistgram[-1] < 0 and not self.__position.exitActive():  
                self.__position.exitMarket()

        except AttributeError:
            print("",end="")
        #except Exception as e: print (str(e))



         

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        feed = GenericBarFeed(Frequency.DAY, None, None)

        path = "C:\\Users\\user\\Desktop\\lastest(8.19)\\cache"
        if os.path.exists(path+"\\8-11.csv") and os.path.exists(path+"\\test.txt"): 
            feed.addBarsFromCSV("item", "./cache/8-11.csv")  
            f = open("./cache/test.txt",'r', encoding = 'utf8')
            u=[]
            line=f.readline()
            while line:
            
                u.append(line)
                line = f.readline()
 
            if u[0] == "ma\n":
                myStrategy = MyStrategy(feed, "item",u[0],u[1])
            elif u[0] == "macd\n": 
                myStrategy = MyStrategy(feed, "item",u[0],u[1],u[2],u[3]) 
            

            plot = plotter.StrategyPlotter(myStrategy)
            myStrategy.run()
            plot.plot()
            self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(300, 300, 350, 300)
        g = open("./cache/fuckfile.txt",'r',encoding = 'utf8')
        gline = g.readline() 
        
        label = QLabel(self)
        pixmap = QPixmap('./cache/8-13.png')
        label.setPixmap(pixmap)

        label2 = QLabel(gline,self)
        label2.move(20,20)
        #self.resize(QSize)
        #self.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = tab_widget()
    w.show()
    sys.exit(app.exec_())


