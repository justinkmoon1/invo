import openpyxl
from openpyxl import workbook, load_workbook
from datetime import date
today = date.today()

import yfinance as yf
import pandas as pd

file_path = r'C:\Users\Serry\Desktop\projects\py\invo\data\excell automation\totalValuation\Total Valuation Model.xlsx.xlsx'

wb = load_workbook(file_path)
ws = wb['Master Inputs Start here']