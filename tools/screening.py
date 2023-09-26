import pandas as pd
from openpyxl import load_workbook

DATA_PATH = 'data/raw/Stock List-FINAL.xlsx'
EVTOEBIT_PATH = 'data/processed/evtoebit.xlsx'
RESULT_PATH = 'data/processed/after_screening.xlsx'
evtoebits = pd.read_excel(EVTOEBIT_PATH)
evtoebits.set_index('Ticker')
stock_list = pd.ExcelFile(DATA_PATH)
financials_sheet = pd.read_excel(stock_list, 'Financials')
consumer_discretionary_sheet = pd.read_excel(stock_list, 'Consumer Discretionary')
industrials_sheet = pd.read_excel(stock_list, 'Industrials')
healthcare_sheet = pd.read_excel(stock_list, 'Healthcare')
energy_sheet = pd.read_excel(stock_list, 'Energy')
utilities_sheet = pd.read_excel(stock_list, 'Utilities')
excel_book = load_workbook(RESULT_PATH)
# financials_avg = 
# consumer_discretionary_avg = 

def screening(sheet, avgevtoebit, new_sheet_name):
    results = {}
    for company_name in sheet['Ticker']:
        try:
            evtoebit = evtoebits['EVtoEBIT'].iloc[evtoebits[evtoebits['Ticker'] == company_name].index]
            if len(evtoebit) == 0:
                raise IndexError
            if evtoebit.values > avgevtoebit:
                results[company_name] = 1
            else:
                results[company_name] = 0
        except:
            results[company_name] = -1
    result_df = pd.DataFrame(data=results, index = [0])
    result_df = result_df.transpose()
    result_df.reset_index(inplace=True)
    result_df.columns = ['Ticker', 'Result']
    final = pd.concat([sheet, result_df['Result']], axis=1)
    with pd.ExcelWriter(RESULT_PATH, engine = 'openpyxl', mode='a') as writer:
        final.to_excel(writer, sheet_name = new_sheet_name)

screening(financials_sheet, 10, 'Financials')
screening(consumer_discretionary_sheet, 10, 'Consumer Discretionary')
        

