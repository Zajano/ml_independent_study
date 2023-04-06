# Author: Zack Jaffe-Notier
# Date: 4/29/2020
# Description: calculates Interquartile Range for a pandas column

def iqr(column):
    """returns range of middle 50% of given data set"""
    return column.quantile(0.75) - column.quantile(0.25)