import pandas as pd
import yfinance as yf

class BS():
    def __init__(self, start):
        self.start = start

    def PE_query(self, start):
        pass
    
    def price_to_book_query(self, start):
        pass

    def revenue_growth_query(self, start):
        pass

    def overall_risk(self, start):
        pass
    

    def get_complete_dataset():
        comp = pd.concat([], axis=1)
        comp = comp.fillna(method='ffill')
        return comp