from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os

from pyalgotrade import plotter  
from pyalgotrade.stratanalyzer import returns, sharpe, drawdown, trades  
from pyalgotrade import strategy  
from pyalgotrade.bar import Frequency  
from pyalgotrade.barfeed.csvfeed import GenericBarFeed  
from pyalgotrade.technical import ma
from pyalgotrade.technical import linreg 


class tab_widget(QTabWidget):
    def __init__(self, parent=None):
        super(tab_widget, self).__init__(parent)
        self.setGeometry(100,100,800,400)
        self.setStyleSheet("QTabBar{font: bold;}")
        self.canvas = App()


        w = QWidget()
        w.setLayout(QVBoxLayout())
        w.layout().addWidget(QPushButton("click me"))
        w.layout().addWidget(QLineEdit("write me"))
        self.yoyo=Example()
        self.addTab(w,"Tab1")
        self.addTab(self.canvas,"Tab2")
        self.addTab(self.yoyo,"Tab3")


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
        self.show()

    def table_sitting(self):
        feed = GenericBarFeed(Frequency.DAY, None, None)
        path = "C:\\Users\\user\\Desktop\\lastest(8.14)"
        if os.path.exists(path+"\\8-11.csv"): 
            feed.addBarsFromCSV("fd", "8-11.csv")  
      
            # 3.实例化策略  
            myStrategy = MyStrategy(feed, "fd")  
            # 4.设置指标和绘图  
            sharpe_ratio = sharpe.SharpeRatio()
            mytrade = trades.Trades() 
            myStrategy.attachAnalyzer(sharpe_ratio)
            myStrategy.attachAnalyzer(mytrade)
            #plt = plotter.StrategyPlotter(myStrategy) 
              
            # 5.运行策略  
            myStrategy.run()
            myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())

            self.tableWidget.setHorizontalHeaderLabels(["第一行", "第二行"])
            self.tableWidget.setVerticalHeaderLabels(["淨利", "毛利","毛損","報酬率","總交易次數","勝率","獲利因子","夏普比率"])
            #设置表头

            lb1 = QLabel(str(int(myStrategy.getResult()-1000000)))
            self.tableWidget.setCellWidget(0,0,lb1)
            lb2 = QLabel("test")
            self.tableWidget.setCellWidget(1,0,lb2)
            a=str(((myStrategy.getResult()-1000000)/1000000)*100)
            last_a=a[:6]+"(%)"
            lb3 = QLabel(last_a)
            self.tableWidget.setCellWidget(3,0,lb3)
            if mytrade.getCount()==0:
                last_a=" N/A"
            else:
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
            lb7 = QLabel(str(sharpe_ratio.getSharpeRatio(0)))
            self.tableWidget.setCellWidget(7,0,lb7)
        


class MyStrategy(strategy.BacktestingStrategy):  
    def __init__(self, feed, instrument):  
        super(MyStrategy, self).__init__(feed)  
        self.__position = None  
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 150)  
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
        # If the exit was canceled, re-submit it.  
        self.__position.exitMarket()  
  
    def getSMA(self):  
        return self.__sma  
  
    def onBars(self, bars):# 每一个数据都会抵达这里，就像becktest中的next  
  
        # Wait for enough bars to be available to calculate a SMA.  
        if self.__sma[-1] is None:  
            return  
        #bar.getTyoicalPrice = (bar.getHigh() + bar.getLow() + bar.getClose())/ 3.0  
  
        bar = bars[self.__instrument]  
        # If a position was not opened, check if we should enter a long position.  
        if self.__position is None:  
            if bar.getPrice() > self.__sma[-1]:  
                # 开多头.  
                self.__position = self.enterLong(self.__instrument, 100, True)  
        # 平掉多头头寸.  
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive(): 
            self.__position.exitMarket()


"""
class run():
    def run():
        feed = GenericBarFeed(Frequency.DAY, None, None)  
        feed.addBarsFromCSV("fd", "8-11.csv")  
  
        # 3.实例化策略  
        myStrategy = MyStrategy(feed, "fd")  
        # 4.设置指标和绘图  
        #sharpe_ratio = sharpe.SharpeRatio()  
        #myStrategy.attachAnalyzer(sharpe_ratio)  
        plt = plotter.StrategyPlotter(myStrategy)  
          
        # 5.运行策略  
        myStrategy.run()
        myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())  
          
        # 6.输出夏普率、绘图  
        #print ("sharpe_ratio", sharpe_ratio.getSharpeRatio(0))  
        plt.plot() 
"""

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        feed = GenericBarFeed(Frequency.DAY, None, None)

        path = "C:\\Users\\user\\Desktop\\lastest(8.14)"
        if os.path.exists(path+"\\8-11.csv"):  
            feed.addBarsFromCSV("fd", "8-11.csv")  
  
            # 3.实例化策略  
            myStrategy = MyStrategy(feed, "fd")
            plot = plotter.StrategyPlotter(myStrategy)
            myStrategy.run()
            plot.plot()
            self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(300, 300, 350, 300)
 
        # Create widget
        label = QLabel(self)
        pixmap = QPixmap('8-13.png')
        label.setPixmap(pixmap)
        #self.resize(QSize)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = tab_widget()
    w.show()
    sys.exit(app.exec_())


