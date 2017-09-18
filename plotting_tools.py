# -*- coding: utf-8 -*-

from math import pi
from bokeh.models import ColumnDataSource, DataRange1d, SingleIntervalTicker,\
    LinearAxis
from bokeh.plotting import figure
from bokeh.models.glyphs import VBar
from bokeh.embed import components


def render_bar_plot(source, plt_title):
    """Renders a bokeh bar plot from a data source.

    Args:
        source (dataframe): A dict-style Pandas dataframe.
        plt_title (str): Title for the plot.

    Returns:
        Components of a bar plot figure.
    """
    xdr = DataRange1d()
    ydr = DataRange1d()
    plot = figure(title=plt_title, x_range=xdr, y_range=ydr, plot_width=1300,
                 plot_height=800, h_symmetry=False, v_symmetry=False,
                 toolbar_location=None, x_axis_type=None)

    # Add vertical bar glyphs to the plot.
    glyph = VBar(x="provider_idx", top="outlier_count", bottom=0, width=0.5)
    plot.add_glyph(source, glyph)

    # Need to convert provider names to tick labels.
    xaxis = LinearAxis(ticker=SingleIntervalTicker(interval=1))
    plot.add_layout(xaxis, 'below')
    plot.xaxis.major_label_overrides = {
        idx: label for idx, label in enumerate(source.data["tick_labels"])
    }

    # Making the plot pretty
    plot.title.text_font_size = '40pt'
    plot.xaxis.axis_label_text_font_size = '30pt'
    plot.yaxis.axis_label_text_font_size = '30pt'
    plot.xaxis.major_label_text_font_size = '20pt'
    plot.yaxis.major_label_text_font_size = '20pt'
    plot.yaxis.axis_label = "Anomaly Count"

    # Rotating the plot labels so that the text fit
    plot.xaxis.major_label_orientation = pi/3

    return components(plot)


def create_source(w_n_df, bar_value):
    """Creates a column data source from the output of the anomaly detector.

    Args:
        w_n_df (DataFrame): A Pandas DataFrame containing an outlier count.
        bar_value (str): Column name for the bar chart values.

    Returns:
        A ColumnDataSource object.

    """
    # Get the info we need from the DataFrame.
    indices = range(w_n_df.shape[0])  # The number of indices is just the rows.
    npis = list(w_n_df.index)  # The NPIs are the row labels.
    last_names = w_n_df['last_name'].values
    o_cts = w_n_df[bar_value].values

    labels = [(l_n + " (" + npi + ")") for l_n, npi in zip(last_names, npis)]

    source = ColumnDataSource(dict(provider_idx=indices,
                                   outlier_count=o_cts,
                                   tick_labels=labels))

    return source


def generate_bar_plot(w_n_df, bar_value='outlier_count', plt_title=None):
    """Method to generate a Bokeh bar plot.

    Args:
        w_n_df (DataFrame): A Pandas data frame containing our bar chart data.
        bar_value (str): Column name that we want to make a bar plot for.
        plt_title (str): A title for the plot.

    Returns:
        Components of a bar plot figure.

    """
    data_source = create_source(w_n_df, bar_value)
    return render_bar_plot(data_source, plt_title=plt_title)
