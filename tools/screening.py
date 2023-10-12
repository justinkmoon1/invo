import pandas as pd
from openpyxl import load_workbook

#PATH Settings
DATA_PATH = 'data/raw/Stock List.xlsx'
EVTOEBIT_PATH = 'data/processed/evtoebit_final.xlsx'
RESULT_PATH = 'data/processed/after_screening_final.xlsx'
AVG_PATH = 'data/processed/evtoebit_avgs.xlsx'
INDLIST_PATH = 'data/processed/industries.xlsx'

#Stats Loading
indlist = pd.read_excel(INDLIST_PATH)
evtoebits = pd.read_excel(EVTOEBIT_PATH)
evtoebitavg = pd.read_excel(AVG_PATH)
stock_list = pd.ExcelFile(DATA_PATH)
evtoebits.set_index('Ticker')

#Sheets Loading
financials_sheet = pd.read_excel(stock_list, 'Financials')
consumer_discretionary_sheet = pd.read_excel(stock_list, 'Consumer Discretionary')
industrials_sheet = pd.read_excel(stock_list, 'Industrials')
healthcare_sheet = pd.read_excel(stock_list, 'Healthcare')
energy_sheet = pd.read_excel(stock_list, 'Energy')
utilities_sheet = pd.read_excel(stock_list, 'Utilities')
excel_book = load_workbook(RESULT_PATH)




def screening(sheet, new_sheet_name):
    errors_A = 0
    errors_B = 0
    results = {}
    evtoebits_final = {}
    evtoebits_avg = {}
    for i in range(sheet.shape[0]):
        company_name = sheet.iloc[i]['Ticker']
        try:
            evtoebit = evtoebits['EVtoEBIT'].iloc[evtoebits[evtoebits['Ticker'] == sheet.iloc[i]['Ticker']].index]
            if len(evtoebit) == 0:
                errors_A += 1
                raise IndexError
            industry = indlist[sheet.iloc[i]['Original']]
            avgevtoebit = float(evtoebitavg.loc[evtoebitavg['Industry Name'] == industry.values[0]]['EV/EBIT'].iloc[0])
            if evtoebit.values > avgevtoebit:
                results[company_name] = 1
                evtoebits_final[company_name] = evtoebit.values
                evtoebits_avg[company_name] = avgevtoebit
            else:
                results[company_name] = 0
                evtoebits_final[company_name] = evtoebit.values
                evtoebits_avg[company_name] = avgevtoebit
        except:
            errors_A += 1
            
            results[company_name] = -1
            evtoebits_final[company_name] = "N/A"
            evtoebits_avg[company_name] = "N/A"
    result_df = pd.DataFrame(data=results, index = [0])
    result_df = result_df.transpose()
    result_df.reset_index(inplace=True)
    result_df.columns = ['Ticker', 'Result']
    final = pd.concat([sheet, result_df['Result']], axis=1)
    evtoebit_df = pd.DataFrame(data=evtoebits_final, index = [0])
    evtoebit_df = evtoebit_df.transpose()
    evtoebit_df.reset_index(inplace=True)
    evtoebit_df.columns = ['Ticker', 'EV/EBIT']
    final2 = pd.concat([final, evtoebit_df['EV/EBIT']], axis=1)
    evtoebits_avg_df = pd.DataFrame(data=evtoebits_avg, index = [0])
    evtoebits_avg_df = evtoebits_avg_df.transpose()
    evtoebits_avg_df.reset_index(inplace=True)
    evtoebits_avg_df.columns = ['Ticker', 'EV/EBIT AVG']
    final3 = pd.concat([final2, evtoebits_avg_df['EV/EBIT AVG']], axis=1)
    with pd.ExcelWriter(RESULT_PATH, engine = 'openpyxl', mode='a') as writer:
        final3.to_excel(writer, sheet_name = new_sheet_name)
    print(errors_A, new_sheet_name)


#Call Functions
screening(financials_sheet, 'Financials')
screening(consumer_discretionary_sheet, 'Consumer Discretionary')
screening(industrials_sheet, 'Industrials')
screening(healthcare_sheet, 'Healthcare')
screening(energy_sheet, 'Energy')
screening(utilities_sheet, 'Utilities')
