# Source code for FraudHacker
This directory contains the source code for FraudHacker. An overall explanation of the workflow can be found in the [parent directory for this repository](https://github.com/dchannah/fraudhacker); here I focus on the content of each file.

* `anomaly_tools.py`: Implementation of tools to label outliers in the CMS.gov dataset. The classes herein operate on a Pandas DataFrame and designed for modularity - all anomaly detectors inherit certain useful functions from a parent super class, and the idea of an "outlier metric" is deliberately intended to be flexible (for example, for K-means clustering, the outlier metric is distance to the cluster centroid, while it is a GLOSH score for HDBSCAN).

* `config.yaml`: Configuration for the PostgreSQL database reader; includes database name, user name (removed), and password (removed). A list of features to extract (to keep the DataFrame size manageable) is also included this file. This lets the user change which features are selected without needing to go into the Python source code.

* `database_tools.py`: Various classes for interacting with PostgreSQL databases. A parent super class is again used, but different subclasses are created for interacting with the raw data PostgreSQL database and the outlier counts PostgreSQL database.

* `fh_config.py`: A collection of lengthy but necessary variables for the Flask app. These variables are stored in their own file to cut down on messiness in the Flask app.

* `flask_app_java.py`: The Flask app which actually collects calculated and ranked outlier count data for each physician and renders it to a webpage for user viewing. It also ties together the rest of the pages on [www.fraudhacker.site](http://www.fraudhacker.site).

* `plotting_tools.py`: A collection of plotting tools to render plots on the webpage. Most of these plotting tools are now deprecated since I switched from Bokeh to ChartJS for my plot rendering, but as at least one of these routines is still used in the Flask app, this file remains (and I left the Bokeh functions in just in case I ever want to quickly switch back to Bokeh for rendering figures).

The `static` and `templates` folders contain the web files for the Flask app.
