
====================
Package organization
====================

The :py:mod:`pygame_menu.widgets` package contains the widget support for the Menu.
Its structure consists of several sub-packages::

    pygame_menu/
        widgets/
            core/           Main object classes for Widget and Selector
            examples/       Some examples of widgets
            selection/      Selection effect applied to widgets
            widget/         Menu widget objects


===============
Create a widget
===============

All widget classes shall inherit from :py:class:`pygame_menu.widgets.core.widget.Widget`,
and they must be located in the :py:mod:`pygame_menu.widgets.widget` package. The most
basic widget should contain this code:

.. code-block:: python

    from pygame_menu.widgets.core.widget import Widget

    class MyWidget(Widget):

        def __init__(self, params):
            super(MyWidget, self).__init__(params)
            ...

        def _apply_font(self):
            """
            Function triggered after a font is applied to the widget
            by Menu._configure_widget() method.
            """
            ...

        def draw(self, surface):
            """
            Draw the widget shape.
            """
            # Required, render first, then draw
            self._render()

            # Draw the background of the Widget (optional)
            self._fill_background_color(surface)

            # Draw the self._surface pygame object on the given surface
            surface.blit(self._surface, self._rect.topleft)

        def _render(self):
            """
            Render the widget surface.
            This method shall update the attribute _surface with a pygame.Surface
            representing the outer borders of the widget.
            """
            # Generate widget surface
            self._surface = pygame.surface....
            # Update the width and height of the Widget
            self._rect.width, self._rect.height = self._surface.get_size() + SomeConstants

        def update(self, events):
            """
            Update internal variable according to the given events list
            and fire the callbacks.
            """
            ...
            return False

.. warning:: After creating the widget, it must be added to the  ``__init__.py`` file of the
             :py:mod:`pygame_menu.widgets` package.

             .. code-block:: python

                 from pygame_menu.widgets.widget.mywidget import MyWidget

To add the widget to the :py:class:`pygame_menu.Menu` class, a public method
:py:meth:`pygame_menu.Menu.add_mywidget` with the following structure has to be
added:

.. code-block:: python

    import pygame_menu.widgets as _widgets

    class Menu(object):
        ...

        def add_mywidget(self, params, current=False, **kwargs):
            """
            Add MyWidget to the menu.
            """
            attributes = self._filter_widget_attributes(kwargs)

            # Create your widget
            widget = _widgets.MyWidget(..., **kwargs)

            self._configure_widget(widget=widget, **attributes)
            self._append_widget(widget)
            return widget

        ...

.. note:: This method uses the **kwargs** parameter for defining the settings of the
          Widget, such as the background, margin, etc. This is applied automatically
          by the Menu in :py:meth:`pygame_menu.Menu._configure_widget`
          method. If **MyWidget** needs additional parameters, please use some that
          are not named as the default kwargs used by the Menu Widget system.

          The function must return the created `widget` object.


=========================
Create a selection effect
=========================

The widgets in Menu are drawn with the following idea:

#. Each time a new Widget is added, regenerate their position.
#. Widgets can either be active or inactive. The active widget will catch user events as keyboard or mouse.
#. Active widgets have a decoration, named *Selection*
#. The drawing process is:

 #. Draw Menu background color/image
 #. Draw all widgets
 #. Draw *Selection* decoration on selected widget surface area
 #. Draw menubar
 #. Draw scrollbar

For defining a new selection effect, a new :py:class:`pygame_menu.widgets.core.Selection`
subclass must be added to the :py:mod:`pygame_menu.widgets.selection` package. A basic class must
contain the following code:

.. code-block:: python

    from pygame_menu.widgets.core.selection import Selection

    class MySelection(Selection):

        def __init__(self):
            # Call the constructor of the Selection providing the left, right, top and bottom margins
            # of your Selection effect box.
            #
            #  --------------------------
            # |          ^ top           |  In this example, XXXX represents the
            # | left  XXXXXXXXXXXX right |  Widget to be Selected.
            # |<----> XXXXXXXXXXXX<----->|  left, right, top and bottom must be described
            # |         v bottom         |  in pixels
            #  --------------------------
            #
            super(MySelection, self).__init__(margin_left, margin_right, margin_top, margin_bottom)
            self.your_params = ...

        def draw(self, surface, widget):
            """
            This method receives the surface to draw the selection and the
            widget itself. For retrieving the Selection coordinates the rect
            object from widget should be used.
            """
            surface.draw(.....)

.. warning:: After creating the selection effect, it must be added to  ``__init__.py`` file of the
             :py:mod:`pygame_menu.widgets` package.

             .. code-block:: python

                 from pygame_menu.widgets.selection.myselection import MySelection

Finally, this new selection effect can be set by following one of these two instructions:

1. Pass it when adding a new widget to the menu

    .. code-block:: python

        import pygame_menu

        menu = pygame_menu.Menu(...)
        menu.add_button(..., selection_effect=pygame_menu.widgets.MySelection(...))

2. To apply it on all menus and widgets (and avoid passing it for each added widget),
   a theme can be created

    .. code-block:: python

        import pygame_menu

        MY_THEME = pygame_menu.themes.Theme(
            ...,
            widget_selection_effect=pygame_menu.widgets.MySelection(...)
        )

        menu = pygame_menu.Menu(..., theme=MY_THEME)
