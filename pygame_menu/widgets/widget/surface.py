"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SURFACE
Surface widget. This widget contains an external surface.
"""

from __future__ import annotations

__all__ = ["SurfaceWidget"]

from typing import TYPE_CHECKING, Any

import pygame

from pygame_menu.widgets.core.widget import (
    Widget,
    WidgetTransformationNotImplemented,
)

if TYPE_CHECKING:
    from pygame_menu._types import CallbackType, EventVectorType


class SurfaceWidget(Widget):
    """
    Surface widget. Implements a widget from an external surface.

    .. note::

        SurfaceWidget only accepts translation transformation.

    :param surface: Pygame surface object
    :param surface_id: Surface ID
    :param onselect: Function when selecting the widget
    """

    _surface_obj: pygame.Surface

    def __init__(
        self,
        surface: pygame.Surface,
        surface_id: str = "",
        onselect: CallbackType = None,
    ) -> None:
        assert isinstance(surface, pygame.Surface)
        assert isinstance(surface_id, str)

        super().__init__(onselect=onselect, widget_id=surface_id)
        self._surface_obj = surface

    def set_title(self, title: str, *args: Any) -> SurfaceWidget:
        return self

    def set_surface(self, surface: pygame.Surface) -> SurfaceWidget:
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

    def scale(self, *args: Any, **kwargs: Any) -> SurfaceWidget:
        raise WidgetTransformationNotImplemented()

    def resize(self, *args: Any, **kwargs: Any) -> SurfaceWidget:
        raise WidgetTransformationNotImplemented()

    def set_max_width(self, *args: Any, **kwargs: Any) -> SurfaceWidget:
        raise WidgetTransformationNotImplemented()

    def set_max_height(self, *args: Any, **kwargs: Any) -> SurfaceWidget:
        raise WidgetTransformationNotImplemented()

    def rotate(self, *args: Any, **kwargs: Any) -> SurfaceWidget:
        raise WidgetTransformationNotImplemented()

    def flip(self, *args: Any, **kwargs: Any) -> SurfaceWidget:
        raise WidgetTransformationNotImplemented()

    def _draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surface_obj, self._rect.topleft)

    def get_surface(self) -> pygame.Surface:
        return self._surface_obj

    def _render(self) -> bool | None:
        self._rect.width, self._rect.height = self._surface_obj.get_size()
        return None

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)
        for event in events:
            if self._check_mouseover(event):
                break
        return False
