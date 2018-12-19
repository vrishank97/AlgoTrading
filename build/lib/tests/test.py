import sys
import os

def run_cci(year, stock):
	import test_cci
	test_cci.test(year, stock)

def run_sma(year, stock):
	import test_sma
	test_sma.test(year, stock)

def run_ema(year, stock):
	import test_ema
	test_ema.test(year, stock)

def run_dema(year, stock):
	import test_dema
	test_dema.test(year, stock)

def run_tema(year, stock):
	import test_tema
	test_tema.test(year, stock)

def run_momentum(year, stock):
	import test_momentum
	test_momentum.test(year, stock)

def run_six_month_cycle(year, stock):
	import test_six_month_cycle
	test_six_month_cycle.test(year, stock)

test_function = {
				"cci" : run_cci,
				"sma" : run_sma,
				"ema" : run_ema,
				"dema" : run_dema,
				"tema" : run_tema,
				"momentum" : run_momentum,
				"sixmonthcycle" : run_six_month_cycle
				}

if __name__ == "__main__":

	if(len(sys.argv) != 4):
		raise Exception("Invalid arguments")

	algo = sys.argv[1]
	year = sys.argv[2]
	stock = sys.argv[3]

	year_list = []
	stock_list = []
	algo_list = {}

	if year == "all":
		year_list = map(str, list(range(2000, 2018)))
	else:
		year_list = [year]

	for yr in year_list:
		stocks_avail = os.listdir("../Historical Data/%s/" %(yr))
		stocks_avail = [x.split("-")[0] for x in stocks_avail]

		if stock == "all":
			stock_list = stocks_avail
		else:
			stock_list = [stock]

		for stck in stock_list:
			if stck not in stocks_avail:
				print("Data for stock %s not available for year %s" %(stck, yr))
				continue

			if algo == "all":
				algo_list = test_function
			elif algo not in test_function.keys():
				print("Algorithm %s not available" %(algo))
			else:
				algo_list[algo] = test_function[algo]

			for alg in algo_list.keys():
				print("Running %s Algorithm on %s stock for %s year." %(alg, stck, yr))
				algo_list[alg](yr, stck)

	print("END")
