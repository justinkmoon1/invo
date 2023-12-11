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
import os

year = 2010

def training(ticker):
    result = {'Ticker': [], 'RMSE_Test' : [], 'RMSE_Train' : []}
    DATA_PATH = f'models/LSTM/data/daily_training/{ticker}.csv'
    # DATA_PATH = f'models/LSTM/data/test_data.csv'
    #convert an array of values into a dataset matrix
    def create_dataset(dataset, look_back=90):
        dataX, dataY = [], []
        for i in range(len(dataset)-look_back-90):
            a = dataset[i:(i+look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back + 90, 0])
        return numpy.array(dataX), numpy.array(dataY)
    #fix random seed for reproducibility
    #numpy.random.seed(7)
    for i in range(1):
        #load the dataset
        dataframe = read_csv(DATA_PATH, usecols=[4], engine='python')
        dataset = dataframe.values
        dataset = dataset.astype('float32')
        #normalize the dataset
        scaler = MinMaxScaler(feature_range=(0, 1))
        dataset = scaler.fit_transform(dataset)
        
        #split into train and test sets
        train_size = int(len(dataset) * 0.8)
        test_size = len(dataset) - train_size
        train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
        '''*************************************'''
        #reshape into X=t and Y=t+1
        look_back = 90 #window-method (t-2,t-1,t,y)
        trainX, trainY = create_dataset(train, look_back)
        testX, testY = create_dataset(test, look_back)
        # print(testX, testY)
        #reshape input to be [samples, time steps, features]
        trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
        print(testX)
        '''**************************************'''
        #create and fit the LSTM network
        model = StockPredictionLSTM(90)
        model.train(trainX, trainY, 10, 28)
        #make predictions
        trainPredict = model.predict(trainX)
        testPredict = model.predict(testX)
        #invert predictions
        trainPredict = scaler.inverse_transform(trainPredict)
        trainY = scaler.inverse_transform([trainY])
        testPredict = scaler.inverse_transform(testPredict)
        testY = scaler.inverse_transform([testY])
        #calculate root mean squared error
        trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
        print('Train Score: %.2f RMSE' % (trainScore))
        testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
        print('Test Score: %.2f RMSE' % (testScore))
        
        result['Ticker'].append(ticker)
        result['RMSE_Test'].append(testScore)
        result['RMSE_Train'].append(trainScore)
        try:
            os.mkdir(f"models/LSTM/res_backtest_{year}")
        except:
            pass

        try:
            os.mkdir(f"models/LSTM/res_backtest_{year}/{str(ticker)}")
        except:
            pass

        torch.save(model, f"models/LSTM/res_backtest_{year}/{str(ticker)}/{str(ticker)}.pth")
    return result


