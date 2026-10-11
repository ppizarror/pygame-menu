"""
pygame-menu

EXAMPLE - MENUBAR STYLES

Preview all available MenuBar styles.
"""

from __future__ import annotations

from typing import Any

import pygame_menu
from pygame_menu.examples import create_example_window
from pygame_menu.widgets.widget.menubar import (
    MENUBAR_STYLE_ADAPTIVE,
    MENUBAR_STYLE_CHEVRON,
    MENUBAR_STYLE_FLOATING_PILL,
    MENUBAR_STYLE_HEXAGON,
    MENUBAR_STYLE_NONE,
    MENUBAR_STYLE_SIMPLE,
    MENUBAR_STYLE_TITLE_ONLY,
    MENUBAR_STYLE_TITLE_ONLY_DIAGONAL,
    MENUBAR_STYLE_UNDERLINE,
    MENUBAR_STYLE_UNDERLINE_TITLE,
)


class App:
    def __init__(self) -> None:

        self.surface = create_example_window("Example - MenuBar Styles", (800, 600))

        self.styles = {
            "Adaptive": MENUBAR_STYLE_ADAPTIVE,
            "Simple": MENUBAR_STYLE_SIMPLE,
            "Title Only": MENUBAR_STYLE_TITLE_ONLY,
            "Title Only Diagonal": MENUBAR_STYLE_TITLE_ONLY_DIAGONAL,
            "None": MENUBAR_STYLE_NONE,
            "Underline": MENUBAR_STYLE_UNDERLINE,
            "Underline Title": MENUBAR_STYLE_UNDERLINE_TITLE,
            "Floating Pill": MENUBAR_STYLE_FLOATING_PILL,
            "Chevron": MENUBAR_STYLE_CHEVRON,
            "Hexagon": MENUBAR_STYLE_HEXAGON,
        }

        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        theme.title_bar_style = MENUBAR_STYLE_ADAPTIVE
        theme.title_font_color = (255, 0, 0)

        self.menu = pygame_menu.Menu(
            title="Welcome",
            width=800,
            height=600,
            theme=theme,
            onclose=pygame_menu.events.EXIT,
        )

        self.menu.add.label(
            "Select a MenuBar style:",
            font_size=25,
        )

        self.menu.add.vertical_margin(10)

        self.menu.add.selector(
            title="Style: ",
            items=[(name, style) for name, style in self.styles.items()],
            onchange=self._on_style_change,
        )

        self.menu.add.vertical_margin(20)

        self.menu.add.label(
            "The MenuBar at the top updates immediately.",
            font_size=20,
        )

        self.menu.add.vertical_margin(20)

        self.menu.add.button(
            "Quit",
            pygame_menu.events.EXIT,
        )

    def _on_style_change(self, selected: Any, style: Any) -> None:
        self.menu.get_menubar().set_style(style)

    def mainloop(self, test: bool = False) -> None:
        self.menu.mainloop(
            self.surface,
            disable_loop=test,
        )


def main(test: bool = False) -> App:
    app = App()
    app.mainloop(test)
    return app


if __name__ == "__main__":
    main()
