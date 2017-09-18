# -*- coding: utf-8 -*-

__author__ = "Daniel Hannah"
__email__ = "dansserioubusisness@gmail.com"

from flask import Flask, render_template, request
from database_tools import PandasDBReader
from anomaly_tools import KMeansAnomalyDetector
from fh_config import regional_options, specialty_options, regression_vars,\
    response_var

# Global variables
YAML_CONFIG = "./config.yaml"


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def fraudhacker_input():
    return render_template("index.html", geo_data=regional_options,
                           provider_data=specialty_options)


@app.route('/output', methods=['POST', 'GET'])
def fraudhacker_output():
    # Get provider and specialty choice from user selections on input.
    state = request.form.get('geo_select')
    specialty = request.form.get('provider_select')

    # Build a Pandas database reader based on those choices (and config).
    pdb_reader = PandasDBReader(YAML_CONFIG, [state], [specialty])

    # Generate an anomaly detector using the queried data and find outliers.
    kmd = KMeansAnomalyDetector(regression_vars, response_var, pdb_reader.d_f,
                                use_response_var=True)
    kmd.compute_centroid_distances(num_clusters=8)

    # As a temporary check, get the worst 10 offenders.
    worst_10 = kmd.d_f.sort_values(by=['outlier_metric'],
                                   ascending=False).head(10)

    return render_template("output.html",
                           dataframe=worst_10.to_html(classes='table'))
