===========
pygame-menu
===========

.. image:: docs/_static/pygame_menu_small.png
    :align: center
    :alt:

.. image:: https://img.shields.io/badge/author-Pablo%20Pizarro%20R.-lightgray.svg
    :target: https://ppizarror.com
    :alt: @ppizarror

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License MIT

.. image:: https://img.shields.io/badge/python-3.9+-red.svg
    :target: https://www.python.org/downloads
    :alt: Python 3.9+

.. image:: https://img.shields.io/badge/pygame-1.9.3%2B%2F2.0%2B-orange
    :target: https://www.pygame.org
    :alt: Pygame 1.9.3+/2.0+

.. image:: https://badge.fury.io/py/pygame-menu.svg
    :target: https://pypi.org/project/pygame-menu
    :alt: PyPi package

.. image:: https://img.shields.io/github/actions/workflow/status/ppizarror/pygame-menu/ci.yml?branch=master
    :target: https://github.com/ppizarror/pygame-menu/actions/workflows/ci.yml
    :alt: Build status
    
.. image:: https://readthedocs.org/projects/pygame-menu/badge/?version=latest
    :target: https://pygame-menu.readthedocs.io
    :alt: Documentation Status

.. image:: https://codecov.io/gh/ppizarror/pygame-menu/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ppizarror/pygame-menu
    :alt: Codecov

.. image:: https://img.shields.io/github/issues/ppizarror/pygame-menu
    :target: https://github.com/ppizarror/pygame-menu/issues
    :alt: Open issues

.. image:: https://img.shields.io/pypi/dm/pygame-menu?color=purple
    :target: https://pypi.org/project/pygame-menu/
    :alt: PyPi downloads

.. image:: https://static.pepy.tech/personalized-badge/pygame-menu?period=total&units=international_system&left_color=grey&right_color=lightgrey&left_text=total%20downloads
    :target: https://pepy.tech/project/pygame-menu
    :alt: Total downloads
    
.. image:: https://img.shields.io/badge/buy%20me%20a-Ko--fi-02b9fe
    :target: https://ko-fi.com/ppizarror
    :alt: Buy me a Ko-fi

Source repo on `GitHub <https://github.com/ppizarror/pygame-menu>`_, 
and run it on `Repl.it <https://repl.it/github/ppizarror/pygame-menu>`_


Introduction
------------

Pygame-menu is a `python-pygame <https://www.pygame.org>`_ library for creating menus and GUIs.
It supports several widgets, such as buttons, color inputs, clock objects, drop selectors,
frames, images, labels, selectors, tables, text inputs, color switches, and many
more, with multiple customization options.

Comprehensive documentation for the latest version is available at
https://pygame-menu.readthedocs.io

Install Instructions
--------------------

Pygame-menu requires either **pygame** (default) or **pygame-ce** to be installed.
If you install pygame-menu normally, the standard pygame backend is used.

To install with the default **pygame** backend:

.. code-block:: bash

    $> pip install pygame-menu -U

To install with **pygame-ce** (Community Edition):

.. code-block:: bash

    $> pip install pygame-menu[ce] -U

To build the documentation from a Git repository:

.. code-block:: bash

    $> git clone https://github.com/ppizarror/pygame-menu
    $> cd pygame-menu
    $> pip install -e ".[docs]"
    $> pip install pygame -U   # or pygame-ce if preferred
    $> cd docs
    $> make html
