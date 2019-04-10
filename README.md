Micropop's Image Dashboard
==========================

This repository hosts notebooks to display microscopy images, videos, as well
as image processing and analysis results in a jupyter notebook. These notebooks
may be served via nbinteract.

Installation
------------
The recommended environment for running image-dashboard is anaconda. The following assumes you have anaconda3
installed and the conda executable is in your $PATH.

After cloning the repo, create a conda environment with

    conda create -p ./env

Activate the environment:

    conda activate ./env
    
Install image-dashboards dependencies:

    conda install --file requirements.txt
  
Finally, install image-dashboard into the newly created environment. If you want to develop image-dashboard, add the -e flag.
In this way, changes to the image-dashboard sources will be reflected in the installed package:

    pip install -e .
  
That's it.

Usage
-----

Active the conda environment:

    conda activate ./env
    
Start your local jupyter notebook server:

    jupyter notebook
    
From the jupyter dashboard, open one of the existing notebooks in notebooks/ or create a new one. If you want the notebook to become part of the repository, don't forget to 

    git add path/to/new/notebook.ipynb
    git commit path/to/new/notebook.ipynb
    
Development
-----------

Please consider working in a forked repository and create merge/pull requests.
