import datetime
import pandas as pd

result = ""

df = pd.read_excel("models/LSTM/data/predictions/" + datetime.datetime.now().strftime('%Y-%m-%d') + ".xlsx")
df = df.set_index('Ticker')
for ticker in df.index:
    dincrease = ""
    qincrease = ""
    if df['daily_increase'][ticker] > 0:
        dincrease = f"+{round(df['daily_increase'][ticker] * 100, 1)}%"
    elif df['daily_increase'][ticker] == 0:
        dincrease = '0%'
    else:
        dincrease = f"{round(df['daily_increase'][ticker] * 100, 1)}%"
    
    if df['quarter_increase'][ticker] > 0:
        qincrease = f"+{round(df['quarter_increase'][ticker] * 100, 1)}%"
    elif df['quarter_increase'][ticker] == 0:
        qincrease = '0%'
    else:
        qincrease = f"{round(df['quarter_increase'][ticker] * 100, 1)}%"
    
    result += f"{ticker} : RNN predicts next week's price ${round(df['day_predict'][ticker], 1)} ({dincrease}); next quarter's price ${round(df['quarter_predict'][ticker], 1)} ({qincrease}), ${round(df['quarter_low'][ticker], 1)} bearish, ${round(df['quarter_high'][ticker], 1)} bullish."
    result += '\n'
with open ("models/LSTM/data/predictions/" + datetime.datetime.now().strftime('%Y-%m-%d') + ".txt", "w+") as f:
    f.write(result)