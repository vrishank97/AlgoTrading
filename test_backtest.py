import pandas as pd
from backtest import Backtest
from sma_agent import SMA_Agent
import matplotlib.pyplot as plt
import numpy as np
import os


stocks = os.listdir("Historical data/")
for stock in stocks[1:7]:
    prices = pd.read_csv("Historical data/"+stock)["Price"]
    agent = SMA_Agent(10000, 10, 0.015, 0.015)
    test = Backtest(agent)
    output = test.run(prices)
    fig, ax = plt.subplots()
    ax.plot(np.arange(len(prices)), output, color='orange')
    ax.plot(np.arange(len(prices)), prices, color='orange')

    ax.set(xlabel='Days', ylabel='INR',
           title=stock)
    ax.grid()
    plt.show()