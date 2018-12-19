from .BaseAgent import BaseAgent
import pandas as pd
import numpy as np
from time import time

class EMA_Agent(BaseAgent):
    def __init__(self, window_size, up, down):
        super().__init__(window_size)
        self.window_size = window_size
        self.multiplier = 2/(window_size + 1)
        self.running_ema = 0
        self.up = up
        self.down = down


    def step(self, price):
        self.memory.append(price)

        if len(self.memory)<self.window_size:
            return 0

        if self.running_ema == 0:
            self.running_ema = np.mean(self.memory)
        else:
            self.running_ema = (price - self.running_ema)*self.multiplier + self.running_ema

        # Buy
        if(price >= self.running_ema*(1-self.down)):
            return 1

        # Sell
        if(price <= self.running_ema*(1+self.up)):
            return -1

        # Hold
        return 0