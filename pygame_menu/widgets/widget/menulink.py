"""
pygame-menu
https://github.com/ppizarror/pygame-menu

MENULINK
Similar to a Button that opens a Menu, MenuLink is a widget that contains a Menu
reference. This Menu can be opened with .open() method.
"""

__all__ = ['MenuLink']

import pygame_menu

from pygame_menu.widgets.widget.none import NoneWidget
from pygame_menu.utils import is_callable

from pygame_menu._types import Callable


# noinspection PyMissingOrEmptyDocstring
class MenuLink(NoneWidget):
    """
    Menu link widget; adds a link to another Menu. The behaviour is similar to a
    button, but this widget is invisible, and cannot be selectable.

    .. note::

        MenuLink does not accept any transformation.

    :param link_id: Link ID
    :param menu_opener_handler: Callback for opening the menu object
    :param menu: Menu object
    """
    menu: 'pygame_menu.Menu'

    def __init__(
            self,
            menu: 'pygame_menu.Menu',
            menu_opener_handler: Callable,
            link_id: str = ''
    ) -> None:
        assert isinstance(menu, pygame_menu.Menu)
        assert is_callable(menu_opener_handler), \
            'menu opener handler must be callable (a function)'
        super(MenuLink, self).__init__(
            widget_id=link_id
        )
        self.menu = menu
        self._onreturn = menu_opener_handler
        self._visible = False
        self.is_selectable = False

    def hide(self) -> 'MenuLink':
        pass

    def show(self) -> 'MenuLink':
        pass

    def open(self) -> None:
        return self._onreturn(self.menu)
