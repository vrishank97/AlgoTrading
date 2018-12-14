import sys
sys.path.append('../')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RISK_FREE_RETURN = 0.07

class Evaluation:
	def __init__(self, prices, output, algo, security):
		self.prices = prices[:365]
		self.output = output[:365]
		self.algo = algo
		self.security = security

	def plot_output(self, scaling_factor=1):
		fig, ax = plt.subplots()
		ax.plot(np.arange(len(self.prices)), self.output, color='red')
		ax.plot(np.arange(len(self.prices)), self.prices*scaling_factor, color='green')

		ax.set(xlabel='Days', ylabel='INR',
		       title='Monies')
		ax.grid()
		plt.show()

	def roi(self):
		return (self.output[-1] - self.output[0])/self.output[0]

	def sharpe_ratio(self):
		roi = self.roi()
		returns = pd.Series((np.array(self.output) - self.output[0])/self.output[0])

		sd = returns.std()

		#print(roi, sd[0])

		return (roi - RISK_FREE_RETURN)/sd

	def complete_evaluation(self, price_scaling_factor=1):
		print("Running ", self.algo)
		print("The Sharpe Ratio is ", self.sharpe_ratio())
		print("The return on investment is(in percentage) ", self.roi()*100)
		self.plot_output(price_scaling_factor)
		
