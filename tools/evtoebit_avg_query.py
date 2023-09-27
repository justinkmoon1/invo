import pandas as pd
import time

df = pd.read_excel("data/raw/23-24 Competition Stock List-FINAL.xlsx")
xls = pd.ExcelFile("data/processed/inds_modified.xlsx")
inds = pd.read_excel(xls, 'Global alphabetical')

modified_inds = inds[["Exchange:Ticker", "Industry Group"]]
print(modified_inds.head())
print(modified_inds.shape)
tickers_list = df["Ticker"].tolist()
industries = {}
went_wrong = []
cnt = 0
#print(type(str(modified_inds.iloc[3629]['Exchange:Ticker']).split(":")[1].strip()))
#print(type(tickers_list[1]))
#prnt(str(modified_inds.iloc[3629]['Exchange:Ticker']).split(":")[1].strip() == tickers_list[1])

for i in range(modified_inds.shape[0] - 1):
    #print(type(str(modified_inds.iloc[i]['Exchange:Ticker']).split(":")[1]), type(ticker))
    if str(modified_inds.iloc[i]['Exchange:Ticker']).split(":")[1] in tickers_list:
        #print("Check A")
        industries[str(modified_inds.iloc[i]['Exchange:Ticker']).split(":")[1]] = modified_inds.iloc[i]['Industry Group']
        cnt += 1
        print(cnt)
        

print(len(industries), len(went_wrong))
print(went_wrong)
result_df = pd.DataFrame(industries, index=[0])
result_df.to_excel('data/processed/industries.xlsx')


