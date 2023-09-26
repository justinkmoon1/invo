import yfinance as yf
import pandas as pd

df = pd.read_excel("data/raw/23-24 Competition Stock List-FINAL.xlsx")
tickers_list = df["Ticker"].tolist()
print(tickers_list)
evtoebit_dict = {}
total = len(tickers_list)
cnt_well = 0
cnt_no = 0
no_info = []
for ticker in tickers_list:
    print(f'Remaining: {total - cnt_well - cnt_no}')
    try:
        stock = yf.Ticker(ticker)
        print('Check A')

        evtoebit = stock.info['enterpriseValue'] / stock.financials.loc['EBIT'].iloc[0]
        print('Check B')
        evtoebit_dict[ticker] = evtoebit
        print('Check C')
        cnt_well += 1
    except:
        print('Wrong Ticker')
        no_info.append(ticker)
        cnt_no += 1
        continue
print(evtoebit_dict)
print(cnt_well, cnt_no)
df = pd.DataFrame(data=evtoebit_dict, index=[0])
df = (df.T)
df.to_excel('data/processed/evtoebit.xlsx')
ticker = yf.Ticker('AAPL')
print(ticker.info['enterpriseValue'] / ticker.financials.loc['EBIT'][0])