import sys

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

test_function = {
				"cci" : run_cci,
				"sma" : run_sma,
				"ema" : run_ema,
				"dema" : run_dema,
				"tema" : run_tema,
				"momentum" : run_momentum
				}

def all_tests(year, stock):
	for key in test_function:
		test_function[key](year, stock)

if __name__ == "__main__":

	if(len(sys.argv) != 4):
		raise StandardError("Invalid arguments")

	algo = sys.argv[1]
	year = sys.argv[2]
	stock = sys.argv[3]

	if(algo == "all"):
		all_tests(year, stock)

	elif algo not in test_function:
		raise StandardError("Invalid algorithm")

	else:
		test_function[algo](year, stock)
