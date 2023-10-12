import yfinance as yf
import pandas as pd

df = pd.read_excel("models/LSTM/data/raw/Stock List.xlsx")
lst = df["Ticker"].tolist()
for l in lst:
    ticker = yf.Ticker(l)