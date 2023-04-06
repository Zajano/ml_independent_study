# Author: Zack Jaffe-Notier
# Date: 4/13/2020
# Description: testing scatter plot

# Import plotting modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# import data
iris_data = pd.read_csv('Iris.csv')
sns.set()

#check data columns
#print(iris_data.head())

#################### MAKING 1-D PETAL LENGTH/WIDTH ARRAYS #####################

#make tuples list of species and lengths
petal_lengths = iris_data['PetalLengthCm']
petal_widths = iris_data['PetalWidthCm']
iris_species = iris_data['Species']
species_petal_lengths = [(petal_lengths[i], iris_species[i]) for i in range(0, len(iris_data))]
species_petal_widths = [(petal_widths[i], iris_species[i]) for i in range(0, len(iris_data))]

# split lengths into 1-D lists
setosa_petal_lengths = []
versicolor_petal_lengths = []
virginica_petal_lengths = []
for petal in species_petal_lengths:
    if petal[1] == 'Iris-setosa':
        setosa_petal_lengths.append(petal[0])
    if petal[1] == 'Iris-versicolor':
        versicolor_petal_lengths.append(petal[0])
    if petal[1] == 'Iris-virginica':
        virginica_petal_lengths.append(petal[0])

# split widths into 1-D lists
setosa_petal_widths = []
versicolor_petal_widths = []
virginica_petal_widths = []
for petal in species_petal_widths:
    if petal[1] == 'Iris-setosa':
        setosa_petal_widths.append(petal[0])
    if petal[1] == 'Iris-versicolor':
        versicolor_petal_widths.append(petal[0])
    if petal[1] == 'Iris-virginica':
        virginica_petal_widths.append(petal[0])

#plot scatters of petals
plt.plot(setosa_petal_lengths, setosa_petal_widths, marker = '.', linestyle = 'none')
plt.plot(versicolor_petal_lengths, versicolor_petal_widths, marker = 'x', linestyle = 'none')
plt.plot(virginica_petal_lengths, virginica_petal_widths, marker = 'd', linestyle = 'none')
plt.xlabel('Petal Length (cm)')
plt.ylabel('Petal Width (cm)')

# keep plot within bounds
plt.margins(0.02)

# Show graphs
plt.show()