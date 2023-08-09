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
        temp = pd.DataFrame.from_dict(ticker_object.info, orient="index")
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

attribute_list = ["trailingPE", "ebitda"]
balance_sheet = combined_data[["Ticker"]].drop_duplicates(keep='first')
print(balance_sheet)
for item in attribute_list:
    temp = combined_data[combined_data["Attribute"] == item].reset_index()
    print("Temp:", temp.head())
    balance_sheet = pd.merge(balance_sheet, temp, how='outer', on='Ticker')


#del balance_sheet["index"]
print(balance_sheet)
balance_sheet.to_csv("data/processed/stocklist_balancesheet.csv")