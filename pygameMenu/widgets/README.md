# pygame-menu Widgets

This module contains the widget support for the Menu. The basic structure of the module consists of:

```
core/           Main object classes for Widget and Selector
examples/       Some examples of widgets
selection/      Selection effect applied to widgets
widget/         Menu widget objects
```

## Widget

All widget object must import [Widget](https://github.com/ppizarror/pygame-menu/blob/master/pygameMenu/widgets/core/widget.py) from `pygameMenu.widgets.core.widget`, and they must be located on `widgets/` directory. The most basic widget should contain this code:

```python
from pygameMenu.widgets.core.widget import Widget

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

```

After creating the widget, it must be added to  `__init__.py` file on this directory.

```python
from pygameMenu.widgets.widget.mywidget import MyWidget
```

For adding the widget to the [Menu](https://github.com/ppizarror/pygame-menu/blob/master/pygameMenu/menu.py) this class must be extended with a public method `add_mywidget()` with the following structure:

`pygameMenu.menu.py:`

```python
import pygameMenu.widgets as _widgets

class Menu(object):
    ...

    def add_mymenu(self, params, **kwargs):
        """
        Add MyWidget to the menu.
        """
        attributes = self._current._filter_widget_attributes(kwargs)
        widget = _widgets.MyWidget(..., **kwargs) # Create your widget
        self._current._configure_widget(widget=widget, **attributes)
        self._current._append_widget(widget)
        return widget
    ...

```

Note that this method uses *kwargs* parameter for defining the settings of the Widget as the background, margin, etc. This is applied automatically by the Menu in `_configure_widget()` method. If *MyWidget* needs additional parameters please use some that are not named as the default kwargs used by the Menu Widget system.

## Selection

The widgets in Menu are drawn with the following idea:

1. Each time a new Widget is added regenerate the position of them.
2. Widgets can be active or not. The active widget will catch user events as keyboard or mouse.
3. Active widgets have a decoration, named *Selection*
4. The drawing process is:
   1. Draw Menu background color/image
   2. Draw all widgets
   3. Draw *Selection* decoration on seleceted widget surface area
   4. Draw the menubar
   5. Draw the scrollbar

For defining a new selection effect a new [Selection](https://github.com/ppizarror/pygame-menu/blob/master/pygameMenu/widgets/core/selection.py) object must be added to `selection/` module. A basic object must contain the following code:

```python
from pygameMenu.widgets.core.selection import Selection

class MySelection(Selection):

    def __init__(self):
        super(MySelection, self).__init__(params)

    def get_margin(self):
        """
        As selection decorations can be described with a box, this method must return the additional margin of the selection. If the margin is zero, then the selection size is the same as the original widget.

        The method must return the width of the bottom, left, top and right margins.

         --------------------------
        |           ^ top          | In this example, XXXX represents the
        | left  XXXXXXXXXXXX right | Widget to be Selected.
        |<----> XXXXXXXXXXXX<----->|
        |           v bottom       |
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

```

After creating the widget, it must be added to  `__init__.py` file on this directory.

```python
from pygameMenu.widgets.selection.myselection import MySelection
```

Finally, for using this Selection the [Theme](https://github.com/ppizarror/pygame-menu/blob/master/pygameMenu/themes.py).*widget_selection_effect* must be created using a new instance of *MySelection*. For example:

```python
import pygameMenu

NEW_THEME = pygameMenu.Theme(
    ...,
    widget_selection_effect=pygameMenu.widgets.MySelection(...)
)

```
