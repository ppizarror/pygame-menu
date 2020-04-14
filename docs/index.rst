:orphan:

.. image:: _static/pygame-menu.png
   :scale: 35%
   :align: center

.. include:: ../README.rst


===========
First steps
===========

Making games using :py:mod:`pygame` is really cool, but most games
(or applications) require end-user configuration. Creating complex GUI
objects to display a menu can be painful. That why :py:mod:`pygame-menu`
was designed.

Here is a simple example of how to create a menu with :py:mod:`pygame-menu`
(the code is available in :py:mod:`pygameMenu.examples.simple`):

1. Import the required libraries

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

    def set_difficulty(value, difficulty):
        # Do the job here !

    def start_the_game():
        # Do the job here !

    menu = pygameMenu.Menu(300, 400, pygameMenu.font.FONT_BEBAS,
                           title="Welcome",
                           theme=pygameMenu.themes.THEME_BLUE)

    menu.add_text_input('Name :')
    menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add_button('Play', start_the_game)
    menu.add_button('Quit', pygameMenu.events.EXIT)
    menu.center_content()

4. Run your menu

.. code-block:: python

    menu.mainloop(surface)

.. figure:: _static/first_steps.png
   :scale: 40%
   :align: center

   Tadada... !!! Such a beautiful menu ＼(^o^)／

**Interested in** :ref:`going deeper into menu design <Creating menus>` **?**

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

A menu is in fact a list of widgets arranged on the same surface.
Access to a widget in a menu can easily be done with two methods:

.. code-block:: python

    widget = menu.get_widget('MyWidgetID')

    selected = menu.get_selected_widget()

Each :py:mod:`pygameMenu` widget and its behaviors are defined in a
class. The currently existing classes are:

 - :py:class:`~pygameMenu.widgets.Button`
 - :py:class:`~pygameMenu.widgets.ColorInput`
 - :py:class:`~pygameMenu.widgets.Image`
 - :py:class:`~pygameMenu.widgets.Label`
 - :py:class:`~pygameMenu.widgets.MenuBar`
 - :py:class:`~pygameMenu.widgets.ScrollBar`
 - :py:class:`~pygameMenu.widgets.Selector`
 - :py:class:`~pygameMenu.widgets.TextInput`
 - :py:class:`~pygameMenu.widgets.VMargin`

For advanced programers, those classes can be used to design custom
menus or windows.

Have a look at :py:mod:`pygameMenu.widgets.examples.scrollbar.py` for
instance. It shows how to use the :py:class:`pygameMenu.widgets.ScrollBar`
class to display large custom surfaces.

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Widgets API

   _source/widget_button
   _source/widget_colorinput
   _source/widget_image
   _source/widget_label
   _source/widget_menubar
   _source/widget_scrollbar
   _source/widget_selector
   _source/widget_textinput
   _source/widget_vmargin


=================
About pygame-menu
=================

This project does not have a mailing list and so the issues tab should
be the first point of contact if wishing to discuss the project. If you
have questions that you do not feel are relevant to the issues tab or
just want to let me know what you think about the library, feel free to
email me at pablo@ppizarror.com

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: About pygame-menu

   _source/license
   _source/contributors


==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
