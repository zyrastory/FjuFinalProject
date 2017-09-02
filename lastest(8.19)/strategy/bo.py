from pyalgotrade.technical import bollinger
from pyalgotrade import strategy
from pyalgotrade.bar import Frequency  
from pyalgotrade.barfeed.csvfeed import GenericBarFeed 

 
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        sigma=2
        self.__bband = bollinger.BollingerBands(feed[instrument].getCloseDataSeries(),15, sigma)
        self.__bbandLow = self.__bband.getLowerBand()
        self.__bbandMiddle = self.__bband.getMiddleBand()
        self.__bbandUpper = self.__bband.getUpperBand()
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
        #self.info("%f Low:%s Middle:%s Upper:%s" % (bar.getClose(),self.__bbandLow[-1],self.__bbandMiddle[-1],self.__bbandUpper[-1]))
        a=str(self.__bbandUpper[-1])
               
        try:
            if self.__bbandUpper[-1] is not None:
                #print("1") 
                bar = bars[self.__instrument]
            if self.__bbandUpper[-1] is None:
                #print("2")
                return 
            if self.__position is None:
                  
                if bar.getClose()<self.__bbandUpper[-1] and bar.getClose()>self.__bbandLow[-1]:
                    #print("3")
                    self.__position = self.enterLong(self.__instrument,3000,True)
            elif  bar.getClose()>self.__bbandUpper[-1] and not self.__position.exitActive():  
                #print("4")
                self.__position.exitMarket()
        except AttributeError:
            print("",end="")
        
feed = GenericBarFeed(Frequency.DAY, None, None)
feed.addBarsFromCSV("item", "./cache/8-11.csv")
 
# Evaluate the strategy with the feed's bars.
myStrategy = MyStrategy(feed, "item")
myStrategy.run()
myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())