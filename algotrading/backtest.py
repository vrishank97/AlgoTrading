import pandas as pd

class Backtest:
	def __init__(self, agent):
		self.agent = agent

	def run(self, data, dates=None):
		results = []
		for i in range(len(data)):
			if dates is not None:
				self.agent.step(data[i], dates[i])
			else:
				self.agent.step(data[i])
			val = self.agent.getPortfolioVal(data[i])
			results.append(val)
			#print("Portfolio valuation : %f" % (val))
		return results