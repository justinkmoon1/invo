
# train and evaluate a multilayer perceptron neural network on the housing regression dataset
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import yfinance as yf
# load dataset
#df = pd.read_excel("models/LSTM/data/raw/Stock List.xlsx")
lst = ["SBSP3.SA"]
wrong_tickers = []
final_dict = {"Ticker": [], "RMSE_train": [], "RMSE": [] }
original_df = pd.read_excel("models/LSTM/data/final/final_quarter_wRMSE.xlsx")
def find_CI (ticker):
    try:
        t = yf.Ticker(ticker)
        df = pd.read_excel(f"models/LSTM/data/result_quarter/{ticker}_results.xlsx")
        RMSE_tr = df["RMSE_Train"]
        RMSE_te = df["RMSE"]
        RMSE_tr = np.asarray(RMSE_tr)
        RMSE_te = np.asarray(RMSE_te)
#        results = df["Prediction"]
        summed_lst = []
#        for v in results.values:
#            num = float(v[1:-1])
#            summed_lst.append(num)

        summed_lst = np.asarray(summed_lst)
        interval = RMSE_te
#        lower, upper = summed_lst.mean() - interval, summed_lst.mean() + interval
        final_dict["Ticker"].append(ticker)
#        final_dict["Lower"].append(lower)
#        final_dict["Predicted"].append(summed_lst.mean())
#        final_dict["Upper"].append(upper)
        final_dict["RMSE_train"].append(RMSE_tr.mean())
        final_dict["RMSE"].append(RMSE_te.mean())
        final_dict["Increase"].append((summed_lst.mean() - yf.download([t]).iloc[-1]['Close']) / yf.download([t]).iloc[-1]['Close'])
    except:
        wrong_tickers.append(ticker)


for l in lst:
    find_CI(l)

dataframe = pd.DataFrame.from_dict(final_dict)
final_df = pd.concat([original_df, dataframe], ignore_index = True)
final_df.to_excel("models/LSTM/data/final/final_quarter.xlsx")
