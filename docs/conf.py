"""
pygame-menu
https://github.com/ppizarror/pygame-menu

CONF
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# -- Path setup ---------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here
#
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame_menu

# -- Project information ------------------------------------------------------

project = pygame_menu.__module_name__
# noinspection PyShadowingBuiltins
copyright = pygame_menu.__copyright__
author = pygame_menu.__author__

# The full version, including alpha/beta/rc tags
release = pygame_menu.__version__

# -- General configuration ----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.viewcode',
              'sphinx.ext.intersphinx',
              'sphinx.ext.autosectionlabel',
              'sphinx_autodoc_typehints'
              ]

# autodoc_default_options = {
#     'private-members': False
# }

# Add any paths that contain templates here, relative to this directory
templates_path = ['_templates']

# The document name of the "master" document, that is, the document that
# contains the root toc-tree directive. Default is 'index'
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files
# This pattern also affects html_static_path and html_extra_path
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']

# -- Intersphinx configuration ------------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3.9', None),
    'pygame': ('https://www.pygame.org/docs', None),
}

# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css"
html_static_path = ['_static']

html_title = f'{project} {release} Documentation'

html_logo = '_static/pygame_menu_small.png'

html_theme_options = {
    'prev_next_buttons_location': None
}

# -- Options for LaTeX output -------------------------------------------------

# noinspection SpellCheckingInspection
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
    'preamble': r'\def\thempfootnote{\arabic{mpfootnote}}'  # workaround sphinx issue #2530
}

latex_documents = [
    (
        'index',  # source start file
        f'{project}.tex',  # target filename
        f'{project} Documentation',  # title
        author,  # author
        'manual',  # documentclass
        True,  # documents ref'd from toc-tree only
    ),
]

latex_show_pagerefs = True

# -- Options for autodoc - typehints ---

set_type_checking_flag = True
