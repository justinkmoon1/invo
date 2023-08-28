import numpy as np
import math
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

class StockPredictionLSTM:
    def __init__(self, look_back):
        self.look_back = look_back
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(LSTM(25, input_shape=(1, self.look_back)))
        model.add(Dropout(0.1))
        model.add(Dense(1))
        model.compile(loss='mse', optimizer='adam')
        return model

    def train(self, trainX, trainY, epochs, batch_size, verbose=1):
        self.model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=verbose)

    def predict(self, data):
        return self.model.predict(data)
