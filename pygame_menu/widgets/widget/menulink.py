"""
pygame-menu
https://github.com/ppizarror/pygame-menu

MENULINK
Similar to a Button that opens a Menu, MenuLink is a widget that contains a Menu
reference. This Menu can be opened with .open() method.
"""

from __future__ import annotations

__all__ = ["MenuLink"]

from typing import TYPE_CHECKING

from pygame_menu.widgets.widget.none import NoneWidget

if TYPE_CHECKING:
    from collections.abc import Callable

    import pygame_menu


class MenuLink(NoneWidget):
    """
    Menu link widget; adds a link to another Menu. The behavior is similar to a
    button, but this widget is invisible, and cannot be selectable.

    .. note::

        MenuLink does not accept transformations.

    :param link_id: Link ID
    :param menu_opener_handler: Callback for opening the menu object
    :param menu: Menu object
    """

    menu: pygame_menu.Menu

    def __init__(
        self, menu: pygame_menu.Menu, menu_opener_handler: Callable, link_id: str = ""
    ) -> None:
        assert callable(menu_opener_handler), (
            "menu opener handler must be callable (a function)"
        )
        super().__init__(widget_id=link_id, visible=False)
        self.menu = menu
        self._onreturn = menu_opener_handler

    def hide(self) -> MenuLink:
        pass

    def show(self) -> MenuLink:
        pass

    def open(self) -> None:
        """
        Open the menu link.
        """
        return self._onreturn(self.menu)
