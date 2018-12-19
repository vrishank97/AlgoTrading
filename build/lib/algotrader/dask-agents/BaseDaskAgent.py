from collections import deque

class BaseDaskAgent:
    def __init__(self, cash, window_size):
        self.cash = cash
        self.stock = 0
        self.memory = deque(maxlen=window_size)

    def deep_reset(self, cash, stock, stock_price, ticker):
        self.cash = cash
        self.stock = stock
        self.portfolio_val = self.cash + self.stock*self.stock_price
        self.ticker = ticker
        self.memory = deque(maxlen=1000)

    def reset_memory(self):
        self.memory = deque(maxlen=1000)

    def getPortfolioVal(self, price):
        return int((self.stock*price)+self.cash)
