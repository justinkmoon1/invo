import yfinance as yf
import pandas as pd
import numpy as np

data = pd.read_csv('C:/Users/Justin Moon/Dropbox/청심국제고 2학년 기록/개인생활/대회/Wharton Investment Competition/invo/data/raw/company_list.csv')
stock_list = data['Symbol'].tolist()



print(stock_list)



