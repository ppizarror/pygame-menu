:orphan:

.. include:: ../README.rst


===========
First steps
===========

Making games using :py:mod:`pygame` is really cool, but most of game
(or application) require end-user configuration. Create complex GUI
object to display a menu can be painful. That why :py:mod:`pygame-menu`
was designe.

Here is a basic example of how to create a menu:

1. Make your imports

.. code-block:: python

    import pygame
    import pygameMenu

2. Initialize pygame

.. code-block:: python

    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    surface = pygame.display.set_mode((400, 600))

3. Make your menu

.. code-block:: python

    menu = pygameMenu.Menu(surface, pygameMenu.font.FONT_BEBAS, "My first menu")

3. Run your menu

.. code-block:: python

    menu.mainloop(surface)

**Interested?** :ref:`Go deeper in menu design <Creating menus>`.

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: First steps

   _source/create_menu
   _source/add_widgets
   _source/add_sounds
   _source/gallery


===========
Widgets API
===========

Each widget is an class that can be inserted in a menu. However
they could be used has it to design custom menu layout.

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Widgets API

   _source/widget_button
   _source/widget_colorinput
   _source/widget_label
   _source/widget_menubar
   _source/widget_scrollbar
   _source/widget_selector
   _source/widget_textinput


=================
About pygame-menu
=================

This project does not have a mailing list and so the issues tab should
be the first point of contact if wishing to discuss the project. If you
have questions that you do not feel are relevant to the issues tab or
just want to let me know what you think about the library, feel free to
email me.

Author email: pablo@ppizarror.com

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: About pygame-menu

   _source/license


==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
