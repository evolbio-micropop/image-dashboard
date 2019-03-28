"""
:module run_analysis_lib: Collection of classes and functions useful for analysis of beam profiles from 2D imaging data.
"""

# Imports
from collections import namedtuple
from image_dashboard.utilities import chunks
from io import StringIO
from plotly import graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from scipy import ndimage
import ipywidgets as widgets
import multiprocessing
import numpy
import os, sys
import pandas
import xarray
from matplotlib import pyplot as plt

def process_chunk(args):
    """ Process a chunk of images given through the args parameter.

    :param args: tuple of (images, instrument, dataset). images is a sequence of 2D ndarrays, instrument and dataset are optional and designate the instrument and dataset identifier (str) in karabo_data.get_array(instrument, dataset).

    """
    pass

##  Widgets

def browse_images(images):
    
    def view_image(i):
        im = images[i]
        im = im/im.max()
        plt.imshow(im, cmap="Greys_r", interpolation='nearest')
        plt.title('Image: %d' % (i))
        plt.show()
    widgets.interact(view_image, i=(0,len(images)-1))
    
class FileBrowser(object):
    """
    :class FileBrowser: Navigate through a file hierarchy to select a file or directory.
    """

    def __init__(self, parent_dir=None, **kwargs):
        """ Construct a new FileBrowser widget
        :param kwargs: Keyword arguments. Only 'parent_dir' is required and should give a valid path under which to search for existing run cycle directories.

        """
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.parent_dir = parent_dir
        self.init_widgets()

    def gui(self):
        """
        Display and all widgets.
        """

        display(self._current_dir, self._dir, self._open)

    def init_widgets(self):
        """
        Initialize all widgets (layout, options, values).
        """

        self.dropdown_layout = widgets.Layout(width='80%')
        self.dropdown_style = {'description_width' : '0%'}

        # Proposal directory dropdown
        self._current_dir = widgets.Text(value=self.parent_dir, layout=widgets.Layout(width='100%'))
        self._dir = widgets.Select(options=get_dirs(self.parent_dir),
                                             value=None,
                                             description="Select directory",
                                             layout=self.dropdown_layout,
                                             style=self.dropdown_style,
                                            )
        
        self._open = widgets.Button(
                        description='Open',
                        disabled=False,
                        button_style='', # 'success', 'info', 'warning', 'danger' or ''
                        tooltip='Click to open directory',
                        icon='',
                    )


        self._open.on_click(self.handle_button_clicked)
        self._dir.observe(self.handle_dir_change, names=['value'])
       
    
    def handle_dir_change(self, change):
        return
    
        self.parent_dir = os.path.abspath(os.path.join(self.parent_dir, change.new))
        print(self.parent_dir)
        
    def handle_button_clicked(self, button):
        """
        Callback handling the change of the directory selection widget.
        """
        
        new_dir = os.path.normpath(os.path.join(self.parent_dir, self._dir.value))
        self._dir.options = get_dirs(new_dir)
        self._dir.value = self._dir.options[0]
        self._current_dir.value = new_dir
        self.parent_dir = new_dir
        
              
def has_access(path, mode='read', verbose=False):
    """ Checks if given file or directory path has given access mode and (if verbose) prints a message.

    :param mode: Which mode to check.
    :type mode: str

    :param verbose: Flag controlling the verbosity of the check (Default: False, no message).
    :type verbose: bool

    """

    valid_modes = ['read', 'write', 'execute', 'r', 'w', 'x']
    mode_map = dict(read=os.R_OK, r=os.R_OK,
                    write=os.W_OK, w=os.W_OK,
                    execute=os.X_OK, x=os.X_OK,
                   )
    if mode not in valid_modes:
        raise("Mode parameter must be one of ", valid_modes)

    access_state = os.access(path, mode_map[mode])

    if verbose:
        print("{0:s} has mode '{1:s}': {2:b}.".format(path, mode, access_state))

    return access_state

def get_dirs(parent_dir):
    """ Get all subdirectories under a given parent directory that the user has 'read' access to.

    :param parent_dir: The parent directory to scan.
    :type parent_dir: str

    """
    
    if not has_access(parent_dir, 'r', verbose=False):
        return []
    
    child_dirs = os.listdir(parent_dir)
    child_dirs.insert(0,"..")
    child_dirs.sort()
    
    return child_dirs
        
