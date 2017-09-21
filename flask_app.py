# -*- coding: utf-8 -*-

__author__ = "Daniel Hannah"
__email__ = "dansserioubusisness@gmail.com"

from flask import Flask, render_template, request
from database_tools import PandasDBReader
from anomaly_tools import KMeansAnomalyDetector, HDBAnomalyDetector
from plotting_tools import generate_bar_plot
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

    # Testing the "worst offenders" output.
    worst = kmd.get_most_frequent()
    worst_10 = kmd.get_n_most_frequent(worst)

    """
    hdb = HDBAnomalyDetector(regression_vars, response_var, pdb_reader.d_f,
                             use_response_var=True)
    hdb.get_outlier_scores(min_size=15)
    
    worst = hdb.get_most_frequent()
    worst_10 = hdb.get_n_most_frequent(worst)
    """


    # Make a bar plot of these suspects.
    fig_div, fig_script = generate_bar_plot(worst_10,
                                            plt_title="Suspicious Providers")

    return render_template("output.html", fig_script=fig_script,
                           fig_div=fig_div,
                           dataframe=worst_10.to_html(classes='table'))


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
