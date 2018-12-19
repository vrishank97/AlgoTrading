import pandas as pd
import sys
sys.path.append('../')
from algotrading.backtest import Backtest
from algotrading.agents.dema_agent import DEMA_Agent
from algotrading.evaluation import Evaluation

def test(year, stock, window=10, up=0.05, down=0.05, get_plots=True, verbose=True):
	filename = "../Historical Data/%s/%s-%s.csv" %(year, stock, year)
	prices = pd.read_csv(filename)["Close"]
	dates = pd.read_csv(filename)["Date"]

	agent = DEMA_Agent(window, up, down)

	test = Backtest(agent, 10000)

	output = test.run(prices)

	# class Evaluation takes for initialization - prices, output, name of algorithm, name of security
	evaluator = Evaluation(prices, dates, output, "DEMA", stock)
	return evaluator.complete_evaluation(get_plots, verbose)

if __name__ == "__main__":
	test(sys.argv[1], sys.argv[2])