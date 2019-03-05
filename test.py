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
    print(test.row_cltr)
    print('')
    print(test.col_cltr)

    # Visualize arrays and print imputed array
    test.visualize(path=r'D:\g_drive\Gima\Thesis\Media', outname='test', xlabel='Columns', ylabel='Rows')
    print(test.Z_imputed)
    print(test.co_cltr_avg)

def larger_array_test():
    import pandas as pd
    df = pd.read_csv(r"D:\g_drive\Gima\Thesis\Data\Regionale_kerncijfers_provincie_basischool\leerlingen_provincie.csv", sep=';', index_col=0)

    array = df.values
    array = array.astype(float)
    original = np.copy(array)
    print(array)

    # Create missing value array
    n_cols, n_rows = np.shape(array)
    for i in range(10):
        row_i = np.random.choice(array.shape[0], (int(n_rows*0.20)))
        col_i = np.random.choice(array.shape[1], (int(n_rows*0.20)))
        for i in range(len(row_i)):
            array[row_i[i], col_i[i]] = np.nan
    Z = numpy_to_r(array)

    # Use the prediction algorithm
    test = BBAC(Z, n_cltr_r=4, n_cltr_c=2, distance='d', scheme=2)
    test.coclustering()
    print(test.row_cltr)
    print(test.col_cltr)
    # test.predict()

    # Visualize arrays and print imputed array
    test.visualize(path=r'D:\g_drive\Gima\Thesis\Media', outname='mexico', xlabel='Columns', ylabel='Rows')
    print('\n\n\n\n')
    # print(test.Z_imputed)
    # print(test.co_cltr_avg)
    # print(test.W)

def bbac_test():
    import pandas as pd
    print('hello')
    df = pd.read_csv(r"D:\numpy_temperature\array_1000.csv", sep = ';', header=None)
    print(df.head())
    print(df.shape)

    array = df.values[:,:500]
    Z = numpy_to_r(array)
    del array
    del df

    # Use the prediction algorithm
    test = BBAC(Z, n_cltr_r=7, n_cltr_c=5, distance='d', scheme=2)
    test.coclustering()
    print(test.row_cltr)
    print(test.col_cltr)


# bbac_test()
basic_test()
# larger_array_test()

# lists=[[0,0,1],
# [1,0,0],
# [0,0,1],
# [0,0,1],
# [0,1,0],
# [1,0,0],
# [1,0,0]]
#
# array = np.array(lists)
# print(array)
# n_cltr = 3
# multiplier = np.arange(1,4)
# print(multiplier)
# a = multiplier * array
# b = (np.sum(a, axis=1)-1)
# print(b)