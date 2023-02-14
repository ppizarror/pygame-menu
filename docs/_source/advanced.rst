====================
Package organization
====================

The :py:mod:`pygame_menu.widgets` package contains the widget support for the Menu.
Its structure consists of several sub-packages::

    pygame_menu/
        widgets/
            core/           Main object classes for Widget and Selector
            selection/      Selection effect applied to widgets
            widget/         Menu widget objects


===============
Create a widget
===============

All widget classes shall inherit from :py:class:`pygame_menu.widgets.core.widget.Widget`,
and they must be located in the :py:mod:`pygame_menu.widgets.widget` package. The
most basic widget should contain this code:

.. code-block:: python

    from pygame_menu.widgets.core.widget import Widget
    from pygame_menu._types import EventVectorType

    class MyWidget(Widget):

        def __init__(self, params):
            super(MyWidget, self).__init__(params)
            ...

        def _apply_font(self) -> None:
            """
            Function triggered after a font is applied to the widget
            by Menu._configure_widget() method.
            """
            ...

        def _draw(self, surface: 'pygame.Surface') -> None:
            """
            Draw the widget on a given surface.
            This method must be overridden by all classes.
            """
            # Draw the self._surface pygame object on the given surface
            surface.blit(self._surface, self._rect.topleft)

        def _render(self) -> Optional[bool]:
            """
            Render the Widget surface.

            This method shall update the attribute ``_surface`` with a :py:class:`pygame.Surface`
            object representing the outer borders of the widget.

            .. note::

                Before rendering, check out if the widget font/title/values are
                set. If not, it is probable that a zero-size surface is set.

            .. note::

                Render methods should call
                :py:meth:`pygame_menu.widgets.core.widget.Widget.force_menu_surface_update`
                to force Menu to update the drawing surface.

            :return: ``True`` if widget has rendered a new state, ``None`` if the widget has not changed, so render used a cache
            """
            ...

            # Generate widget surface
            self._surface = pygame.surface....

            # Update the width and height of the Widget
            self._rect.width, self._rect.height = self._surface.get_size() + SomeConstants

            # Force menu to update its surface on next Menu.render() call
            self.force_menu_surface_update()

        def update(self, events: EventVectorType) -> bool:
            """
            Update according to the given events list and fire the callbacks. This
            method must return ``True`` if it updated (the internal variables
            changed during user input).

            .. note::

                Update is not performed if the Widget is in ``readonly`` state or
                it's hidden. However, ``apply_update_callbacks`` method is called
                in most widgets, except :py:class:`pygame_menu.widgets.NoneWidget`.

            :param events: List/Tuple of pygame events
            :return: ``True`` if updated
            """
            ...
            return False

.. warning:: After creating the widget, it must be added to the ``__init__.py`` file of the
             :py:mod:`pygame_menu.widgets` package.

    .. code-block:: python

        from pygame_menu.widgets.widget.mywidget import MyWidget

To add the widget to the :py:class:`pygame_menu.menu.Menu` class, a public method
:py:meth:`add_mywidget` must be added to the :py:class:`pygame_menu._widgetmanager.WidgetManager`
class with the following structure. Or :py:meth:`pygame_menu._widgetmanager.WidgetManager.generic_widget`
can be used.

.. code-block:: python

    import pygame_menu.widgets

    class WidgetManager(object):
        ...

        def mywidget(self, params, **kwargs):
            """
            Add MyWidget to the menu.
            """
            attributes = self._filter_widget_attributes(kwargs)

            # Create your widget
            widget = pygame_menu.widgets.MyWidget(..., **kwargs)

            self._configure_widget(widget=widget, **attributes)
            widget.set_default_value(default) # May add the default value
            self._append_widget(widget)

            return widget

        ...

.. note::

    This method uses the **kwargs** parameter for defining the settings of the
    Widget, such as the background, margin, etc. This is applied automatically
    by the Menu widget addition class (``WidgetManager``). If **MyWidget** needs
    additional parameters, please use some that are not named as the default kwargs
    used by the Menu Widget system.

    The function must return the created `widget` object.

.. note::

    The widget ``_render`` method should always call
    :py:meth:`pygame_menu.widgets.core.widget.Widget.force_menu_surface_update`
    method, this ensures that Menu updates the surface and the positioning.

.. note::

    From ``v4`` menu introduced a cache state for the draw surface. This cache
    is updated if any widget update its status (``update()`` returned True) or
    the surface was rendered. Anyway, execution-time elements that changes over
    time (outside ``_render``) should force cache rendering (for example the
    blinking cursor of text). If your widget has any property like this, the method
    :py:meth:`pygame_menu.widgets.core.widget.Widget.force_menu_surface_cache_update`
    must be called within your Widget.


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
subclass must be added to the :py:mod:`pygame_menu.widgets.selection` package. A
basic class must contain the following code:

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

.. warning::

    After creating the selection effect, it must be added to ``__init__.py`` file
    of the :py:mod:`pygame_menu.widgets` package.

    .. code-block:: python

        from pygame_menu.widgets.selection.myselection import MySelection

Finally, this new selection effect can be set by following one of these two
instructions:

1. Pass it when adding a new widget to the menu

    .. code-block:: python

        import pygame_menu

        menu = pygame_menu.Menu(...)
        menu.add.button(..., selection_effect=pygame_menu.widgets.MySelection(...))

2. To apply it on all menus and widgets (and avoid passing it for each added widget),
   a theme can be created

    .. code-block:: python

        import pygame_menu

        MY_THEME = pygame_menu.themes.Theme(
            ...,
            widget_selection_effect=pygame_menu.widgets.MySelection(...)
        )

        menu = pygame_menu.Menu(..., theme=MY_THEME)


=========================
Decorate a Menu / Widgets
=========================

All menu objects can be decorated with polygons (lines, circles, rectangles, paths),
images, text, or callable functions. The decorations can be drawn before the source
object (``prev``) or after the object (``post``) depending of the object type.

To add a decoration, you must access the decorator class from the object (Menu,
ScrollArea, any Widget) using ``get_decorator()`` method. And use the ``Decorator``
class API to add decorations to your object.

.. note::

    Decorations don't change the width/height of the object. These are visual/only.
    If applied on a widget, use padding to *enlarge* the widget rect if you need
    such feature.

.. note::

    For all decoration, the *(0, 0)* coordinate belongs to the center of the object.

.. code-block:: python

    decorator = my_widget.get_decorator()
    decorator.add_polygon([(1, 1), (1, 10), (10, 1)], color=(255, 0, 0))

    # If the widget needs a bigger margin
    my_widget.set_padding((25, 25, 10, 10))

    decorator = menu.get_decorator()
    decorator.add_line((10, 10), (100, 100), color=(45, 180, 34), width=10)


Decorator API
-------------

.. autoclass:: pygame_menu._decorator.Decorator
    :members:
