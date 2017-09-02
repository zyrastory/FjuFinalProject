from pyalgotrade.stratanalyzer import returns, sharpe, drawdown, trades  
from pyalgotrade import strategy  
from pyalgotrade.bar import Frequency  
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
import os
import importlib
import sys



feed = GenericBarFeed(Frequency.DAY, None, None)
feed.addBarsFromCSV("item", "./strategy/8-11.csv")
os.system("rename .\\cache\\compiler.md compiler.py")
sys.path.append('C:\\Users\\user\\Desktop\\lastest(8.19)\\cache')


module = importlib.import_module("compiler", package=None)
MyStrategy = getattr(importlib.import_module("compiler"), 'MyStrategy')

print("編譯程序啟用")
myStrategy = MyStrategy(feed, "item")

sharpe_ratio = sharpe.SharpeRatio()
mytrade = trades.Trades() 
myStrategy.attachAnalyzer(sharpe_ratio)
myStrategy.attachAnalyzer(mytrade)
myStrategy.run()

os.system("rename .\\cache\\compiler.py compiler.md")