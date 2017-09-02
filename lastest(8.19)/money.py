from pyalgotrade import plotter  
from pyalgotrade.stratanalyzer import returns, sharpe, drawdown, trades  
from pyalgotrade import strategy  
from pyalgotrade.bar import Frequency  
from pyalgotrade.barfeed.csvfeed import GenericBarFeed  
from pyalgotrade.technical import ma  
from pyalgotrade import broker  
# 1.构建一个策略  
class MyStrategy(strategy.BacktestingStrategy):  
    def __init__(self, feed, instrument, brk):  
        super(MyStrategy, self).__init__(feed, brk)  
        self.__position = None  
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 150)  
        self.__instrument = instrument  
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
                self.__position = self.enterLong(self.__instrument, 10, True)  
        # 平掉多头头寸.  
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():  
            self.__position.exitMarket()  
  

feed = GenericBarFeed(Frequency.DAY, None, None)  
feed.addBarsFromCSV("fd", "./cache/2_aaa_1998-1-1_2017-12-31.csv")  
# 3.broker setting  
# 3.1 commission类设置  
broker_commission = broker.backtesting.TradePercentage(0.001)  
# 3.2 fill strategy设置  

# 3.3完善broker类  
brk = broker.backtesting.Broker(5000, feed, broker_commission)  
  
# 4.把策略跑起来  
  
myStrategy = MyStrategy(feed, "fd", brk)  
  
# Attach a returns analyzers to the strategy.  
trade_situation = trades.Trades()  
myStrategy.attachAnalyzer(trade_situation)  
# Attach the plotter to the strategy.  
plt = plotter.StrategyPlotter(myStrategy)  
  
# Run the strategy.  
myStrategy.run()  
myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())  
print ("total number of trades", trade_situation.getCount())  
print ("commissions for each trade",trade_situation.getCommissionsForAllTrades()) 
# Plot the strategy.  
plt.plot()  