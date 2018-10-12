import pandas as pd
import numpy as np
from time import time

class SMA_Agent:
    def __init__(self, data):
        self.data=data
        self.stock=1
        self.cash=0
        self.price=self.data["Price"][0]
        self.prices=np.array(self.data["Price"])
        self.value=self.stock*self.price+self.cash
        self.up=0.1
        self.down=0.1
        self.length=len(data)
        self.moving_avg=self.MovingAverages(self.prices)
        self.portfolio=[]

    def reset(self):
        """
        Reset agent
        """
        self.cash=0
        self.stock=1
        self.portfolio=[]
    
    def getPortfolioVal(self):
        """
        Returns current portfolio valuation
        """
        return self.stock*self.price+self.cash
    
    def MovingAverages(self, data, window_size=50):
        """
        Generate moving averages for a variable window size
        """
        prices = np.array(data)
        averages = np.array(data)
        for i in range(0, len(data)):
            a = max(0,int(i)-window_size)
            window = prices[a:i+1]
            #print(prices[a:i])
            averages[i] = window.mean()
        averages[0]=prices[0]
        return averages
    
    def Volatility(self, window_size=50):
        """
        Generate Volatility score for a variable window size
        """
        prices = np.array(self.prices)
        volatilities = np.array(self.prices)
        for i in range(0, self.length):
            a = max(0,int(i)-window_size)
            window = prices[a:i+1]
            #print(prices[a:i])
            volatilities[i] = np.sqrt(np.sum(np.square(window-window.mean())))
        volatilities[0]=0
        return volatilities
    
    def run(self, up, down, verbose=0):
        """
        Run agent with constraints about percent above and below the moving average
        """
        self.reset()
        moving_avg = self.moving_avg
        prices = self.prices
        for i in range(0, self.length):
            # buy
            self.portfolio.append(self.stock*self.price+self.cash)
            if(self.cash>prices[i] and prices[i]<(1-down)*moving_avg[i]):
                stocks_to_buy = int(self.cash/prices[i])
                cash_required = prices[i]*int(self.cash/prices[i])
                self.stock += stocks_to_buy
                self.cash -= cash_required
                if verbose:
                    print("Day :%d, Buying %d stocks for %f" % (i, stocks_to_buy, cash_required))
                    #print("Stocks owned %d" % (self.stock))
                    #print("Cash owned %f" % (self.cash))
                    print("Portfolio valuation : %f" % (self.stock*self.price+self.cash))
                continue
            
            # sell
            if(self.stock>0 and prices[i]<(1+up)*moving_avg[i]):
                stocks_to_sell = int(self.stock)
                cash_recieved = prices[i]*(self.stock)
                self.cash+=prices[i]*(self.stock)
                self.stock=0
                if verbose:
                    print("Day :%d, Selling %d stocks for %f" % (i, stocks_to_sell, cash_recieved))
                    #print("Stocks owned %d" % (self.stock))
                    #print("Cash owned %f" % (self.cash))
                    print("Portfolio valuation : %f" % (self.stock*self.price+self.cash))
                continue
        return self.stock*self.price+self.cash