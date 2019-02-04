from BBAC_classes import *
from BBAC_classes import BBAC
import os


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




test = BBAC(Z, n_cltr_r=3, n_cltr_c=2)
test.get_missing()
test.create_coclustering()
test.calculate_averages()

print(test.row_avg, '\n', test.col_avg)
