# Set the correct R environment
import os
os.environ['R_HOME'] = r'C:\ProgramData\Anaconda3\envs\BBAC_missing_values\Lib\R'
# Import R functionality
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
# import regular functions
import numpy as np

# Import and apply source function from R
r_source = robjects.r['source']
r_source(r"D:\g_drive\Gima\Thesis\Github\R_bbac\bbac.R")

# Set seed
r_setseed = robjects.r['set.seed']
r_setseed(1)

# Generate synthethic data
list_of_list = [[2.5, 3.0, 3.2, 5.1, 5.3],
                [7.5, 7.8, 7.6, 5.1, 5.2],
                [2.5, 3.2, 3.0, 5.0, 5.5],
                [5.2, 5.2, 5.0, 3.1, 3.2],
                [5.3, 5.0, 5.4, 3.2, 3.1],
                [5.0, 5.2, 5.1, 3.3, 3.1],
                [7.8, 8.0, 8.0, 5.2, 5.3]]

# Set automatic numpy conversion
rpy2.robjects.numpy2ri.activate()

# Create array from lists
Z = np.array(list_of_list)
nr, nc = np.shape(Z)
r_Z = robjects.r.matrix(Z, nrow=nr, ncol=nc)
robjects.r.assign('Z', r_Z)

# Create Z missing
Z[2,0]=0
nr, nc = np.shape(Z)
r_Z_missing = robjects.r.matrix(Z, nrow=nr, ncol=nc)
robjects.r.assign('Z', r_Z_missing)

# Get BBAC
r_bbac = robjects.r['bbac']

# Run with different distance measurements and W matrices
inf_theoretic_d = r_bbac(r_Z, k=3, l=2, distance='d', scheme=6)
inf_theoretic_W = r_bbac(r_Z_missing, k=3, l=2, distance='d', scheme=6)

print(inf_theoretic_d[0])
print(inf_theoretic_W[0])