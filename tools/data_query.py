import yfinance as yf
import pandas as pd
import numpy as np

def get_stock_list(company_list_path, new_file_path):
    data = pd.read_csv(company_list_path)
    stock_list = data['Symbol'].tolist()[:400]
    stock_data = yf.download(stock_list, start='2010-01-01', group_by='Ticker')
    stock_data.to_csv(new_file_path)




