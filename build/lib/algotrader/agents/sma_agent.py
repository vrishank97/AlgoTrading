from .BaseAgent import BaseAgent
import pandas as pd
import numpy as np
from time import time

class SMA_Agent(BaseAgent):
    def __init__(self, window_size, up, down):
        super().__init__(window_size)
        self.up = up
        self.down = down
        self.window_size = window_size

    def step(self, price):
        self.memory.append(price)
        if len(self.memory)<self.window_size:
            return 0

        # Buy
        if(price<=np.mean(self.memory)*(1-self.down)):
            return 1

        # Sell
        if(price>=np.mean(self.memory)*(1+self.up)):
            return -1

        # Hold
        return 0