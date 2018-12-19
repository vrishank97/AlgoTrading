from collections import deque

class BaseAgent:
    def __init__(self, window_size):
        self.memory = deque(maxlen=window_size)

    def deep_reset(self, stock_price, ticker):
        self.ticker = ticker
        self.memory = deque(maxlen=1000)

    def reset_memory(self):
        self.memory = deque(maxlen=1000)