from pyalgotrade.technical import rsi
from pyalgotrade.technical import ma
from pyalgotrade.technical import vwap
from pyalgotrade import strategy  

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument,*args):
        super(MyStrategy, self).__init__(feed)

        print("執行內建rsi")
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(),int(args[0].replace("\n","")))
        self.__rsi6 = rsi.RSI(feed[instrument].getCloseDataSeries(),int(args[1]))

        self.__instrument = instrument
        self.__position = None
        self.getBroker()
    def onEnterOk(self, position):  
        execInfo = position.getEntryOrder().getExecutionInfo()  
        self.info("BUY at %.2f" % (execInfo.getPrice())) 
        
  
    def onEnterCanceled(self, position):  
        self.__position = None  
  
    def onExitOk(self, position):  
        execInfo = position.getExitOrder().getExecutionInfo()  
        self.info("SELL at $%.2f" % (execInfo.getPrice()))  
        self.__position = None  
  
    def onExitCanceled(self, position):  
        self.__position.exitMarket()
 
    def onBars(self, bars):
        bar = bars[self.__instrument]
        try:
            if self.__rsi[-1] is not None: 
                bar = bars[self.__instrument]
            elif self.__rsi[-1] is None:
                return 
            if self.__position is None:  
                #if self.__rsi6[-1] < self.__rsi[-1]:
                if self.__rsi6[-1] < 25:
                    self.__position = self.enterLong(self.__instrument,5000,True)

            #elif self.__rsi6[-1] > self.__rsi[-1]  and not self.__position.exitActive():
            elif self.__rsi6[-1] > 75  and not self.__position.exitActive():  
                self.__position.exitMarket()


        except AttributeError:
            print("",end="")