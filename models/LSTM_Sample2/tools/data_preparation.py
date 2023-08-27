from macro_query import Macro
from stock_data import Data
import pandas as pd

macro = Macro(2010)
data = Data("data/raw/FINAL-22-23-Approved-Stock-List-V2_September9.csv")
macro_df = macro.get_complete_macro()
stock_df = data.get_one_historical_data()
comp_stat = pd.concat([stock_df, macro_df], axis=1)
comp_statistics = comp_stat.dropna(axis=0)
print(macro_df)
print(stock_df)
print(comp_statistics)
comp_statistics = comp_statistics[['Open', 'High', 'Low', 'Close', 'Adj Close', 'CPI Index', 'GDP', 'Fed Fund Rate']]
comp_statistics.to_csv('models/LSTM_Sample2/data/test_data.csv')