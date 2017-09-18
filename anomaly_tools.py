# -*- coding: utf-8 -*-

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

__author__ = "Daniel Hannah"
__email__ = "dansseriousbusiness@gmail.com"

"""Tools and classes for anomaly detection in insurance claims data sets.

Right now I've implemented K-means clustering, but there are plans to implement
other outlier detection methods based on:
    - Gaussian Mixture Models
    - Decision trees
    - Multivariate regression
This class will also eventually include probabilistic schemes for estimating
how likely it is that a particular point is an outlier.

"""


class AnomalyDetector:
    """General anomaly detector class; not for direct use.

    This is a super class to bundle the representation of an anomaly
    detector so that we can easily pass features and labels onto the more
    specific detector implementations.

    Attributes:
        regression_vars (list): List of labels for regression variables.
        response_var (str): Label for the response variable.
        d_f (DataFrame): A Pandas dataframe containing queried data.
        use_response_var (Boolean): Use response variable in clustering?
        data_matrix (Matrix): A Numpy matrix object of value data.

    Note that the feature labels in regression and response variable attributes
    must match a column label in the DataFrame, or an error will be thrown.

    """

    def __init__(self, regression_vars, response_var, d_f, use_response_var):
        """Initialization for the AnomalyDetector.

        Args:
            regression_vars (list): A list of strings for regression variables.
            response_var (str): Label for the response variable for regression.
            d_f (DataFrame): A Pandas DataFrame containing queried data.
            use_response_var (Boolean): Use response variable in clustering?

        """
        self.regression_vars = regression_vars
        self.response_var = response_var
        self.d_f = d_f
        self.use_response_var = use_response_var
        self.data_matrix = self.build_data_matrix()

    def build_data_matrix(self):
        """Creates a matrix of variable data for further use in analysis.

        Returns:
            A Numpy matrix.

        """
        data_list = [self.d_f[reg_var].values() for reg_var in
                     self.regression_vars]
        if self.use_response_var:
            data_list.append(self.d_f[self.response_var].values())
        return np.matrix(list(zip(*data_list)))

    def scale_data(self, method=StandardScaler()):
        """Scales the data prior to analysis.

        Args:
            method: Scaling method to use, defaults to StandardScaler.

        Returns:
            A scaled numpy data matrix.

        """
        return method.fit_transform(self.data_matrix)


class KMeansAnomalyDetector(AnomalyDetector):
    """Anomaly detection scheme based on k-means clustering.

    This type of anomaly detector searches for outliers based on the distance
    to a cluster center in k-means clustering.

    Attributes:
        regression_vars (list): List of labels for regression variables.
        response_var (str): Label for the response variable.
        d_f (DataFrame): A Pandas dataframe containing queried data.
        use_response_var (Boolean): Use response variable in clustering?
        data_matrix (Matrix): A Numpy matrix object of value data.
        scaled_dm (Matrix): A scaled Numpy matrix of the data.

    """

    def __init__(self, regression_vars, response_var, d_f, use_response_var):
        """Initialization for KMeansAnomalyDetector.

        Args:
            regression_vars (list): A list of strings for regression variables.
            response_var (str): Label for the response variable for regression.
            d_f (DataFrame): A Pandas DataFrame containing queried data.
            use_response_var (Boolean): Use response variable in clustering?

        """
        super().__init__(regression_vars, response_var, d_f,
                         use_response_var)
        self.scaled_dm = self.scale_data()

    def cluster_data(self, num_clusters, method='k-means++'):
        """Performs k-means cluster on the associated data frame.

        Note: Right now the user must specify the number of clusters, but one
        could implement an automatic detection scheme and pass the result of it
        to num_clusters.

        Args:
            num_clusters (int): Number of clusters to use.
            method (str): The centroid initialization method to use.

        Returns:
            A k-means clustered data set (KMeans)

        """
        return KMeans(init=method, n_clusters=num_clusters).fit(self.scaled_dm)

    def assign_clusters(self, clustered_data):
        """Adds a "cluster membership" label to the dataframe.

        Args:
            clustered_data (KMeans): The clustered data.

        Returns:
            None

        """
        self.d_f['cluster_label'] = clustered_data.labels_
        return

    def compute_centroid_distances(self, num_clusters):
        """Computes the distances of each data point to its member centroid.

        For now, this method creates a new column in the data frame rather than
        returning a list of distances.

        Args:
            num_clusters (int): Number of clusters to use.

        Returns:
            None.

        """
        # Perform k-means clustering and get the cluster-distance space data.
        kmeans_result = self.cluster_data(num_clusters)
        transformed = kmeans_result.transform(self.scaled_dm)

        # Iterate through dataframe rows and get appropriate distances.
        self.assign_clusters(kmeans_result)
        self.d_f['centroid_distance'] = [transformed[:, label][idx]
                                         for idx, label in
                                         enumerate(self.d_f['cluster_label'])]
        return
