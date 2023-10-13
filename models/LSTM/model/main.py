import yfinance as yf
import pandas as pd
from final_data_query import get_data
from predict import inference
from training import training

df = pd.read_excel("models/LSTM/data/raw/Stock List.xlsx")
lst = df["Ticker"].tolist()
wrong_tickers = []

cur = 0
for l in lst:
    try:
        total_results = {"Ticker": [], "RMSE_Test": [], "RMSE_Train": [], "Prediction": []}
        print(l)
        cur += 1
        print(wrong_tickers)
        print(cur)
        #ticker = yf.Ticker(l)
        get_data(l)
        training_dict = training(l)
        for t in training_dict["Ticker"]:
            total_results["Ticker"].append(t)
        for tr in training_dict["RMSE_Train"]:
            total_results["RMSE_Train"].append(tr)
        for te in training_dict["RMSE_Test"]:
            total_results["RMSE_Test"].append(te)
        prediction_dict= inference(l)
        for pr in prediction_dict["Prediction"]:
            total_results["Prediction"].append(pr)

        df = pd.DataFrame.from_dict(total_results)
        df.to_excel(f"models/LSTM/data/result_quarter/{l}_results.xlsx")
    except:
        wrong_tickers.append(l)


#df = pd.DataFrame.from_dict(total_results)

print(wrong_tickers)
        #find_CI(ticker)
