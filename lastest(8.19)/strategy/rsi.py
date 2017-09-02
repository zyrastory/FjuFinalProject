from pyalgotrade.technical import rsi
from pyalgotrade.technical import ma
from pyalgotrade.technical import vwap
from pyalgotrade import plotter  
from pyalgotrade.stratanalyzer import returns, sharpe, drawdown, trades  
from pyalgotrade import strategy  
from pyalgotrade.bar import Frequency  
from pyalgotrade.barfeed.csvfeed import GenericBarFeed  

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
        self.__rsi6 = rsi.RSI(feed[instrument].getCloseDataSeries(), 6)

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
        self.info("%f 6-RSI:%s 14-RSI%s" % (bar.getClose(),self.__rsi6[-1],self.__rsi[-1]))
        try:
            if self.__rsi[-1] is not None: 
                bar = bars[self.__instrument]
            elif self.__rsi[-1] is None:
                return 
            if self.__position is None:  
                #if self.__rsi6[-1] < self.__rsi[-1]:
                if self.__rsi6[-1] < 25:
                    self.__position = self.enterLong(self.__instrument,3000,True)

            #elif self.__rsi6[-1] > self.__rsi[-1]  and not self.__position.exitActive():
            elif self.__rsi6[-1] > 75  and not self.__position.exitActive():  
                self.__position.exitMarket()


        except AttributeError:
            print("",end="")
 
 

feed = GenericBarFeed(Frequency.DAY, None, None)
feed.addBarsFromCSV("item", "./cache/8-11.csv")
 
# Evaluate the strategy with the feed's bars.
myStrategy = MyStrategy(feed, "item")
myStrategy.run()
myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())