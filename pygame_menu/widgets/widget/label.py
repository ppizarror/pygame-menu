"""
pygame-menu
https://github.com/ppizarror/pygame-menu

LABEL
Label class, adds a simple text to the Menu.
"""

from __future__ import annotations

__all__ = ["Label"]

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Optional

import pygame

from pygame_menu.utils import assert_color, make_surface, warn
from pygame_menu.widgets.core.widget import Widget

if TYPE_CHECKING:
    from pygame_menu._types import (
        CallbackType,
        ColorInputType,
        ColorType,
        EventVectorType,
    )

LabelTitleGeneratorType = Optional[Callable[[], str]]


class Label(Widget):
    """
    Label widget.

    .. note::

        Label accepts all transformations.

    :param title: Label title/text
    :param label_id: Label ID
    :param onselect: Function when selecting the label widget
    :param wordwrap: Wraps label if newline is found on widget
    :param leading: Font leading for ``wordwrap``. If ``None`` retrieves from widget font
    :param max_nlines: Number of maximum lines for ``wordwrap``. If ``None`` the number is dynamically computed. If exceeded, ``get_overflow_lines()`` will return the non-displayed lines
    """

    _last_underline: list[str | tuple[ColorType, int, int] | None]
    _leading: int | None
    _lines: list[str]
    _max_nlines: int | None
    _overflow_lines: list[str]  # Store how many lines are overflowed
    _title_generator: LabelTitleGeneratorType
    _wordwrap: bool

    def __init__(
        self,
        title: Any,
        label_id: str = "",
        onselect: CallbackType = None,
        wordwrap: bool = False,
        leading: int | None = None,
        max_nlines: int | None = None,
        accept_events: bool = False,
    ) -> None:
        assert isinstance(leading, (type(None), int))
        assert isinstance(max_nlines, (type(None), int))
        assert isinstance(wordwrap, bool)
        super().__init__(
            title=title,
            onselect=onselect,
            widget_id=label_id,
            accept_events=accept_events,
        )
        self._last_underline = ["", None]  # deco id, (color, offset, width)
        self._leading = leading
        self._lines = []  # Lines of text displayed
        self._max_nlines = max_nlines
        self._overflow_lines = []
        self._title_generator = None
        self._wordwrap = wordwrap

    def add_underline(
        self, color: ColorInputType, offset: int, width: int, force_render: bool = False
    ) -> Label:
        """
        Adds an underline to text. This is added if widget is rendered. Underline
        is only enabled for non wordwrap mode.

        :param color: Underline color
        :param offset: Underline offset
        :param width: Underline width
        :param force_render: If ``True`` force widget render after addition
        :return: Self reference
        """
        assert not self._wordwrap, "underline is not enabled for wordwrap is active"
        color = assert_color(color)
        assert isinstance(offset, int)
        assert isinstance(width, int) and width > 0
        self._last_underline[1] = (color, offset, width)
        if force_render:
            self._force_render()
        return self

    def remove_underline(self) -> Label:
        """
        Remove the underline.

        :return: Self reference
        """
        assert not self._wordwrap, "underline is not enabled for wordwrap is active"
        if self._last_underline[0] != "":
            self._decorator.remove(self._last_underline[0])
            self._last_underline[0] = ""
        return self

    def _apply_font(self) -> None:
        pass

    def _draw(self, surface: pygame.Surface) -> None:
        # The minimal width of any surface is 1px, so the background will be a line
        if self._title == "":
            return
        surface.blit(self._surface, self._rect.topleft)

    def set_title_generator(self, generator: LabelTitleGeneratorType) -> Label:
        """
        Set a title generator. This function is executed each time the label updates,
        returning a new title (string) which replaces the current label title.

        The generator does not take any input as argument.

        :param generator: Function which generates a new text status
        :return: Self reference
        """
        if generator is not None:
            assert callable(generator)
        self._title_generator = generator

        # Update update widgets
        menu_update_widgets = self._get_menu_update_widgets()
        if generator is None and self in menu_update_widgets:
            menu_update_widgets.remove(self)
        if generator is not None and self not in menu_update_widgets:
            menu_update_widgets.append(self)
        return self

    def set_title(self, title: str, *args: Any) -> Label:
        super().set_title(title)
        if self._title_generator is not None:
            if self._verbose:
                warn(
                    f"{self.get_class_id()} title generator is not None, thus, the new"
                    f' title "{title}" will be overridden after next update'
                )
        return self

    def _get_leading(self) -> int:
        """
        Computes the font leading.

        :return: Leading
        """
        assert self._font
        return self._font.get_linesize() if self._leading is None else self._leading

    def get_lines(self) -> list[str]:
        """
        Return the lines of text displayed. Each new line belongs to an item on list.

        :return: List of displayed lines
        """
        return self._lines

    @staticmethod
    def _wordwrap_line(
        line: str,
        font: pygame.font.Font,
        max_width: int,
        tab_size: int,
    ) -> list[str]:
        """
        Wordwraps line.

        :param line: Line
        :param font: Font
        :param max_width: Max width
        :param tab_size: Tab size
        :return: List of strings
        """
        final_lines: list[str] = []
        words: list[str] = line.split(" ")

        while True:
            split_line: bool = False
            current_line: str = ""
            i: int = 0
            for i, _ in enumerate(words):
                current_line = " ".join(words[: i + 1]).replace("\t", " " * tab_size)
                current_line_size = font.size(current_line)
                if current_line_size[0] > max_width:
                    split_line = True
                    break

            if split_line:
                i = i if i > 0 else 1
                final_lines.append(" ".join(words[:i]))
                words = words[i:]
            else:
                final_lines.append(current_line)
                break

        return final_lines

    def _get_max_container_width(self) -> int:
        """
        Return the maximum container width. It can be the column width,
        menu width or frame width.

        :return: Container width (px)
        """
        menu = self._menu
        max_width: int
        if menu is None:
            return 0
        elif self._frame is not None:
            max_width = self._frame.get_width()
        else:  # Infers width from container Menu
            try:
                # noinspection PyProtectedMember
                max_width = menu._column_widths[self.get_col_row_index()[0]]
            except IndexError:
                max_width = menu.get_width(inner=True)
        return (
            max_width
            - self._padding[1]
            - self._padding[3]
            - self._selection_effect.get_width()
        )

    def get_overflow_lines(self) -> list[str]:
        """
        Return the overflow lines if ``wordwrap`` is active and ``max_nlines`` is set.

        :return: Non displayed lines
        """
        assert self._wordwrap, "wordwrap must be enabled"
        assert isinstance(self._max_nlines, int), "max_nlines must be defined"
        return self._overflow_lines

    def _render(self) -> bool | None:
        font_color: ColorType = self.get_font_color_status()
        if not self._render_hash_changed(
            self._title,
            font_color,
            self._visible,
            self._menu,
            self._font,
            self._last_underline[1],
            self._padding,
            self._selection_effect.get_width(),
            self.readonly,
            self._frame,
        ):
            return True
        self._lines.clear()

        # Generate surface
        max_width: int = 0
        if not self._wordwrap:
            self._surface = self._render_string(self._title, font_color)
            self._lines.append(self._title)

        else:
            self._overflow_lines.clear()
            if self._font is None or self._menu is None:
                self._surface = make_surface(0, 0, alpha=True)
            else:
                max_width = self._get_max_container_width()
                lines: list[str] = sum(
                    (
                        self._wordwrap_line(
                            line=line,
                            font=self._font,
                            max_width=max_width,
                            tab_size=self._tab_size,
                        )
                        for line in self._title.split("\n")
                    ),
                    [],
                )
                num_lines = len(lines)
                if isinstance(self._max_nlines, int):
                    if num_lines > self._max_nlines:
                        for j in range(num_lines - self._max_nlines):
                            self._overflow_lines.append(lines[num_lines - j - 1])
                    num_lines = min(num_lines, self._max_nlines)

                self._surface = make_surface(
                    max(self._font.size(line)[0] for line in lines),
                    num_lines * self._get_leading(),
                    alpha=True,
                )

                for n_line, line in enumerate(lines):
                    line_surface = self._render_string(line, font_color)
                    self._surface.blit(
                        line_surface,
                        pygame.Rect(
                            0,
                            n_line * self._get_leading(),
                            self._rect.width,
                            self._rect.height,
                        ),
                    )
                    self._lines.append(line)
                    if n_line + 1 == num_lines:
                        break

        # Apply max width if wordwrap exceeds size
        if self._wordwrap and self.get_width() > max_width > 0:
            verbose_prev: bool = self._verbose
            self._verbose = False  # Disable auto-warns while setting max width
            self.set_max_width(max_width, render=False)
            self._verbose = verbose_prev

        # Update rect object
        self._apply_transforms()
        self._rect.width, self._rect.height = self._surface.get_size()

        # Add underline
        if not self._wordwrap:
            self.remove_underline()
            if self._last_underline[1] is not None:
                w = self._surface.get_width()
                h = self._surface.get_height()
                color, offset, width = self._last_underline[1]
                if w > 0 and h > 0:
                    self._last_underline[0] = self._decorator.add_line(
                        pos1=(-w / 2, h / 2 + offset),
                        pos2=(w / 2, h / 2 + offset),
                        color=color,
                        width=width,
                    )

        self.force_menu_surface_update()
        return None

    def update(self, events: EventVectorType) -> bool:
        # If generator is not None
        if self._title_generator is not None:
            gen_title = self._title_generator()
            assert isinstance(gen_title, str), (
                f"object generated by the title generator ({gen_title}) is not string-type"
            )
            self._title = gen_title
            self._render()
        self.apply_update_callbacks(events)
        for event in events:
            if self._check_mouseover(event):
                break
        return False

    def clear(self) -> Label:
        """
        Clear the label text.

        Equivalent to setting the title to an empty string.

        :return: Self reference
        """
        self.set_title("")
        return self

    def get_line_count(self) -> int:
        """
        Return the number of currently displayed lines.

        If wordwrap is enabled, this returns the number of visible wrapped
        lines. Otherwise, returns ``1`` for non-empty labels.

        :return: Number of displayed lines
        """
        return len(self._lines)

    def has_overflow(self) -> bool:
        """
        Check whether the label contains overflow lines.

        This method is intended for labels using ``wordwrap`` together with
        ``max_nlines``.

        :return: ``True`` if text overflow exists
        """
        return len(self._overflow_lines) > 0

    def get_overflow_count(self) -> int:
        """
        Return the number of overflow lines.

        :return: Number of non-displayed lines
        """
        return len(self._overflow_lines)

    def is_empty(self) -> bool:
        """
        Check whether the label title is empty.

        :return: ``True`` if the label contains no text
        """
        return self._title == ""
