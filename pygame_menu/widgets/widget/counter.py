from __future__ import annotations

__all__ = ["Counter", "CounterManager"]

from abc import ABC
from typing import TYPE_CHECKING

from pygame_menu.widgets.core.widget import AbstractWidgetManager
from pygame_menu.widgets.widget.label import Label

if TYPE_CHECKING:
    import pygame_menu


class Counter(Label):
    """
    Counter label widget.
    Displays an integer counter value dynamically formatted via a title generator.
    """

    _value: int
    _initial_value: int
    _title_format: str

    def __init__(
        self,
        value: int = 0,
        title_format: str = "{0}",
        label_id: str = "",
        **kwargs,
    ) -> None:
        assert isinstance(value, int)
        assert isinstance(title_format, str)
        super().__init__(
            title="",
            label_id=label_id,
            **kwargs,
        )
        self._value = value
        self._initial_value = value
        self._title_format = title_format
        self.set_title_generator(lambda: self._title_format.format(self._value))

    def increment(self, amount: int = 1) -> Counter:
        """
        Increase counter value.
        :param amount: Increment amount
        :return: Self reference
        """
        assert isinstance(amount, int)
        self._value += amount
        self._title = self._title_format.format(self._value)
        self._render()
        return self

    def decrement(self, amount: int = 1) -> Counter:
        """
        Decrease counter value.
        :param amount: Decrement amount
        :return: Self reference
        """
        assert isinstance(amount, int)
        self._value -= amount
        self._title = self._title_format.format(self._value)
        self._render()
        return self

    def set_value(self, value: int) -> Counter:
        """
        Set the counter value directly.
        :param value: New value
        :return: Self reference
        """
        assert isinstance(value, int)
        self._value = value
        self._title = self._title_format.format(self._value)
        self._render()
        return self

    def get_value(self) -> int:
        """
        Return the current counter value.
        :return: Integer value
        """
        return self._value

    def reset(self) -> Counter:
        """
        Reset counter value to its initial state.
        :return: Self reference
        """
        self._value = self._initial_value
        self._title = self._title_format.format(self._value)
        self._render()
        return self


class CounterManager(AbstractWidgetManager, ABC):
    """
    Counter manager.
    """

    def counter(
        self,
        value: int = 0,
        title_format: str = "{0}",
        **kwargs,
    ) -> pygame_menu.widgets.Counter:
        """
        Adds a counter label to the Menu.

        kwargs (Optional)
            - ``align`` (str) – Widget alignment
            - ``font_color`` (tuple, list, str, int, pygame.Color) – Widget font color
            - ``font_size`` (int) – Font size of the widget
            - ``label_id`` (str) – Widget ID
            - ``margin`` (tuple, list) – Widget (left, bottom) margin in px
            - ``padding`` (int, float, tuple, list) – Widget padding according to CSS rules

        :param value: Initial counter value
        :param title_format: Format string, e.g. "Score: {0}"
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Counter`
        """
        assert isinstance(value, int)
        assert isinstance(title_format, str)

        label_id = kwargs.pop("label_id", "")
        attributes = self._filter_widget_attributes(kwargs)

        widget = Counter(
            value=value,
            title_format=title_format,
            label_id=label_id,
        )
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        return widget
