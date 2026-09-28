"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - CUSTOM SELECTORS
Demonstrates all custom selection effects (Dot, Double Arrow, Image, Rounded Highlight, Underline).
"""

from __future__ import annotations

__all__ = ["main"]

from typing import TYPE_CHECKING

import pygame

import pygame_menu
from pygame_menu.baseimage import IMAGE_MODE_SIMPLE, BaseImage
from pygame_menu.examples import create_example_window
from pygame_menu.widgets.core.selection import Selection
from pygame_menu.widgets.selection.highlight import HighlightSelection

if TYPE_CHECKING:
    from pygame_menu._types import NumberType, Tuple2IntType
    from pygame_menu.widgets.core.widget import Widget


class DotSelection(Selection):
    """Widget selection dot indicator."""

    _radius: int
    _margin: int
    _vertical_offset: int

    def __init__(
        self, radius: int = 5, margin: NumberType = 6, vertical_offset: NumberType = 0
    ) -> None:
        super().__init__(
            margin_left=radius * 2 + margin,
            margin_right=0,
            margin_top=0,
            margin_bottom=0,
        )
        self._radius = radius
        self._margin = int(margin)
        self._vertical_offset = int(vertical_offset)

    def draw(self, surface: pygame.Surface, widget: Widget) -> DotSelection:
        rect = widget.get_rect()
        center = (
            rect.left - self._margin - self._radius,
            rect.centery + self._vertical_offset,
        )
        pygame.draw.circle(surface, self.color, center, self._radius)
        return self


class DoubleArrowSelection(
    pygame_menu.widgets.selection.arrow_selection.ArrowSelection
):
    """Widget selection double-arrow effect."""

    _arrow_margin: int

    def __init__(
        self,
        arrow_size: Tuple2IntType = (10, 15),
        arrow_margin: int = 5,
        arrow_vertical_offset: int = 0,
        blink_ms: NumberType = 0,
    ) -> None:
        super().__init__(
            margin_left=arrow_size[0] + arrow_margin,
            margin_right=arrow_size[0] + arrow_margin,
            margin_top=0,
            margin_bottom=0,
            arrow_size=arrow_size,
            arrow_vertical_offset=arrow_vertical_offset,
            blink_ms=blink_ms,
        )
        self._arrow_margin = arrow_margin

    def draw(self, surface: pygame.Surface, widget: Widget) -> DoubleArrowSelection:
        rect = widget.get_rect()
        la = (
            rect.left - self._arrow_size[0] - self._arrow_margin,
            rect.centery - self._arrow_size[1] // 2,
        )
        lb = (rect.left - self._arrow_margin, rect.centery)
        lc = (
            rect.left - self._arrow_size[0] - self._arrow_margin,
            rect.centery + self._arrow_size[1] // 2,
        )

        ra = (
            rect.right + self._arrow_size[0] + self._arrow_margin,
            rect.centery - self._arrow_size[1] // 2,
        )
        rb = (rect.right + self._arrow_margin, rect.centery)
        rc = (
            rect.right + self._arrow_size[0] + self._arrow_margin,
            rect.centery + self._arrow_size[1] // 2,
        )

        self._draw_arrow(surface, widget, la, lb, lc)
        self._draw_arrow(surface, widget, ra, rb, rc)
        return self


class ImageSelection(Selection):
    """Widget selection image indicator."""

    _image: BaseImage
    _margin: int
    _vertical_offset: int

    def __init__(
        self, image: BaseImage, margin: NumberType = 5, vertical_offset: NumberType = 0
    ) -> None:
        super().__init__(
            margin_left=image.get_width() + int(margin),
            margin_right=0,
            margin_top=0,
            margin_bottom=0,
        )
        self._image = image.copy()
        self._margin = int(margin)
        self._vertical_offset = int(vertical_offset)

    def draw(self, surface: pygame.Surface, widget: Widget) -> ImageSelection:
        rect = widget.get_rect()
        x = rect.left - self._image.get_width() - self._margin
        y = rect.centery - self._image.get_height() // 2 + self._vertical_offset
        self._image.draw(surface, position=(x, y))
        return self


class RoundedHighlightSelection(HighlightSelection):
    """Widget selection rounded highlight effect."""

    _border_radius: int

    def __init__(
        self,
        border_width: int = 1,
        border_radius: int = 8,
        margin_x: NumberType = 16,
        margin_y: NumberType = 8,
    ) -> None:
        super().__init__(
            border_width=border_width, margin_x=margin_x, margin_y=margin_y
        )
        self._border_radius = border_radius

    def draw(
        self, surface: pygame.Surface, widget: Widget
    ) -> RoundedHighlightSelection:
        if self._border_width == 0:
            return self
        pygame.draw.rect(
            surface,
            self.color,
            self.inflate(widget.get_rect()),
            width=self._border_width,
            border_radius=self._border_radius,
        )
        return self


class UnderlineSelection(Selection):
    """Widget selection underline effect."""

    _line_width: int
    _margin: int
    _line_length_offset: int

    def __init__(
        self,
        line_width: int = 2,
        margin: NumberType = 4,
        line_length_offset: NumberType = 0,
    ) -> None:
        super().__init__(
            margin_left=0,
            margin_right=0,
            margin_top=0,
            margin_bottom=line_width + margin,
        )
        self._line_width = line_width
        self._margin = int(margin)
        self._line_length_offset = int(line_length_offset)

    def draw(self, surface: pygame.Surface, widget: Widget) -> UnderlineSelection:
        rect = widget.get_rect()
        start = (rect.left - self._line_length_offset, rect.bottom + self._margin)
        end = (rect.right + self._line_length_offset, rect.bottom + self._margin)
        pygame.draw.line(surface, self.color, start, end, self._line_width)
        return self


def create_sample_indicator_image() -> BaseImage:
    """Creates a small icon surface dynamically in code with IMAGE_MODE_SIMPLE."""
    surf = pygame.Surface((12, 12), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (200, 100, 255), [(0, 2), (10, 6), (0, 10)])
    return BaseImage(surf, drawing_mode=IMAGE_MODE_SIMPLE)


def main(test: bool = False) -> None:
    surface = create_example_window("Example - Custom Selectors", (500, 480))

    theme = pygame_menu.Theme(
        background_color=(30, 30, 30),
        title_background_color=(45, 45, 45),
        title_font_size=30,
        widget_font_size=22,
        widget_font_color=(240, 240, 240),
        widget_alignment=pygame_menu.locals.ALIGN_CENTER,
    )

    menu = pygame_menu.Menu("Custom Selectors", 500, 480, theme=theme)

    menu.add.label(
        "Test Different Selectors:", font_size=20, font_color=(200, 200, 200)
    )
    menu.add.vertical_margin(10)

    # 1. Rounded Highlight Selector
    b1 = menu.add.button("1. Rounded Highlight", lambda: print("Clicked Rounded"))
    b1.set_selection_effect(
        RoundedHighlightSelection(border_width=2, border_radius=10).set_color(
            (80, 180, 250)
        )
    )

    # 2. Dot Selector
    b2 = menu.add.button("2. Dot Indicator", lambda: print("Clicked Dot"))
    b2.set_selection_effect(DotSelection(radius=6, margin=8).set_color((250, 100, 100)))

    # 3. Double Arrow Selector
    b3 = menu.add.button("3. Double Arrows", lambda: print("Clicked Arrows"))
    b3.set_selection_effect(
        DoubleArrowSelection(arrow_size=(8, 12), arrow_margin=6).set_color(
            (100, 250, 100)
        )
    )

    # 4. Image Selector (Using programmatic indicator)
    indicator_img = create_sample_indicator_image()
    b4 = menu.add.button("4. Image Indicator", lambda: print("Clicked Image"))
    b4.set_selection_effect(
        ImageSelection(image=indicator_img, margin=8).set_color((200, 100, 255))
    )

    # 5. Underline Selector
    b5 = menu.add.button("5. Underline Style", lambda: print("Clicked Underline"))
    b5.set_selection_effect(
        UnderlineSelection(line_width=3, margin=5).set_color((250, 200, 50))
    )

    menu.add.vertical_margin(15)
    menu.add.button("Exit", pygame_menu.events.EXIT, font_color=(255, 100, 100))

    menu.mainloop(surface, disable_loop=test)


if __name__ == "__main__":
    main()
