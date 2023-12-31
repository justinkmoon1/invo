import yfinance as yf
import pandas as pd
from final_data_query import get_data
from predict import inference
from training import training
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import torch
from model import StockPredictionLSTM
import datetime

#df = pd.read_excel("models/LSTM/data/raw/Stock List.xlsx")
#lst = df["Ticker"].tolist()

year = 2010

def create_dataset(dataset, look_back=7):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back + 1, 0])
    return numpy.array(dataX), numpy.array(dataY)


def inference(ticker, t):
    result = {"Ticker":[], "Prediction": []}
    DATA_PATH = f'models/LSTM/data/daily_training/{ticker}.csv'
#convert an array of values into a dataset matrix
#load the dataset
    dataframe = pd.read_csv(DATA_PATH, usecols=[4], engine='python')
    dataset = dataframe.values
    dataset = dataset.astype('float32')
#normalize the dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)
#split into train and test sets
    train_size = len(dataset) - 100
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
    look_back = 90 #window-method (t-2,t-1,t,y)
    testX, testY = create_dataset(test, look_back)
#reshape input to be [samples, time steps, features]
    testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

    for j in range(1):
        model = StockPredictionLSTM(90)
        model = torch.load(f"models/LSTM/res_backtest_{year}/{ticker}/{ticker}.pth")
        testPredict = model.predict(testX)
        testPredict = scaler.inverse_transform(testPredict)
        print(testPredict)
        result["Ticker"].append(ticker)
        result["Prediction"].append(testPredict[-1])
    prediction = numpy.asarray(result["Prediction"]).mean()
    return prediction



lst = lst = ["KO", "WFC", "AXP", "MSFT", "JNJ", "SNY"]
daily_rmse = {"AAL": 1.09, "APAM": 2.03, "BBSEY": 0.23, "BEN": 1.18, "CYD": 0.48, "DAL": 2.37, "GILD": 2.61, "GMAB": 2.09, "GM": 2.67, "HMC": 0.81, "LAZ": 1.56, "PCAR": 3.36, "SEIC": 2.33, "PAVE": 1.19, "INDA" : 1.31, "SMH": 8.25, "VGT": 16.18, "PCG": 0.63, "PSX": 5.21, "SBSP3.SA": 2.35}
weekly_rmse = {"GM": 4.07, "HMC": 1.36, "AAL": 1.67, "PCAR": 4.35, "CYD": 0.78, "DAL": 3.36, "GMAB": 3.3, "GILD": 3.35, "SEIC": 2.89, "APAM": 2.84 , "BEN": 1.72, "BBSEY": 0.37, "PAVE": 1.37, "INDA": 1.95, "SMH": 10.99, "VGT": 22.65, "PCG": 0.69, "PSX": 5.35, "SBSP3.SA": 3.4}
quarter_rmse = {"GM": 9.6, "HMC": 3.2, "AAL": 4.55, "PCAR": 7.63, "CYD": 1.62, "DAL": 7.09, "GILD": 10.15, "GMAB": 7.02, "SEIC": 5.62, "APAM": 5.12, "BEN": 3.6, "BBSEY": 0.83, "PAVE": 3.16, "INDA": 6.28, "SMH": 52.46, "VGT": 122.44, "PCG": 0.66, "PSX": 5.15, "SBSP3.SA": 3.38}
complete_results = {"Ticker": [], "day_low": [], "day_predict" : [], "day_high": [], "week_low": [], "week_predict" : [], "week_high": [], "quarter_low": [], "quarter_predict" : [], "quarter_high": [], "daily_increase": [], "weekly_increase": [], "quarter_increase": []}
complete_result = {"Ticker": [], 'quarter_increase': []}
for l in lst:
    ticker = yf.Ticker(l)
    previousClose = yf.download([l], start=2011-12-31).iloc[0]['Close']
    complete_result["Ticker"].append(l)
    #res_daily = inference(l, "daily")
    #complete_result["day_low"].append(res_daily - daily_rmse[l])
    #complete_result["day_predict"].append(res_daily)
    #complete_result["day_high"].append(res_daily + daily_rmse[l])
    #complete_result["daily_increase"].append((res_daily - previousClose) / previousClose)
    #res_weekly = inference(l, "weekly")
    #complete_result["week_low"].append(res_weekly - weekly_rmse[l])
    #complete_result["week_predict"].append(res_weekly)
    #complete_result["week_high"].append(res_weekly + weekly_rmse[l])
    #complete_result["weekly_increase"].append((res_weekly - previousClose) / previousClose)

    res_quarter = inference(l, "quarter")
    #complete_result["quarter_low"].append(res_quarter - quarter_rmse[l])
    #complete_result["quarter_predict"].append(res_quarter)
    #complete_result["quarter_high"].append(res_quarter + quarter_rmse[l])
    complete_result["quarter_increase"].append((res_quarter - previousClose) / previousClose)
    print(complete_result)

dataframe = pd.DataFrame.from_dict(complete_result)
dataframe.to_excel("models/LSTM/data/predictions/" + datetime.datetime.now().strftime('%Y-%m-%d') + ".xlsx")