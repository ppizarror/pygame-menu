
===========
pygame-menu
===========

.. image:: https://raw.githubusercontent.com/ppizarror/pygame-menu/master/docs/_static/pygame-menu-small.png
   :scale: 25%

Currently, Python 2.7+ and 3.4+ (3.4, 3.5, 3.6, 3.7) are supported.

.. image:: https://travis-ci.org/ppizarror/pygame-menu.svg?branch=master
   :target: https://travis-ci.org/ppizarror/pygame-menu
   :alt: Travis

.. image:: https://codecov.io/gh/ppizarror/pygame-menu/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ppizarror/pygame-menu
    :alt: Codecov

.. image:: https://img.shields.io/lgtm/alerts/g/ppizarror/pygame-menu.svg?logo=lgtm&logoWidth=18
    :target: https://lgtm.com/projects/g/ppizarror/pygame-menu/alerts
    :alt: Total alerts

.. image:: https://img.shields.io/lgtm/grade/python/g/ppizarror/pygame-menu.svg?logo=lgtm&logoWidth=18
    :target: https://lgtm.com/projects/g/ppizarror/pygame-menu/context:python
    :alt: Language grade: Python

Source repo on `github <https://github.com/ppizarror/pygame-menu>`_ ,
and run it on `Repl.it <https://repl.it/github/ppizarror/pygame-menu>`_

Introduction
------------

Pygame-menu is a python-pygame library for creating menus, it supports
selectors, buttons, labels, color inputs, text inputs with many options to customize.

Comprehensive documentation is available at https://pygame-menu.readthedocs.io.

Install Instructions
--------------------

Pygame-menu can be installed via pip. Simply run::

    $> pip install pygame-menu

To build the documentation from git repository:

.. code-block:: bash

    $> clone https://github.com/ppizarror/pygame-menu
    $> cd pygame-menu
    $> pip install -e .[doc]
    $> cd docs
    $> make html

Dependencies
------------

This library is dependent on the following

- `Pygame <http://www.pygame.org/download.shtml>`_
- `pyperclip <https://pypi.org/project/pyperclip/>`_
