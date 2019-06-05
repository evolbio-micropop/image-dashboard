#!/usr/bin/env python
""" :module tablevis.app: Bokeh app for interactive visualization of cell tracking data from time-lapse microscopy. """

# Imports
import os
import pandas

from bokeh.io import output_notebook, show, push_notebook
from bokeh.plotting import figure, curdoc
from bokeh.models import CustomJS
from bokeh.models.sources import ColumnDataSource
from bokeh.layouts import column, row, WidgetBox
from bokeh.models.widgets import DataTable, Slider, Spinner, TableColumn, Button, Panel, Tabs, HTMLTemplateFormatter, Select, CheckboxGroup
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application


# Dir to load data from.
data_dir = '/home/grotec/Desktop/Results/DATA_OLex_0_CaCl2_pH_0_0p5M_Pro_0p5M_PP_0p2gmL.tif'

# Directory listing.
data_files = os.listdir(data_dir)

# Sort.
data_files.sort()

# Setup a dict to contain all data.
frames=dict()

# Loop over files and read data as pandas dataframe.
for data_file in data_files:
    print(data_file)
    key = data_file.split("_")[-1].split(".")[0]
    try:
        frames[key] = pandas.read_csv(os.path.join(data_dir, data_file), delimiter=",", header=0, encoding="Latin-1")
    except:
        print("Could not read %s" % data_file)
        raise


# Widget callbacks.
def idx_spinner_update(attr, old, new):
    if idx_selection_slider.value != new:
        idx_selection_slider.value=new

    replot(new)

def idx_slider_update(attr, old, new):
    if idx_selection_spinner.value != new:
        idx_selection_spinner.value=new

    replot(new)

def replot(idx):
    cds = ColumnDataSource(frames[str(int(idx))])

    p = figure(plot_width=700,
           plot_height=700,
           title=str(int(idx)),
           x_axis_label = x_column_selection.value,
           y_axis_label = y_column_selection.value,
           )
    p.circle(x=x_column_selection.value, y=y_column_selection.value, source=cds, size=10, alpha=0.8)

    tabs.tabs[0].child.children[1] = p

def x_update(attr, old, new):
    replot(idx_selection_spinner.value)
    #tabs.tabs[0].child.children[1].renderers[0].glyph.x = new
    #tabs.tabs[0].child.children[1].renderers[0].xaxis.axis_label = new

def y_update(attr, old, new):
    replot(idx_selection_spinner.value)
    #tabs.tabs[0].child.children[1].renderers[0].glyph.y = new
    #tabs.tabs[0].child.children[1].renderers[0].yaxis.axis_label = new

# Widgets and attach callbacks.
idx_as_ints = [int(k) for k in frames.keys()]
idx_as_ints.sort()

# Slider to select frame.
idx_selection_slider = Slider(start=idx_as_ints[0], end=idx_as_ints[-1], step=1.0, value=idx_as_ints[0], title="Select frame id")
idx_selection_slider.on_change('value', idx_slider_update)

# Spinner to select frame.
idx_selection_spinner = Spinner(low=idx_as_ints[0], high=idx_as_ints[-1], step=1.0, value=idx_as_ints[0], title="Select frame id")
idx_selection_spinner.on_change('value', idx_spinner_update)

# Selection for column to plot along x axis.
x_column_selection = Select(options=frames[str(int(idx_selection_spinner.value))].columns.to_list(), title="Select x axis column", value="Volume (µm^3)")
x_column_selection.on_change('value', x_update)

# Selection for column to plot along y axis.
y_column_selection = Select(options=frames[str(int(idx_selection_spinner.value))].columns.to_list(), title="Select y axis column", value="Volume (µm^3)")
y_column_selection.on_change('value', y_update)

# Initial data population.
cds = ColumnDataSource(frames[str(int(idx_selection_spinner.value))])

# Initial figure.
p = figure(plot_width=700,
           plot_height=700,
           title=str(int(idx_selection_spinner.value)),
           x_axis_label = x_column_selection.value,
           y_axis_label = y_column_selection.value,
          )
p.circle(x=x_column_selection.value, y=y_column_selection.value, source=cds, size=10, alpha=0.8)

# Put figure and widgets in a tab.
tab = Panel(child=row(column(idx_selection_spinner, idx_selection_slider, x_column_selection, y_column_selection), p))

tabs = Tabs(tabs=[tab])

# Attach to current document.
curdoc().add_root(tabs)

