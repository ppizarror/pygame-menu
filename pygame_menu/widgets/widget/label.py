"""
pygame-menu
https://github.com/ppizarror/pygame-menu

LABEL
Label class, adds a simple text to the Menu.
"""

__all__ = [
    'Label',
    'LabelManager'
]

import pygame
import pygame_menu
import textwrap
import time

from abc import ABC
from pygame_menu.utils import assert_color, warn, uuid4, make_surface
from pygame_menu.widgets.core.widget import Widget, AbstractWidgetManager

from pygame_menu._types import Any, CallbackType, List, Union, Tuple, Optional, \
    ColorType, ColorInputType, EventVectorType, Callable

LabelTitleGeneratorType = Optional[Callable[[], str]]


# noinspection PyMissingOrEmptyDocstring
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
    :param max_nlines: Number of maximum lines for ``wordwrap``. If ``None`` the number is dynamically computed. If exceded, ``label.get_overflow_lines()`` will return the lines not displayed
    """
    _last_underline: List[Union[str, Optional[Tuple[ColorType, int, int]]]]
    _leading: Optional[int]
    _lines: List[str]
    _max_nlines: Optional[int]
    _overflow_lines: List[str]  # Store how many lines are overflowed starting end
    _title_generator: LabelTitleGeneratorType
    _wordwrap: bool

    def __init__(
            self,
            title: Any,
            label_id: str = '',
            onselect: CallbackType = None,
            wordwrap: bool = False,
            leading: Optional[int] = None,
            max_nlines: Optional[int] = None
    ) -> None:
        assert isinstance(leading, (type(None), int))
        assert isinstance(max_nlines, (type(None), int))
        super(Label, self).__init__(
            title=title,
            onselect=onselect,
            widget_id=label_id
        )
        self._last_underline = ['', None]  # deco id, (color, offset, width)
        self._leading = leading
        self._lines = []  # Lines of text displayed
        self._max_nlines = max_nlines
        self._overflow_lines = []
        self._title_generator = None
        self._wordwrap = wordwrap

    def add_underline(
            self,
            color: ColorInputType,
            offset: int,
            width: int,
            force_render: bool = False
    ) -> 'Label':
        """
        Adds an underline to text. This is added if widget is rendered. Underline
        is only enabled for non wordwrap label.

        :param color: Underline color
        :param offset: Underline offset
        :param width: Underline width
        :param force_render: If ``True`` force widget render after addition
        :return: Self reference
        """
        assert not self._wordwrap, 'underline is not enabled for wordwrap is active'
        color = assert_color(color)
        assert isinstance(offset, int)
        assert isinstance(width, int) and width > 0
        self._last_underline[1] = (color, offset, width)
        if force_render:
            self._force_render()
        return self

    def remove_underline(self) -> 'Label':
        """
        Remove underline of the label.

        :return: Self reference
        """
        assert not self._wordwrap, 'underline is not enabled for wordwrap is active'
        if self._last_underline[0] != '':
            self._decorator.remove(self._last_underline[0])
            self._last_underline[0] = ''
        return self

    def _apply_font(self) -> None:
        pass

    def _draw(self, surface: 'pygame.Surface') -> None:
        # The minimal width of any surface is 1px, so the background will be a line
        if self._title == '':
            return
        surface.blit(self._surface, self._rect.topleft)

    def set_title_generator(self, generator: LabelTitleGeneratorType) -> 'Label':
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

    def set_title(self, title: str) -> 'Label':
        super(Label, self).set_title(title)
        if self._title_generator is not None:
            if self._verbose:
                warn(
                    f'{self.get_class_id()} title generator is not None, thus, the new'
                    f' title "{title}" will be overridden after next update'
                )
        return self

    def _get_leading(self) -> int:
        """
        Computes the font leading.

        :return: Leading
        """
        assert self._font
        return (
            self._font.get_linesize()
            if self._leading is None
            else self._leading
        )

    def get_lines(self) -> List[str]:
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
    ) -> List[str]:
        """
        Wordwraps line.

        :param line: Line
        :param font: Font
        :param max_width: Max width
        :param tab_size: Tab size
        :return: List of strings
        """
        final_lines = []
        words = line.split(' ')
        i, current_line = 0, ''

        while True:
            split_line = False
            for i, _ in enumerate(words):
                current_line = ' '.join(words[:i + 1])
                current_line = current_line.replace('\t', ' ' * tab_size)
                current_line_size = font.size(current_line)
                if current_line_size[0] > max_width:
                    split_line = True
                    break

            if split_line:
                i = i if i > 0 else 1
                final_lines.append(' '.join(words[:i]))
                words = words[i:]
            else:
                final_lines.append(current_line)
                break

        return final_lines

    def _get_max_container_width(self) -> int:
        """
        Return the maximum label container width. It can be the column width,
        menu width or frame width if horizontal.

        :return: Container width
        """
        menu = self._menu
        if menu is None:
            return 0
        try:
            # noinspection PyProtectedMember
            max_width = menu._column_widths[self.get_col_row_index()[0]]
        except IndexError:
            max_width = menu.get_width(inner=True)
        return max_width - self._padding[1] - self._padding[3] - self._selection_effect.get_width()

    def get_overflow_lines(self) -> List[str]:
        """
        Return the overflow lines ir ``wordwrap`` is active and ``max_nlines`` is set.

        :return: Lines not displayed
        """
        assert self._wordwrap, 'wordwrap must be enabled'
        assert isinstance(self._max_nlines, int), 'max_nlines must be defined'
        return self._overflow_lines

    def _render(self) -> Optional[bool]:
        if not self._render_hash_changed(
                self._title, self._font_color, self._visible, self._menu, self._font,
                self._last_underline[1], self._padding, self._selection_effect.get_width()):
            return True
        self._lines = []

        # Generate surface
        if not self._wordwrap:
            self._surface = self._render_string(self._title, self._font_color)
            self._lines.append(self._title)

        else:
            self._overflow_lines = []
            if self._font is None or self._menu is None:
                self._surface = make_surface(0, 0, alpha=True)
            else:
                lines = self._title.split('\n')
                lines = sum(
                    (
                        self._wordwrap_line(
                            line=line,
                            font=self._font,
                            max_width=self._get_max_container_width(),
                            tab_size=self._tab_size
                        )
                        for line in lines
                    ),
                    []
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
                    alpha=True
                )

                for n_line, line in enumerate(lines):
                    line_surface = self._render_string(line, self._font_color)
                    self._surface.blit(
                        line_surface,
                        pygame.Rect(
                            0,
                            n_line * self._get_leading(),
                            self._rect.width,
                            self._rect.height
                        )
                    )
                    self._lines.append(line)
                    if n_line + 1 == num_lines:
                        break

        # Update rect object
        self._apply_transforms()
        self._rect.width, self._rect.height = self._surface.get_size()

        # Apply underline
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
                        width=width
                    )

        self.force_menu_surface_update()

    def update(self, events: EventVectorType) -> bool:
        # If generator is not None
        if self._title_generator is not None:
            gen_title = self._title_generator()
            assert isinstance(gen_title, str), \
                f'object generated by the title generator ({gen_title}) is not string-type'
            self._title = gen_title
            self._render()
        self.apply_update_callbacks(events)
        for event in events:
            if self._check_mouseover(event):
                break
        return False


class LabelManager(AbstractWidgetManager, ABC):
    """
    Label manager.
    """

    # noinspection PyProtectedMember
    def label(
            self,
            title: Any,
            label_id: str = '',
            max_char: int = 0,
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            selectable: bool = False,
            wordwrap: bool = False,
            **kwargs
    ) -> Union['pygame_menu.widgets.Label', List['pygame_menu.widgets.Label']]:
        """
        Add a simple text to the Menu.

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``float``                         (bool) - If ``True`` the widget don't contribute width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``leading``                       (int) - Font leading for ``wordwrap``. If ``None`` retrieves from widget font
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``max_nlines``                    (int) - Number of maximum lines for ``wordwrap``. If ``None`` the number is dynamically computed. If exceded, ``label.get_overflow_lines()`` will return the lines not displayed
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect. Applied only if ``selectable`` is ``True``
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled
            - ``tab_size``                      (int) – Width of a tab character
            - ``underline_color``               (tuple, list, str, int, :py:class:`pygame.Color`, None) – Color of the underline. If ``None`` use the same color of the text
            - ``underline_offset``              (int) – Vertical offset in px. ``2`` by default
            - ``underline_width``               (int) – Underline width in px. ``2`` by default
            - ``underline``                     (bool) – Enables text underline, using a properly placed decoration. ``False`` by default

        .. note::

            All theme-related optional kwargs use the default Menu theme if not defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param title: Text to be displayed
        :param label_id: ID of the label
        :param max_char: Split the title in several labels if the string length exceeds ``max_char``; ``0``: don't split, ``-1``: split to Menu width
        :param onselect: Callback executed when selecting the widget; only executed if ``selectable`` is ``True``
        :param selectable: Label accepts user selection; useful to move along the Menu using label selection
        :param wordwrap: Wraps label if newline is found on widget. If ``False`` the manager splits the string and creates a list of widgets, else, the widget itself splits and updates the height
        :param kwargs: Optional keyword arguments
        :return: Widget object, or List of widgets if the text overflows
        :rtype: :py:class:`pygame_menu.widgets.Label`, :py:class:`typing.List` [:py:class:`pygame_menu.widgets.Label`]
        """
        assert isinstance(label_id, str)
        assert isinstance(max_char, int)
        assert isinstance(selectable, bool)
        assert max_char >= -1

        title = str(title)
        if len(label_id) == 0:
            label_id = uuid4()

        # If newline detected, split in two new lines
        if '\n' in title and not wordwrap:
            title = title.split('\n')
            widgets = []
            for t in title:
                wig = self.label(
                    title=t,
                    label_id=label_id + '+' + str(len(widgets) + 1),
                    max_char=max_char,
                    onselect=onselect,
                    selectable=selectable,
                    **kwargs
                )
                if isinstance(wig, list):
                    for w in wig:
                        widgets.append(w)
                else:
                    widgets.append(wig)
            return widgets

        # Wrap text to Menu width (imply additional calls to render functions)
        if max_char < 0:
            if len(title) > 0:
                dummy_attrs = self._filter_widget_attributes(kwargs.copy())
                dummy = pygame_menu.widgets.Label(title=title)
                self._configure_widget(dummy, **dummy_attrs)
                max_char = int(1.0 * self._menu.get_width(inner=True) * len(title) / dummy.get_width())
            else:
                max_char = 0

        leading = kwargs.pop('leading', None)
        max_nlines = kwargs.pop('max_nlines', None)

        # If no overflow
        if len(title) <= max_char or max_char == 0 or wordwrap:
            attributes = self._filter_widget_attributes(kwargs)

            # Filter additional parameters
            underline = kwargs.pop('underline', False)
            underline_color = kwargs.pop('underline_color', attributes['font_color'])
            underline_offset = kwargs.pop('underline_offset', 1)
            underline_width = kwargs.pop('underline_width', 1)

            widget = Label(
                label_id=label_id,
                onselect=onselect,
                title=title,
                wordwrap=wordwrap and not underline,
                leading=leading,
                max_nlines=max_nlines
            )
            widget.is_selectable = selectable
            self._check_kwargs(kwargs)
            self._configure_widget(widget=widget, **attributes)

            if underline:
                widget.add_underline(underline_color, underline_offset, underline_width)

            self._append_widget(widget)

        else:
            self._menu._check_id_duplicated(label_id)  # Before adding + LEN
            widget = []
            for line in textwrap.wrap(title, max_char):
                widget.append(
                    self.label(
                        title=line,
                        label_id=label_id + '+' + str(len(widget) + 1),
                        max_char=max_char,
                        onselect=onselect,
                        selectable=selectable,
                        wordwrap=wordwrap,
                        leading=leading,
                        max_nlines=max_nlines,
                        **kwargs
                    )
                )

        return widget

    def clock(
            self,
            clock_format: str = '%Y/%m/%d %H:%M:%S',
            clock_id: str = '',
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            selectable: bool = False,
            title_format: str = '{0}',
            wordwrap: bool = False,
            **kwargs
    ) -> 'pygame_menu.widgets.Label':
        """
        Add a clock label to the Menu. This creates a Label with a text generator
        that request a string from ``time.strftime`` module using ``clock_format``.

        Commonly used format codes:
            - **%Y**    – Year with century as a decimal number
            - **%m**    – Month as a decimal number [01, 12]
            - **%d**    – Day of the month as a decimal number [01, 31]
            - **%H**    – Hour (24-hour clock) as a decimal number [00, 23]
            - **%M**    – Minute as a decimal number [00, 59]
            - **%S**    – Second as a decimal number [00, 61]
            - **%z**    – Time zone offset from UTC
            - **%a**    – Locale's abbreviated weekday name
            - **%A**    – Locale's full weekday name
            - **%b**    – Locale's abbreviated month name
            - **%B**    – Locale's full month name
            - **%c**    – Locale's appropriate date and time representation
            - **%I**    – Hour (12-hour clock) as a decimal number [01, 12]
            - **%p**    – Locale's equivalent of either AM or PM

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int,  :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``float``                         (bool) - If ``True`` the widget don't contribute width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``leading``                       (int) - Font leading for ``wordwrap``. If ``None`` retrieves from widget font
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``max_nlines``                    (int) - Number of maximum lines for ``wordwrap``. If ``None`` the number is dynamically computed. If exceded, ``label.get_overflow_lines()`` will return the lines not displayed
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect. Applied only if ``selectable`` is ``True``
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled
            - ``tab_size``                      (int) – Width of a tab character
            - ``underline_color``               (tuple, list, str, int, :py:class:`pygame.Color`, None) – Color of the underline. If ``None`` use the same color of the text
            - ``underline_offset``              (int) – Vertical offset in px. ``2`` by default
            - ``underline_width``               (int) – Underline width in px. ``2`` by default
            - ``underline``                     (bool) – Enables text underline, using a properly placed decoration. ``False`` by default

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param clock_format: Format of clock used by ``time.strftime``
        :param clock_id: ID of the clock
        :param onselect: Callback executed when selecting the widget; only executed if ``selectable`` is ``True``
        :param selectable: Label accepts user selection; useful to move along the Menu using label selection
        :param title_format: Title format which accepts ``{0}`` as the string from ``time.strftime``, for example, ``'My Clock {0}'`` can be a title format
        :param wordwrap: Wraps label if newline is found on widget. If ``False`` the manager splits the string and creates a list of widgets, else, the widget itself splits and updates the height
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Label`
        """
        label = self.label(
            title='',
            label_id=clock_id,
            onselect=onselect,
            selectable=selectable,
            wordwrap=wordwrap,
            **kwargs
        )

        assert isinstance(title_format, str) and '{0}' in title_format
        assert not isinstance(label, list)
        label.set_title_generator(lambda: title_format.format(time.strftime(clock_format)))
        label.update([])

        return label
