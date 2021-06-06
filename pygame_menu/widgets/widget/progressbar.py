"""
pygame-menu
https://github.com/ppizarror/pygame-menu

PROGRESS BAR
Progress bar widget.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

__all__ = [

    # Class
    'ProgressBar',

    # Types
    'ProgressBarTextFormatType'

]

import pygame
import pygame_menu

from pygame_menu.font import FontType, assert_font
from pygame_menu.locals import ALIGN_LEFT, ALIGN_CENTER
from pygame_menu.utils import assert_color, assert_vector, make_surface, \
    is_callable, assert_alignment, parse_padding
from pygame_menu.widgets.core.widget import Widget, WidgetTransformationNotImplemented

from pygame_menu._types import Any, CallbackType, Optional, ColorType, NumberType, \
    Tuple2IntType, NumberInstance, ColorInputType, EventVectorType, Callable, \
    PaddingType, Tuple4IntType

ProgressBarTextFormatType = Callable[[NumberType], str]


# noinspection PyMissingOrEmptyDocstring
class ProgressBar(Widget):
    """
    Progress bar widget, offers a bar that accepts a percentage from ``0`` to ``100``.

    .. note::

        ProgressBar only accepts translation transformation.

    :param title: Progressbar title
    :param progressbar_id: ProgressBar ID
    :param default: Default value of the progressbar, from ``0`` to ``100``
    :param width: Progress bar width in px
    :param onselect: Function when selecting the widget
    :param box_background_color: Background color of the box
    :param box_border_color: Border color of the box
    :param box_border_width: Border width of the box in px
    :param box_margin: Box margin on x-axis and y-axis (x, y) respect to the title of the widget in px
    :param box_progress_color: Box progress color
    :param box_progress_padding: Box progress padding
    :param progress_text_align: Align of the progress text, can be CENTER, LEFT or RIGHT. See :py:mod:`pygame_menu.locals`
    :param progress_text_enabled: Enables the progress text over box
    :param progress_text_font: Progress font. If ``None`` uses the same as the widget font
    :param progress_text_font_color: Progress font color. If ``None`` uses the same as the widget font
    :param progress_text_font_hfactor: Height factor of the font height relative to the widget font height
    :param progress_text_format: Format function of the progress text, which considers as input the progress value (0-100)
    :param progress_text_margin: Margin of the progress box on x-axis and y-axis in px
    :param progress_text_placeholder: Placeholder of the progress text, which considers as format the output of ``progress_text_format``
    :param args: Optional arguments for callbacks
    :param kwargs: Optional keyword arguments
    """
    _box: 'pygame.Surface'
    _box_background_color: ColorType
    _box_border_color: ColorType
    _box_border_width: int
    _box_height: int
    _box_margin: Tuple2IntType
    _box_pos: int
    _box_progress_color: ColorType
    _box_progress_padding: Tuple4IntType
    _progress: NumberType
    _progress_font: FontType
    _progress_text_align: str
    _progress_text_enabled: bool
    _progress_text_font: Optional[FontType]
    _progress_text_font_color: ColorType
    _progress_text_font_height: int
    _progress_text_font_height_factor: float
    _progress_text_format: ProgressBarTextFormatType
    _progress_text_margin: Tuple2IntType
    _progress_text_placeholder: str
    _width: int

    def __init__(
            self,
            title: Any,
            progressbar_id: str = '',
            default: NumberType = 0,
            width: int = 150,
            onselect: CallbackType = None,
            box_background_color: ColorInputType = (255, 255, 255),
            box_border_color: ColorInputType = (0, 0, 0),
            box_border_width: int = 1,
            box_margin: Tuple2IntType = (25, 0),
            box_progress_color: ColorInputType = (0, 255, 0),
            box_progress_padding: PaddingType = (1, 1),
            progress_text_align: str = ALIGN_CENTER,
            progress_text_enabled: bool = True,
            progress_text_font: Optional[FontType] = None,
            progress_text_font_color: ColorInputType = (0, 0, 0),
            progress_text_font_hfactor: float = 0.8,
            progress_text_format: ProgressBarTextFormatType = lambda x: str(round(x, 1)),
            progress_text_margin: Tuple2IntType = (0, 0),
            progress_text_placeholder: str = '{0} %',
            *args,
            **kwargs
    ) -> None:
        super(ProgressBar, self).__init__(
            args=args,
            kwargs=kwargs,
            onselect=onselect,
            title=title,
            widget_id=progressbar_id
        )

        # Check the value
        assert isinstance(default, NumberInstance)
        assert 0 <= default <= 100, 'default value must range from 0 to 100'

        # Check fonts
        if progress_text_font is not None:
            assert_font(progress_text_font)
        assert isinstance(progress_text_font_hfactor, NumberInstance)
        assert progress_text_font_hfactor > 0, \
            'progress text font height factor must be greater than zero'

        # Check colors
        box_background_color = assert_color(box_background_color)
        box_border_color = assert_color(box_border_color)
        box_progress_color = assert_color(box_progress_color)
        progress_text_font_color = assert_color(progress_text_font_color)

        # Check dimensions and sizes
        assert isinstance(box_border_width, int)
        assert box_border_width >= 0, \
            'box border width must be equal or greater than zero'
        assert_vector(box_margin, 2, int)
        assert_vector(progress_text_margin, 2, int)
        assert isinstance(width, int)
        assert width > 0, 'width must be greater than zero'
        box_progress_padding = parse_padding(box_progress_padding)
        self._box_progress_padding = box_progress_padding

        # Check progress text
        assert isinstance(progress_text_enabled, bool)
        assert is_callable(progress_text_format)
        assert isinstance(progress_text_format(0), str)
        assert isinstance(progress_text_placeholder, str)
        assert_alignment(progress_text_align)

        # Store properties
        self._default_value = default
        self._box_background_color = box_background_color
        self._box_border_color = box_border_color
        self._box_border_width = box_border_width
        self._box_margin = box_margin
        self._box_progress_color = box_progress_color
        self._progress = default
        self._progress_text_align = progress_text_align
        self._progress_text_enabled = progress_text_enabled
        self._progress_text_font = progress_text_font
        self._progress_text_font_color = progress_text_font_color
        self._progress_text_font_height = 0
        self._progress_text_font_height_factor = progress_text_font_hfactor
        self._progress_text_format = progress_text_format
        self._progress_text_margin = progress_text_margin
        self._progress_text_placeholder = progress_text_placeholder
        self._width = width

    def set_value(self, value: NumberType) -> None:
        assert isinstance(value, NumberInstance), 'progress value must be numeric'
        assert 0 <= value <= 100, 'value must be between 0 and 100'
        self._progress = value
        self._render()

    def scale(self, *args, **kwargs) -> 'ProgressBar':
        raise WidgetTransformationNotImplemented()

    def resize(self, *args, **kwargs) -> 'ProgressBar':
        raise WidgetTransformationNotImplemented()

    def set_max_width(self, *args, **kwargs) -> 'ProgressBar':
        raise WidgetTransformationNotImplemented()

    def set_max_height(self, *args, **kwargs) -> 'ProgressBar':
        raise WidgetTransformationNotImplemented()

    def rotate(self, *args, **kwargs) -> 'ProgressBar':
        raise WidgetTransformationNotImplemented()

    def flip(self, *args, **kwargs) -> 'ProgressBar':
        raise WidgetTransformationNotImplemented()

    def get_value(self) -> NumberType:
        return self._progress

    def _apply_font(self) -> None:
        if self._progress_text_font is None:
            self._progress_text_font = self._font_name
        self._progress_text_font_height = int(self._font_size * self._progress_text_font_height_factor)
        self._progress_font = pygame_menu.font.get_font(
            self._progress_text_font, self._progress_text_font_height
        )
        self._box_height = self._font_render_string('TEST').get_height()

    def _draw(self, surface: 'pygame.Surface') -> None:
        # Draw title
        surface.blit(self._surface, (self._rect.x, self._rect.y))

        # Draw box
        box_rect = self._box.get_rect()
        box_rect.x += self._rect.x + self._box_margin[0] + self._box_pos
        box_rect.y += self._rect.y + self._box_margin[1]
        surface.blit(self._box, box_rect)

        # Draw box border
        if self._box_border_width > 0:
            pygame.draw.rect(surface, self._box_border_color, box_rect, self._box_border_width)

    def _render(self) -> Optional[bool]:
        if not hasattr(self, '_progress_font'):
            return False

        if not self._render_hash_changed(
                self._selected, self._title, self._visible, self.readonly,
                self._progress):
            return True

        # Create basic title
        self._surface = self._render_string(self._title, self.get_font_color_status())
        self._rect.width, self._rect.height = self._surface.get_size()

        # Create box
        self._box = make_surface(self._width, self._box_height,
                                 fill_color=self._box_background_color)
        box_progress = make_surface(int(self._width * self._progress / 100),
                                    self._box_height - self._box_progress_padding[0] - self._box_progress_padding[2],
                                    fill_color=self._box_progress_color)
        self._box.blit(box_progress, (self._box_progress_padding[1], self._box_progress_padding[0]))
        self._box_pos = self._rect.width

        # Create progress text
        text = self._progress_font.render(
            self._progress_text_placeholder.format(self._progress_text_format(self._progress)),
            self._font_antialias,
            self._progress_text_font_color
        )
        text_y = int((self._box_height - text.get_height()) / 2)
        if self._progress_text_align == ALIGN_LEFT:
            text_x = self._box_progress_padding[1]
        elif self._progress_text_align == ALIGN_CENTER:
            text_x = int((self._width - text.get_width()) / 2)
        else:
            text_x = self._width - self._box_progress_padding[3] - text.get_width()
        text_x += self._progress_text_margin[0]
        text_y += self._progress_text_margin[1]

        if self._progress_text_enabled:
            self._box.blit(text, (text_x, text_y))

        # Update maximum rect height
        self._rect.height = max(self._rect.height, self._box.get_height())
        self._rect.width += self._width + self._box_margin[0]

        # Finals
        self.force_menu_surface_update()

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)
        return False
