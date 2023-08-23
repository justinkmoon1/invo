import pandas_datareader.data as web
import pandas as pd
import datetime

import pyfred

start = datetime.datetime(2021, 1, 1)
end = datetime.datetime.now()

# PyFRED 라이브러리를 사용하여 FRED 데이터 가져오기
gdp = pyfred.get_series('GDP', start, end)
unrate = pyfred.get_series('UNRATE', start, end)

# Pandas-datareader 라이브러리를 사용하여 S&P 500 지수 가져오기
sp500 = web.DataReader('^GSPC', 'yahoo', start, end)['Adj Close']

# 데이터프레임으로 변환
df = pd.concat([gdp, unrate, sp500], axis=1, sort=False)

# 컬럼명 변경
df.columns = ['GDP', 'Unemployment Rate', 'S&P 500']

# 데이터프레임 출력
print(df.head())