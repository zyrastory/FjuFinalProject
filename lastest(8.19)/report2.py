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



def tab_widget():
    path = "C:\\Users\\user\\Desktop\\lastest(8.19)\\cache"
    listR = []
    for dirPath, dirNames, fileNames in os.walk (path):
        fileNames = [ fi for fi in fileNames if  fi.endswith(".csv") ]
        for f in fileNames:
            if int(f[0])>=1:
                listR.append(f)
    print(listR)


    for r in range(len(listR)):
        #print(listR[r])
        feed = GenericBarFeed(Frequency.DAY, None, None)
        feed.addBarsFromCSV("item", "./cache/%s"%(listR[r]))
        f = open("./cache/%s"%(listR[r][2:].replace("csv","txt")),'r', encoding = 'utf8')
        u=[]
        line=f.readline()
        while line:            
            u.append(line)
            line = f.readline() 



        a = u[0].replace("\n","")

        if a[:2]=="my":     #使用者寫的策略(不傳參數給策略，已經寫在裡面)
            os.system("rename .\\strategy\\User\\%s.md %s.py"%(a[2:],a[2:]))
            sys.path.append('C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\User')
            #new_module = __import__(a)

            module = importlib.import_module(a[2:], package=None)
            MyStrategy = getattr(importlib.import_module(a[2:]), 'MyStrategy')

            print("商品為"+listR[r])
            print("啟用使用者策略---"+a[2:])
            myStrategy = MyStrategy(feed, "item")

        elif len(u)==2: #確認非使用者策略，且傳一參數之策略

            os.system("rename .\\strategy\\internal\\%s.md %s.py"%(a,a))

            sys.path.append('C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\internal')
            module = importlib.import_module(a, package=None)   #所有內建策略
            MyStrategy = getattr(importlib.import_module(a), 'MyStrategy')
            print("商品為"+listR[r])
            print("啟用內建策略---"+a)
            myStrategy = MyStrategy(feed, "item",u[1])

        elif len(u)==4: #確認非使用者策略(macd)，且傳一參數之策略

            os.system("rename .\\strategy\\internal\\%s.md %s.py"%(a,a))

            sys.path.append('C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\internal')
            module = importlib.import_module(a, package=None)   #所有內建策略
            MyStrategy = getattr(importlib.import_module(a), 'MyStrategy')
            print("商品為"+listR[r])
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
        os.system("del %s\\%s"%(path,listR[r][2:].replace("csv","png")))
        os.system("rename %s\\8-13.png %s"%(path,listR[r][2:].replace("csv","png")))



        