
.. module:: pygame_menu.themes

===============
Creating themes
===============

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
:py:data:`pygame_menu.themes.THEME_DEFAULT`     .. image:: ../_static/theme_default.png
:py:data:`pygame_menu.themes.THEME_BLUE`        .. image:: ../_static/theme_blue.png
:py:data:`pygame_menu.themes.THEME_DARK`        .. image:: ../_static/theme_dark.png
:py:data:`pygame_menu.themes.THEME_GREEN`       .. image:: ../_static/theme_green.png
:py:data:`pygame_menu.themes.THEME_ORANGE`      .. image:: ../_static/theme_orange.png
:py:data:`pygame_menu.themes.THEME_SOLARIZED`   .. image:: ../_static/theme_solarized.png
==============================================  ================================================


Create a theme
--------------

If none of the proposed theme fit to the needs, the :py:class:`Theme`
give the opportunity to create custom themes.

.. code-block:: python

    mytheme = Theme(background_color=(0, 0, 0, 0), # transparent background
                    title_shadow=True,
                    title_background_color=(4, 47, 126),
                    ...)

    menu = Menu(..., theme=mytheme)

Of course it is also possible to start from a predefined theme by
copying it first.

.. code-block:: python

    mytheme = pygame_menu.themes.THEME_ORANGE.copy()
    mytheme.title_background_color=(0, 0, 0)

    menu = Menu(..., theme=mytheme)


Background Color/Images
-----------------------

Theme background can be both a color or an image. All colors can be defined
using a tuple or an list of 3 or 4 numbers between 0 and 255. The format of
numers are:

.. code-block:: python

    color_opaque = (R,G,B)
    color_transparent = (R,G,B,A)

*A* alpha channels goes from *0* to *255*. *0* is transparent, *255* is opaque.
For using images as a background color, class :py:class:`pygame_menu.baseimage.BaseImage`
must be used.

Images needs a Path (file location on disk), a drawing mode, and an optional offset.

.. code-block:: python

    myimage = pygame_menu.baseimage.BaseImage(
        image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
        offset=(0,0)
    )
    mytheme.background_color = myimage

=====================================================   =========================================
Image drawing modes                                     Description
=====================================================   =========================================
:py:data:`pygame_menu.baseimage.IMAGE_MODE_CENTER`      Centers the image in the surface
:py:data:`pygame_menu.baseimage.IMAGE_MODE_FILL`        Fill the image on the surface
:py:data:`pygame_menu.baseimage.IMAGE_MODE_REPEAT_X`    Repeat the image on x axis
:py:data:`pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY`   Repeat the image on x and y axis
:py:data:`pygame_menu.baseimage.IMAGE_MODE_REPEAT_Y`    Repeat the image on y axis
:py:data:`pygame_menu.baseimage.IMAGE_MODE_SIMPLE`      Write the image on top-left location
=====================================================   =========================================

Currently, :py:class:`Theme` class only supports images for :py:attr:`background_color` and
:py:attr:`widget_background_color`. Also, only `IMAGE_MODE_FILL` drawing mode is valid for
:py:attr:`widget_background_color`.


Menubar style
-------------

The visual style of the menubar is managed using the theme parameter
``title_bar_style`` which can take the following values:

=================================================================   =======================================================
Menubar style                                                       Example
=================================================================   =======================================================
:py:data:`pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE`               .. image:: ../_static/menubar_adaptive.png
:py:data:`pygame_menu.widgets.MENUBAR_STYLE_SIMPLE`                 .. image:: ../_static/menubar_simple.png
:py:data:`pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY`             .. image:: ../_static/menubar_title_only.png
:py:data:`pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL`    .. image:: ../_static/menubar_title_only_diagonal.png
:py:data:`pygame_menu.widgets.MENUBAR_STYLE_NONE`                   .. image:: ../_static/menubar_none.png
:py:data:`pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE`              .. image:: ../_static/menubar_underline.png
:py:data:`pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE`        .. image:: ../_static/menubar_underline_title.png
=================================================================   =======================================================


Widget selection effect
-----------------------

A **selection effect** is a drawing class used to define the way to highlight the focused widget.
An instance of the selection effect class is defined in the :py:attr:`Theme.widget_selection_effect`
parameter of a theme. See example on how to add a selection effect in :ref:`Create a selection effect`
chapter.

The available selection effects are:

======================================================  ============================
Class                                                   Selection effect
======================================================  ============================
:py:class:`pygame_menu.widgets.HighlightSelection`      Rectangular highlight
:py:class:`pygame_menu.widgets.LeftArrowSelection`      Left arrow on the widget
:py:class:`pygame_menu.widgets.NoneSelection`           No selection
:py:class:`pygame_menu.widgets.RightArrowSelection`     Right arrow on the widget
======================================================  ============================

The selection color is defined in :py:attr:`Theme.widget_selection_color`.


Fonts
-----

This library also has some fonts to use. To load a font, run this code:

.. code-block:: python

    import pygame_menu

    font = pygame_menu.font.FONT_NAME
    my_theme = Theme(widget_font=font, ...)

==================================================  =============================================
Available fonts                                     Preview
==================================================  =============================================
:py:class:`pygame_menu.font.FONT_8BIT`              .. image:: ../_static/font_8bit.png
:py:class:`pygame_menu.font.FONT_BEBAS`             .. image:: ../_static/font_bebas.png
:py:class:`pygame_menu.font.FONT_COMIC_NEUE`        .. image:: ../_static/font_comic_neue.png
:py:class:`pygame_menu.font.FONT_FRANCHISE`         .. image:: ../_static/font_franchise.png
:py:class:`pygame_menu.font.FONT_HELVETICA`         .. image:: ../_static/font_helvetica.png
:py:class:`pygame_menu.font.FONT_MUNRO`             .. image:: ../_static/font_munro.png
:py:class:`pygame_menu.font.FONT_NEVIS`             .. image:: ../_static/font_nevis.png
:py:class:`pygame_menu.font.FONT_OPEN_SANS`         .. image:: ../_static/font_open_sans.png
:py:class:`pygame_menu.font.FONT_OPEN_SANS_BOLD`    .. image:: ../_static/font_open_sans_bold.png
:py:class:`pygame_menu.font.FONT_OPEN_SANS_ITALIC`  .. image:: ../_static/font_open_sans_italic.png
:py:class:`pygame_menu.font.FONT_OPEN_SANS_LIGHT`   .. image:: ../_static/font_open_sans_light.png
:py:class:`pygame_menu.font.FONT_PT_SERIF`          .. image:: ../_static/font_pt_serif.png
==================================================  =============================================

System fonts can also be used. The available system fonts can be listed using the following command in a python shell:

.. code-block:: python

    import pygame
    print(pygame.font.get_fonts())

Theme API
---------

.. autoclass:: Theme
    :members:
