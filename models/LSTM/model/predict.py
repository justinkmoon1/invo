#LSTM with window method
import numpy
import matplotlib.pyplot as plt
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import torch
from model import StockPredictionLSTM

def create_dataset(dataset, look_back=7):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-7):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back + 7, 0])
    return numpy.array(dataX), numpy.array(dataY)


def inference(ticker):
    result = {"Ticker":[], "Prediction": []}
    DATA_PATH = f'models/LSTM/data/training/{ticker}.csv'
#convert an array of values into a dataset matrix
#load the dataset
    dataframe = read_csv(DATA_PATH, usecols=[1], engine='python')
    dataset = dataframe.values
    dataset = dataset.astype('float32')
#normalize the dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)
#split into train and test sets
    train_size = len(dataset) - 98
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
    look_back = 90 #window-method (t-2,t-1,t,y)
    testX, testY = create_dataset(test, look_back)
#reshape input to be [samples, time steps, features]
    testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

    for j in range(10):
        model = StockPredictionLSTM(90)
        model = torch.load(f"models/LSTM/res_quarter/{ticker}/{ticker}{j}.pth")
        testPredict = model.predict(testX)
        testPredict = scaler.inverse_transform(testPredict)
        result["Ticker"].append(ticker)
        result["Prediction"].append(testPredict[-1])

    return result
        
    
    