from pyalgotrade.technical import macd
from pyalgotrade import strategy

class MyStrategy(strategy.BacktestingStrategy):  
    def __init__(self, feed, instrument,*args):  
        super(MyStrategy, self).__init__(feed) 


        print("執行macd,i am gold town five")
        self.__macd = macd.MACD(feed[instrument].getCloseDataSeries(),12,26,9)
        self.__macdHistgram=self.__macd.getHistogram()
        self.__macdSignal=self.__macd.getSignal()

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

    def getMACD(self):  
        return self.__macd   

    def onBars(self, bars):   
        
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