import pandas as pd
from openpyxl import load_workbook
DATA_PATH = 'data/raw/Stock List-FINAL.xlsx'
EVTOEBIT_PATH = 'data/processed/evtoebit.xlsx'
RESULT_PATH = 'data/processed/after_screening.xlsx'
AVG_PATH = 'data/processed/evtoebit_avgs.xlsx'
INDLIST_PATH = 'data/processed/industries.xlsx'
indlist = pd.read_excel(INDLIST_PATH)
evtoebits = pd.read_excel(EVTOEBIT_PATH)
evtoebitavg = pd.read_excel(AVG_PATH)
evtoebits.set_index('Ticker')
stock_list = pd.ExcelFile(DATA_PATH)
financials_sheet = pd.read_excel(stock_list, 'Financials')
consumer_discretionary_sheet = pd.read_excel(stock_list, 'Consumer Discretionary')
industrials_sheet = pd.read_excel(stock_list, 'Industrials')
healthcare_sheet = pd.read_excel(stock_list, 'Healthcare')
energy_sheet = pd.read_excel(stock_list, 'Energy')
utilities_sheet = pd.read_excel(stock_list, 'Utilities')
excel_book = load_workbook(RESULT_PATH)

results = {}
evtoebit = evtoebits['EVtoEBIT'].iloc[evtoebits[evtoebits['Ticker'] == 'AMZN'].index]
print('check A')
if len(evtoebit) == 0:
    raise IndexError
industry = indlist['AMZN'].values[0]
print('check B')
print(evtoebitavg.head())
print(industry)
#evtoebitavg.columns = ['Industry Name', 'Number of firms', 'EV/EBITDA', 'EV/EBIT', 'EV/EBIT (1-t)']
print(evtoebitavg.loc[evtoebitavg['Industry Name'] == 'Retail (Online)']['EV/EBIT'])
avgevtoebit = float(evtoebitavg.loc[evtoebitavg['Industry Name'] == industry]['EV/EBIT'])
print('check C')
print(avgevtoebit)
print(evtoebit.values)
print(avgevtoebit)
if evtoebit.values > avgevtoebit:
    results['AMZN'] = 1
else:
    results['AMZN'] = 0

print(results)