# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import hdbscan
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.cluster import KMeans

__author__ = "Daniel Hannah"
__email__ = "dan@danhannah.site"

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
        data_list = [self.d_f[reg_var].values for reg_var in
                     self.regression_vars]
        if self.use_response_var:
            data_list.append(self.d_f[self.response_var].values)
        return np.matrix(list(zip(*data_list)))

    def scale_data(self, method=StandardScaler()):
        """Scales the data prior to analysis.

        Args:
            method: Scaling method to use, defaults to StandardScaler.

        Returns:
            A scaled numpy data matrix.

        """
        return method.fit_transform(self.data_matrix)

    def get_most_frequent(self, threshold):
        """Gets the most frequent offenders ranked by number of outliers.

        This method finds all of the outliers associated with a particular
        provider (i.e. NPI) and returns a dataframe of the top N providers.
        If the outlier metric hasn't been defined, an error will be thrown.

        Note:
            Threshold is typically defined *very* differently for different
            outlier detection schemes; check the inherited methods in those
            subclasses for more information.

        Args:
            threshold (float): What cutoff defines an outlier?

        Returns:
            A Pandas dataframe which is a subset of the larger dataframe.

        """
        if 'outlier_metric' not in self.d_f.columns:
            print("Outlier metrics must be calculated prior to grouping.")
            return
        else:
            suspect_dict = {}
            for row_tuple in self.d_f.iterrows():
                row = row_tuple[1]
                if row["npi"] not in suspect_dict:
                    suspect_dict[row["npi"]] = {}
                    suspect_dict[row["npi"]]["last_name"] = \
                        row["nppes_provider_last_org_name"]
                    suspect_dict[row["npi"]]["address"] = {
                        "street1": row['nppes_provider_street1'],
                        "street2": row['nppes_provider_street2'],
                        "zip": row['nppes_provider_zip'],
                        "state": row['nppes_provider_state']
                    }
                    suspect_dict[row["npi"]]["outlier_count"] = 0
                if row["outlier_metric"] > threshold:
                    suspect_dict[row["npi"]]["outlier_count"] += 1
            suspect_d_f = pd.DataFrame.from_dict(suspect_dict, orient='index')
            worst = suspect_d_f.sort_values(by="outlier_count", ascending=False)

            return worst

    @staticmethod
    def get_n_most_frequent(sorted_df, top_n_return=20):
        """Gets the n most frequent offenders from a sorted list of them.

        Args:
            sorted_df (DataFrame): A sorted Pandas DataFrame
            top_n_return (int): How many of the list do we want?

        Returns:
            A DataFrame containing the n most outlier-y providers.

        """
        return sorted_df.head(top_n_return)


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
        self.assign_clusters(kmeans_result)
        transformed = kmeans_result.transform(self.scaled_dm)

        # Iterate through dataframe rows and get appropriate distances.
        self.assign_clusters(kmeans_result)
        self.d_f['outlier_metric'] = [transformed[:, label][idx]
                                      for idx, label in
                                      enumerate(self.d_f['cluster_label'])]
        return

    def get_most_frequent(self, threshold=None, top_n_return=10, percent=10):
        """Inherited from parent class, exists here to define threshold.

        Args:
            threshold (float): Cutoff metric to determine if outlier.
            top_n_return (int): How many offenders do we want a list of?
            percent (float): Top <percent> % of distant points are outliers.

        Returns:
            A Pandas dataframe which is a subset of the larger dataframe.

        """
        all_centroid_distances = self.d_f['outlier_metric'].values
        threshold = np.percentile(all_centroid_distances, 100 - percent)
        return super().get_most_frequent(threshold)


class HDBAnomalyDetector(AnomalyDetector):
    """Class for outlier detection based on HDBScan clustering.

    This anomaly detector is based on a better clustering algorithm (HDBSCAN)
    but otherwise functions similarly to the K-means clustering data - we are
    clustering the data and looking for outliers.

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

    def cluster_data(self, min_size):
        """Perform clustering on the data using the HDBSCAN algorithm.

        Args:
            min_size (int): Minimum cluster size.

        Returns:
            A fit from an HDBSCAN clusterer.

        """
        return hdbscan.HDBSCAN(min_cluster_size=min_size).fit(self.scaled_dm)

    def get_outlier_scores(self, min_size):
        """Gets the outlier score associated with each data point.

        Rather than returning anything, this method populates the
        "outlier_metric" column of the object's internal dataframe.

        Args:
            min_size (int): Minimum cluster size to the feed to the algorihtm.

        Returns:
            None

        """
        clustered_data = self.cluster_data(min_size=min_size)
        outlier_scores = clustered_data.outlier_scores_
        self.d_f['outlier_metric'] = [outlier_scores[idx] for idx, pt in
                                      enumerate(self.d_f['npi'])]
        return

    def get_most_frequent(self, threshold=None, percent=2):
        """Gets the most frequent

        Args:
            threshold (float): Cutoff in metric to define an outlier.
            percent (int): Top N% of outliers are returned.

        Returns:
            A Pandas DataFrame which is a subset of the larger dataframe.

        """
        all_outlier_scores = self.d_f['outlier_metric'].values
        threshold = np.percentile(all_outlier_scores, 100-percent)
        return super().get_most_frequent(threshold)


