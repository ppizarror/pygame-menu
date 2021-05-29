"""
pygame-menu
https://github.com/ppizarror/pygame-menu

MENULINK
Similar to a Button that opens a Menu, MenuLink is a widget that contains a Menu
reference. This Menu can be opened with .open() method.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
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
