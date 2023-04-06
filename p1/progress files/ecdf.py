# Author: Zack Jaffe-Notier
# Date: 4/15/2020
# Description: Empirical Cumulative Distribution Function (for percentiles)

import numpy as np

def ecdf_1D(data):
    """Compute ECDF for a one-dimensional array of measurements."""
    # Number of data points: n
    n = len(data)

    # x-data for the ECDF: x
    x = np.sort(data)

    # y-data for the ECDF: y
    y = np.arange(1, len(x)+1) / n

    return x, y