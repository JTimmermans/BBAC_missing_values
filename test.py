from BBAC_classes import *
import os
import timeit
np.set_printoptions(threshold=np.inf)

def basic_test():
    # Generate synthethic data
    list_of_list = [[0.0, 3.0, 3.2, 5.1, 5.3],
                    [2.5, 3.2, 3.0, 5.0, 0.0],
                    [5.0, 5.2, 5.1, 3.2, 3.1],
                    [5.2, 5.2, 0.0, 3.1, 3.2],
                    [0.0, 5.0, 5.0, 3.2, 3.1],
                    [7.8, 8.0, 8.0, 5.2, 5.3],
                    [7.5, 7.8, 7.6, 5.1, 0.0]]

    # Create array from lists and convert to rpy2-array
    array = np.array(list_of_list)
    Z = numpy_to_r(array)

    # Use the prediction algorithm
    test = BBAC(Z, n_cltr_r=3, n_cltr_c=2, distance='d', scheme=2)
    test.coclustering()
    test.predict()

    # Visualize arrays and print imputed array
    test.visualize(path=r'D:\g_drive\Gima\Thesis\Media', outname='test', xlabel='Columns', ylabel='Rows')
    print(test.Z_imputed)
    print(test.co_cltr_avg)


basic_test()


