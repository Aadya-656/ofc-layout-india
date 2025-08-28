import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sorted_urban-rural.csv")

x = df['OFC Density']
y = df['% Rural Households']

plt.scatter(x, y)    
plt.xlabel('OFC Density')
plt.ylabel('% Rural Households')
plt.title('Plot of OFC Density vs % Rural Households')
plt.show()

