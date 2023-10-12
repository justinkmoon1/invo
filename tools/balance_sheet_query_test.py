import pandas as pd
import yfinance as yf
ticker = yf.Ticker('AAPL')
#print(ticker.get_dividends())
#print(ticker.get_balance_sheet(freq='quarterly')) #LongTermDebt CurrentDebt
#print(ticker.get_income_stmt()) #PretaxIncome InterestExpense TaxProvision
#print(ticker.get_info()) #sharesOutstanding
#
#print(ticker.get_balance_sheet().iloc[:, 0].loc['LongTermDebt'])
#print(ticker.get_balance_sheet().iloc[:, 0].loc['CurrentDebt'])
#print(ticker.get_balance_sheet().iloc[:, 1].loc['LongTermDebt'])
#print(ticker.get_balance_sheet().iloc[:, 1].loc['CurrentDebt'])
#print(ticker.get_income_stmt().iloc[:, 0].loc['PretaxIncome'])
#print(ticker.get_income_stmt().iloc[:, 0].loc['InterestExpense'])
#print(ticker.get_income_stmt().iloc[:, 0].loc['TaxProvision'])
#print(ticker.get_info()['sharesOutstanding'])
#print(ticker.get_info()['previousClose'])
print(ticker.get_info())
all = []
growth = []
df = ticker.get_dividends()
for i in range(10):
    try:
        if sum(df.loc[str(2013 + i)].values) != 0:
            all.append(sum(df.loc[str(2013+i)].values))
    except:
        continue
for j in range(1, len(all)):
    growth.append((all[j] - all[j - 1])/all[j-1])
print(((sum(growth) / len(growth)) * all[-1]))
print(all)
print(growth)

"""
Current Quote
Statistics에서 Shares Outstanding
Historical Data에서 과거 10년 Dividents
Balance Sheet에서 Current Debt, Long Term Debt
Imcome Statement에서 Interest Expense, Pretax Income, Tax Provision"""