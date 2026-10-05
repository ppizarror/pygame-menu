"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - COUNTER
Simple counter application.
"""

from __future__ import annotations

__all__ = ["main"]

import pygame

import pygame_menu
from pygame_menu.examples import create_example_window
from pygame_menu.widgets.selection.highlight import HighlightSelection


class CounterApp:
    """Simple counter application."""

    def __init__(self) -> None:
        self.surface = create_example_window("Example - Counter", (500, 400))

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
            "Counter",
            500,
            400,
            theme=theme,
            center_content=True,
            onclose=pygame_menu.events.EXIT,
        )

        self.menu.add.label(
            "Use the buttons or arrow keys",
            font_size=20,
            font_color=(180, 180, 180),
        )

        self.menu.add.vertical_margin(25)

        self.counter = self.menu.add.counter(
            value=0,
            title_format="Value: {0}",
            font_size=42,
            font_color=(255, 220, 80),
            selectable=False,
        )

        self.menu.add.vertical_margin(25)

        self.menu.add.button(
            "Increment",
            self.increment,
            font_size=25,
        )

        self.menu.add.button(
            "Decrement",
            self.decrement,
            font_size=25,
        )

        self.menu.add.button(
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

    def increment(self) -> None:
        """Increase the counter."""
        self.counter.increment()

    def decrement(self) -> None:
        """Decrease the counter."""
        self.counter.decrement()

    def reset(self) -> None:
        """Restore the counter's initial value."""
        self.counter.reset()

    def process_events(
        self,
        events: list[pygame.event.Event],
        _: object | None = None,
    ) -> None:
        """Process keyboard input."""
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key in (pygame.K_UP, pygame.K_RIGHT, pygame.K_PLUS):
                self.increment()

            elif event.key in (pygame.K_DOWN, pygame.K_LEFT, pygame.K_MINUS):
                self.decrement()

            elif event.key in (pygame.K_r, pygame.K_0):
                self.reset()

    def mainloop(self, test: bool = False) -> None:
        """Run the application."""
        self.menu.mainloop(self.surface, disable_loop=test)


def main(test: bool = False) -> CounterApp:
    """Create and run the counter application."""
    app = CounterApp()
    app.mainloop(test)
    return app


if __name__ == "__main__":
    main()
