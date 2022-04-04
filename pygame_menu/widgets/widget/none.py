"""
pygame-menu
https://github.com/ppizarror/pygame-menu

NONE WIDGET
None widget definition.
"""

__all__ = [
    'NoneWidget',
    'NoneWidgetManager'
]

import pygame
import pygame_menu

from abc import ABC
from pygame_menu.utils import make_surface
from pygame_menu.widgets.core.widget import Widget, WidgetTransformationNotImplemented, \
    AbstractWidgetManager

from pygame_menu._types import Optional, NumberType, EventVectorType


# noinspection PyMissingOrEmptyDocstring
class NoneWidget(Widget):
    """
    None widget. Useful if used for filling column/row layout. None widget don't
    accept values, padding, margin, cursors, position, sound, controls, and
    cannot be selected. Also, none widget cannot accept callbacks, except draw
    and update callbacks.

    .. note::

        NoneWidget does not accept any transformation.

    :param widget_id: ID of the widget
    """

    def __init__(
            self,
            widget_id: str = ''
    ) -> None:
        super(NoneWidget, self).__init__(widget_id=widget_id)
        self.is_selectable = False
        self._surface = make_surface(0, 0, alpha=True)

    def _apply_font(self) -> None:
        pass

    def set_padding(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def get_selected_time(self) -> NumberType:
        return 0

    def set_title(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def get_rect(self, *args, **kwargs) -> 'pygame.Rect':
        return pygame.Rect(0, 0, 0, 0)

    def set_background_color(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def _draw_background_color(self, *args, **kwargs) -> None:
        pass

    def _draw_border(self, *args, **kwargs) -> None:
        pass

    def set_selection_effect(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def apply(self, *args) -> None:
        pass

    def change(self, *args) -> None:
        pass

    def _draw(self, *args, **kwargs) -> None:
        pass

    def _render(self, *args, **kwargs) -> Optional[bool]:
        pass

    def set_margin(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def _apply_transforms(self, *args, **kwargs) -> None:
        pass

    def set_font(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def update_font(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_position(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def scale(self, *args, **kwargs) -> 'NoneWidget':
        raise WidgetTransformationNotImplemented()

    def resize(self, *args, **kwargs) -> 'NoneWidget':
        raise WidgetTransformationNotImplemented()

    def set_max_width(self, *args, **kwargs) -> 'NoneWidget':
        raise WidgetTransformationNotImplemented()

    def set_max_height(self, *args, **kwargs) -> 'NoneWidget':
        raise WidgetTransformationNotImplemented()

    def rotate(self, *args, **kwargs) -> 'NoneWidget':
        raise WidgetTransformationNotImplemented()

    def flip(self, *args, **kwargs) -> 'NoneWidget':
        raise WidgetTransformationNotImplemented()

    def translate(self, *args, **kwargs) -> 'NoneWidget':
        raise WidgetTransformationNotImplemented()

    def select(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_font_shadow(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_sound(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_cursor(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_controls(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_border(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def _check_mouseover(self, *args, **kwargs) -> bool:
        self._mouseover = False
        return False

    def mouseleave(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def mouseover(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_onchange(self, *args, **kwargs) -> 'NoneWidget':
        self._onchange = None
        return self

    def set_onreturn(self, *args, **kwargs) -> 'NoneWidget':
        self._onreturn = None
        return self

    def set_onmouseleave(self, *args, **kwargs) -> 'NoneWidget':
        self._onmouseleave = None
        return self

    def set_onmouseover(self, *args, **kwargs) -> 'NoneWidget':
        self._onmouseover = None
        return self

    def set_onselect(self, *args, **kwargs) -> 'NoneWidget':
        self._onselect = None
        return self

    def set_tab_size(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def shadow(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)
        return False


class NoneWidgetManager(AbstractWidgetManager, ABC):
    """
    NoneWidget manager.
    """

    def none_widget(
            self,
            widget_id: str = ''
    ) -> 'pygame_menu.widgets.NoneWidget':
        """
        Add a none widget to the Menu.

        .. note::

            This widget is useful to fill column/rows layout without compromising
            any visuals. Also, it can be used to store information or even to add
            a ``draw_callback`` function to it for being called on each Menu draw.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
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
