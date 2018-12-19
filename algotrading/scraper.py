import pandas as pd
import sys
sys.path.append('../')
import numpy as np
import os
import quandl

def getNifty():
	nifty_list = pd.read_csv("../Historical data/Nifty50list.csv")
	quandl.ApiConfig.api_key = "FDEDsMbK1E2t_PMf7X3M"
	
	for stock in nifty_list["Symbol"]:
	    try:
	        print(stock)
	        for i in range(2000,2018):
	            print(i)
	            df = quandl.get('NSE/'+stock, start_date=str(i)+'-01-01', end_date=str(i)+'-12-31')
	            if len(df)>0:
	                df.to_csv("../Historical data/%s/%s-%s.csv" % (i, stock, i))
	    except:
	        print("An exception occurred while retrieving %s" % (stock))