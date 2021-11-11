"""
pygame-menu
https://github.com/ppizarror/pygame-menu

MENULINK
Similar to a Button that opens a Menu, MenuLink is a widget that contains a Menu
reference. This Menu can be opened with .open() method.
"""

__all__ = [
    'MenuLink',
    'MenuLinkManager'
]

import pygame_menu

from abc import ABC
from pygame_menu.widgets.core.widget import AbstractWidgetManager
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


class MenuLinkManager(AbstractWidgetManager, ABC):
    """
    MenuLink manager.
    """

    def menu_link(
            self,
            menu: 'pygame_menu.Menu',
            link_id: str = ''
    ) -> 'pygame_menu.widgets.MenuLink':
        """
        Adds a link to another Menu. The behaviour is similar to a button, but
        this widget is invisible, and cannot be selectable.

        Added menus can be opened using the ``.open()`` method. Opened menus change
        the state of the parent Menu (the current pointer).

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param menu: Menu to be added as a link (the new submenu)
        :param link_id: ID of the menu link
        :return: Menu link widget
        :rtype: :py:class:`pygame_menu.widgets.MenuLink`
        """
        if isinstance(menu, type(self._menu)):
            # Check for recursive
            if menu == self._menu or menu.in_submenu(self._menu, recursive=True):
                raise ValueError(
                    f'Menu "{menu.get_title()}" is already on submenu structure,'
                    f' recursive menus lead to unexpected behaviours. For '
                    f'returning to previous menu use pygame_menu.events.BACK '
                    f'event defining an optional back_count number of menus to '
                    f'return from, default is 1'
                )

        else:
            raise ValueError('menu object is not a pygame_menu.Menu class')

        # noinspection PyProtectedMember
        widget = MenuLink(
            menu=menu,
            menu_opener_handler=self._menu._open,
            link_id=link_id
        )
        self.configure_defaults_widget(widget)
        self._append_widget(widget)
        self._add_submenu(menu, widget)

        return widget
