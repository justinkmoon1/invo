from lxml import html
import requests
import pandas as pd
import yfinance
import numpy as np
import json

def parse(ticker):
    url = "https://stockanalysis.com/stocks/{}/financials/cash-flow-statement".format(ticker)
    response = requests.get(url, verify=False)
    parser = html.fromstring(response.content)

    # Rest of the parse function remains the same

    return {
        'fcf': fcfs_equity,
        'op_fcfs': op_fcfs,
        'capexs': capexs,
        'dbt': dbt,
        'ni': net_income,
        'revenues': revenues,
        'nd': net_debt,
        'res': res,
        'ge': ge,
        'yr': 5,
        'dr': 10,
        'pr': 2.5,
        'shares': shares,
        'eps': eps,
        'mp': market_price
    }

def dcf(data):
    # Rest of the dcf function remains the same
    # You can remove Streamlit-specific warnings or visualizations

def reverse_dcf(data):
    pass

def graham(data):
    if data['eps'] > 0:
        expected_value = round(data['eps'] * (8.5 + 2 * (data['ge'])), 2)
        
        try:
            ge_priced_in = round((data['mp'] / data['eps'] - 8.5) / 2, 2)
        except:
            ge_priced_in = "N/A"

        print("Expected value based on growth rate: {}".format(expected_value))
        print("Growth rate priced in for next 7-10 years: {}\n".format(ge_priced_in))
    else:
        print("Not applicable since EPS is negative.")

if __name__ == "__main__":
    ticker = "AAPL"  # Replace with the desired ticker symbol

    data = parse(ticker)

    # Modify data dictionary as needed (e.g., change growth rate, discount rate, etc.)
    data['ge'] = 5.0  # Example: Set a fixed growth rate of 5%

    fv = dcf(data)

    print("=" * 80)
    print("Fair Value (DCF) Calculation")
    print("=" * 80)
    print("Ticker: ", ticker)
    print("Discount Rate: ", data['dr'], "%")
    print("Growth Estimate: ", data['ge'], "%")
    print("Fair Value: ", fv)

    print("=" * 80)
    print("Graham Style Valuation")
    print("=" * 80)
    graham(data)
