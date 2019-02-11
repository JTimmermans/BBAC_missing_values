import os
import numpy as np

# Set the correct R environment
os.environ['R_HOME'] = r'C:\ProgramData\Anaconda3\envs\BBAC_missing_values\Lib\R'

# Load R functionalites
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri

# Set automatic numpy to R array conversion
rpy2.robjects.numpy2ri.activate()

# Import BBAC functionality
r_source = robjects.r['source']
r_source(r"R_bbac\bbac.R")
bbac = robjects.r['bbac']

# Other R functionality
r_source = robjects.r['source']
r_setseed = robjects.r['set.seed']
r_setseed(1)

def numpy_to_r(array):
    """Converts a Python numpy array to an array suitable for r2py

    Args:
        array(array):   A m x n numpy array

    Out: array(array):  A m x n array usable in both numpy and rpy2"""
    nr, nc = np.shape(array)
    r_array = robjects.r.matrix(array, nrow=nr, ncol=nc)
    robjects.r.assign('array', r_array)
    return array