# -*- coding: utf-8 -*-

__author__ = "Daniel Hannah"
__email__ = "dan@danhannah.site"

"""A configuration file for the Flask app.

This is not the most elegant way to do this but because there are various types
of objects I want to import from an external file, a direct python file is
easiest for now.

"""

regional_options = [
    {'state': 'AL'},
    {'state': 'AK'},
    {'state': 'AZ'},
    {'state': 'AR'},
    {'state': 'CA'},
    {'state': 'CO'},
    {'state': 'CT'},
    {'state': 'DC'},
    {'state': 'DE'},
    {'state': 'FL'},
    {'state': 'GA'},
    {'state': 'HI'},
    {'state': 'ID'},
    {'state': 'IL'},
    {'state': 'IN'},
    {'state': 'IA'},
    {'state': 'KS'},
    {'state': 'KY'},
    {'state': 'LA'},
    {'state': 'ME'},
    {'state': 'MD'},
    {'state': 'MA'},
    {'state': 'MI'},
    {'state': 'MN'},
    {'state': 'MS'},
    {'state': 'MO'},
    {'state': 'MT'},
    {'state': 'NE'},
    {'state': 'NV'},
    {'state': 'NH'},
    {'state': 'NJ'},
    {'state': 'NM'},
    {'state': 'NY'},
    {'state': 'NC'},
    {'state': 'ND'},
    {'state': 'OH'},
    {'state': 'OK'},
    {'state': 'OR'},
    {'state': 'PA'},
    {'state': 'RI'},
    {'state': 'SC'},
    {'state': 'SD'},
    {'state': 'TN'},
    {'state': 'TX'},
    {'state': 'UT'},
    {'state': 'VT'},
    {'state': 'VA'},
    {'state': 'WA'},
    {'state': 'WV'},
    {'state': 'WI'},
    {'state': 'WY'},
]

specialty_options = [
    {'type': 'Cardiology'},
    {'type': 'Endocrinology'},
    {'type': 'Family Practice'},
    {'type': 'Internal Medicine'},
    {'type': 'Ophthalmology'},
    {'type': 'Neurology'},
    {'type': 'Psychiatry'},
    {'type': 'Physical Medicine and Rehabilitation'}
]

regression_vars = [
    "line_srvc_cnt",
    "bene_unique_cnt",
    "bene_day_srvc_cnt",
    "average_medicare_allowed_amt",
    "average_submitted_chrg_amt"
]

response_var = "average_medicare_payment_amt"

fraudulent_npis = [1245298371, 1922021195, 1225082886, 1023119898, 1881660959,
                   1942373923, 1013038629, 1356311591, 1013998640, 1881746501,
                   1881622090, 1295836245, 1275534935, 1801909338, 1528086618,
                   1235182189, 1730383993, 1376697995, 1457696908, 1033145487,
                   1619930260, 1356341911, 1427060375, 1013059740, 1235135138,
                   1225022627, 1326044835, 1720255144, 1073589420, 1396906160,
                   1659355840, 1841493707, 1356354252, 1477606614, 1659399897,
                   1609071836, 1154498277, 1316151525, 1912049388, 1316935406,
                   1841218799, 1780708594, 1093809907, 1285889782, 1942206198,
                   1245377787, 1477559037, 1952455941, 1336220425, 1861493009,
                   1619162898, 1184786196, 1053499673, 1750320412, 1720003882,
                   1164414769, 1245212471, 1588675896, 1841268026, 1013093178,
                   1801846597, 1427361609, 1770555724, 1457303380, 1841230166,
                   1164459350, 1124055900, 1740396381, 1316947807, 1194745695,
                   1275695975, 1902815087, 1174545271, 1578510723, 1275588485,
                   1225129349, 1841246105, 1750451613, 1225188766, 1053492132,
                   1174607782, 1275559338, 1649317298, 1639169972, 1801850292,
                   1952477622, 1043219405, 1831225812, 1376629717, 1609861590,
                   1437276128, 1124058086, 1427029479, 1184601577, 1003813866,
                   1518028281, 1942320635]
