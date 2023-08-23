from fredapi import Fred
import pandas as pd
fred = Fred(api_key="03f777d7451a764390719c59f94775b1")
data = fred.get_series('pi')
print(data.head())
print(dir(Fred.get_series))