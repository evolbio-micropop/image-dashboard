#!/usr/bin/env python
""" :module tablevis.app: Bokeh app for interactive visualization of cell tracking data from time-lapse microscopy. """

# Imports
import os
import pandas

import matplotlib as mpl
from matplotlib import cm
from bokeh.io import output_notebook, show, push_notebook
from bokeh.plotting import figure, curdoc
from bokeh.models import CustomJS
from bokeh.models.sources import ColumnDataSource
from bokeh.layouts import column, row, WidgetBox
from bokeh.models.widgets import DataTable, Slider, Spinner, TableColumn, Button, Panel, Tabs, HTMLTemplateFormatter, Select, CheckboxGroup
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.transform import linear_cmap
from bokeh.palettes import Spectral6


class Model(object):
    """ Struct to store effectively global variables. """

    def __init__(self):
        self.parent_dir = "static"

    @property
    def frames(self):
        return self.__frames
    @frames.setter
    def frames(self, val):
        self.__frames = val
        self.idxs = [k for k in self.__frames.keys()]
        self.idxs.sort()

model = Model()

# Widget callbacks.
def idx_spinner_update(attr, old, new):
    new = int(new)
    if new != old:
        idx_selection_spinner.value = new
    if idx_selection_slider.value != new:
        idx_selection_slider.value=new

    replot(new)

def idx_slider_update(attr, old, new):
    new = int(new)
    if idx_selection_spinner.value != new:
        idx_selection_spinner.value=new

    replot(new)

def replot(idx):
    if idx in model.frames.keys():
        frame = model.frames[idx]

    else:
        print("No dataset with index %d found." % idx)
        return

    x_values = frame[x_column_selection.value]
    y_values = frame[y_column_selection.value]
    size_values = symbol_size(frame[size_column_selection.value].to_numpy())
    print(size_values)
    color_values = frame[color_column_selection.value].to_numpy()

    colors = [
    "#%02x%02x%02x" % (int(r), int(g), int(b)) for r, g, b, _ in 255*mpl.cm.viridis(mpl.colors.Normalize()(color_values))
]
    p = figure(plot_width=700,
           plot_height=700,
           title=str(idx),
           x_axis_label = x_column_selection.value,
           y_axis_label = y_column_selection.value,
           )

    p.circle(x=x_values,
             y=y_values,
             size=size_values,
             color=colors,
             alpha=0.8)

    tabs.tabs[0].child.children[1] = p

def size_update(attr, old, new):
    replot(int(idx_selection_spinner.value))

def color_update(attr, old, new):
    replot(int(idx_selection_spinner.value))

def x_update(attr, old, new):
    replot(int(idx_selection_spinner.value))

def y_update(attr, old, new):
    replot(int(idx_selection_spinner.value))

def directory_update(attr, old, new):
    # Setup a dict to contain all data.
    frames=get_frames(new)

    model.frames=frames

    replot(int(idx_selection_spinner.value))

def get_frames(directory):
    data_dir = os.path.join(model.parent_dir, directory)
    data_files = os.listdir(data_dir)
    data_files.sort()
    frames = {}

    # Loop over files and read data as pandas dataframe.
    for data_file in data_files:
        print(data_file)
        key = data_file.split("_")[-1].split(".")[0]
        key = int(key)
        try:
            frames[key] = pandas.read_csv(os.path.join(data_dir, data_file), delimiter="\t", header=0, encoding="Latin-1")
            frames[key]['index'] = frames[key].index.to_list()

        except:
            print("Could not read %s" % data_file)

    return frames

def symbol_size(values):
    """ Rescale given values to reasonable symbol sizes in the plot. """

    max_size = 50.0
    min_size = 5.0

    # Rescale max.
    slope = (max_size - min_size)/(values.max() - values.min())

    return slope*(values - values.max()) + max_size

# Directory selection.
dirs = os.listdir(model.parent_dir)
dirs.sort()
directory_selection = Select(options=dirs, value = dirs[1])
directory_selection.on_change('value', directory_update)

# Init model first time.
model.frames = get_frames(directory_selection.value)

# Slider to select frame.
idx_selection_slider = Slider(start=model.idxs[0], end=model.idxs[-1], step=1.0, value=model.idxs[0], title="Select frame id")
idx_selection_slider.on_change('value', idx_slider_update)

# Spinner to select frame.
idx_selection_spinner = Spinner(low=model.idxs[0], high=model.idxs[-1], step=1.0, value=model.idxs[0], title="Select frame id")
idx_selection_spinner.on_change('value', idx_spinner_update)

# Selection for column to yield symbol color.
color_column_selection = Select(options=model.frames[int(idx_selection_spinner.value)].columns.to_list(), title="Select symbol color from column", value="Volume (µm^3)")
color_column_selection.on_change('value', color_update)

# Selection for column to yield symbol size.
size_column_selection = Select(options=model.frames[int(idx_selection_spinner.value)].columns.to_list(), title="Select symbol size from column", value="Volume (µm^3)")
size_column_selection.on_change('value', size_update)

# Selection for column to plot along x axis.
x_column_selection = Select(options=model.frames[int(idx_selection_spinner.value)].columns.to_list(), title="Select x axis column", value="Volume (µm^3)")
x_column_selection.on_change('value', x_update)

# Selection for column to plot along y axis.
y_column_selection = Select(options=model.frames[int(idx_selection_spinner.value)].columns.to_list(), title="Select y axis column", value="Volume (µm^3)")
y_column_selection.on_change('value', y_update)

# Initial data population.
cds = ColumnDataSource(model.frames[int(idx_selection_spinner.value)])

# Initial figure.
p = figure(plot_width=700,
           plot_height=700,
           title=str(int(idx_selection_spinner.value)),
           x_axis_label = x_column_selection.value,
           y_axis_label = y_column_selection.value,
          )

# Put figure and widgets in a tab.
tab = Panel(child=row(column(directory_selection, idx_selection_spinner, idx_selection_slider, x_column_selection, y_column_selection, size_column_selection, color_column_selection), p))

tabs = Tabs(tabs=[tab])

replot(int(idx_selection_spinner.value))
# Attach to current document.
curdoc().add_root(tabs)

