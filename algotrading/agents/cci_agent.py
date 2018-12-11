from .BaseAgent import BaseAgent
import numpy as np
from time import time

class CCI_Agent(BaseAgent):
    def __init__(self, cash, window_size):
        super().__init__(cash, window_size)

    def reset(self):
        """
        Reset agent
        """
        self.cash=0
        self.stock=1
        self.portfolio=[]
    
    def getCCI(self, n_days):
        TP = (self.data['High'] + self.data['Low'] + self.data['Close']) / 3 
        CCI = pd.Series((TP - TP.rolling(n_days).mean()) / (0.015 * TP.rolling(n_days).std()),
        name = 'CCI') 
        self.data = self.data.join(CCI)
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
                    print("Day :%d, Buying %d stocks for %f" % (i, stocks_to_buy, cash_required))
                    #print("Stocks owned %d" % (self.stock))
                    #print("Cash owned %f" % (self.cash))
                    print("Portfolio valuation : %f" % (self.stock*self.price+self.cash))
                continue
            
            # sell
            if(self.stock>0 and CCI[i]<100):
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