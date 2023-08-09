import pandas as pd
df = pd.read_csv("models/LSTM_Sample1/data/stock_data_s1.csv")
df_drop_row = df.dropna(axis=0)
df_drop_row.to_csv("models/LSTM_Sample1/data/stock_data_s1_modified.csv")
