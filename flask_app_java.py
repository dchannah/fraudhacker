# -*- coding: utf-8 -*-

__author__ = "Daniel Hannah"
__email__ = "dan@danhannah.site"

from flask import Flask, render_template, request
from database_tools import OutlierCountDBReader
from plotting_tools import get_bar_colors
from fh_config import regional_options, specialty_options, fraudulent_npis

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
    npis = list(w_n_df['npi'].values)
    last_names = w_n_df['lastname'].values
    o_cts = list(w_n_df['outlier_count'].values)

    labels = [(l_n + " (" + npi + ")") for l_n, npi in zip(last_names, npis)]
    colorlist = get_bar_colors(npis)

    return render_template("charts_internal.html", labels=labels, cts=o_cts,
                           state=state, specialty=specialty,
                           colorlist=colorlist)


@app.route('/slides')
def show_slides():
    return render_template("slides.html")

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
