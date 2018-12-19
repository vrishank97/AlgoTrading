import sys
sys.path.append('../')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RISK_FREE_RETURN = 0.07

class Evaluation:
	def __init__(self, prices, dates, output, algo, security):
		self.prices = prices
		self.dates = dates
		self.output = output
		self.algo = algo
		self.security = security
		self.risk_free = []
		self.adjusted = None

	def plot_output(self):
		scaling_factor = 10000/self.prices[0]
		fig, ax = plt.subplots()
		ax.plot(np.arange(len(self.prices)), self.output, color='red')
		ax.plot(np.arange(len(self.prices)), self.risk_free, color='blue')
		ax.plot(np.arange(len(self.prices)), self.prices*scaling_factor, color='green')

		ax.set(xlabel='Days', ylabel='INR',
		       title='Running %s on %s stocks' % (self.algo, self.security))
		ax.grid()
		plt.show()

	def get_days(self, date):
		date_form = date.split("-")

		return (int(date_form[1]) - 1)*30 + int(date_form[2])

	def roi(self):
		return (self.output[-1] - self.output[0])/self.output[0]

	def get_adjusted_return(self):
		if(self.adjusted is not None):
			return self.adjusted

		adjusted = []
		for i in range(len(self.dates)):
			days = self.get_days(self.dates[i])
			risk_free = (1 + (days/361)*RISK_FREE_RETURN)*self.output[0]
			self.risk_free.append(risk_free)
			adjusted.append((self.output[i] - risk_free)/risk_free)

		self.adjusted = adjusted

		return adjusted

	def sharpe_ratio(self):
		roi = self.roi()
		returns = pd.Series(self.get_adjusted_return())
		#print(returns)
		sd = returns.std()
		#print(sd)

		#print(roi, sd[0])

		return (roi - RISK_FREE_RETURN)/sd

	def sortino_ratio(self):
		roi = self.roi()

		returns = pd.Series([x for x in self.get_adjusted_return() if x < 0])
		#print(returns)
		sd = returns.std()
		#print(sd)

		return (roi - RISK_FREE_RETURN)/sd

	def complete_evaluation(self, get_plots=True, verbose=True):
		'''
		if verbose is True:
			print("Running ", self.algo)
			print("The Sharpe Ratio is ", self.sharpe_ratio())
			print("The Sortino Ratio is ", self.sortino_ratio())
			print("The return on investment is(in percentage) ", self.roi()*100)

		if get_plots is True:
			self.plot_output()
		'''
		return self.sharpe_ratio(), self.sortino_ratio(), self.roi()*100
		
