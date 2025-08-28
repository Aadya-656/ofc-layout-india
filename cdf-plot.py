import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv("ofc-density.csv")


density = data['Density'].values


plt.hist(density, bins=30, density=True, cumulative=True, histtype='step', color='blue')
plt.xlabel('Density')
plt.ylabel('CDF')
plt.title('CDF of Density (Histogram Approximation)')
plt.grid(True)
plt.show()
