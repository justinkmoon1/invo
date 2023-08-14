#currently code to fetch trailingPE from yfinance

import pandas as pd
import yfinance as yf

data = pd.read_csv("data/raw/FINAL-22-23-Approved-Stock-List-V2_September9.csv")
stock_list = data['Ticker'].tolist()[:10]
fundamental_data = {}
wrong_ticker_list = []
for ticker in stock_list:
    try:
        print("Going Well")
        ticker_object = yf.Ticker(ticker)
        temp = pd.DataFrame.from_dict(ticker_object.financials, orient="index")
        temp.reset_index(inplace=True)
        temp.columns = ["Attribute", "Recent"]
    
    except:
        print("wrong ticker")
        print(ticker)
        wrong_ticker_list.append(ticker)
        continue
    
    # add (ticker, dataframe) to main dictionary
    fundamental_data[ticker] = temp

print(wrong_ticker_list)
combined_data = pd.concat(fundamental_data)
combined_data = combined_data.reset_index()
del combined_data["level_1"]
combined_data.columns = ["Ticker", "Attribute", "Recent"]
trailingPE = combined_data[combined_data["Attribute"] == "trailingPE"].reset_index()
del trailingPE["index"]

trailingPE.to_csv("data/processed/stocklist_stat.csv")

#trailingPE