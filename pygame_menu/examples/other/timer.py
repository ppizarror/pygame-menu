"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - TIMER
Simple timer application.
"""

from __future__ import annotations

__all__ = ["main"]

import pygame

import pygame_menu
from pygame_menu.examples import create_example_window
from pygame_menu.widgets.selection.highlight import HighlightSelection


class TimerApp:
    """Simple timer application."""

    def __init__(self) -> None:
        self.surface = create_example_window("Example - Timer", (500, 400))

        theme = pygame_menu.Theme(
            background_color=(35, 35, 35),
            title_background_color=(25, 25, 25),
            title_font_size=32,
            widget_font_size=26,
            widget_font_color=(255, 255, 255),
            widget_selection_effect=HighlightSelection(1, 0, 0).set_color((80, 80, 80)),
            widget_alignment=pygame_menu.locals.ALIGN_CENTER,
            widget_padding=10,
        )

        self.menu = pygame_menu.Menu(
            "Timer",
            500,
            400,
            theme=theme,
            center_content=True,
            onclose=pygame_menu.events.EXIT,
        )

        self.menu.add.label(
            "Use the buttons or keyboard shortcuts",
            font_size=20,
            font_color=(180, 180, 180),
        )

        self.menu.add.vertical_margin(25)

        self.timer = self.menu.add.timer(
            title_format="{0:02d}:{1:02d}",
            font_size=64,
            font_color=(255, 220, 80),
            selectable=False,
        )

        # Keep track of whether the timer has been started.
        self.timer_started = False

        self.menu.add.vertical_margin(25)

        self.start_button = self.menu.add.button(
            "Start",
            self.start,
            font_size=25,
        )

        self.pause_button = self.menu.add.button(
            "Pause",
            self.pause,
            font_size=25,
        )

        self.reset_button = self.menu.add.button(
            "Reset",
            self.reset,
            font_size=25,
        )

        self.menu.add.vertical_margin(15)

        self.menu.add.button(
            "Quit",
            pygame_menu.events.EXIT,
            font_size=20,
        )

        self.menu.set_onupdate(self.process_events)

    def start(self) -> None:
        """Start or resume the timer."""
        if self.timer_started and self.timer.is_paused():
            self.timer.resume()
        else:
            self.timer.start()
            self.timer_started = True

    def pause(self) -> None:
        """Pause the timer."""
        if self.timer_started:
            self.timer.pause()

    def reset(self) -> None:
        """Reset the timer."""
        self.timer.reset()
        self.timer_started = False

    def process_events(
        self,
        events: list[pygame.event.Event],
        _: object | None = None,
    ) -> None:
        """Process keyboard input."""
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key in (pygame.K_SPACE, pygame.K_s):
                self.start()

            elif event.key == pygame.K_p:
                self.pause()

            elif event.key in (pygame.K_r, pygame.K_0):
                self.reset()

    def mainloop(self, test: bool = False) -> None:
        """Run the application."""
        self.menu.mainloop(self.surface, disable_loop=test)


def main(test: bool = False) -> TimerApp:
    """Create and run the timer application."""
    app = TimerApp()
    app.mainloop(test)
    return app


if __name__ == "__main__":
    main()
