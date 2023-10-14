from macro_query2 import Macro
from stock_data import Data
import pandas as pd

def get_data(ticker):
    macro = Macro(2010)
    data = Data()
    macro_df = macro.get_complete_macro()
    stock_df = data.get_one_historical_data(ticker)
    comp_stat = pd.concat([stock_df, macro_df], axis=1)
    comp_statistics = comp_stat.dropna(axis=0)
    comp_statistics = comp_statistics[['Open', 'High', 'Low', 'Close', 'Adj Close', 'CPI Index', 'GDP', 'Fed Fund Rate']]
    comp_statistics.to_csv(f'models/LSTM/data/daily_training/{ticker}.csv', index=False, header=False)
