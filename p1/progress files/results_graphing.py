# Author: Zack Jaffe-Notier
# Date: 5/5/2020
# Description: plotting 475 homework results

# Import plotting modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#import data
results = pd.read_csv('results.csv')
sns.set()

# figure size
sns.set(rc={'figure.figsize':(16,8)})

#line sizes
sns.set(rc={'lines.linewidth': 2})

#check data frame
print(results)

#plot box and whiskers of petals
sns.lineplot(data=results["Deer"], linewidth = 4)
sns.lineplot(data=results["Height(in)"], linewidth = 3)
sns.lineplot(data=results["Temp(C)"])
sns.lineplot(data=results["Precip(in)"])

# keep plot within bounds
plt.margins(0.02)

# Show graphs
plt.xlabel('Months Passed')
plt.legend(('Deer', 'Height(in)', 'Temp(C)', 'Precipitation(in)'), prop={"size":20}, frameon=False, loc = 'upper left', ncol = 4)
plt.savefig('output.png')

# do this last!
plt.show()
