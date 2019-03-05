from rpy2_setup import bbac, numpy_to_r
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()
# ignore dividing by zero or np.nan
np.seterr(divide='ignore', invalid='ignore')
from scipy import nanmean



class BBAC():
    """A missing value imputation using the BBAC alghorithm by Banjeree et al,
    using the previsouly created R script from <instert github>


    :param: Z(array):      A m x n Rpy2 numpy array.
    :param: n_cltr_r(int): Number of row clusters.
    :param: n_cltr_c(int): Number of column clusters.
    :param: distance(str): Distance measure, either 'e' for Euclidean, or 'd' for Bregman I-divergence.
    :param: scheme(int):   Scheme 1 to 6 from Banjeree et al.,.
    :param: source(str):   Path to the original bbac.R file, available at https://github.com/fnyanez/bbac .
        """

    def __init__(self, Z, n_cltr_r, n_cltr_c, scheme=2, distance='d'):
        # initial variables
        self.Z = Z
        self.n_cltr_r = n_cltr_r
        self.n_cltr_c = n_cltr_c
        self.distance = distance
        self.n_row, self.n_col = np.shape(self.Z)[0], np.shape(self.Z)[1]
        self.scheme = scheme

    def get_missing(self, missing_value):
        """Returns the indices of  missing values in matrix Z

        :param: missing value(type):  Symbol (use other word) to note the missing values (e.g., np.nan, 0, or -99999).
        :return: missing_value(str || numeric): Symbol (use other word) to note the missing values (e.g., np.nan, 0, or -99999).
        :return: missing_indices(array): Array containing the indices of missing values in self.Z.
            """

        itemindex = np.argwhere(self.Z == 0)
        # itemindex = np.argwhere(np.isnan(self.Z))
        missing_indices = itemindex
        return missing_value, missing_indices

    def coclustering(self):
        """Returns the row, column and co-clusters.

        :return: row_cltr(array): Row clustering array.
        :return: col_cltr(array): Column clustering array.
        :return: co_cltr(array):  Co-cluster array.
            """

        # Retrieve missing value information
        self.missing_value, self.missing_indices = self.get_missing(missing_value=np.nan)

        # Create W matrix
        W = np.ones((self.n_row, self.n_col), np.int)

        for i in self.missing_indices:
            W[i[0], i[1]] = 0
        self.W = numpy_to_r(W)

        # Create co-clustering
        co_clustering = bbac(self.Z, W = self.W,  k=self.n_cltr_r, l=self.n_cltr_c, nruns=10, distance=self.distance, scheme=self.scheme)

        # Set row and column clusters
        self.row_cltr = np.array(co_clustering[0])
        self.col_cltr = np.array(co_clustering[1])

    def calculate_averages(self):
        """Returns the clustering averages for prediction.

        :return: co_cltr_avg(array):  Array 1 x m array with the averages per co-cluster.
            """

        # Initialize empty average arrays:
        co_cltr_avg = np.zeros((self.n_cltr_r, self.n_cltr_c), np.double)

        # Initialize empty count arrays
        co_cltr_count = np.zeros((self.n_cltr_r, self.n_cltr_c), np.double)

        # Initialize empty sum arrays
        co_cltr_sum = np.zeros((self.n_cltr_r, self.n_cltr_c), np.double)

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

        return co_cltr_avg

    def re_order_matrix(self):
        """Returns a re-ordered array of self.Z input.

        :return: self.Z_rd(array): Re-ordered input array.
        :return: self.W_rd(array): Re-ordered W-array.
        """

        # Create row and column ordering
        row_indices = [np.where(r==1)[0][0] for r in self.row_cltr]
        row_ordering = np.argsort(row_indices)
        col_indices = [np.where(r==1)[0][0] for r in self.col_cltr]
        col_ordering = np.argsort(col_indices)

        # Create re-orderd Z and W arrays
        Z_rd = self.Z[:,col_ordering]
        Z_rd = self.Z[row_ordering,:]
        W_rd = self.W[:,col_ordering]
        W_rd = self.W[row_ordering,:]

        return Z_rd, W_rd

    def predict(self):
        """Predicts the missing values and returns an imputed array.

        :return: Z_imputed(array): m x n numpy array with imputed missing values.
        """

        # Retrieve clustering averages
        self.co_cltr_avg = self.calculate_averages()

        # Create a copy of the array to store imputed values
        self.Z_imputed = np.copy(self.Z)

        # Compute the index of row columns clusters
        multiplier = np.arange(1, self.n_cltr_r + 1)
        row_indices = np.sum((multiplier * self.row_cltr), axis=1)-1

        # Compute the index of column clusters
        multiplier = np.arange(1, self.n_cltr_c + 1)
        col_indices = np.sum((multiplier * self.col_cltr), axis=1) - 1

        for index in self.missing_indices:
            # Set indices of missing index
            rc = int(row_indices[index[0]])
            cc = int(col_indices[index[1]])

            # Estimate value for missing index
            self.Z_imputed[index[0], index[1]] = self.co_cltr_avg[rc,cc]

    def visualize(self, path, outname, xlabel, ylabel):
        """
        Creates .png images of the original array Z and the imputed array Z_imputed as heatmaps. Missing values are displayed in grey.

        :param: path(str): Path to store the resulting figures.
        :param: outname(str): Name of the resulting figures.
        :param: xlabel(str): Name of the x-axis label.
        :param: ylabel(str): Name pf the y-axis label.
        :return: <>_Z.png(.png): Heatmap of original array. with missing values.
        :return: <>_Z_imputed.png(.png): Heatmap of imputed array.
        :return: <>_Z_re_ordered.png(.png): Heatmap of re-ordered array. with missing values.
        :return: <>_Z_re_ordered_imputed.png(.png): Heatmap of the re-ordered imputed array.
        """

        # Function to plot heatmaps
        def plot_heatmap(array, mask, Z='_Z'):
            # Create and store heatmap of the array with an mask
            ax = sns.heatmap(array, cmap="YlGnBu", mask=mask, vmin=minval)
            ax.set(xlabel=xlabel, ylabel=ylabel)
            fig = ax.get_figure()
            fig.savefig('{}/{}{}.png'.format(path, outname,Z))
            # Clear current figure
            fig.clf()

        # Create an mask to display missing values in orignal array
        mask = 1 - self.W

        # Find minimum values
        minval = np.min(self.W[np.nonzero(self.W)])

        # Plot orignal matrix with missing values
        plot_heatmap(array=self.Z, mask=mask, Z='_Z')

        # Plot imputed matrix
        plot_heatmap(array=self.Z_imputed, mask=None, Z='_Z_imputed')

        # # Retrieve re-ordered W and Z arrays
        # Z_rd, W_rd = self.re_order_matrix()
        #
        # # Create mask for re-orederd array
        # r_mask = 1 - W_rd
        #
        # # Plot re-ordered matrix with missing values
        # plot_heatmap(Z_rd, mask=r_mask, Z='_Z_re_ordered.png')

