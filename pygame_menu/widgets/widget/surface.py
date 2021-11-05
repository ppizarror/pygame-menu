"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SURFACE
Surface widget. This widget contains an external surface.
"""

__all__ = ['SurfaceWidget']

import pygame

from pygame_menu.widgets.core.widget import Widget, WidgetTransformationNotImplemented

from pygame_menu._types import CallbackType, Optional, EventVectorType


# noinspection PyMissingOrEmptyDocstring
class SurfaceWidget(Widget):
    """
    Surface widget. Implements a widget from a external surface.

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
