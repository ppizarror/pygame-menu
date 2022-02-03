"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SURFACE
Surface widget. This widget contains an external surface.
"""

__all__ = [
    'SurfaceWidget',
    'SurfaceWidgetManager'
]

import pygame
import pygame_menu

from abc import ABC
from pygame_menu.widgets.core.widget import Widget, WidgetTransformationNotImplemented, \
    AbstractWidgetManager

from pygame_menu._types import CallbackType, Optional, EventVectorType, Callable, \
    Any


# noinspection PyMissingOrEmptyDocstring
class SurfaceWidget(Widget):
    """
    Surface widget. Implements a widget from an external surface.

    .. note::

        SurfaceWidget only accepts translation transformation.

    :param surface: Pygame surface object
    :param surface_id: Surface ID
    :param onselect: Function when selecting the widget
    """
    _surface_obj: 'pygame.Surface'

    def __init__(
            self,
            surface: 'pygame.Surface',
            surface_id: str = '',
            onselect: CallbackType = None
    ) -> None:
        assert isinstance(surface, pygame.Surface)
        assert isinstance(surface_id, str)

        super(SurfaceWidget, self).__init__(
            onselect=onselect,
            widget_id=surface_id
        )
        self._surface_obj = surface

    def set_title(self, title: str) -> 'SurfaceWidget':
        return self

    def set_surface(self, surface: 'pygame.Surface') -> 'SurfaceWidget':
        """
        Update the widget surface.
        
        :param surface: New surface
        :return: Self reference
        """
        assert isinstance(surface, pygame.Surface)
        self._surface_obj = surface
        self._render()
        self.force_menu_surface_update()
        return self

    def _apply_font(self) -> None:
        pass

    def scale(self, *args, **kwargs) -> 'SurfaceWidget':
        raise WidgetTransformationNotImplemented()

    def resize(self, *args, **kwargs) -> 'SurfaceWidget':
        raise WidgetTransformationNotImplemented()

    def set_max_width(self, *args, **kwargs) -> 'SurfaceWidget':
        raise WidgetTransformationNotImplemented()

    def set_max_height(self, *args, **kwargs) -> 'SurfaceWidget':
        raise WidgetTransformationNotImplemented()

    def rotate(self, *args, **kwargs) -> 'SurfaceWidget':
        raise WidgetTransformationNotImplemented()

    def flip(self, *args, **kwargs) -> 'SurfaceWidget':
        raise WidgetTransformationNotImplemented()

    def _draw(self, surface: 'pygame.Surface') -> None:
        surface.blit(self._surface_obj, self._rect.topleft)

    def get_surface(self) -> 'pygame.Surface':
        return self._surface_obj

    def _render(self) -> Optional[bool]:
        self._rect.width, self._rect.height = self._surface_obj.get_size()
        return

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)
        for event in events:
            if self._check_mouseover(event):
                break
        return False


class SurfaceWidgetManager(AbstractWidgetManager, ABC):
    """
    SurfaceWidget manager.
    """

    def surface(
            self,
            surface: 'pygame.Surface',
            surface_id: str = '',
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            selectable: bool = False,
            **kwargs
    ) -> 'pygame_menu.widgets.SurfaceWidget':
        """
        Add a surface widget to the Menu.

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``float``                         (bool) - If ``True`` the widget don't contribute width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect. Applied only if ``selectable`` is ``True``
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param surface: Pygame surface object
        :param surface_id: Surface ID
        :param onselect: Callback executed when selecting the widget; only executed if ``selectable`` is ``True``
        :param selectable: Surface accepts user selection
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.SurfaceWidget`
        """
        assert isinstance(selectable, bool)

        # Remove invalid keys from kwargs
        for key in list(kwargs.keys()):
            if key not in ('align', 'background_color', 'background_inflate',
                           'border_color', 'border_inflate', 'border_width',
                           'cursor', 'margin', 'padding', 'selection_color',
                           'selection_effect', 'border_position', 'float',
                           'float_origin_position', 'shadow_color', 'shadow_radius',
                           'shadow_type', 'shadow_width'):
                kwargs.pop(key, None)

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        widget = SurfaceWidget(
            surface=surface,
            surface_id=surface_id,
            onselect=onselect
        )
        widget.is_selectable = selectable

        self._check_kwargs(kwargs)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget
