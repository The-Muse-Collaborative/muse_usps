#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.githubpages']
source_suffix = '.rst'
master_doc = 'index'
project = 'muse_usps'
copyright = '2017, Aaron Jones'
author = 'Aaron Jones'
version = '0.0.1'
release = '0.0.1'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = 'alabaster'
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
        'donate.html',
    ]
}
htmlhelp_basename = 'muse_uspsdoc'
