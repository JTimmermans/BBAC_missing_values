from BBAC_classes import *
from rpy2_setup import *
import os
import timeit

def basic_test():
    # Generate synthethic data
    list_of_list = [[2.5, 3.0, 3.2, 5.1, 5.3],
                    [2.5, 3.2, 3.0, 5.0, 5.5],
                    [5.2, 5.2, 0.0, 3.1, 3.2],
                    [0.0, 5.0, 5.0, 3.2, 3.1],
                    [5.0, 5.2, 5.1, 0, 3.1],
                    [7.8, 8.0, 8.0, 5.2, 5.3],
                    [7.5, 7.8, 7.6, 5.1, 5.2]]

    # Create array from lists and convert to rpy2-array
    array = np.array(list_of_list)
    Z = numpy_to_r(array)

    # Use the prediction algorithm
    test = BBAC(Z, n_cltr_r=3, n_cltr_c=2, distance='e')
    test.coclustering()
    test.predict()
    test.visualize(path=r'D:\g_drive\Gima\Thesis\Media', outname='test', xlabel='Columns', ylabel='Rows')
    # print(test.col_cltr, '\n\n', test.row_cltr)
    print(test.Z_imputed)


def larger_array_test():
    #do something
    pass

basic_test()
larger_array_test()