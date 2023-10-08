import pandas as pd
import yfinance as yf

xls = pd.ExcelFile('data/raw/Stock List.xlsx')
data = pd.read_excel(xls, 'Companies')
stock_list = data['Ticker'].tolist()
print(stock_list)
WACC_data = {'Ticker': stock_list, 'previousClose': [], 'sharesOutstanding': [], 'LongTermDebt(2022)': [], 'CurrentDebt(2022)': [], 'LongTermDebt(2023)': [], 'CurrentDebt(2023)': [], 'PretaxIncome': [], 'InterestExpense': [], 'TaxProvision':[], 'TotalDebt2023': [], 'TotalDebt2022': []
            , 'DebtAverage':[], 'InterestExpense/DebtAverage':[],
            'avgtaxrate':[], 'mktvequity': [], 'E+D': [], 'perE': [], 'perD': [], 'costofequity': [], 'WACC': []}
cur = 0
ticker = yf.Ticker('CCL')
for t in stock_list:
    cur += 1
    print(cur)
    ticker = yf.Ticker(t)
    try:
        WACC_data['LongTermDebt(2022)'].append(ticker.get_balance_sheet(freq='quarterly').iloc[:, 2].loc['LongTermDebt'])
    except:
        WACC_data['LongTermDebt(2022)'].append('N/A')
    try:
        WACC_data['LongTermDebt(2023)'].append(ticker.get_balance_sheet(freq='quarterly').iloc[:, 0].loc['LongTermDebt'])
    except:
        WACC_data['LongTermDebt(2023)'].append('N/A')
    try:
        WACC_data['CurrentDebt(2022)'].append(ticker.get_balance_sheet(freq='quarterly').iloc[:, 2].loc['CurrentDebt'])
    except:
        WACC_data['CurrentDebt(2022)'].append('N/A')
    try:
        WACC_data['CurrentDebt(2023)'].append(ticker.get_balance_sheet(freq='quarterly').iloc[:, 0].loc['CurrentDebt'])
    except:
        WACC_data['CurrentDebt(2023)'].append('N/A')
    try:
        WACC_data['PretaxIncome'].append(ticker.get_income_stmt(freq='quarterly').iloc[:, 1].loc['PretaxIncome'])
    except:
        WACC_data['PretaxIncome'].append('N/A')
    try:
        WACC_data['InterestExpense'].append(ticker.get_income_stmt(freq='quarterly').iloc[:, 1].loc['InterestExpense'])
    except:
        WACC_data['InterestExpense'].append('N/A')
    try:
        WACC_data['TaxProvision'].append(ticker.get_income_stmt(freq='quarterly').iloc[:, 1].loc['TaxProvision'])
    except:
        WACC_data['TaxProvision'].append('N/A')
    try:
        WACC_data['sharesOutstanding'].append(ticker.get_info()['sharesOutstanding'])
    except:
        WACC_data['sharesOutstanding'].append('N/A')
    try:
        WACC_data['previousClose'].append(ticker.get_info()['previousClose'])
    except:
        WACC_data['previousClose'].append('N/A')
    try:
        WACC_data['TotalDebt2022'].append(ticker.get_balance_sheet(freq='quarterly').iloc[:, 0].loc['TotalDebt'])
    except:
        WACC_data['TotalDebt2022'].append('N/A')
    try:
        WACC_data['TotalDebt2023'].append(ticker.get_balance_sheet(freq='quarterly').iloc[:, 2].loc['TotalDebt'])
    except:
        WACC_data['TotalDebt2023'].append('N/A')

    try:
        WACC_data['DebtAverage'].append((WACC_data['TotalDebt2022'][-1] + WACC_data['TotalDebt2023'][-1])/2)
    except:
        WACC_data['DebtAverage'].append('N/A')
    try:
        WACC_data['InterestExpense/DebtAverage'].append(WACC_data['InterestExpense'][-1] / WACC_data['DebtAverage'][-1])
    except:
        WACC_data['InterestExpense/DebtAverage'].append('N/A')
    try:
        WACC_data['avgtaxrate'].append(WACC_data['TaxProvision'][-1] / WACC_data['PretaxIncome'][-1])
    except:
        WACC_data['avgtaxrate'].append('N/A')

    try:
        WACC_data['mktvequity'].append(WACC_data['previousClose'][-1] * WACC_data['sharesOutstanding'][-1])
    except:
        WACC_data['mktvequity'].append('N/A')
    try:
        WACC_data['E+D'].append(WACC_data['mktvequity'][-1] + WACC_data['DebtAverage'][-1])
    except:
        WACC_data['E+D'].append('N/A')
    try:
        WACC_data['perE'].append(WACC_data['DebtAverage'][-1] / WACC_data['E+D'][-1])
    except:
        WACC_data['perE'].append('N/A')
    try:
        WACC_data['perD'].append(WACC_data['mktvequity'][-1] / WACC_data['E+D'][-1])
    except:
        WACC_data['perD'].append('N/A')

    try:
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
        avggrowth = sum(growth) / len(growth)
        predicted = avggrowth * WACC_data['previousClose'][-1]
        WACC_data['costofequity'].append(predicted)
    except:
        WACC_data['costofequity'].append('N/A')
    
    try:
        WACC_data['WACC'].append(WACC_data['InterestExpense/DebtAverage'][-1] * WACC_data['perD'][-1] * (1 - WACC_data['avgtaxrate'][-1]) + WACC_data['perE'][-1] * WACC_data['costofequity'][-1])
    except:
        WACC_data['WACC'].append('N/A')

WACC = pd.DataFrame.from_dict(WACC_data)
WACC.set_index('Ticker')
print(WACC)
WACC.to_excel('data\processed\WACC.xlsx')
print(WACC)
