import pandas as pd

xls = pd.ExcelFile("data/raw/indname.xlsx")
inds = pd.read_excel(xls, 'Global alphabetical')

for i in range(inds.shape[0] - 1):
    try:
        a = inds['Exchange:Ticker'][i].split(":")

    except:
        inds['Exchange:Ticker'][i] = '0:0'

inds.to_excel('data/processed/inds_modified.xlsx')