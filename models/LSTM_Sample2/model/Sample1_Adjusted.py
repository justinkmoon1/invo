import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
#from keras.layers.core import Dense, Activation, Dropout
from Sample1_Adjusted_Model import StockPredictionLSTM
import torch
import time #helper libraries

# file is downloaded from finance.yahoo.com, 1.1.1997-1.1.2017
# training data = 1.1.1997 - 1.1.2007
# test data = 1.1.2007 - 1.1.2017
input_file="models/LSTM_Sample2/data/test_data.csv"

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)

# fix random seed for reproducibility
np.random.seed(5)

# load the dataset
df = read_csv(input_file, header=None, index_col=None, delimiter=',')

# take close price column[5]
all_y = df[4].values

dataset=all_y.reshape(-1, 1)

# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)

# split into train and test sets, 50% test data, 50% training data
#-> 10% test data, 90% training data
train_size = int(len(dataset) * 0.9)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

print(test)
# reshape into X=t and Y=t+1, timestep 240
look_back = 240
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

# reshape input to be [samples, time steps, features]
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

# create and fit the LSTM network, optimizer=adam, 25 neurons, dropout 0.1
model = StockPredictionLSTM(look_back)
# model = Sequential()
# model.add(LSTM(25, input_shape=(1, look_back)))
# model.add(Dropout(0.1))
# model.add(Dense(1))
# model.compile(loss='mse', optimizer='adam')
model.train(trainX, trainY, epochs=100, batch_size=240, verbose=1)
torch.save(model,'models/LSTM_Sample2/res/AAPL.pth')

# make predictions
trainPredict = model.predict(trainX)
print(f"testx: {testX}")
testPredict = model.predict(testX)

# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])

# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore))

# shift train predictions for plotting
trainPredictPlot = np.empty_like(dataset)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict

# shift test predictions for plotting
testPredictPlot = np.empty_like(dataset)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict
testPredictPlot_ratio = testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :]
for i in range(1, len(testPredictPlot_ratio)):
	testPredictPlot_ratio[i] = testPredictPlot_ratio[i] / testPredictPlot_ratio[0]

# plot baseline and predictions
#plt.plot(scaler.inverse_transform(dataset))
#plt.plot(trainPredictPlot)
print('testPrices:')
testPrices=scaler.inverse_transform(dataset[test_size+look_back:])
testPrices_ratio = testPrices
for i in range(1, len(testPrices)):
	testPrices_ratio[i] = testPrices_ratio[i] / testPrices[0]

print('testPredictions:')
print(testPredict)

# export prediction and actual prices

# print(len(list(testPredict.reshape(-1))))
# print(len(list(testPrices.reshape(-1))))
# print(list(testPredict.reshape(-1)))
# print(list(testPrices.reshape(-1))[:len(list(testPredictPlot.reshape(-1)))])
print(len(testPredictPlot_ratio))
print(len(testPrices_ratio))
df = pd.DataFrame(data={"prediction": np.around(list(testPredictPlot_ratio.reshape(-1)), decimals=2), "test_price": np.around(list(testPrices_ratio.reshape(-1))[:len(testPredictPlot_ratio.reshape(-1))], decimals=2)})

#df.to_csv("models/LSTM_Sample2/data/lstm_result_s1.csv", sep=';', index=None)

# plot the actual price, prediction in test data=red line, actual price=blue line
#plt.plot(testPredictPlot)
plt.plot(testPrices_ratio)
plt.plot(testPredictPlot_ratio)
plt.show()