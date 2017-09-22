# -*- coding: utf-8 -*-

__author__ = "Daniel Hannah"
__email__ = "dansserioubusisness@gmail.com"

from flask import Flask, render_template, request
from database_tools import OutlierCountDBReader
# from anomaly_tools import KMeansAnomalyDetector, HDBAnomalyDetector
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


@app.route('/charts_internal', methods=['POST', 'GET'])
def fraudhacker_output():
    # Get provider and specialty choice from user selections on input.
    state = request.form.get('geo_select')
    specialty = request.form.get('provider_select')

    odb = OutlierCountDBReader(YAML_CONFIG, [state], [specialty])
    w_n_df = odb.d_f.head(20)
    npis = w_n_df['npi'].values
    last_names = w_n_df['lastname'].values
    o_cts = list(w_n_df['outlier_count'].values)

    labels = [(l_n + " (" + npi + ")") for l_n, npi in zip(last_names, npis)]

    return render_template("charts_internal.html", labels=labels, cts=o_cts, state=state, specialty=specialty)


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
