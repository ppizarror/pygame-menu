"""
pygame-menu
https://github.com/ppizarror/pygame-menu

NONE WIDGET
None widget definition.
"""

from __future__ import annotations

__all__ = ["NoneWidget", "NoneWidgetManager"]

from abc import ABC
from typing import TYPE_CHECKING, Any

import pygame

from pygame_menu.utils import make_surface
from pygame_menu.widgets.core.widget import (
    AbstractWidgetManager,
    Widget,
    WidgetTransformationNotImplemented,
)

if TYPE_CHECKING:
    import pygame_menu
    from pygame_menu._types import EventVectorType, NumberType


class NoneWidget(Widget):
    """
    None widget. Useful if used for filling column/row layout. None widget don't
    accept values, padding, margin, cursors, position, sound, controls, and
    cannot be selected. Also, none widget cannot accept callbacks, except draw
    and update callbacks.

    .. note::

        NoneWidget does not accept transformations.

    :param widget_id: ID of the widget
    """

    def __init__(self, widget_id: str = "", *, visible: bool = True) -> None:
        super().__init__(widget_id=widget_id, selectable=False, visible=visible)
        self._surface = make_surface(0, 0, alpha=True)

    def _apply_font(self) -> None:
        pass

    def set_padding(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def get_selected_time(self) -> NumberType:
        return 0

    def set_title(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def get_rect(self, *args: Any, **kwargs: Any) -> pygame.Rect:
        return pygame.Rect(0, 0, 0, 0)

    def set_background_color(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def _draw_background_color(self, *args: Any, **kwargs: Any) -> None:
        pass

    def _draw_border(self, *args: Any, **kwargs: Any) -> None:
        pass

    def set_selection_effect(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def apply(self, *args: Any) -> None:
        pass

    def change(self, *args: Any) -> None:
        pass

    def _draw(self, *args: Any, **kwargs: Any) -> None:
        pass

    def _render(self, *args: Any, **kwargs: Any) -> bool | None:
        pass

    def set_margin(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def _apply_transforms(self, *args: Any, **kwargs: Any) -> None:
        pass

    def set_font(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def update_font(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def set_position(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def scale(self, *args: Any, **kwargs: Any) -> NoneWidget:
        raise WidgetTransformationNotImplemented()

    def resize(self, *args: Any, **kwargs: Any) -> NoneWidget:
        raise WidgetTransformationNotImplemented()

    def set_max_width(self, *args: Any, **kwargs: Any) -> NoneWidget:
        raise WidgetTransformationNotImplemented()

    def set_max_height(self, *args: Any, **kwargs: Any) -> NoneWidget:
        raise WidgetTransformationNotImplemented()

    def rotate(self, *args: Any, **kwargs: Any) -> NoneWidget:
        raise WidgetTransformationNotImplemented()

    def flip(self, *args: Any, **kwargs: Any) -> NoneWidget:
        raise WidgetTransformationNotImplemented()

    def translate(self, *args: Any, **kwargs: Any) -> NoneWidget:
        raise WidgetTransformationNotImplemented()

    def select(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def set_font_shadow(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def set_sound(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def set_cursor(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def set_controls(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def set_border(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def _check_mouseover(self, *args: Any, **kwargs: Any) -> bool:
        self._mouseover = False
        return False

    def mouseleave(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def mouseover(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def set_onchange(self, *args: Any, **kwargs: Any) -> NoneWidget:
        self._onchange = None
        return self

    def set_onreturn(self, *args: Any, **kwargs: Any) -> NoneWidget:
        self._onreturn = None
        return self

    def set_onmouseleave(self, *args: Any, **kwargs: Any) -> NoneWidget:
        self._onmouseleave = None
        return self

    def set_onmouseover(self, *args: Any, **kwargs: Any) -> NoneWidget:
        self._onmouseover = None
        return self

    def set_onselect(self, *args: Any, **kwargs: Any) -> NoneWidget:
        self._onselect = None
        return self

    def set_tab_size(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def shadow(self, *args: Any, **kwargs: Any) -> NoneWidget:
        return self

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)
        return False


class NoneWidgetManager(AbstractWidgetManager, ABC):
    """
    NoneWidget manager.
    """

    def none_widget(self, widget_id: str = "") -> pygame_menu.widgets.NoneWidget:
        """
        Add a none widget to the Menu.

        .. note::

            This widget is useful to fill column/rows layout without compromising
            any visuals. Also, it can be used to store information or even to add
            a ``draw_callback`` function to it for being called on each Menu draw.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param widget_id: Widget ID
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.NoneWidget`
        """
        attributes = self._filter_widget_attributes({})

        widget = NoneWidget(widget_id=widget_id)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget
