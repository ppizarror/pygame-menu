
.. module:: pygameMenu.themes

========
Skinning
========

:py:mod:`pygame-menu` offers many parameters to control the visual
aspect of the menu. For an easier usage, all of them are gathered in
a specific object called a ``theme``. It is used to customize the
menu window itself and all its widgets.

.. code-block:: python
    :emphasize-lines: 2

    menu = pygameMenu.Menu(300, 400,
                           theme=pygameMenu.themes.THEME_BLUE,
                           title='Welcome')

.. note:: The theme parameters can be overwritten locally
          when adding a widget to the menu. See the overwritable
          ones in the :ref:`add_... methods <Adding widgets>`

Default themes
--------------

Several predefined themes are proposed by :py:mod:`pygame-menu`.

==============================================  ================================================
Theme                                           Example
==============================================  ================================================
:py:data:`pygameMenu.themes.THEME_DEFAULT`      .. image:: ../_static/theme_default.png
:py:data:`pygameMenu.themes.THEME_BLACK`        .. image:: ../_static/theme_black.png
:py:data:`pygameMenu.themes.THEME_BLUE`         .. image:: ../_static/theme_blue.png
:py:data:`pygameMenu.themes.THEME_GREEN`        .. image:: ../_static/theme_green.png
:py:data:`pygameMenu.themes.THEME_ORANGE`       .. image:: ../_static/theme_orange.png
:py:data:`pygameMenu.themes.THEME_SOLARIZED`    .. image:: ../_static/theme_solarized.png
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

    mytheme = pygameMenu.themes.THEME_ORANGE.copy()
    mytheme.title_background_color=(0, 0, 0)

    menu = Menu(..., theme=mytheme)


.. autoclass:: Theme
    :members:
