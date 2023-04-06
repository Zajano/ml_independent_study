# Author: Zack Jaffe-Notier
# Date: 4/13/2020
# Description: testing scatter plot

# Import plotting modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from itertools import chain

# import data
bgg_data = pd.read_csv('game_data.csv', encoding='latin-1', converters={'mechanics': eval, 'categories': eval})
sns.set()

# number of each type of game
mech_counts = pd.Series(list(chain.from_iterable(bgg_data.mechanics))).value_counts()
cat_counts = pd.Series(list(chain.from_iterable(bgg_data.categories))).value_counts()

# manipulate figure size
sns.set(rc={'figure.figsize':(16,8)})

# check data
# print(bgg_data.columns)
# print(bgg_data.head())
# print(bgg_data.dtypes)


# filter to recent years
bgg_1989 = bgg_data[bgg_data["year"] > 1989]

# convert years to strings
bgg_1989.year = bgg_1989.year.astype(str)

sns.lineplot(x='year', y='avg_rating', data=bgg_1989)
# sns.scatterplot(x='year', y='avg_rating', data=bgg2, x_jitter=.3, hue='year')
sns.stripplot(x='year', y='avg_rating', data=bgg_1989, jitter=.3)

# for i in range(2011, 2019):
plt.show()
#
# sns.set(rc={'figure.figsize':(8,8)})
#
#  ## FILTER BY MECHANICS DESIRED!!
mask = bgg_data.mechanics.apply(lambda row: 'Trading' in row)
trading_games = bgg_data[mask]
trading_games['mechanics'] = 'Trading'

print(trading_games['mechanics'])
#
# mask = bgg2.mechanics.apply(lambda row: 'Variable Player Powers' in row)
# variable_games = bgg2[mask]
#
#
# sns.scatterplot(x='year', y='avg_rating',data=trading_games)
# sns.scatterplot(x='year', y='avg_rating',data=variable_games)
# plt.show()