
====================
Package organization
====================

The :py:mod:`pgameMenu.widgets` package contains the widget support for the Menu.
Its structure consists of several sub-packages::

    core/           Main object classes for Widget and Selector
    examples/       Some examples of widgets
    selection/      Selection effect applied to widgets
    widget/         Menu widget objects


===============
Create a widget
===============

All widget classes shall inherit from :py:class:`pygameMenu.widgets.Widget`,
and they must be located in the :py:mod:`pgameMenu.widgets` package. The most
basic widget should contain this code:

.. code-block:: python

    from pygameMenu.widgets import Widget

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

.. warning:: After creating the widget, it must be added to  ``__init__.py`` file of the
             :py:mod:`pgameMenu.widgets` package.

.. code-block:: python

    from pygameMenu.widgets import MyWidget

For adding the widget to the :py:class:`pygameMenu.menu.Menu` this class must be extended
with a public method :py:meth:`pygameMenu.menu.Menu.add_mywidget` with the following
structure:

.. code-block:: python

    import pygameMenu.widgets as _widgets

    class Menu(object):
        ...

        def add_mymenu(self, params, **kwargs):
            """
            Add MyWidget to the menu.
            """
            attributes = self._current._filter_widget_attributes(kwargs)

            # Create your widget
            widget = _widgets.MyWidget(..., **kwargs)

            self._current._configure_widget(widget=widget, **attributes)
            self._current._append_widget(widget)
            return widget

        ...

.. note:: This method uses **kwargs** parameter for defining the settings of the
          Widget as the background, margin, etc. This is applied automatically
          by the Menu in :py:meth:`pygameMenu.menu.Menu._configure_widget`
          method. If **MyWidget** needs additional parameters please use some that
          are not named as the default kwargs used by the Menu Widget system.

=========================
Create a selection effect
=========================

The widgets in Menu are drawn with the following idea:

1. Each time a new Widget is added regenerate the position of them.
2. Widgets can be active or not. The active widget will catch user events as keyboard or mouse.
3. Active widgets have a decoration, named *Selection*
4. The drawing process is:
   1. Draw Menu background color/image
   2. Draw all widgets
   3. Draw *Selection* decoration on selected widget surface area
   4. Draw the menubar
   5. Draw the scrollbar

For defining a new selection effect a new :py:class:`pygameMenu.widgets.core.selection.Selection`
object must be added to ``selection`` package . A basic object must contain the following code:

.. code-block:: python

    from pygameMenu.widgets import Selection

    class MySelection(Selection):

        def __init__(self):
            super(MySelection, self).__init__(params)

        def get_margin(self):
            """
            As selection decorations can be described with a box, this method must return
            the additional margin of the selection. If the margin is zero, then the selection
            size is the same as the original widget.

            The method must return the width of the bottom, left, top and right margins.

             --------------------------
            |          ^ top           | In this example, XXXX represents the
            | left  XXXXXXXXXXXX right | Widget to be Selected.
            |<----> XXXXXXXXXXXX<----->|
            |         v bottom         |
             --------------------------

             All distances must be in pixels (px).
            """
            return top, left, bottom, right

        def draw(self, surface, widget):
            """
            This method receives the surface to draw the selection and the
            widget itself. For retrieving the Selection coordinates the rect
            object from widget should be used.
            """
            surface.draw(.....)

.. warning:: After creating the selection effect, it must be added to  ``__init__.py`` file of the
             :py:mod:`pgameMenu.widgets` package.

.. code-block:: python

    from pygameMenu.widgets import MySelection

Finally, this new selection effect can be used following one of these two ways:

1. Pass it when adding ad new widget to the menu

    .. code-block:: python

        import pygameMenu

        menu = pygameMenu.Menu(...)

        menu.add_button(..., selection_effect=pygameMenu.widgets.MySelection(...))

2. To apply it on alls menus and widgets (and avoid passing it for each added widget),
   a theme can be created

    .. code-block:: python

        import pygameMenu

        MY_THEME = pygameMenu.Theme(
            ...,
            widget_selection_effect=pygameMenu.widgets.MySelection(...)
        )

        menu = pygameMenu.Menu(..., theme=MY_THEME)
