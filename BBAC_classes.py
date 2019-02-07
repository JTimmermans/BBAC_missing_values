from rpy2_setup import *
import numpy as np
# ignore dividing by zero or np.nan
np.seterr(divide='ignore', invalid='ignore')



class BBAC():
    '''A missing value imputation using the BBAC alghorithm by Banjeree et al,
    using the previsouly created R script from <instert github>

    Args:
        Z(array):      A m x n numpy array. .
        n_cltr_r(int): Number of row clusters. .
        n_cltr_c(int): Number of column clusters. .
        distance(str): Distance measure, either 'e' for Euclidean, or 'd' for Bregman I-divergence. .
        scheme(int):   Scheme 1 to 6 from Banjeree et al.,
        source(str):   Path to the original bbac.R file, available from https://github.com/fnyanez/bbac . .
        '''

    def __init__(self, Z, n_cltr_r, n_cltr_c, distance='d', source=r"D:\g_drive\Gima\Thesis\Github\R_bbac\bbac.R"):
        # initial variables
        self.Z = Z
        self.n_cltr_r = n_cltr_r
        self.n_cltr_c = n_cltr_c
        self.source=source
        self.distance = distance
        self.n_row, self.n_col = np.shape(self.Z)[0], np.shape(self.Z)[1]

    def get_missing(self, missing_value=0):
        '''Returns the indices of  missing values in matrix Z

        Args:
            missing value(type):  Symbol (use other word) to note the missing values (e.g., np.nan, 0, or -99999). .
            '''

        itemindex = np.argwhere(self.Z == missing_value)
        missing_indices = itemindex
        return missing_value, missing_indices

    def coclustering(self):
        '''Returns the row, column and co-clusters

        Out:
            row_cltr(array): Row clustering array. .
            col_cltr(array): Column clustering array. .
            co_cltr(array):  Co-cluster array. .
            '''

        # Set the correct source and seed
        r_source(self.source)
        r_setseed(1)

        # Retrieve BBAC function from R
        bbac = robjects.r['bbac']

        # Retrieve missing value information
        self.missing_value, self.missing_indices = self.get_missing()

        # Create W
        # ToDo USE A W MATRIX, R part errors
        W = np.ones((self.n_row, self.n_col), np.int)
        for i in self.missing_indices:
            W[i[0], i[1]] = 0
        self.W = numpy_to_r(W)

        # Create co-clustering
        co_clustering = bbac(self.Z, k=self.n_cltr_r, l=self.n_cltr_c, distance=self.distance, scheme=2)

        # Set row and column clusters
        self.row_cltr = np.array(co_clustering[0])
        self.col_cltr = np.array(co_clustering[1])

    def calculate_averages(self):
        '''Returns the averages for prediction

        Out:
            row_avg(array):     Array 1 x m array with the averages per row. .
            col_avgarray):      Array 1 x m array with the averages per column. .
            row_cltr_avgarray): Array 1 x m array with the averages per row cluster. .
            col_cltr_avgarray): Array 1 x m array with the averages per column cluster. .
            co_cltr_avgarray):  Array 1 x m array with the averages per co-cluster. .
            '''

        # Add row and column averages
        row_avg = self.Z.mean(1)
        col_avg = self.Z.mean(0)

        # Initialize empty average arrays:
        row_cltr_avg = np.zeros(self.n_row, np.double)
        col_cltr_avg = np.zeros(self.n_col, np.double)
        co_cltr_avg = np.zeros((self.n_cltr_r, self.n_cltr_c), np.double)

        # Initialize empty count arrays
        row_cltr_count = np.zeros(self.n_cltr_r, np.double)
        col_cltr_count = np.zeros(self.n_cltr_c, np.double)
        co_cltr_count = np.zeros((self.n_cltr_r, self.n_cltr_c), np.double)

        # Initialize empty sum arrays
        row_cltr_sum = np.zeros(self.n_cltr_r, np.double)
        col_cltr_sum = np.zeros(self.n_cltr_c, np.double)
        co_cltr_sum = np.zeros((self.n_cltr_r, self.n_cltr_c), np.double)

        # Compute sums, counts, and averages for row clusters
        for cluster in range(0, self.n_cltr_r):
            for row in range(0, self.n_row):
                if self.row_cltr[row, cluster] == 1.0:
                    # Increment count by self.W matrix, if one of n values in the row is missing, count is 1-1/n
                    row_cltr_count[cluster] += self.W[row, :].mean()
                    row_cltr_sum[cluster] += self.Z[row].mean()
        row_cltr_avg = np.divide(row_cltr_sum, row_cltr_count)

        # Compute sums, counts, and averages for column clusters
        for cluster in range(0, self.n_cltr_c):
            for col in range(0, self.n_col):
                if self.col_cltr[col, cluster] == 1.0:
                    # Increment count by self.W matrix, if one of n values in the column is missing, count is 1-1/n
                    col_cltr_count[cluster] += self.W[:, col].mean()
                    col_cltr_sum[cluster] += self.Z[:,col].mean()
        col_cltr_avg = np.divide(col_cltr_sum, col_cltr_count)

        # Compute sums, counts, and averages for co-cluster
        for rc in range(0, self.n_cltr_r):
            for row in range(0, self.n_row):
                if self.row_cltr[row, rc] == 1.0:
                    for cc in range(0, self.n_cltr_c):
                        for col in range(0, self.n_col):
                            if self.col_cltr[col, cc] == 1.0:
                                # Increment count by self.W matrix, if value is missing, W matrix = 0, count+= 0
                                co_cltr_count[rc, cc] += self.W[row, col]
                                co_cltr_sum[rc, cc] += self.Z[row, col]
        co_cltr_avg = np.divide(co_cltr_sum, co_cltr_count)

        return row_avg, col_avg, row_cltr_avg, col_cltr_avg, co_cltr_avg

    def predict(self):
        '''Predicts the missing values and returns an imputed array

            Out:
                Z_imputed(array): m x n numpy array with imputed missing values. .
        '''

        # Retrieve clustering averages
        self.row_avg, self.col_avg, self.row_cltr_avg, self.col_cltr_avg, self.co_cltr_avg = self.calculate_averages()

        # Create a copy of the array to store imputed values
        self.Z_imputed = self.Z


        for index in self.missing_indices:
            # Determine corresponding row cluster index
            for rc in range(0, self.n_cltr_r):
                if self.row_cltr[index[0], rc] == 1.0:
                    break

            # Determine corresponding column cluster index
            for cc in range(0, self.n_cltr_c):
                if self.col_cltr[index[1], cc] == 1.0:
                    break

            # Determine corresponding co-cluster index
            for rcc in range(0, self.n_cltr_r):
                if self.row_cltr[index[0], rc] == 1.0:
                    for ccc in range(0, self.n_cltr_c):
                        if self.col_cltr[index[1], cc] == 1.0:
                            break

            # Estimate value for missing index
            # estimation = average of co-cluster + (row mean - row cluster mean) + (column mean - column cluster mean)
            self.Z[index[0], index[1]] = self.co_cltr_avg[rcc,ccc] + (self.row_avg[index[0]] - self.row_cltr_avg[rc]) + (self.col_avg[index[1]] - self.col_cltr_avg[cc])



