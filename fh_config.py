# -*- coding: utf-8 -*-

__author__ = "Daniel Hannah"
__email__ = "dansserioubusisness@gmail.com"

"""A configuration file for the Flask app.

This is not the most elegant way to do this but because there are various types
of objects I want to import from an external file, a direct python file is
easiest for now.

"""

regional_options = [
    {'state': 'MA'},
    {'state': 'FL'}
]

specialty_options = [
    {'type': 'Thoracic Surgery'},
    {'type': 'Ophthalmology'},
    {'type': 'Cardiology'}
]

regression_vars = [
    "line_srvc_cnt",
    "bene_unique_cnt",
    "bene_day_srvc_cnt",
    "average_medicare_allowed_amt",
    "average_submitted_chrg_amt"
]

response_var = "average_medicare_payment_amt"