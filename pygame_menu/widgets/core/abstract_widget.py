"""
pygame-menu
https://github.com/ppizarror/pygame-menu

ABSTRACT WIDGET MANAGER
Base class for AbstractWidgetManager.
"""

from __future__ import annotations

__all__ = [
    # Main class
    "AbstractWidgetManager",
]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pygame_menu
    from pygame_menu.widgets.core.widget import Widget


class AbstractWidgetManager(ABC):
    """
    Add/Remove widgets to the Menu.
    """

    _menu: pygame_menu.Menu

    def __init__(self) -> None:
        pass

    @property
    @abstractmethod
    def _theme(self) -> pygame_menu.Theme:
        """
        Return menu theme.

        :return: Menu theme reference
        """
        pass

    @abstractmethod
    def _add_submenu(self, menu: pygame_menu.Menu, hook: Widget) -> None:
        """
        Adds a submenu. Requires the menu instance and the widget that adds the
        sub-menu.

        :param menu: Menu reference
        :param hook: Widget hook
        """
        pass

    @abstractmethod
    def _filter_widget_attributes(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        """
        Return the valid widgets attributes from a dictionary.

        The valid (key, value) are removed from the initial dictionary.

        :param kwargs: Optional keyword arguments (input attributes)
        :return: Dictionary of valid attributes
        """
        pass

    @abstractmethod
    def _configure_widget(self, widget: Widget, **kwargs: Any) -> None:
        """
        Update the given widget with the parameters defined at the Menu level.
        This method does not add widget to Menu.

        :param widget: Widget object
        :param kwargs: Optional keywords arguments
        """
        pass

    @staticmethod
    @abstractmethod
    def _check_kwargs(kwargs: dict[str, Any]) -> None:
        """
        Check kwargs after widget addition. It should be empty. Raises ``ValueError``.

        :param kwargs: Kwargs dict
        """
        pass

    @abstractmethod
    def _append_widget(self, widget: Widget) -> None:
        """
        Add a widget to the list of widgets.

        :param widget: Widget object
        """
        pass

    @abstractmethod
    def configure_defaults_widget(self, widget: Widget) -> None:
        """
        Apply default menu settings to widget. This method does not add widget to
        the Menu.

        :param widget: Widget to be configured
        """
        pass
