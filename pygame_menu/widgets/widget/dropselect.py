"""
pygame-menu
https://github.com/ppizarror/pygame-menu

DROPSELECT
Drop select widget. This is similar to HTML selects, it can contain many items
(options) to select. The selection is unique.

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

__all__ = ['DropSelect']

import pygame
import pygame_menu
import pygame_menu.controls as _controls

from pygame_menu.font import FontType, FontInstance, get_font
from pygame_menu.locals import ORIENTATION_VERTICAL
from pygame_menu.utils import check_key_pressed_valid, assert_color, assert_vector, make_surface, parse_padding
from pygame_menu.widgets.core import Widget
from pygame_menu.widgets.widget.button import Button
from pygame_menu.widgets.widget.frame import Frame
from pygame_menu.widgets.widget.selector import check_selector_items

from pygame_menu._types import Tuple, Union, List, Any, Optional, CallbackType, ColorType, Dict, \
    ColorInputType, Tuple2IntType, Tuple3IntType, PaddingType, PaddingInstance, Tuple4IntType, NumberType


# noinspection PyMissingOrEmptyDocstring
class DropSelect(Widget):
    """
    Drop select is a selector within a Frame. This drops a vertical frame if requested.
    Drop select can contain selectable items (options), only 1 can be selected.

    The items of the DropSelect are:

    .. code-block:: python

        items = [('Item1', a, b, c...), ('Item2', d, e, f...)]

    The callbacks receive the current selected item, its index in the list,
    the associated arguments, and all unknown keyword arguments, where
    ``selected_item=widget.get_value()`` and ``selected_index=widget.get_index()``:

    .. code-block:: python

        onchange((selected_item, index), a, b, c..., **kwargs)
        onreturn((selected_item, index), a, b, c..., **kwargs)

    For example, if ``selected_index=0`` then ``selected_item=('Item1', a, b, c...)``.

    .. note::

        DropSelect only implements translation.

    :param title: Selector title
    :param items: Items of the selector
    :param dropselect_id: ID of the selector
    :param default: Index of default element to display
    :param onchange: Callback when changing the selector
    :param onreturn: Callback when pressing return on the selector
    :param onselect: Function when selecting the widget
    :param placeholder: Text shown if no option is selected yet
    :param selection_box_arrow_color: Selection box arrow color
    :param selection_box_arrow_margin: Selection box arrow margin (left, right, vertical) in px
    :param selection_box_bgcolor: Selection box background color
    :param selection_box_border_color: Selection box border color
    :param selection_box_border_width: Selection box border width
    :param selection_box_height: Selection box height, counted as how many options are packed before showing scroll
    :param selection_box_inflate: Selection box inflate on x-axis and y-axis (px)
    :param selection_box_margin: Selection box left margin from title (px)
    :param selection_box_text_margin: Selection box text margin (left) in px
    :param selection_box_width: Selection box width (px). If ``0`` compute automatically to fit placeholder
    :param selection_infinite: If ``True`` selection can rotate through bottom/top
    :param selection_option_border_color: Option border color
    :param selection_option_border_width: Option border width
    :param selection_option_font: Option font. If ``None`` use the same font as the widget
    :param selection_option_font_color: Option font color
    :param selection_option_font_size: Option font size. If ``None`` use the 75% of the widget font size
    :param selection_option_padding: Selection padding. See padding styling
    :param selection_option_selected_bgcolor: Selected option background color
    :param selection_option_selected_font_color: Selected option font color
    :param kwargs: Optional keyword arguments
    """
    _drop_frame: Optional['Frame']
    _drop_maked: bool
    _index: int
    _items: Union[List[Tuple[Any, ...]], List[str]]
    _opened: bool
    _option_buttons: List['Button']
    _option_font: Optional['pygame.font.Font']
    _placeholder: str
    _selection_box_arrow_color: ColorType
    _selection_box_arrow_margin: Tuple3IntType
    _selection_box_bgcolor: ColorType
    _selection_box_border_color: ColorType
    _selection_box_border_width: int
    _selection_box_height: int
    _selection_box_inflate: Tuple2IntType
    _selection_box_margin: int
    _selection_box_text_margin: int
    _selection_box_width: int
    _selection_infinite: bool
    _selection_option_border_color: ColorType
    _selection_option_border_width: int
    _selection_option_font_style: Dict[str, Any]
    _selection_option_padding: Tuple4IntType
    _selection_option_selected_bgcolor: ColorType
    _theme: Optional['pygame_menu.Theme']
    _title_size: Tuple2IntType

    def __init__(self,
                 title: Any,
                 items: Union[List[Tuple[Any, ...]], List[str]],
                 dropselect_id: str = '',
                 default: int = -1,
                 onchange: CallbackType = None,
                 onreturn: CallbackType = None,
                 onselect: CallbackType = None,
                 placeholder: str = 'Select an option',
                 selection_box_arrow_color: ColorInputType = (150, 150, 150),
                 selection_box_arrow_margin: Tuple3IntType = (5, 5, 0),
                 selection_box_bgcolor: ColorInputType = (255, 255, 255),
                 selection_box_border_color: ColorInputType = (150, 150, 150),
                 selection_box_border_width: int = 1,
                 selection_box_height: int = 3,
                 selection_box_inflate: Tuple2IntType = (0, 0),
                 selection_box_margin: int = 25,
                 selection_box_text_margin: int = 5,
                 selection_box_width: int = 0,
                 selection_infinite: bool = False,
                 selection_option_border_color: ColorInputType = (220, 220, 220),
                 selection_option_border_width: int = 1,
                 selection_option_font: Optional[FontType] = None,
                 selection_option_font_color: ColorInputType = (0, 0, 0),
                 selection_option_font_size: Optional[int] = None,
                 selection_option_padding: PaddingType = 5,
                 selection_option_selected_bgcolor: ColorInputType = (230, 250, 247),
                 selection_option_selected_font_color: ColorInputType = (0, 0, 0),
                 *args,
                 **kwargs
                 ) -> None:
        assert isinstance(items, list)
        assert isinstance(dropselect_id, str)
        assert isinstance(default, int)
        assert isinstance(placeholder, str)

        # Check element list
        check_selector_items(items)
        assert default >= -1, 'default position must be equal or greater than zero'
        assert default < len(items), 'default position should be lower than number of values'
        assert isinstance(dropselect_id, str), 'id must be a string'
        assert isinstance(default, int), 'default must be an integer'

        # Check styling
        assert isinstance(selection_box_border_width, int) and selection_box_border_width >= 0
        assert isinstance(selection_box_height, int) and selection_box_height >= 1
        assert isinstance(selection_box_margin, int)
        assert isinstance(selection_box_text_margin, int) and selection_box_text_margin >= 0
        assert isinstance(selection_box_width, int) and selection_box_width >= 0
        assert isinstance(selection_infinite, bool)
        assert isinstance(selection_option_border_width, int) and selection_option_border_width >= 0
        assert isinstance(selection_option_padding, PaddingInstance)
        assert_vector(selection_box_arrow_margin, 3, int)
        assert_vector(selection_box_inflate, 2, int)
        selection_box_arrow_color = assert_color(selection_box_arrow_color)
        selection_box_bgcolor = assert_color(selection_box_bgcolor)
        selection_box_border_color = assert_color(selection_box_border_color)
        selection_option_border_color = assert_color(selection_option_border_color)
        selection_option_font_color = assert_color(selection_option_font_color)
        selection_option_selected_bgcolor = assert_color(selection_option_selected_bgcolor)
        selection_option_selected_font_color = assert_color(selection_option_selected_font_color)

        if selection_option_font is not None:
            assert isinstance(selection_option_font, FontInstance)
        if selection_option_font_size is not None:
            assert isinstance(selection_option_font_size, int) and selection_option_font_size > 0

        super(DropSelect, self).__init__(
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            title=title,
            widget_id=dropselect_id,
            args=args,
            kwargs=kwargs
        )

        self._drop_frame = None
        self._drop_maked = False
        self._index = -1
        self._items = items
        self.active = False
        self._placeholder = placeholder
        self._theme = None
        self._title_size = (0, 0)

        # Style
        self._option_font = None
        self._selection_box_arrow_color = selection_box_arrow_color
        self._selection_box_arrow_margin = selection_box_arrow_margin
        self._selection_box_bgcolor = selection_box_bgcolor
        self._selection_box_border_color = selection_box_border_color
        self._selection_box_border_width = selection_box_border_width
        self._selection_box_height = selection_box_height
        self._selection_box_inflate = selection_box_inflate
        self._selection_box_margin = selection_box_margin
        self._selection_box_text_margin = selection_box_text_margin
        self._selection_box_width = selection_box_width
        self._selection_infinite = selection_infinite
        self._selection_option_border_color = selection_option_border_color
        self._selection_option_border_width = selection_option_border_width
        self._selection_option_padding = parse_padding(selection_option_padding)
        self._selection_option_selected_bgcolor = selection_option_selected_bgcolor

        self._selection_option_font_style = {
            'color': selection_option_font_color,
            'color_selected': selection_option_selected_font_color,
            'name': selection_option_font,
            'size': selection_option_font_size
        }

        # Apply default item
        if default >= 0:
            default %= len(self._items)
            for k in range(0, default):
                self._up()
        self.set_default_value(default)

        # Configure publics
        self._selection_effect_draw_post = False

    def set_theme(self, theme: 'pygame_menu.Theme') -> 'DropSelect':
        """
        Set object theme.

        :param theme: Theme
        :return: Self reference
        """
        self._theme = theme
        return self

    def set_default_value(self, index: int) -> 'DropSelect':
        self._default_value = index
        return self

    def reset_value(self) -> 'DropSelect':
        self._index = self._default_value
        return self

    def _apply_font(self) -> None:
        # Compute title size
        title_render = self._font.size(self._title)
        w = int(title_render[0] + self._selection_box_margin
                - self._selection_box_inflate[0] / 2)
        h = int(title_render[1] + self._selection_box_inflate[1] / 2 - self._selection_box_border_width)
        self._title_size = (w, h)

        # Load option font
        if self._selection_option_font_style['name'] is None:
            self._selection_option_font_style['name'] = self._font_name
        if self._selection_option_font_style['size'] is None:
            self._selection_option_font_style['size'] = int(0.75 * self._font_size)
        self._option_font = get_font(self._selection_option_font_style['name'],
                                     self._selection_option_font_style['size'])
        if self._selection_box_width == 0:
            f = self._render_option_string(self._placeholder)
            h = self._render_string(self._title, self.get_font_color_status()).get_height()
            self._selection_box_width = int(f.get_width() + self._selection_box_arrow_margin[0] +
                                            self._selection_box_arrow_margin[1] + h - h / 4)

    def make_selection_drop(self, **kwargs) -> 'DropSelect':
        """
        Make selection drop box.

        kwargs (Optional)
            - ``scrollbar_color``           *(tuple, list, str, int,* :py:class:`pygame.Color` *)* - Scrollbar color
            - ``scrollbar_cursor``          *(int, :py:class:`pygame.cursors.Cursor`, None)* - Cursor of the scrollbars if mouse is placed over. By default is ``None``
            - ``scrollbar_shadow_color``    *(tuple, list, str, int,* :py:class:`pygame.Color` *)* - Color of the shadow of each scrollbar
            - ``scrollbar_shadow_offset``   *(int)* - Offset of the scrollbar shadow (px)
            - ``scrollbar_shadow_position`` *(str)* - Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
            - ``scrollbar_shadow``          *(bool)* - Indicate if a shadow is drawn on each scrollbar
            - ``scrollbar_slider_color``    *(tuple, list, str, int,* :py:class:`pygame.Color` *)* - Color of the sliders
            - ``scrollbar_slider_pad``      *(int, float)* - Space between slider and scrollbars borders (px)
            - ``scrollbar_thick``           *(int)* - Scrollbar thickness (px)
            - ``scrollbars``                *(str)* - Scrollbar position. See :py:mod:`pygame_menu.locals`

        :param kwargs: Optional keyword arguments
        :return: Self reference
        """
        from pygame_menu.scrollarea import get_scrollbars_from_position

        if not self.configured:
            raise RuntimeError('{0} must be configured before creating selection drop'.format(self.get_class_id()))
        if self._theme is None:
            if self._menu is not None:
                self.set_theme(self._menu.get_theme())
            else:
                raise RuntimeError('{0} theme must be defined')

        # Create options buttons
        total_height = 0
        max_height = 0
        frame_width = self._selection_box_width + self._selection_box_inflate[0]
        max_width = frame_width
        self._option_buttons = []

        for optid in range(len(self._items)):
            option = self._items[optid]
            btn = Button(option[0], onreturn=self._click_option, index=optid)
            btn.set_background_color(
                color=self._selection_box_bgcolor
            )
            btn.set_border(
                width=self._selection_option_border_width,
                color=self._selection_option_border_color
            )
            btn.set_controls(
                joystick=self._joystick_enabled,
                mouse=self._mouse_enabled,
                touchscreen=self._touchscreen_enabled
            )
            btn.set_font(
                antialias=self._font_antialias,
                background_color=None,
                color=self._selection_option_font_style['color'],
                font=self._selection_option_font_style['name'],
                font_size=self._selection_option_font_style['size'],
                readonly_color=self._font_readonly_color,
                readonly_selected_color=self._font_readonly_selected_color,
                selected_color=self._font_selected_color
            )
            btn.set_margin(
                x=0,
                y=0
            )
            btn.set_padding(
                padding=self._selection_option_padding
            )
            btn.configured = True
            btn.set_menu(self._menu)
            self._option_buttons.append(btn)
            bh = btn.get_height() - self._selection_option_border_width
            total_height += bh
            if optid + 1 <= self._selection_box_height:
                max_height += bh
            max_width = max(max_width, btn.get_width() - self._selection_option_border_width)

        # Update options rect delta width
        for btn in self._option_buttons:
            btn._rect_size_delta = (max_width - btn.get_width(), 0)

        # Subtract border width to button height (last)
        total_height -= self._selection_option_border_width
        max_height -= self._selection_option_border_width

        # Create frame
        self._drop_frame = Frame(max_width, total_height, ORIENTATION_VERTICAL)
        self._drop_frame.set_background_color(
            color=self._selection_box_bgcolor
        )
        self._drop_frame.set_border(
            width=self._selection_box_border_width,
            color=self._selection_box_border_color
        )
        self._drop_frame.set_menu(self._menu)
        self._drop_frame.relax()
        self._drop_frame.configured = True

        # Create scroll area
        scrollbar_thickness = kwargs.get('scrollbar_thick', self._theme.scrollbar_thick)
        if max_height != total_height:
            frame_width -= scrollbar_thickness

        self._drop_frame.make_scrollarea(
            max_width=frame_width,
            max_height=max_height,
            scrollbar_color=kwargs.get('scrollbar_color', self._theme.scrollbar_color),
            scrollbar_cursor=kwargs.get('scrollbar_cursor', self._theme.scrollbar_cursor),
            scrollbar_shadow_color=kwargs.get('scrollbar_shadow_color', self._theme.scrollbar_shadow_color),
            scrollbar_shadow_offset=kwargs.get('scrollbar_shadow_offset', self._theme.scrollbar_shadow_offset),
            scrollbar_shadow_position=kwargs.get('scrollbar_shadow_position', self._theme.scrollbar_shadow_position),
            scrollbar_shadow=kwargs.get('scrollbar_shadow', self._theme.scrollbar_shadow),
            scrollbar_slider_color=kwargs.get('scrollbar_slider_color', self._theme.scrollbar_slider_color),
            scrollbar_slider_pad=kwargs.get('scrollbar_slider_pad', self._theme.scrollbar_slider_pad),
            scrollbar_thick=scrollbar_thickness,
            scrollbars=get_scrollbars_from_position(kwargs.get('scrollbars', self._theme.scrollarea_position))
        )
        self._drop_frame.set_attribute('height',
                                       max_height + scrollbar_thickness - self._selection_option_border_width)
        self._drop_frame.set_scrollarea(self._scrollarea)
        if self._frame is not None:
            self._drop_frame.set_frame(self._frame)

        for opt in self._option_buttons:
            self._drop_frame.pack(opt, margin=(0, -self._selection_option_border_width))

        # Update options if index is defined
        if self._index != -1:
            self.set_value(self._index)
        self._drop_maked = True

        return self

    def set_scrollarea(self, scrollarea: 'pygame_menu.scrollarea.ScrollArea') -> None:
        super(DropSelect, self).set_scrollarea(scrollarea)
        if self._drop_frame is not None:
            self._drop_frame.set_scrollarea(scrollarea)

    def set_frame(self, frame: 'pygame_menu.widgets.Frame') -> 'DropSelect':
        super(DropSelect, self).set_frame(frame)
        if self._drop_frame is not None:
            self._drop_frame.set_frame(frame)
        return self

    def _click_option(self, index: int) -> None:
        """
        Function triggered after option has been selected or clicked.

        :param index: Option index within list
        :return: None
        """
        self.set_value(index)
        self.active = False

    def set_position(self, posx: NumberType, posy: NumberType) -> 'DropSelect':
        super(DropSelect, self).set_position(posx, posy)
        if self._drop_frame is not None:
            self._drop_frame.set_position(posx + self._title_size[0], posy + self._title_size[1])
            for w in self._option_buttons:
                w.set_position_relative_to_frame()
            self._drop_frame.update_position()
        return self

    def translate(self, x: NumberType, y: NumberType) -> 'DropSelect':
        super(DropSelect, self).translate(x, y)
        if self._drop_frame is not None:
            self._drop_frame.translate(x, y)
        return self

    def scale(self, *args, **kwargs) -> 'DropSelect':
        return self

    def resize(self, *args, **kwargs) -> 'DropSelect':
        return self

    def set_max_width(self, *args, **kwargs) -> 'DropSelect':
        return self

    def set_max_height(self, *args, **kwargs) -> 'DropSelect':
        return self

    def rotate(self, *args, **kwargs) -> 'DropSelect':
        return self

    def flip(self, *args, **kwargs) -> 'DropSelect':
        return self

    def _draw(self, surface: 'pygame.Surface') -> None:
        surface.blit(self._surface, self._rect.topleft)
        if self.active:
            self._drop_frame.draw(surface)

    def _render_option_string(self, text: str) -> 'pygame.Surface':
        """
        Render option string surface.

        :param text: Text to render
        :return: Option string surface
        """
        color = self._selection_option_font_style['color']
        if self.readonly or self._index == -1:
            color = self._font_readonly_color
        return self._option_font.render(text, self._font_antialias, color)

    def _render(self) -> Optional[bool]:
        if self._option_font is None:
            return

        if self._index == -1:
            current_selected = self._placeholder
        else:
            current_selected = self.get_value()[0][0]

        if not self._render_hash_changed(current_selected, self._selected, self._visible, self._index, self.readonly,
                                         self.active):
            return True

        title = self._render_string(self._title, self.get_font_color_status())
        current = self._render_option_string(current_selected)

        # Compute virtual inflate to be applied to current rect
        vi = 0  # Virtual inflate
        if current.get_height() < title.get_height():
            vi = (title.get_height() - current.get_height()) / 2

        # Create arrows
        h = title.get_height()
        arrow = pygame.Rect(
            title.get_width() + self._selection_box_margin + self._selection_box_width - h,
            self._selection_box_arrow_margin[2] + (self._selection_box_inflate[1] + vi / 2) / 2,
            h,
            h
        )
        w = h + self._selection_box_arrow_margin[1]
        arrow_right_pos = (
            (arrow.right - w + h / 2 - h / 16, arrow.centery - h / 6),
            (arrow.right - w + h / 2 + h / 4 - h / 16, arrow.centery + h / 4),
            (arrow.right - w + h - h / 16, arrow.centery - h / 6),
        )

        self._surface = make_surface(title.get_width() + self._selection_box_margin +
                                     self._selection_box_width + self._selection_box_inflate[0] / 2 +
                                     self._selection_box_border_width,
                                     title.get_height() + self._selection_box_inflate[1])
        self._surface.blit(title, (0, self._selection_box_inflate[1] / 2))
        current_rect_bg = current.get_rect()
        current_rect_bg.x += title.get_width() + self._selection_box_margin
        current_rect_bg.y += (self._selection_box_inflate[1]) / 2 + vi
        current_rect_bg.width = self._selection_box_width
        current_rect_bg = current_rect_bg.inflate((self._selection_box_inflate[0],
                                                   self._selection_box_inflate[1] + 2 * vi))
        pygame.draw.rect(self._surface, self._selection_box_bgcolor, current_rect_bg)
        pygame.draw.rect(self._surface, self._selection_box_border_color, current_rect_bg,
                         self._selection_box_border_width)

        # Crop current max width
        cropped_current_w = self._selection_box_width - self._selection_box_arrow_margin[0] - \
                            self._selection_box_arrow_margin[1] - h / 2 - h / 16 - self._selection_box_text_margin
        assert cropped_current_w > 0, \
            'there is no left space for text width, try increasing selection_box_width size'
        new_current = make_surface(cropped_current_w, current.get_height())
        new_current.blit(current, (0, 0))
        # new_current.fill((0, 0, 0))
        self._surface.blit(new_current,
                           (title.get_width() + self._selection_box_margin + self._selection_box_text_margin,
                            self._selection_box_inflate[1] / 2 + vi))
        pygame.draw.polygon(self._surface, self._selection_box_arrow_color, arrow_right_pos)

        self._rect.width, self._rect.height = self._surface.get_size()
        self.force_menu_surface_update()

    def get_index(self) -> int:
        """
        Get selected index.

        :return: Selected index
        """
        return self._index

    def get_value(self) -> Tuple[Union[Tuple[Any, ...], str], int]:
        """
        Return the current value of the selector at the selected index.

        :return: Value and index as a tuple, (value, index)
        """
        return self._items[self._index], self._index

    def _down(self) -> None:
        """
        Move current selection down.

        :return: None
        """
        if self.readonly:
            return
        if not self.active:
            return self._toggle_drop()
        if self._selection_infinite:
            self.set_value((self._index - 1) % len(self._items))
        else:
            prev = self._index
            new = max(0, self._index - 1)
            if prev == new:
                return
            self.set_value(new)
        self.change(*self._items[self._index][1:])
        self._sound.play_key_add()

    def _up(self) -> None:
        """
        Move current selection up.

        :return: None
        """
        if self.readonly:
            return
        if not self.active:
            return self._toggle_drop()
        if self._selection_infinite:
            self.set_value((self._index + 1) % len(self._items))
        else:
            prev = self._index
            new = min(self._index + 1, len(self._items) - 1)
            if prev == new:
                return
            self.set_value(new)
        self.change(*self._items[self._index][1:])
        self._sound.play_key_add()

    def set_value(self, item: Union[str, int]) -> None:
        """
        Set the current value of the widget, selecting the element that matches
        the text if ``item`` is a string, or the index if ``item`` is an integer.
        This method raises ``ValueError`` if no element found.

        For example, if widget item list is ``[['a',0],['b',1],['a',2]]``:

        - *widget*.set_value('a') -> Widget selects the first element (index 0)
        - *widget*.set_value(2) -> Widget selects the third element (index 2)

        :param item: Item to select, can be a string or an integer.
        :return: None
        """
        assert isinstance(item, (str, int)), 'item must be an string or an integer'

        if isinstance(item, str):
            for element in self._items:
                if element[0] == item:
                    self._index = self._items.index(element)
                    return
            raise ValueError('no value "{}" found in selector'.format(item))
        elif isinstance(item, int):
            assert 0 <= item < len(self._items), \
                'item index must be greater than zero and lower than the number of elements on the selector'
            self._index = item

        # Update options background selection
        for bindx in range(len(self._option_buttons)):
            btn = self._option_buttons[bindx]
            if bindx == self._index:
                btn.set_background_color(self._selection_option_selected_bgcolor)
                btn.update_font({'color': self._selection_option_font_style['color_selected']})
                btn.scroll_to_widget(margin=5)
            else:
                btn.set_background_color(self._selection_box_bgcolor)
                btn.update_font({'color': self._selection_option_font_style['color']})

    def update_elements(self, elements: Union[List[Tuple[Any, ...]], List[str]]) -> None:
        """
        Update selector elements.

        .. note::

            If the length of the list is different than the previous one,
            the new index of the selector will be the first element of the list.

        :param elements: Elements of the selector ``[('Item1', a, b, c...), ('Item2', d, e, f...)]``
        :return: None
        """
        check_selector_items(elements)
        selected_element = self._items[self._index]
        self._items = elements
        try:
            self._index = self._items.index(selected_element)
        except ValueError:
            if self._index >= len(self._items):
                self._index = 0
                self._default_value = 0
        self._drop_maked = False
        self._drop_frame = None

    def update(self, events: Union[List['pygame.event.Event'], Tuple['pygame.event.Event']]) -> bool:
        if self.readonly:
            return False
        updated = False

        # Check scroll
        if self._drop_frame is not None:
            updated = self._drop_frame.update(events)
            if updated:
                return True

        for event in events:

            if event.type == pygame.KEYDOWN:  # Check key is valid
                if not check_key_pressed_valid(event):
                    continue

            # Events
            keydown = self._keyboard_enabled and event.type == pygame.KEYDOWN
            joy_hatmotion = self._joystick_enabled and event.type == pygame.JOYHATMOTION
            joy_axismotion = self._joystick_enabled and event.type == pygame.JOYAXISMOTION
            joy_button_down = self._joystick_enabled and event.type == pygame.JOYBUTTONDOWN

            # Left button
            if keydown and event.key == _controls.KEY_MOVE_DOWN or \
                    joy_hatmotion and event.value == _controls.JOY_LEFT or \
                    joy_axismotion and event.axis == _controls.JOY_AXIS_X and event.value < _controls.JOY_DEADZONE:
                self._down()
                updated = True

            # Right button
            elif keydown and event.key == _controls.KEY_MOVE_UP or \
                    joy_hatmotion and event.value == _controls.JOY_RIGHT or \
                    joy_axismotion and event.axis == _controls.JOY_AXIS_X and event.value > -_controls.JOY_DEADZONE:
                self._up()
                updated = True

            # Press enter
            elif keydown and event.key == _controls.KEY_APPLY or \
                    joy_button_down and event.button == _controls.JOY_BUTTON_SELECT:
                if self.active:
                    self._sound.play_open_menu()
                    self.apply(*self._items[self._index][1:])
                self._toggle_drop()
                updated = True

            # Click on selector; don't consider the mouse wheel (button 4 & 5)
            elif self._mouse_enabled and event.type == pygame.MOUSEBUTTONUP and event.button in (1, 2, 3) or \
                    self._touchscreen_enabled and event.type == pygame.FINGERUP and \
                    not (self._drop_frame is not None and self._drop_frame.get_scrollarea(inner=True).is_scrolling()):

                # Check for mouse clicks within
                if self.active:
                    for btn in self._option_buttons:
                        updated = btn.update(events)
                        if updated:
                            return True

                # Get event position based on input type
                if self._touchscreen_enabled and event.type == pygame.FINGERUP and self._menu is not None:
                    window_size = self._menu.get_window_size()
                    event_pos = (event.x * window_size[0], event.y * window_size[1])
                else:
                    event_pos = event.pos

                # If collides
                rect = self.get_rect(to_real_position=True, apply_padding=False)
                if rect.collidepoint(*event_pos):
                    # Check if mouse collides left or right as percentage, use only X coordinate
                    mousex, _ = event.pos
                    topleft, _ = rect.topleft
                    topright, _ = rect.topright
                    dist = mousex - (topleft + self._title_size[0])  # Distance from title
                    if dist > 0:  # User clicked the options, not title
                        self._toggle_drop()
                        updated = True

        if updated:
            self.apply_update_callbacks()

        return updated

    def _toggle_drop(self) -> None:
        """
        Open drop selection.

        :return: None
        """
        if not self._drop_maked:
            self.make_selection_drop()
        self.active = not self.active

    def get_focus_rect(self) -> 'pygame.Rect':
        if not self._drop_maked:
            self.make_selection_drop()
        rect = self.get_rect(apply_padding=False, to_real_position=True)
        if self.active:
            rect.width = self._selection_box_width
            rect.x += self._title_size[0]
            rect.height += self._drop_frame.get_attribute('height')
        return rect
