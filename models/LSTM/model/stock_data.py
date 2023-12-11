import yfinance as yf
import pandas as pd
import numpy as np

class Data:
    def __init__(self):
        pass
    
    def get_historical_data(self, new_file_path):
        stock_data = yf.download(self.stock_list, start='2010-01-01', group_by='Ticker')
        stock_data.to_csv(new_file_path)

    def get_one_historical_data(self, ticker, year):
        stock_data = yf.download([ticker], start=f'{year - 10}-01-01', end = f'{year}-12-31')
        return stock_data[['Open', 'High', 'Low', 'Close', 'Adj Close']]     

    
    def get_balance_sheet(self, new_file_path):
        pass

    def merge_data(self, sheet1, sheet2):
        index = sheet1['Ticker']

    def finanacial_data(self, new_file_path):
        attribute_list = ['Research And Development']
        financial_data = {}
        for a in attribute_list:
            financial_data[a] = {}
        for ticker in self.stock_list:
            try:
                stock = yf.Ticker(ticker)
                for a in attribute_list:
                    stat = stock.financials.transpose()[a][0]
                    financial_data[a][ticker] = stat
                print("Going Well")
            except:
                print("Wrong Ticker")
                continue
        df = pd.DataFrame(financial_data)
        df.to_csv(new_file_path)




