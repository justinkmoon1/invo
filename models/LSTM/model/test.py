import yfinance as yf

print(yf.download(['GM']).iloc[-1]['Close'])