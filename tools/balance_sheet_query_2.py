import pandas as pd
import yfinance as yf
import yahooquery as yq
df = pd.DataFrame(yf.Ticker('AAPL').get_balance_sheet())
print(df.columns)
# data = pd.read_csv("data/raw/FINAL-22-23-Approved-Stock-List-V2_September9.csv")
# stock_list = data['Ticker'].tolist()[:10]

# attribute_list = ['trailingPE', 'priceToBook', 'revenueGrowth', 'overallRisk']
# fundamental_data = {}
# #for a in attribute_list:
# #    financial_data[a] = {}
# for ticker in stock_list:
#     try:
#         stock = yf.Ticker(ticker)
#         for a in attribute_list:
#             stat = stock.financials.transpose()[a][0]
#             financial_data[a][ticker] = stat
#         print("Going Well")
#     except:
#         print("Wrong Ticker")
#         continue

# df = pd.DataFrame(financial_data)
# df.to_csv('data/processed/rnd')
# print(df)
# print(financial_data)


