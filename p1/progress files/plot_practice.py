# Author: Zack Jaffe-Notier
# Date: 4/13/2020
# Description: Testing data imports and simple displays

# Import plotting modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set default Seaborn style for better graphics
sns.set()

# import data and set column titles
# columns named in file
# columns = ['Id','SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm','Species']
iris_data = pd.read_csv('Iris.csv')
# print(len(iris_data))
# print(iris_data.head())

# Plot histogram of petal lengths
# plt.hist(iris_data['SepalLengthCm'])
# plt.xlabel('Petal Length (cm)')
# plt.ylabel('Number of Samples')

# Plot histogram of sepal widths
plt.hist(iris_data['SepalLengthCm'], bins = 10)
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Number of Samples')

#plot bee swarm of petal lengths
sns.swarmplot(x='Species',y='PetalLengthCm', data=iris_data)

# plt.hist([setosa_sepal_lengths, versicolor_sepal_lengths, virginica_sepal_lengths], bins = 10)
# plt.legend(('setosa', 'versicolor', 'virginica'), loc = 'lower right')


# Show graphs
plt.show()