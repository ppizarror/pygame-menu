from __future__ import annotations

__all__ = ["FPS"]

import pygame

from pygame_menu.widgets.widget.label import Label


class FPS(Label):
    """
    FPS label widget.
    Displays the current FPS value from a pygame Clock.
    """

    _clock: pygame.time.Clock

    def __init__(
        self,
        clock: pygame.time.Clock,
        title_format: str = "FPS: {0:.0f}",
        label_id: str = "",
        **kwargs,
    ) -> None:
        assert isinstance(clock, pygame.time.Clock)
        assert isinstance(title_format, str)

        self._clock = clock
        self._title_format = title_format

        super().__init__(
            title=title_format.format(clock.get_fps()),
            label_id=label_id,
            **kwargs,
        )

        self.set_title_generator(
            lambda: self._title_format.format(self._clock.get_fps())
        )

    def get_fps(self) -> float:
        """
        Return the current FPS.

        :return: FPS value
        """
        return self._clock.get_fps()
