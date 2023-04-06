# Author: Zack Jaffe-Notier
# Date: 4/13/2020
# Description: testing scatter plot

# Import plotting modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pcc import pcc

#import data
iris_data = pd.read_csv('Iris.csv')
sns.set()

#plot box and whiskers of petals
sns.boxplot(x = 'Species', y = 'PetalWidthCm', data = iris_data)

# keep plot within bounds
plt.margins(0.02)

#legend placement and labels
# plt.legend(('setosa', 'versicolor', 'virginica'), loc = 'lower right')

# Show graphs
plt.show()

#check covariances
print("Setosa: ", pcc(setosa_petal_lengths,setosa_petal_widths))
print("Versicolor: ", pcc(versicolor_petal_lengths,versicolor_petal_widths))
print("Virginica: ", pcc(virginica_petal_lengths,virginica_petal_widths))