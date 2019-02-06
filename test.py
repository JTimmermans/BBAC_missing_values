from BBAC_classes import *
from rpy2_setup import *
import os
import timeit

# Generate synthethic data
list_of_list = [[2.5, 3.0, 3.2, 5.1, 5.3],
                [2.5, 3.2, 3.0, 5.0, 5.5],
                [5.2, 5.2, 0, 3.1, 3.2],
                [5.3, 5.0, 5.0, 3.2, 3.1],
                [5.0, 5.2, 5.1, 3.3, 3.1],
                [7.8, 8.0, 8.0, 5.2, 5.3],
                [7.5, 7.8, 7.6, 5.1, 5.2]]


# Set automatic numpy conversion

# Create array from lists and convert to rpy2-array
array = np.array(list_of_list)
Z = numpy_to_r(array)

# Actual tests
test = BBAC(Z, n_cltr_r=3, n_cltr_c=2, distance='e')
test.coclustering()
test.predict()
print(test.Z_imputed)
