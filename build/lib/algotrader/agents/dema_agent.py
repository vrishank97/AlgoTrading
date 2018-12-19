from .BaseAgent import BaseAgent
import pandas as pd
import numpy as np
from time import time
from collections import deque

class DEMA_Agent(BaseAgent):
    def __init__(self, window_size, up, down):
        super().__init__(window_size)
        self.window_size = window_size
        self.multiplier = 2/(window_size + 1)
        self.running_ema = 0
        self.up = up
        self.down = down
        self.running_dema_memory = deque(maxlen=window_size)
        self.running_dema = 0
        self.running_dema_memory.append(0)


    def step(self, price):
        self.memory.append(price)

        if len(self.memory)<self.window_size:
            return 0

        if self.running_ema == 0:
            self.running_ema = np.mean(self.memory)
        else:
            self.running_ema = (price - self.running_ema)*self.multiplier + self.running_ema

        if len(self.running_dema_memory)<self.window_size:
            self.running_dema = np.mean(self.running_dema_memory)
        else:
            self.running_dema = (self.running_ema - self.running_dema)*self.multiplier + self.running_dema

        # print("EMA: %s, EMA(EMA): %s" % (self.running_ema, self.running_dema))
        DEMA = (2*self.running_ema) - self.running_dema
        self.running_dema_memory.append(self.running_ema)
        


        # Buy
        if(price >= DEMA*(1-self.down)):
            return 1

        # Sell
        if(price <= DEMA*(1+self.up)):
            return -1

        # Hold
        return 0