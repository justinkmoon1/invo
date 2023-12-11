import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv("data\PieChart_sectors_284365.csv")

fig = plt.figure(figsize=(0,0))
fig.set_facecolor('cyan')

fig.patch.set_alpha(0.3)
ax = fig.add_subplot()
labels = data['Sector'].values

values = data['pct']
ax.pie(values, labels= labels, autopct='%1.1f%%')

print(labels)

plt.pie(values, labels= labels, autopct='%1.1f%%')



plt.show()