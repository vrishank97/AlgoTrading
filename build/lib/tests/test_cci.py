import pandas as pd
import sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.cci_agent import CCI_Agent
from algotrading.evaluation import Evaluation

def test(year, stock):
	filename = "../Historical Data/%s/%s-%s.csv" %(year, stock, year)
	prices = pd.read_csv(filename)["Close"]
	dates = pd.read_csv(filename)["Date"]

	agent = CCI_Agent(25, 0.015, 0.015)

	test = Backtest(agent, 10000)

	output = test.run(prices)

	# class Evaluation takes for initialization - prices, output, name of algorithm, name of security
	evaluator = Evaluation(prices, dates, output, "CCI", stock)
	evaluator.complete_evaluation()

if __name__ == "__main__":
	test(sys.argv[1], sys.argv[2])