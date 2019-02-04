import os

# Set the correct R environment
os.environ['R_HOME'] = r'C:\ProgramData\Anaconda3\envs\BBAC_missing_values\Lib\R'
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
import numpy as np

# Set automatic numpy to R array conversion
rpy2.robjects.numpy2ri.activate()

# Other R functionality
r_source = robjects.r['source']
r_setseed = robjects.r['set.seed']

class BBAC():
    '''A missing value imputation using the BBAC alghorithm by Banjeree et al,
    using the previsouly created R script from <instert github>


    Args:
        n_cltr_r(int): Number of row clusters. .
        n_cltr_c(int): Number of column clusters. .
        ToDo Add all args.
        '''

    def __init__(self, Z, n_cltr_r, n_cltr_c, distance='d', source =r"D:\g_drive\Gima\Thesis\Github\R_bbac\bbac.R", missing_value=0):
        # initial variables
        self.Z = Z
        self.n_cltr_r = n_cltr_r
        self.n_cltr_c = n_cltr_c
        self.source=source
        self.missing_value = missing_value
        self.distance = distance

    def get_missing(self):
        '''Returns the indices of  missing values in matrix Z'''
        itemindex = np.argwhere(self.Z == self.missing_value)
        self.missing_indices = itemindex

    def create_coclustering(self):
        '''Returns the row, column and co-clusters'''
        # Set the correct source and seed
        r_source(self.source)
        r_setseed(1)

        # Retrieve BBAC function from R
        bbac = robjects.r['bbac']

        # Create co-clustering
        co_clustering = bbac(self.Z, k=self.n_cltr_r, l=self.n_cltr_c, distance=self.distance, scheme=6)

        # Set row and column clusters
        self.row_c = co_clustering[0]
        self.col_c = co_clustering[1]

        # Set co_clusters
        co_c = np.zeros((self.n_cltr_r, self.n_cltr_c))
        # ToDo define co-clusters as indices
        self.co_c = co_c

    def calculate_averages(self):
        '''Returns the averages for prediction'''
        # Add row and column averages
        self.row_avg = self.Z.mean(1)
        self.col_avg = self.Z.mean(0)

        # Add row and column cluster averages
        # ToDo add row_cl_avg
        self.row_cl_avg = None
        # ToDo add col_cl_avg
        self.col_cl_avg = None

        # Add co-cluster averages
        # ToDo add column cluster avrages
        self.co_cl_avg = None

    def predict(self):
        '''Predicts the missing values and returns the new array'''
        for index in self.missing_indices:
            # estimation
            # estimation = average of co-cluster + (row mean - row cluster mean) + (column mean - column cluster mean)
            estimation = self.co_cl_avg + (self.row_avg - self.row_cl_avg) + (self.col_avg - self.col_cl_avg)
            print(index)
            # Set index to estimation


