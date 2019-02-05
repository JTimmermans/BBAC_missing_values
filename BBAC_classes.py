import os
import numpy as np
# Set the correct R environment
os.environ['R_HOME'] = r'C:\ProgramData\Anaconda3\envs\BBAC_missing_values\Lib\R'
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
# Set automatic numpy to R array conversion
rpy2.robjects.numpy2ri.activate()
# Other R functionality
r_source = robjects.r['source']
r_setseed = robjects.r['set.seed']

class BBAC():
    '''A missing value imputation using the BBAC alghorithm by Banjeree et al,
    using the previsouly created R script from <instert github>

    Args:
        Z(array):      A m x n numpy array. .
        n_cltr_r(int): Number of row clusters. .
        n_cltr_c(int): Number of column clusters. .
        distance(str): Distance measure, either 'e' for Euclidean, or 'd' for Bregman I-divergence. .
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

        self.missing_value = missing_value
        itemindex = np.argwhere(self.Z == self.missing_value)
        self.missing_indices = itemindex

    def create_coclustering(self):
        '''Returns the row, column and co-clusters

        Out:
            row_cltr(array): Row clustering array. .
            col_cltr(array): Column clustering array. .
            co_cltr(array):  Co-clustering indices. .
            '''

        # Set the correct source and seed
        r_source(self.source)
        r_setseed(1)

        # Retrieve BBAC function from R
        bbac = robjects.r['bbac']

        # Create co-clustering
        co_clustering = bbac(self.Z, k=self.n_cltr_r, l=self.n_cltr_c, distance=self.distance, scheme=6)

        # Set row and column clusters
        self.row_cltr = np.array(co_clustering[0])
        self.col_cltr = np.array(co_clustering[1])

        # Set co_clusters
        co_cltr = np.zeros((self.n_cltr_r, self.n_cltr_c))
        # ToDo define co-clusters as indices
        self.co_cltr = np.array(co_cltr)

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
        self.row_avg = self.Z.mean(1)
        self.col_avg = self.Z.mean(0)

        # Initialize empty average arrays:
        row_cltr_avg = np.zeros(self.n_row, np.double)
        col_cltr_avg = np.zeros(self.n_col, np.double)
        co_cltr_avg = np.zeros((self.n_cltr_r, self.n_cltr_c), np.double)

        # Initialize empty count arrays
        row_cltr_count = np.zeros(self.n_cltr_r, np.int)
        col_cltr_count = np.zeros(self.n_cltr_c, np.int)
        co_cltr_count = np.zeros((self.n_cltr_r, self.n_cltr_c), np.int)

        # Initialize empty sum arrays
        row_cltr_sum = np.zeros(self.n_cltr_r, np.double)
        col_cltr_sum = np.zeros(self.n_cltr_c, np.double)
        co_cltr_sum = np.zeros((self.n_cltr_r, self.n_cltr_c), np.double)

        # Compute sums, counts, and averages for rows clusters
        for i in range(0, self.n_cltr_r):
            for row in range(0, self.n_row):
                if self.row_cltr[row, i] == 1.0:
                    row_cltr_count[i] += 1
                    print(self.Z[row])
                    print(self.Z[row].mean())
                    row_cltr_sum[i] += self.Z[row].mean()
        row_cltr_avg = np.divide(row_cltr_sum, row_cltr_count)

        # Compute sums, counts, and averages for rows clusters


        # ToDo add column clusters averages
        self.col_cltr_avg = None

        # Add co-cluster averages
        n_co_cltr = self.n_cltr_r * self.n_cltr_c
        # ToDo add co-cluster averages
        self.co_cltr_avg = None

    def predict(self):
        '''Predicts the missing values and returns the new array

            Out:
                Z(array): m x n numpy array with imputed missing values. .
        '''

        for index in self.missing_indices:
            # estimation = average of co-cluster + (row mean - row cluster mean) + (column mean - column cluster mean)
            self.Z[index] = self.co_cltr_avg + (self.row_avg - self.row_cltr_avg) + (self.col_avg - self.col_cltr_avg)
            print(index)


