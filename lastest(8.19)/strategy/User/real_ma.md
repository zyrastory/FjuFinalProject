from pyalgotrade.technical import ma
from pyalgotrade import strategy

class MyStrategy(strategy.BacktestingStrategy):  
    def __init__(self, feed, instrument,*args):  
        super(MyStrategy, self).__init__(feed) 
        print("執行使用者策略 in real_ma")
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(),150)


        self.__position = None
        self.__instrument = instrument  
        self.getBroker()
        self.a = 0 
    def onEnterOk(self, position):  
        execInfo = position.getEntryOrder().getExecutionInfo()  
        self.info("BUY at %.2f" % (execInfo.getPrice())) 
        self.a+=1
  
    def onEnterCanceled(self, position):  
        self.__position = None  
  
    def onExitOk(self, position):  
        execInfo = position.getExitOrder().getExecutionInfo()  
        self.info("SELL at $%.2f" % (execInfo.getPrice()))  
        self.__position = None  
  
    def onExitCanceled(self, position):  
        self.__position.exitMarket()  
  
    def getSMA(self):  
        return self.__sma


    def onBars(self, bars):   
        try:
            if self.__sma[-1] is not None:
                bar = bars[self.__instrument]
            elif self.__sma[-1] is None:
                return    
            if self.__position is None:  
                if bar.getPrice() > self.__sma[-1]:    
                    self.__position = self.enterLong(self.__instrument, 2000, True)  
            elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive(): 
                self.__position.exitMarket()
        except AttributeError:
            print("",end="")