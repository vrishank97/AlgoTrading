import pandas as pd
import sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.sma_agent import SMA_Agent
import matplotlib.pyplot as plt
import numpy as np

prices = pd.read_csv("../Historical data/DABU Historical Data.csv")["Price"]

agent = SMA_Agent(10000, 10, 0.015, 0.015)

test = Backtest(agent)

output = test.run(prices)

fig, ax = plt.subplots()
ax.plot(np.arange(len(prices)), output, color='green')
ax.plot(np.arange(len(prices)), prices, color='green')

ax.set(xlabel='Days', ylabel='INR',
       title='Monies')
ax.grid()
plt.show()