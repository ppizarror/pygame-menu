
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

.. image:: https://img.shields.io/badge/python-3.6+-red.svg
    :target: https://www.python.org/downloads
    :alt: Python 3.6+

.. image:: https://img.shields.io/badge/pygame-1.9.3%2B%2F2.0%2B-orange
    :target: https://www.pygame.org
    :alt: Pygame 1.9.3+/2.0+

.. image:: https://badge.fury.io/py/pygame-menu.svg
    :target: https://pypi.org/project/pygame-menu
    :alt: PyPi package

.. image:: https://travis-ci.com/ppizarror/pygame-menu.svg?branch=master
    :target: https://travis-ci.com/ppizarror/pygame-menu
    :alt: Travis

.. image:: https://img.shields.io/lgtm/alerts/g/ppizarror/pygame-menu.svg?logo=lgtm&logoWidth=18
    :target: https://lgtm.com/projects/g/ppizarror/pygame-menu/alerts
    :alt: Total alerts

.. image:: https://img.shields.io/lgtm/grade/python/g/ppizarror/pygame-menu.svg?logo=lgtm&logoWidth=18
    :target: https://lgtm.com/projects/g/ppizarror/pygame-menu/context:python
    :alt: Language grade: Python

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

Source repo on `GitHub <https://github.com/ppizarror/pygame-menu>`_, 
and run it on `Repl.it <https://repl.it/github/ppizarror/pygame-menu>`_


Introduction
------------

Pygame-menu is a python-pygame library for creating menus. It supports several widgets, such as
buttons, color inputs, clock objects, drop selectors, frames, images, labels, selectors, tables,
text inputs, color switches, and many more, with many options to customize.

Comprehensive documentation for the latest version is available at
https://pygame-menu.readthedocs.io


Install Instructions
--------------------

Pygame-menu can be installed via pip. Simply run:

.. code-block:: bash

    $> pip install pygame-menu
    
If you are using Pygame<2.0.1, please upgrade:

.. code-block:: bash
    
    $> pip install -U pygame

To build the documentation from a Git repository:

.. code-block:: bash

    $> clone https://github.com/ppizarror/pygame-menu
    $> cd pygame-menu
    $> pip install -e .[docs]
    $> cd docs
    $> make html
