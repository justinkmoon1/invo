from lxml import html
import requests
import pandas as pd
import yfinance
import json
import argparse
import streamlit as st
import numpy as np
from collections import OrderedDict

from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

import warnings
warnings.filterwarnings('ignore')

def parse(ticker):
   def parse(ticker):
    url = "https://stockanalysis.com/stocks/{}/financials/cash-flow-statement".format(ticker)
    response = requests.get(url, verify=False)
    parser = html.fromstring(response.content)
    # Cash Flows

    op_fcfs = parser.xpath('//table[contains(@id,"financial-table")]//tr[td/span/text()[contains(., "Operating Cash Flow")]]')[0].xpath('.//td/span/text()')[1:]
    capexs = parser.xpath('//table[contains(@id,"financial-table")]//tr[td/span/text()[contains(., "Capital Expenditures")]]')[0].xpath('.//td/span/text()')[1:]
    dbt = parser.xpath('//table[contains(@id,"financial-table")]//tr[td/span/text()[contains(., "Debt Issued / Paid")]]')[0].xpath('.//td/span/text()')[1:]
    net_income = parser.xpath('//table[contains(@id,"financial-table")]//tr[td/span/text()[contains(., "Net Income")]]')[0].xpath('.//td/span/text()')[1:]

    op_fcfs = [float(x.replace(',', '')) for x in op_fcfs]
    capexs = [float(x.replace(',', '')) for x in capexs]
    dbt = [float(x.replace(',', '')) for x in dbt]
    net_income = [float(x.replace(',', '')) for x in net_income]

    fcfs_equity = list(np.array(op_fcfs) + np.array(capexs)) # + np.array(dbt) (difficult to predict when company will borrow money)
    
    # Revenues

    url = "https://stockanalysis.com/stocks/{}/financials".format(ticker)
    response = requests.get(url, verify=False)
    parser = html.fromstring(response.content)

    revenues = parser.xpath('//table[contains(@id,"financial-table")]//tr[td/span/text()[contains(., "Revenue")]]')[0].xpath('.//td/span/text()')[1:]
    revenues = [float(x.replace(',', '')) for x in revenues]

    # Debt

    url = "https://finance.yahoo.com/quote/{}/analysis?p={}".format(ticker, ticker)
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'})
    parser = html.fromstring(response.content)

    net_debt = parser.xpath('//table[contains(@id,"financial-table")]//tr[td/span/text()[contains(., "Net Cash / Debt")]]')[0].xpath('.//td/span/text()')[1:]
    net_debt = [float(x.replace(',', '')) for x in net_debt][0]

    url = "https://finance.yahoo.com/quote/{}/analysis?p={}".format(ticker, ticker)
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'})
    parser = html.fromstring(response.content)
    tables = parser.xpath('//table')

    for t in tables:
        if t.xpath("thead//tr//th/span/text()")[0] == 'Revenue Estimate':
            vals = t.xpath("tbody//tr//td/span/text()")
            ind = vals.index("Low Estimate")
            res = [vals[ind - 2], vals[ind - 1]]
            
            for i in range(len(res)):
                if 'B' in res[i]:
                    res[i] = float(res[i].replace('B', ''))  * 1000
                elif 'M'  in res[i]:
                    res[i] = float(res[i].replace('M', ''))
        
            break

    ge = tables[-1].xpath("tbody//tr")

    for row in ge:
        label = row.xpath("td/span/text()")[0]

        if 'Next 5 Years' in label:
            try:
                ge = float(row.xpath("td/text()")[0].replace('%', ''))
            except:
                ge = []
            break

    url = "https://stockanalysis.com/stocks/{}/".format(ticker)
    response = requests.get(url, verify=False)
    parser = html.fromstring(response.content)
    shares = parser.xpath('//div[@class="order-1 flex flex-row gap-4"]//table//tbody//tr[td/text()[contains(., "Shares Out")]]')

    shares = shares[0].xpath('td/text()')[1]
    factor = 1000 if 'B' in shares else 1 
    shares = float(shares.replace('B', '').replace('M', '')) * factor

    url = "https://stockanalysis.com/stocks/{}/financials/".format(ticker)
    response = requests.get(url, verify=False)
    parser = html.fromstring(response.content)
    eps = parser.xpath('//table[contains(@id,"financial-table")]//tr[td/span/text()[contains(., "EPS (Diluted)")]]')[0].xpath('.//td/span/text()')[1:]
    eps = float(eps[0].replace(",", ""))

    try:
        market_price = float(parser.xpath('//div[@class="price-ext"]/text()')[0].replace('$', '').replace(',', ''))
    except:
        market_price = round(yfinance.Ticker(ticker).history().tail(1).Close.iloc[0], 2)

    return {'fcf': fcfs_equity, 'op_fcfs': op_fcfs, 'capexs': capexs, 'dbt': dbt, 'ni': net_income, 'revenues': revenues, 'nd': net_debt, 'res': res, 'ge': ge, 'yr': 5, 'dr': 10, 'pr': 2.5, 'shares': shares, 'eps': eps, 'mp': market_price}


url = "https://stockanalysis.com/stocks/{}/financials/cash-flow-statement".format("AAPL")
response = requests.get(url, verify=False)
parser = html.fromstring(response.content)
    # Cash Flows

op_fcfs = parser.xpath('//table[contains(@id,"financial-table")]//tr[td/span/text()[contains(., "Operating Cash Flow")]]')[0].xpath('.//td/span/text()')[1:]
capexs = parser.xpath('//table[contains(@id,"financial-table")]//tr[td/span/text()[contains(., "Capital Expenditures")]]')[0].xpath('.//td/span/text()')[1:]
dbt = parser.xpath('//table[contains(@id,"financial-table")]//tr[td/span/text()[contains(., "Debt Issued / Paid")]]')[0].xpath('.//td/span/text()')[1:]
net_income = parser.xpath('//table[contains(@id,"financial-table")]//tr[td/span/text()[contains(., "Net Income")]]')[0].xpath('.//td/span/text()')[1:]

op_fcfs = [float(x.replace(',', '')) for x in op_fcfs]
capexs = [float(x.replace(',', '')) for x in capexs]
dbt = [float(x.replace(',', '')) for x in dbt]
net_income = [float(x.replace(',', '')) for x in net_income]

fcfs_equity = list(np.array(op_fcfs) + np.array(capexs)) # + np.array(dbt) (difficult to predict when company will borrow money)
print(fcfs_equity)