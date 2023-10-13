#enter ticker
Ticker = 'AAPL'
#from summary page
Beta = 1.31

PreviousClose = 177.49

#from financials -> income statement
PretaxIncome = 22733000

TaxProvision = 2852000

InterestExpense = 998000

#from financials -> balance sheet
TotalDebt2023 = 109280000

TotalDebt2022 = 111110000

#from statistics
SharesOutstanding = 15630000000



#computation
#0.04795 is the risk free rate
CostofEquity = 0.04795 + Beta * 0.06

print(f"Cost of Equity:{CostofEquity}")

DebtAverage = (TotalDebt2022 + TotalDebt2023) / 2

CostofDebt = InterestExpense / DebtAverage

print(f"Cost of Debt: {CostofDebt}")

AverageTaxRate = TaxProvision / PretaxIncome

print(f"Average Tax Rate: {AverageTaxRate}")

MarketValueofEquity = SharesOutstanding * PreviousClose

EandD = MarketValueofEquity + DebtAverage

perE = MarketValueofEquity / EandD

perD = DebtAverage / EandD

WACC = CostofDebt * perD * (1 - AverageTaxRate) + perE * CostofEquity

print(f"WACC of {Ticker}: {WACC}")
