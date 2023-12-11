from final_data_query import get_data
import pandas as pd

year = 2010

for l in ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "TSLA", "GOOG", "BRK.B", "META", "UNH", "XOM", "LLY", "JPM", "JNJ", "V", "PG", "MA", "AAVGO", "HD", "CVX", "MRK", "ABBV", "COST", "PEP", "KO"]:
    get_data(l, year)