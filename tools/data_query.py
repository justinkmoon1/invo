import yfinance as yf
import pandas as pd
import numpy as np

data = pd.read_csv("data/raw/company_list.csv")
stock_list = data['Symbol'].tolist()[:400]
stock_data = yf.download(stock_list, start='2010-01-01', group_by='Ticker')
file_path = 'data/raw/stock_data.csv'
stock_data.to_csv(file_path)




