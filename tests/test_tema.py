import pandas as pd
import sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.tema_agent import TEMA_Agent
from algotrading.evaluation import Evaluation

prices = pd.read_csv("../Historical data/AXBK Historical Data.csv")["Price"]

agent = TEMA_Agent(10000, 10, 0.05, 0.05)

test = Backtest(agent)

output = test.run(prices)

# class Evaluation takes for initialization - prices, output, name of algorithm, name of security
evaluator = Evaluation(prices, output, "TEMA", "AXBK")
evaluator.complete_evaluation()