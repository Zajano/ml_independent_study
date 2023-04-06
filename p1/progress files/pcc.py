# Author: Zack Jaffe-Notier
# Date: 4/25/2020
# Description: Pearson Correlation Coefficient calculator

import numpy as np

def pcc(a1, a2):
    """compute PCC for two 1-D arrays"""

    #get coefficient matrix from numpy
    pcc_matix = np.corrcoef(a1, a2)

    #only [0,1] and [1, 0] have coefficient values
    return pcc_matix[0, 1]