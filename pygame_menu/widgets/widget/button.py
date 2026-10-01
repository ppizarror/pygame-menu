"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BUTTON
Button widget. Basically, a label with callback function and enhanced events.
"""

from __future__ import annotations

__all__ = ["Button"]

from typing import TYPE_CHECKING, Any

import pygame

from pygame_menu.locals import FINGERUP
from pygame_menu.utils import get_finger_pos
from pygame_menu.widgets.widget.label import Label

if TYPE_CHECKING:
    from collections.abc import Callable

    import pygame_menu
    from pygame_menu._types import CallbackType, EventVectorType
    from pygame_menu.widgets.core.widget import Widget


class Button(Label):
    """
    Button widget.

    The arguments and unknown keyword arguments are passed to the ``onreturn``
    function:

    .. code-block:: python

        onreturn(*args, **kwargs)

    .. note::

        Button accepts all transformations.

    :param title: Button title
    :param button_id: Button ID
    :param onreturn: Callback when pressing the button
    :param args: Optional arguments for callbacks
    :param kwargs: Optional keyword arguments
    """

    to_menu: bool

    def __init__(
        self,
        title: Any,
        button_id: str = "",
        onreturn: CallbackType = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(title=title, label_id=button_id, accept_events=True)
        self._args = list(args)
        self._kwargs = kwargs
        self.set_onreturn(onreturn)
        self.to_menu = False  # True if button opens a new Menu

    def set_selection_callback(
        self, callback: Callable[[bool, Widget, pygame_menu.Menu], Any] | None
    ) -> None:
        """
        Update the button selection callback, once button is selected, the callback
        function is executed as follows:

        .. code-block:: python

            callback(selected, widget, menu)

        :param callback: Callback when selecting the widget, executed in :py:meth:`pygame_menu.widgets.core.widget.Widget.set_selected`
        """
        if callback is not None:
            assert callable(callback), (
                "callback must be callable (function-type) or None"
            )
        self._onselect = callback

    def update_callback(self, callback: Callable, *args: Any) -> None:
        """
        Update function triggered by the button; ``callback`` cannot point to a Menu, that
        behavior is only valid using :py:meth:`pygame_menu.menu.Menu.add.button` method.

        .. note::

            If button points to a submenu, and the callback is changed to a
            function, the submenu will be removed from the parent Menu. Thus
            preserving the structure.

        :param callback: Function
        :param args: Arguments used by the function once triggered
        """
        assert callable(callback), "only callable (function-type) are allowed"

        # If return is a Menu object, remove it from submenus list
        if self._menu is not None and self._onreturn is not None and self.to_menu:
            assert len(self._args) == 1
            submenu = self._args[0]  # Menu
            assert self._menu.in_submenu(submenu), (
                "pointed menu is not in submenu list of parent container"
            )
            # noinspection PyProtectedMember
            assert self._menu._remove_submenu(submenu, self), (
                "submenu could not be removed"
            )
            self.to_menu = False

        self._args = args or []
        self._onreturn = callback

    def _draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surface, self._rect.topleft)

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)
        rect: pygame.Rect = self.get_rect(to_real_position=True)

        if self.readonly or not self.is_visible():
            self._readonly_check_mouseover(events, rect)
            return False

        for event in events:
            # Check mouse over
            self._check_mouseover(event, rect)

            # User applies with key
            if (
                event.type == pygame.KEYDOWN
                and self._keyboard_enabled
                and self._ctrl.apply(event, self)
                or event.type == pygame.JOYBUTTONDOWN
                and self._joystick_enabled
                and self._ctrl.joy_select(event, self)
            ):
                if self.to_menu:
                    self._sound.play_open_menu()
                else:
                    self._sound.play_key_add()
                self.apply()
                return True

            # User clicks the button; don't consider the mouse wheel (button 4 & 5)
            elif (
                event.type == pygame.MOUSEBUTTONUP
                and self._mouse_enabled
                and event.button in (1, 2, 3)
                or event.type == FINGERUP
                and self._touchscreen_enabled
                and self._menu is not None
            ):
                if event.type == pygame.MOUSEBUTTONUP:
                    self._sound.play_click_mouse()
                else:
                    self._sound.play_click_touch()

                event_pos = get_finger_pos(self._menu, event)
                if rect.collidepoint(*event_pos):
                    self.apply()
                    return True

        return False
