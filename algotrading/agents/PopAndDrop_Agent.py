import pandas as pd
import numpy as np
from time import time
import matplotlib.pyplot as plt


class PopAndDrop_Agent:
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
    
    def getStochasticOscillator(self, n_days):
        self.data['Close'] = self.data['Price']
        
        rolling_high = pd.Series((data["High"].rolling(n_days).max()),
        name = 'Rolling High') 
        self.data = self.data.join(rolling_high)
        rolling_low = pd.Series((data["Low"].rolling(n_days).min()),
        name = 'Rolling Low') 
        self.data = self.data.join(rolling_low)
        
        self.data["K"] = 100*(self.data['Close'] - self.data['Rolling Low'])/(self.data['Rolling High'] - self.data['Rolling Low'])
        self.data["D"] = self.data["K"].rolling(3).mean()
        return self.data.head()
    
    def MovingAverages(self, data, n_days=50):
        """
        Generate moving averages for a variable window size
        """
        data = pd.Series(data)
        avg = pd.Series((data.rolling(n_days).mean()),
        name = '%d Moving Average' % (n_days))
        return avg
    
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
    
    def run(self, verbose=0):
        """
        Run agent with constraints about percent above and below the moving average
        """
        self.reset()
        CCI = self.data["CCI"]
        prices = self.prices
        for i in range(0, self.length):
            # buy
            self.portfolio.append(self.stock*self.price+self.cash)
            if(self.cash>prices[i] and CCI[i]>100):
                stocks_to_buy = int(self.cash/prices[i])
                cash_required = prices[i]*int(self.cash/prices[i])
                self.stock += stocks_to_buy
                self.cash -= cash_required
                if verbose:
                    #print("Day :%d, Buying %d stocks for %f" % (i, stocks_to_buy, cash_required))
                    #print("Stocks owned %d" % (self.stock))
                    #print("Cash owned %f" % (self.cash))
                    #print("Portfolio valuation : %f" % (self.stock*self.price+self.cash))
                continue
            
            # sell
            if(self.stock>0 and CCI[i]<100):
                stocks_to_sell = int(self.stock)
                cash_recieved = prices[i]*(self.stock)
                self.cash+=prices[i]*(self.stock)
                self.stock=0
                if verbose:
                    #print("Day :%d, Selling %d stocks for %f" % (i, stocks_to_sell, cash_recieved))
                    #print("Stocks owned %d" % (self.stock))
                    #print("Cash owned %f" % (self.cash))
                    #print("Portfolio valuation : %f" % (self.stock*self.price+self.cash))
                continue
        return self.stock*self.price+self.cash