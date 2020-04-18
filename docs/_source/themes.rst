
.. module:: pygame_menu.themes

========
Skinning
========

:py:mod:`pygame-menu` offers many parameters to control the visual
aspect of the menu. For an easier usage, all of them are gathered in
a specific object called a ``theme``. It is used to customize the
menu window itself and all its widgets.

.. code-block:: python
    :emphasize-lines: 2

    menu = pygame_menu.Menu(300, 400,
                           theme=pygame_menu.themes.THEME_BLUE,
                           title='Welcome')

.. note:: The theme parameters can be overwritten locally
          when adding a widget to the menu. See the overwritable
          ones in the :ref:`add_... methods <Adding widgets>`


Default themes
--------------

Several predefined themes are proposed by :py:mod:`pygame-menu`.

==============================================  ================================================
Theme name                                      Example
==============================================  ================================================
:py:data:`pygame_menu.themes.THEME_DEFAULT`      .. image:: ../_static/theme_default.png
:py:data:`pygame_menu.themes.THEME_BLUE`         .. image:: ../_static/theme_blue.png
:py:data:`pygame_menu.themes.THEME_DARK`         .. image:: ../_static/theme_dark.png
:py:data:`pygame_menu.themes.THEME_GREEN`        .. image:: ../_static/theme_green.png
:py:data:`pygame_menu.themes.THEME_ORANGE`       .. image:: ../_static/theme_orange.png
:py:data:`pygame_menu.themes.THEME_SOLARIZED`    .. image:: ../_static/theme_solarized.png
==============================================  ================================================


Create a theme
--------------

If none of the proposed theme fit to the needs, the :py:class:`Theme`
give the opportunity to create custom themes.

.. code-block:: python

    mytheme = Theme(background_color=(0, 0, 0, 0), # transparent background
                    title_shadow=True,
                    title_background_color=(4, 47, 126))

    menu = Menu(..., theme=mytheme)

Of course it is also possible to start from a predefined theme by
copying it first.

.. code-block:: python

    mytheme = pygame_menu.themes.THEME_ORANGE.copy()
    mytheme.title_background_color=(0, 0, 0)

    menu = Menu(..., theme=mytheme)


Menubar style
-------------

The visual style of the menubar is managed using the theme parameter
``title_bar_style`` which can take the following values:

=================================================================   =======================================================
Menubar style                                                       Example
=================================================================   =======================================================
:py:data:`pygame_menu.widgets.MENUBAR_STYLE_ADAPTATIVE`             .. image:: ../_static/menubar_adaptive.png
:py:data:`pygame_menu.widgets.MENUBAR_STYLE_SIMPLE`                 .. image:: ../_static/menubar_simple.png
:py:data:`pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY`             .. image:: ../_static/menubar_title_only.png
:py:data:`pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL`    .. image:: ../_static/menubar_title_only_diagonal.png
:py:data:`pygame_menu.widgets.MENUBAR_STYLE_NONE`                   .. image:: ../_static/menubar_none.png
:py:data:`pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE`              .. image:: ../_static/menubar_underline.png
:py:data:`pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE`        .. image:: ../_static/menubar_underline_title.png
=================================================================   =======================================================

Widget selection effect
-----------------------

A **selection effect** is a drawing class used to define the way to highlight the focussed widget.
An instance of the selection effect class is defined in the :py:attr:`Theme.widget_selection_effect`
parameter of a theme. See example on how to add a selection effect in :ref:`Create a selection effect`
chapter.

The selection effects available are:

======================================================  ============================
Class                                                   Selection effect            
======================================================  ============================
:py:class:`pygame_menu.widgets.HighlightSelection`      Rectangular highlight
:py:class:`pygame_menu.widgets.LeftArrowSelection`      Left arrow on the widget
:py:class:`pygame_menu.widgets.NoneSelection`           No selection
:py:class:`pygame_menu.widgets.RightArrowSelection`     Right arrow on the widget
======================================================  ============================

The selection color is defined in :py:attr:`Theme.widget_selection_color`.

.. autoclass:: Theme
    :members:
