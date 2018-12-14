import pandas as pd
import sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.dema_agent import DEMA_Agent
from algotrading.evaluation import Evaluation

prices = pd.read_csv("../Historical data/2017/ADANIPORTS-2017.csv")["Close"]

agent = DEMA_Agent(10000, 10, 0.015, 0.015)

test = Backtest(agent)

output = test.run(prices)

# class Evaluation takes for initialization - prices, output, name of algorithm, name of security
evaluator = Evaluation(prices, output, "DEMA", "GE")
evaluator.complete_evaluation()