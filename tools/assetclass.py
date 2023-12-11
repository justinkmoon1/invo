import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv("data\PieChart_assetclass_284365.csv")

labels = data['AssetClass'].values

values = data['Value']
print(labels)
plt.pie(values, labels= labels, autopct='%1.1f%%')
plt.show()