# -*- coding: utf-8 -*-

import yaml
import psycopg2
import pandas as pd

__author__ = "Daniel Hannah"
__email__ = "dan@danhannah.site"

"""Tools for interacting with a PostgreSQL database that stores CMS claim data.

The PandasDBReader class builds a dataframe from the database with a requested
set of features as the columns. Eventually I may include a PandasCSVReader which
populates the same fields so that the Flask app can take CSV input.

"""


class CMSDBReader:
    """General superclass for database readers.

    Attributes:
        configuration (JSON): A YAML-read configuration set.
        connection (psycopg2): An SQL database connection.

    """

    def __init__(self, config_yaml):
        """Initialization for all of the DB Readers.

        Args:
            config_yaml (str): Path to a configuration yaml.

        """
        # Get the DB reader config from a YAML file.
        with open(config_yaml, 'r') as f:
            self.configuration = yaml.load(f)

        # Set up an SQL connection.
        self.connection = psycopg2.connect(
            database=self.configuration['database_name'],
            user=self.configuration['user_name'],
            password=self.configuration['password']
        )

    @staticmethod
    def build_query(need_cols, q_dict, table='cms'):
        """Queries the SQL database for a subset of the data.

        This routine is specifically tailored to query specific data from
        specific regions. Custom query functionality is pending.

        Args:
            need_cols (list): A list of properties we want to query.
            q_dict (dict): A dictionary mapping columns to allowed values.
            table (str): The table to query from in the database.

        Returns:
            A properly-formatted SQL query.

        """
        query_str = "SELECT "
        for idx, col in enumerate(need_cols):
            if idx == len(need_cols) - 1:
                query_str += col
            else:
                query_str += col + ", "
        query_str += " from " + table + " WHERE "
        for cname in q_dict:
            opt_list = str(q_dict[cname]).replace('[', '(').replace(']', ')')
            query_str += cname + " IN " + opt_list + " AND "
        return query_str[:-4]  # Need to remove final AND


class PandasDBReader(CMSDBReader):
    """Class for interacting with the PostgreSQL database containing CMS data.

    Right now this class bundles the "go-between" for the Flask app and the
    database.

    Attributes:
        connection (psycopg2): A SQL database connection.
        d_f (DataFrame): A Pandas data frame.

    """

    def __init__(self, config_yaml, region_list, specialty_list):
        """Initialization for the PandasDBReader.

        Args:
            config_yaml (YAML): A YAML file containing configuration info.
            region_list (list): A list of US states to get info from.
            specialty_list (list): A list of specialties to get info on.

        """
        super().__init__(config_yaml)

        # Build a query from the provided region/specialty lists.
        query_dict = {"provider_type": specialty_list,
                      "nppes_provider_state": region_list}
        query = self.build_query(self.configuration['features'], query_dict)

        # Use the query to create a dataframe from the database.
        self.d_f = pd.read_sql_query(query, self.connection)


class OutlierCountDBReader(CMSDBReader):
    """A database reader class for the outlier counts table (for speed!)

    Attributes:
        connection (psycopg2): A SQL database connection.
        d_f (DataFrame): A Pandas data frame.

    """

    def __init__(self, config_yaml, region_list, specialty_list, metric='hdb_total'):
        """Initialization for the PandasDBReader.

        Args:
            config_yaml (YAML): A YAML file containing configuration info.
            region_list (list): A list of US states to get info from.
            specialty_list (list): A list of specialties to get info on.
            metric (str): Which outlier metric should be pulled?

        """
        super().__init__(config_yaml)

        outlier_cols = ['npi', 'state', 'lastname', 'provider_type',
                        'outlier_count', 'cost', 'outlier_rate']
        table_name = "provider_anomaly_counts_" + metric
        print(table_name)

        # Build a query from the provided region/specialty lists.
        query_dict = {"provider_type": specialty_list,
                      "state": region_list}
        query = self.build_query(outlier_cols, query_dict, table=table_name)
        print("RUNNING QUERY " + query)

        # Use the query to create a dataframe from the database.
        self.d_f = pd.read_sql_query(query, self.connection)
