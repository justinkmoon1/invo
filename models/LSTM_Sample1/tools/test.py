import yfinance as yf

ticker = yf.Ticker('AAPL')

print(ticker.financials.transpose().columns)

print(dir(yf.Ticker))