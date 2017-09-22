# -*- coding: utf-8 -*-

from bokeh.models import ColumnDataSource, DataRange1d, SingleIntervalTicker,\
    LinearAxis, LabelSet
from bokeh.plotting import figure
from bokeh.models.glyphs import HBar
from bokeh.embed import components

__author__ = "Daniel Hannah"
__email__ = "dan@danhannah.site"

"""Tools for plotting bar charts with Bokeh.

This set of tools has been deprecated and is no longer in use on FraudHacker (I
switched to chartJS for a variety of reasons), but is here just in case it
becomes useful in the future.

"""


def render_bar_plot(source, plt_title):
    """Renders a bokeh bar plot from a data source.

    Args:
        source (dataframe): A dict-style Pandas dataframe.
        plt_title (str): Title for the plot.

    Returns:
        Components of a bar plot figure.
    """
    bar_height = 0.5
    top_stop = len(source.data["tick_labels"]) - 1 + bar_height
    bottom_start = -1 * bar_height

    xdr = DataRange1d()
    ydr = DataRange1d(start=bottom_start, end=top_stop)
    plot = figure(title=plt_title, x_range=xdr, y_range=ydr, plot_width=1200,
                  plot_height=1200, h_symmetry=False, v_symmetry=False,
                  toolbar_location=None, y_axis_type=None, x_axis_type=None)

    # Add vertical bar glyphs to the plot.
    glyph = HBar(y="provider_idx", right="outlier_count", left=0,
                 height=bar_height, fill_color="#DB4437")
    plot.add_glyph(source, glyph)

    # Need to convert provider names to tick labels.
    yaxis = LinearAxis(ticker=SingleIntervalTicker(interval=1),
                       axis_line_color='white', major_tick_line_color='white',
                       minor_tick_line_color='white')
    plot.add_layout(yaxis, 'left')
    plot.yaxis.major_label_overrides = {
        idx: label for idx, label in enumerate(source.data["tick_labels"])
    }

    # Add some labels to the bar plots
    labels = LabelSet(x='outlier_count', y='provider_idx', x_offset=5,
                      y_offset=-8, text='outlier_count', source=source,
                      text_font_size='18pt')
    plot.add_layout(labels)

    # Making the plot pretty
    plot.title.text_font_size = '40pt'
    plot.yaxis.axis_label_text_font_size = '30pt'
    plot.yaxis.major_label_text_font_size = '18pt'
    plot.xaxis.axis_label = "Anomaly Count"
    plot.outline_line_color = None

    # Rotating the plot labels so that the text fit
    # plot.xaxis.major_label_orientation = pi/3

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
    indices = [i for i in range(w_n_df.shape[0])]
    npis = w_n_df['npi'].values
    last_names = w_n_df['lastname'].values
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
    data_source = create_source(w_n_df.iloc[::-1], bar_value)
    return render_bar_plot(data_source, plt_title=plt_title)
