import pandas as pd
import os
import numpy as np

complete_dict = {"Ticker": [], "RMSE": []}
for file in os.listdir("models/LSTM/data/result_daily"):
    df = pd.read_excel("models/LSTM/data/result_daily" + "/" + file)
    rmse_lst = np.asarray(df["RMSE_Test"].values)
    complete_dict["Ticker"].append(df["Ticker"].iloc[0])
    complete_dict["RMSE"].append(rmse_lst.mean())

dataframe = pd.DataFrame.from_dict(complete_dict)
dataframe.to_excel("models/LSTM/data/final/final_daily_wRMSE.xlsx")
