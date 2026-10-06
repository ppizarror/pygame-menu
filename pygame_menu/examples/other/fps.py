"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - FPS
Simple FPS monitor application.
"""

from __future__ import annotations

__all__ = ["main"]

import pygame

import pygame_menu
from pygame_menu.examples import create_example_window
from pygame_menu.widgets.selection.highlight import HighlightSelection


class FPSApp:
    """Simple FPS monitor application."""

    def __init__(self) -> None:
        self.surface = create_example_window("Example - FPS", (500, 400))
        self.clock = pygame.time.Clock()

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
            "FPS Monitor",
            500,
            400,
            theme=theme,
            center_content=True,
            onclose=pygame_menu.events.EXIT,
        )

        self.menu.add.label(
            "Current rendering performance",
            font_size=20,
            font_color=(180, 180, 180),
        )

        self.menu.add.vertical_margin(25)

        self.fps = self.menu.add.fps(
            self.clock,
            title_format="FPS: {0:.0f}",
            font_size=48,
            font_color=(80, 220, 120),
            selectable=False,
        )

        self.menu.add.vertical_margin(25)

        self.menu.add.label(
            "The value updates every frame",
            font_size=18,
            font_color=(180, 180, 180),
        )

        self.menu.add.vertical_margin(25)

        self.menu.add.button(
            "Quit",
            pygame_menu.events.EXIT,
            font_size=20,
        )

        self.menu.set_onupdate(self.process_events)

    def process_events(
        self,
        events: list[pygame.event.Event],
        _: object | None = None,
    ) -> None:
        """Limit the frame rate and process keyboard input."""
        # Update the Clock before the FPS widget reads get_fps().
        self.clock.tick(60)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.menu.disable()

    def mainloop(self, test: bool = False) -> None:
        """Run the application."""
        self.menu.mainloop(self.surface, disable_loop=test)


def main(test: bool = False) -> FPSApp:
    """Create and run the application."""
    app = FPSApp()
    app.mainloop(test)
    return app


if __name__ == "__main__":
    main()
