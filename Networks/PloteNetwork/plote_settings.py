import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import os
import inspect
import sys

from library_hvac_app.pandas import*

from library_hvac_app.list import*
# mpl.use('Agg')

def mpl_fig_setting(show_grid=False):
    fig, ax = plt.subplots()
    fig.set_size_inches(22, 14)
    ax.spines['top'].set_visible(show_grid)
    ax.spines['bottom'].set_visible(show_grid)
    ax.spines['left'].set_visible(show_grid)
    ax.spines['right'].set_visible(show_grid)
    ax.axes.xaxis.set_visible(show_grid)
    ax.axes.yaxis.set_visible(show_grid)
    ax.grid(show_grid)
    return fig, ax

box_1 = {
    'facecolor': 'red',
    'edgecolor': 'black',
    'boxstyle': 'round'
}

box_2 = {
    'facecolor': 'pink',
    'edgecolor': 'black',
    'boxstyle': 'round'
}
text_style = {
    "horizontalalignment": 'center',
    "verticalalignment": 'center',
    "fontsize": 10,
    "style": 'italic',
}