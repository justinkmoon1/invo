import pandas as pd

stock_data = pd.read_csv("data/raw/stock_data.csv")
file_path = "models/LSTM_Sample1/data/stock_data_s1.csv"

print(stock_data.columns)
print(stock_data[["Date", "AAPL", "AAPL.1", "AAPL.2", "AAPL.3", "AAPL.4", "AAPL.5"]].head())

stock_data[["Date", "AAPL", "AAPL.1", "AAPL.2", "AAPL.3", "AAPL.4"]].to_csv(file_path)