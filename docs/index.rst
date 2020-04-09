:orphan:

.. include:: ../README.rst


Common usage
============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   _source/menu
   _source/add_widgets


Widgets API
===========

Here is the library structure:

====================  ====================================
Module                Description
====================  ====================================
*pygameMenu.config*   Default configuration of Menus
*pygameMenu.controls* Control definition, constants, etc.
*pygameMenu.events*   Events definition, constants, etc.
*pygameMenu.font*     Menu font management
*pygameMenu.locals*   Menu constants
*pygameMenu.menu*     Menu class
*pygameMenu.widgets*  Package of widgets
*pygameMenu.sound*    Sound management
*pygameMenu.version*  Version of the library
====================  ====================================

Each widget is an class that can be inserted in a menu. However
they could be used has it to design custom menu layout.

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Widgets API:

   _source/widget_button
   _source/widget_colorinput
   _source/widget_label
   _source/widget_menubar
   _source/widget_scrollbar
   _source/widget_selector
   _source/widget_textinput


About pygame-menu
=================

   .. toctree::
      :maxdepth: 2
      :caption: About pygame-menu:

      _source/gallery
      _source/license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
