# Author: Zack Jaffe-Notier
# Date: 4/13/2020
# Description: testing plotting ECDFs for percentiles


# Import plotting modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from ecdf import ecdf_1D

#import data
iris_data = pd.read_csv('Iris.csv')
sns.set()

#make tuples list of species and lengths
sepal_lengths = iris_data['SepalLengthCm']
iris_species = iris_data['Species']
species_sepal_lengths = [(sepal_lengths[i], iris_species[i]) for i in range(0, len(iris_data))]


# split into 1-D lists
setosa_sepal_lengths = []
versicolor_sepal_lengths = []
virginica_sepal_lengths = []
for petal in species_sepal_lengths:
    if petal[1] == 'Iris-setosa':
        setosa_sepal_lengths.append(petal[0])
    if petal[1] == 'Iris-versicolor':
        versicolor_sepal_lengths.append(petal[0])
    if petal[1] == 'Iris-virginica':
        virginica_sepal_lengths.append(petal[0])

# use ECDF function to get ready to plot
setosa_x, setosa_y = ecdf_1D(setosa_sepal_lengths)
versi_x, versi_y = ecdf_1D(versicolor_sepal_lengths)
virgin_x, virgin_y = ecdf_1D(virginica_sepal_lengths)

#ECDF plots for perfcentiles of all 3 species
# plt.plot(setosa_x, setosa_y, marker = '.', linestyle = 'none')
# plt.plot(versi_x, versi_y, marker = '.', linestyle = 'none')
# plt.plot(virgin_x, virgin_y, marker = '.', linestyle = 'none')
# plt.xlabel('Sepal Length (cm)')

# keep plot within bounds
plt.margins(0.02)

# combined histograms of data
plt.hist([setosa_sepal_lengths, versicolor_sepal_lengths, virginica_sepal_lengths], bins = 10)
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Number of samples')
plt.legend(('setosa', 'versicolor', 'virginica'), loc = 'upper right')

# Show graphs
plt.show()