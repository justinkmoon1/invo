
# train and evaluate a multilayer perceptron neural network on the housing regression dataset
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
# load dataset
DATA_PATH = ""
dataframe = read_csv(DATA_PATH)
values = dataframe.values
# split into input and output values
X, y = values[:, :-1], values[:,-1]
# split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.67, random_state=1)
# scale input data
scaler = MinMaxScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
# define neural network model
features = X_train.shape[1]
model = Sequential()
model.add(Dense(20, kernel_initializer='he_normal', activation='relu', input_dim=features))
model.add(Dense(5, kernel_initializer='he_normal', activation='relu'))
model.add(Dense(1))
# compile the model and specify loss and optimizer
opt = Adam(learning_rate=0.01, beta_1=0.85, beta_2=0.999)
model.compile(optimizer=opt, loss='mse')
# fit the model on the training dataset
model.fit(X_train, y_train, verbose=2, epochs=300, batch_size=16)
# make predictions on the test set
yhat = model.predict(X_test, verbose=0)
# calculate the average error in the predictions
mae = mean_absolute_error(y_test, yhat)
print('MAE: %.3f' % mae)