from __future__ import annotations

__all__ = ["Counter"]

from pygame_menu.widgets.widget.label import Label


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
