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

import math

import pygame
import pygame_menu

from pygame_menu.controls import KEY_APPLY, KEY_MOVE_DOWN, KEY_MOVE_UP, JOY_BUTTON_SELECT, JOY_LEFT, \
    JOY_DEADZONE, JOY_RIGHT, JOY_AXIS_X
from pygame_menu.font import FontType, get_font, assert_font
from pygame_menu.locals import ORIENTATION_VERTICAL, FINGERDOWN, FINGERUP
from pygame_menu.utils import check_key_pressed_valid, assert_color, assert_vector, make_surface, \
    parse_padding, get_finger_pos, uuid4, assert_cursor
from pygame_menu.widgets.core import Widget
from pygame_menu.widgets.widget.button import Button
from pygame_menu.widgets.widget.frame import Frame
from pygame_menu.widgets.widget.selector import check_selector_items

from pygame_menu._types import Tuple, Union, List, Any, Optional, CallbackType, ColorType, Dict, \
    ColorInputType, Tuple2IntType, Tuple3IntType, PaddingType, PaddingInstance, Tuple4IntType, \
    NumberType, EventVectorType, Tuple2NumberType, CursorInputType, CursorType


# noinspection PyMissingOrEmptyDocstring,PyProtectedMember
class DropSelect(Widget):
    """
    Drop select is a selector within a Frame. This drops a vertical frame if
    requested. Drop select can contain selectable items (options), only 1 can be
    selected.

    The items of the DropSelect are:

    .. code-block:: python

        items = [('Item1', a, b, c...), ('Item2', d, e, f...)]

    The callbacks receive the current selected item, its index in the list, the
    associated arguments, and all unknown keyword arguments, where
    ``selected_item=widget.get_value()`` and ``selected_index=widget.get_index()``:

    .. code-block:: python

        onchange((selected_item, selected_index), a, b, c..., **kwargs)
        onreturn((selected_item, selected_index), a, b, c..., **kwargs)

    For example, if ``selected_index=0`` then ``selected_item=('Item1', a, b, c...)``.

    .. note::

        DropSelect only implements translation.

    :param title: Drop select title
    :param items: Items of the drop select
    :param dropselect_id: ID of the drop select
    :param default: Index of default item to display
    :param onchange: Callback when changing the drop select item
    :param onreturn: Callback when pressing return on the selected item
    :param onselect: Function when selecting the widget
    :param open_middle: If ``True`` the selection box is opened in the middle of the menu
    :param placeholder: Text shown if no option is selected yet
    :param placeholder_add_to_selection_box: If ``True`` adds the placeholder button to the selection box
    :param selection_box_arrow_color: Selection box arrow color
    :param selection_box_arrow_margin: Selection box arrow margin (left, right, vertical) in px
    :param selection_box_bgcolor: Selection box background color
    :param selection_box_border_color: Selection box border color
    :param selection_box_border_width: Selection box border width
    :param selection_box_height: Selection box height, counted as how many options are packed before showing scroll
    :param selection_box_inflate: Selection box inflate on x-axis and y-axis (x, y) in px
    :param selection_box_margin: Selection box on x-axis and y-axis (x, y) margin from title in px
    :param selection_box_text_margin: Selection box text margin (left) in px
    :param selection_box_width: Selection box width in px. If ``0`` compute automatically to fit placeholder
    :param selection_infinite: If ``True`` selection can rotate through bottom/top
    :param selection_option_border_color: Option border color
    :param selection_option_border_width: Option border width
    :param selection_option_cursor: Option cursor. If ``None`` use the same cursor as the widget
    :param selection_option_font: Option font. If ``None`` use the same font as the widget
    :param selection_option_font_color: Option font color
    :param selection_option_font_size: Option font size. If ``None`` use the 100% of the widget font size
    :param selection_option_padding: Selection padding. See padding styling
    :param selection_option_selected_bgcolor: Selected option background color
    :param selection_option_selected_font_color: Selected option font color
    :param kwargs: Optional keyword arguments
    """
    _close_on_apply: bool
    _drop_frame: Optional['Frame']
    _index: int
    _items: Union[List[Tuple[Any, ...]], List[str]]
    _open_bottom: bool
    _open_middle: bool
    _opened: bool
    _option_buttons: List['Button']
    _option_font: Optional['pygame.font.Font']
    _placeholder: str
    _placeholder_add_to_selection_box: bool
    _selection_box_arrow_color: ColorType
    _selection_box_arrow_margin: Tuple3IntType
    _selection_box_bgcolor: ColorType
    _selection_box_border_color: ColorType
    _selection_box_border_width: int
    _selection_box_height: int
    _selection_box_inflate: Tuple2IntType
    _selection_box_margin: Tuple2IntType
    _selection_box_text_margin: int
    _selection_box_width: int
    _selection_infinite: bool
    _selection_option_border_color: ColorType
    _selection_option_border_width: int
    _selection_option_cursor: CursorType
    _selection_option_font_style: Dict[str, Any]
    _selection_option_left_space: bool
    _selection_option_left_space_height_factor: float
    _selection_option_left_space_margin: Tuple3IntType
    _selection_option_padding: Tuple4IntType
    _selection_option_selected_bgcolor: ColorType
    _theme: Optional['pygame_menu.Theme']
    _title_size: Tuple2IntType

    def __init__(
            self,
            title: Any,
            items: Union[List[Tuple[Any, ...]], List[str]],
            dropselect_id: str = '',
            default: int = -1,
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: CallbackType = None,
            open_middle: bool = False,
            placeholder: str = 'Select an option',
            placeholder_add_to_selection_box: bool = True,
            selection_box_arrow_color: ColorInputType = (150, 150, 150),
            selection_box_arrow_margin: Tuple3IntType = (5, 5, 0),
            selection_box_bgcolor: ColorInputType = (255, 255, 255),
            selection_box_border_color: ColorInputType = (150, 150, 150),
            selection_box_border_width: int = 1,
            selection_box_height: int = 3,
            selection_box_inflate: Tuple2IntType = (0, 0),
            selection_box_margin: Tuple2NumberType = (25, 0),
            selection_box_text_margin: int = 5,
            selection_box_width: int = 0,
            selection_infinite: bool = False,
            selection_option_border_color: ColorInputType = (220, 220, 220),
            selection_option_border_width: int = 1,
            selection_option_cursor: CursorInputType = None,
            selection_option_font: Optional[FontType] = None,
            selection_option_font_color: ColorInputType = (0, 0, 0),
            selection_option_font_size: Optional[int] = None,
            selection_option_padding: PaddingType = 5,
            selection_option_selected_bgcolor: ColorInputType = (188, 227, 244),
            selection_option_selected_font_color: ColorInputType = (0, 0, 0),
            *args,
            **kwargs
    ) -> None:
        assert isinstance(default, int)
        assert isinstance(dropselect_id, str)
        assert isinstance(items, list)
        assert isinstance(open_middle, bool)
        assert isinstance(placeholder, str)
        assert isinstance(placeholder_add_to_selection_box, bool)

        # Check items list
        check_selector_items(items)
        assert default >= -1, \
            'default position must be equal or greater than zero'
        assert default < len(items), \
            'default position should be lower than number of values'
        assert isinstance(dropselect_id, str), 'id must be a string'
        assert isinstance(default, int), 'default must be an integer'

        # Check styling
        assert isinstance(selection_box_border_width, int) and selection_box_border_width >= 0
        assert isinstance(selection_box_height, int) and selection_box_height >= 1
        assert isinstance(selection_box_text_margin, int) and selection_box_text_margin >= 0
        assert isinstance(selection_box_width, int) and selection_box_width >= 0
        assert isinstance(selection_infinite, bool)
        assert isinstance(selection_option_border_width, int) and selection_option_border_width >= 0
        assert isinstance(selection_option_padding, PaddingInstance)
        assert_cursor(selection_option_cursor)
        assert_vector(selection_box_arrow_margin, 3, int)
        assert_vector(selection_box_inflate, 2, int)
        assert_vector(selection_box_margin, 2)
        selection_box_arrow_color = assert_color(selection_box_arrow_color)
        selection_box_bgcolor = assert_color(selection_box_bgcolor)
        selection_box_border_color = assert_color(selection_box_border_color)
        selection_option_border_color = assert_color(selection_option_border_color)
        selection_option_font_color = assert_color(selection_option_font_color)
        selection_option_selected_bgcolor = assert_color(selection_option_selected_bgcolor)
        selection_option_selected_font_color = assert_color(selection_option_selected_font_color)

        if selection_option_font is not None:
            assert_font(selection_option_font)
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

        self._close_on_apply = True
        self._default_value = default
        self._drop_frame = None
        self._index = default
        self._items = items.copy()
        self._open_bottom = True
        self._open_middle = open_middle
        self._placeholder = placeholder
        self._placeholder_add_to_selection_box = placeholder_add_to_selection_box
        self._selection_effect_draw_post = False
        self._theme = None
        self._title_size = (0, 0)

        # If True adds a space equals to the height of the option at left, used for
        # drawing some options (for example, ticks, boxes, etc)
        self._selection_option_left_space = False
        self._selection_option_left_space_height_factor = 1
        self._selection_option_left_space_margin = (0, 0, 0)  # left, right, top

        # Style
        self._option_font = None
        self._selection_box_arrow_color = selection_box_arrow_color
        self._selection_box_arrow_margin = selection_box_arrow_margin
        self._selection_box_bgcolor = selection_box_bgcolor
        self._selection_box_border_color = selection_box_border_color
        self._selection_box_border_width = selection_box_border_width
        self._selection_box_height = selection_box_height
        self._selection_box_inflate = selection_box_inflate
        self._selection_box_margin = (int(selection_box_margin[0]),
                                      int(selection_box_margin[1]))
        self._selection_box_text_margin = selection_box_text_margin
        self._selection_box_width = selection_box_width
        self._selection_infinite = selection_infinite
        self._selection_option_border_color = selection_option_border_color
        self._selection_option_border_width = selection_option_border_width
        self._selection_option_cursor = selection_option_cursor
        self._selection_option_padding = parse_padding(selection_option_padding)
        self._selection_option_selected_bgcolor = selection_option_selected_bgcolor

        self._selection_option_font_style = {
            'color': selection_option_font_color,
            'color_selected': selection_option_selected_font_color,
            'name': selection_option_font,
            'size': selection_option_font_size
        }

        # Configure public's
        self.active = False

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

    def _apply_font(self) -> None:
        # Compute title size
        title_render = self._font.size(self._title)
        w = int(title_render[0] + self._selection_box_margin[0]
                - self._selection_box_inflate[0] / 2)
        h = int(title_render[1] + self._selection_box_inflate[1] / 2
                - self._selection_box_border_width)
        self._title_size = (w, h)

        # Load option font
        if self._selection_option_font_style['name'] is None:
            self._selection_option_font_style['name'] = self._font_name
        if self._selection_option_font_style['size'] is None:
            self._selection_option_font_style['size'] = int(self._font_size)
        self._option_font = get_font(self._selection_option_font_style['name'],
                                     self._selection_option_font_style['size'])
        if self._selection_box_width == 0:
            f = self._render_option_string(self._placeholder)
            h = self._render_string(self._title, self.get_font_color_status()).get_height()
            self._selection_box_width = int(f.get_width()
                                            + self._selection_box_arrow_margin[0]
                                            + self._selection_box_arrow_margin[1]
                                            + h - h / 4
                                            + 2 * self._selection_box_border_width)

    def make_selection_drop(self, **kwargs) -> 'DropSelect':
        """
        Make selection drop box.

        kwargs (Optional)
            - ``scrollbar_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Scrollbar color
            - ``scrollbar_cursor``              (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the scrollbars if mouse is placed over. By default is ``None``
            - ``scrollbar_shadow_color``        (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the shadow of each scrollbar
            - ``scrollbar_shadow_offset``       (int) – Offset of the scrollbar shadow in px
            - ``scrollbar_shadow_position``     (str) – Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
            - ``scrollbar_shadow``              (bool) – Indicate if a shadow is drawn on each scrollbar
            - ``scrollbar_slider_color``        (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the sliders
            - ``scrollbar_slider_hover_color``  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the slider if hovered or clicked
            - ``scrollbar_slider_pad``          (int, float) – Space between slider and scrollbars borders in px
            - ``scrollbar_thick``               (int) – Scrollbar thickness in px
            - ``scrollbars``                    (str) – Scrollbar position. See :py:mod:`pygame_menu.locals`

        :param kwargs: Optional keyword arguments
        :return: Self reference
        """
        # noinspection PyUnresolvedReferences
        from pygame_menu._scrollarea import get_scrollbars_from_position

        if not self.configured:
            raise RuntimeError('{0} must be configured before creating selection drop'
                               ''.format(self.get_class_id()))
        if self._theme is None:
            if self._menu is not None:
                self.set_theme(self._menu.get_theme())
            else:
                raise RuntimeError('{0} theme must be defined')
        scrollbar_thickness = kwargs.get('scrollbar_thick', self._theme.scrollbar_thick)

        # Create options buttons
        total_height = 0
        max_height = 0
        frame_width = self._selection_box_width + self._selection_box_inflate[0]
        self._option_buttons = []

        # Add placeholder button
        if self._placeholder_add_to_selection_box:
            self._items.insert(0, (self._placeholder, -1))

        for opt_id in range(len(self._items)):
            option = self._items[opt_id]
            btn = Button(option[0],
                         onreturn=self._click_option,
                         index=opt_id - (1 if self._placeholder_add_to_selection_box else 0),
                         button_id=self._id + '+option-' + uuid4(short=True))
            btn.set_background_color(
                color=self._selection_box_bgcolor
            )
            btn.set_border(
                width=self._selection_option_border_width,
                color=self._selection_option_border_color
            )
            btn.set_controls(
                joystick=False,  # Only drop select controls the joystick behaviour
                mouse=self._mouse_enabled,
                touchscreen=self._touchscreen_enabled,
                keyboard=False  # Only drop select controls the keyboard behaviour
            )
            btn.set_cursor(  # This feature does not work properly
                cursor=self._selection_option_cursor
            )
            font_c = self._selection_option_font_style['color']
            if self._placeholder_add_to_selection_box:
                font_color = font_c if opt_id != 0 else self._font_readonly_color
            else:
                font_color = font_c
            btn.set_font(
                antialias=self._font_antialias,
                background_color=None,
                color=font_color,
                font=self._selection_option_font_style['name'],
                font_size=self._selection_option_font_style['size'],
                readonly_color=self._font_readonly_color,
                readonly_selected_color=self._font_readonly_selected_color,
                selected_color=self._font_selected_color
            )
            btn.set_padding(
                padding=self._selection_option_padding
            )
            btn.add_self_to_kwargs('btn')
            btn.set_tab_size(self._tab_size)
            btn.configured = True
            btn.set_menu(self._menu)
            btn._update__repr___(self)

            self._option_buttons.append(btn)

            bh = btn.get_height() - self._selection_option_border_width
            if self._selection_option_left_space and not \
                    (self._placeholder_add_to_selection_box and opt_id == 0):
                prev_pad = btn._padding  # top, right, bottom, left
                prev_pad_t: Tuple4IntType = btn._padding_transform
                dh = int(btn.get_height(apply_padding=False) *
                         self._selection_option_left_space_height_factor)
                btn.set_attribute('left_space_height', dh)
                m = self._selection_option_left_space_margin
                btn._padding = prev_pad[0], prev_pad[1], prev_pad[2], \
                               prev_pad[3] + dh + m[0] + m[1]
                btn._padding_transform = prev_pad_t[0], prev_pad_t[1], \
                                         prev_pad_t[2], prev_pad_t[3] + dh + m[0] + m[1]

            total_height += bh
            if opt_id + 1 <= self._selection_box_height:
                max_height += bh

        max_width = frame_width
        if total_height != max_height:
            max_width -= scrollbar_thickness
            frame_width -= scrollbar_thickness
            total_height -= self._selection_box_border_width
            max_height -= self._selection_box_border_width
        elif total_height > 0:
            total_height += self._selection_box_border_width
            max_height += self._selection_box_border_width
        for btn in self._option_buttons:
            max_width = max(max_width, btn.get_width() - self._selection_option_border_width)

        # Update options rect delta width
        for btn in self._option_buttons:
            btn._rect_size_delta = (max_width - btn.get_width(), 0)

        # Pop placeholder
        if self._placeholder_add_to_selection_box:
            self._items.pop(0)
            placeholder_button = self._option_buttons.pop(0)
        else:
            placeholder_button = None

        # Unpack previous frame (if exists)
        if self._drop_frame is not None:
            self._drop_frame.set_menu(None)

        # Create frame
        self._drop_frame = Frame(max_width, max(total_height, 1), ORIENTATION_VERTICAL,
                                 frame_id=self._id + '+frame-' + uuid4(short=True))
        self._drop_frame._accepts_title = False
        self._drop_frame._menu_can_be_none_pack = True
        self._drop_frame.hide()
        self._drop_frame.set_background_color(
            color=self._selection_box_bgcolor
        )
        self._drop_frame.set_border(
            width=self._selection_box_border_width,
            color=self._selection_box_border_color
        )
        self._drop_frame.set_scrollarea(self._scrollarea)
        self._drop_frame.relax()
        self._drop_frame.configured = True
        self._drop_frame.set_tab_size(self._tab_size)
        self._drop_frame._update__repr___(self)

        if total_height > 0:
            scrollbar_color = kwargs.get('scrollbar_color',
                                         self._theme.scrollbar_color)
            scrollbars = kwargs.get('scrollbars',
                                    self._theme.scrollarea_position)
            if not kwargs.get('scrollbars_parsed', False):
                scrollbars = get_scrollbars_from_position(scrollbars)
            self._drop_frame.make_scrollarea(
                max_width=frame_width,
                max_height=max_height,
                scrollarea_color=self._selection_box_arrow_color,
                scrollbar_color=scrollbar_color,
                scrollbar_cursor=kwargs.get('scrollbar_cursor',
                                            self._theme.scrollbar_cursor),
                scrollbar_shadow_color=kwargs.get('scrollbar_shadow_color',
                                                  self._theme.scrollbar_shadow_color),
                scrollbar_shadow_offset=kwargs.get('scrollbar_shadow_offset',
                                                   self._theme.scrollbar_shadow_offset),
                scrollbar_shadow_position=kwargs.get('scrollbar_shadow_position',
                                                     self._theme.scrollbar_shadow_position),
                scrollbar_shadow=kwargs.get('scrollbar_shadow',
                                            self._theme.scrollbar_shadow),
                scrollbar_slider_color=kwargs.get('scrollbar_slider_color',
                                                  self._theme.scrollbar_slider_color),
                scrollbar_slider_hover_color=kwargs.get('scrollbar_slider_hover_color',
                                                        self._theme.scrollbar_slider_hover_color),
                scrollbar_slider_pad=kwargs.get('scrollbar_slider_pad',
                                                self._theme.scrollbar_slider_pad),
                scrollbar_thick=scrollbar_thickness,
                scrollbars=scrollbars
            )

        self._drop_frame.set_menu(self._menu)
        self._drop_frame.set_scrollarea(self._scrollarea)
        if self._frame is not None:
            self._drop_frame.set_frame(self._frame)

        # Set sizing properties
        if total_height > 0:
            add_scrollbar = scrollbar_thickness if max_width != frame_width else 0
            border_w = self._selection_box_border_width if total_height != max_height else 0
            self._drop_frame.set_attribute('height',
                                           max_height + add_scrollbar - border_w)
            self._drop_frame.set_attribute('width', frame_width)
        else:
            self._drop_frame.set_attribute('height', 0)
            self._drop_frame.set_attribute('width', 0)
            if self._placeholder_add_to_selection_box:
                placeholder_button.hide()
        margin_width = self._selection_box_border_width if total_height == max_height else 0
        self._drop_frame.set_attribute('extra_margin', margin_width)
        self._drop_frame.set_attribute('placeholder_button', placeholder_button)

        # Pack options
        if self._placeholder_add_to_selection_box:
            self._drop_frame.pack(placeholder_button)
        for opt in self._option_buttons:
            self._drop_frame.pack(opt, margin=(0, -self._selection_option_border_width))

        # Update options if index is defined
        if self._index != -1:
            self.set_value(self._index)

        return self

    def on_remove_from_menu(self) -> 'DropSelect':
        if self._drop_frame is not None:
            self._drop_frame.set_menu(None)
        return self

    def hide(self) -> 'DropSelect':
        super(DropSelect, self).hide()
        if self._drop_frame is not None:
            self._drop_frame.hide()
        return self

    def show(self) -> 'DropSelect':
        super(DropSelect, self).show()
        if self.active:
            self._toggle_drop()
        return self

    def scrollh(self, value: NumberType) -> 'DropSelect':
        """
        Scroll to horizontal value.

        :param value: Horizontal scroll value, if ``0`` scroll to left; ``1`` scroll to right
        :return: Self reference
        """
        if self._drop_frame is not None:
            self._drop_frame.scrollh(value)
        return self

    def scrollv(self, value: NumberType) -> 'DropSelect':
        """
        Scroll to vertical value.

        :param value: Vertical scroll value, if ``0`` scroll to top; ``1`` scroll to bottom
        :return: Self reference
        """
        if self._drop_frame is not None:
            self._drop_frame.scrollv(value)
        return self

    def get_scroll_value_percentage(self, orientation: str) -> float:
        """
        Get the scroll value in percentage, if ``0`` the scroll is at top/left,
        ``1`` bottom/right.

        .. note::

            If ScrollArea does not contain such orientation scroll, or frame is
            not scrollable, ``-1`` is returned.

        :param orientation: Orientation. See :py:mod:`pygame_menu.locals`
        :return: Value from ``0`` to ``1``
        """
        if self._drop_frame is not None:
            return self._drop_frame.get_scroll_value_percentage(orientation)
        return -1

    def set_scrollarea(self, scrollarea: 'pygame_menu._scrollarea.ScrollArea') -> None:
        super(DropSelect, self).set_scrollarea(scrollarea)
        if self._drop_frame is not None:
            self._drop_frame.set_scrollarea(scrollarea)

    def set_frame(self, frame: 'pygame_menu.widgets.Frame') -> 'DropSelect':
        super(DropSelect, self).set_frame(frame)
        if self._drop_frame is not None:
            self._drop_frame.set_frame(frame)
        return self

    def _click_option(self, index: int, btn: 'Button') -> None:
        """
        Function triggered after option has been selected or clicked.

        :param index: Option index within list
        :return: None
        """
        btn.set_attribute('ignore_scroll_to_widget')
        prev_index = self._index
        self.set_value(index)
        if self._index != prev_index and self._index != -1:
            self.change(*self._items[self._index][1:])
        if self._close_on_apply:
            self.active = False
            if self._drop_frame is not None:
                self._drop_frame.hide()
        btn.remove_attribute('ignore_scroll_to_widget')

    def set_position(self, x: NumberType, y: NumberType) -> 'DropSelect':
        super(DropSelect, self).set_position(x, y)
        if self._drop_frame is not None:
            x = self._rect.x
            y = self._rect.y
            if not self._open_middle:
                if self._open_bottom:
                    self._drop_frame.set_position(x + self._title_size[0],
                                                  y + self._title_size[1]
                                                  + self.get_attribute('delta_title_height', 0))
                else:
                    self._drop_frame.set_position(x + self._title_size[0],
                                                  y - self._drop_frame.get_attribute('height')
                                                  + self._drop_frame.get_attribute('extra_margin'))
            else:
                self._drop_frame.set_position(*self._compute_position_middle())
            for w in self._option_buttons:
                w.set_position_relative_to_frame()
            if self._placeholder_add_to_selection_box:
                placeholder_button: 'Button' = self._drop_frame.get_attribute('placeholder_button')
                placeholder_button.set_position_relative_to_frame()
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

    def draw_after_if_selected(self, surface: Optional['pygame.Surface']) -> 'DropSelect':
        if self.is_selected() and self._selection_effect_draw_post:
            self._selection_effect.draw(surface, self)
        if self.active and self.is_visible():
            self._check_drop_maked()

            if not self._open_middle:
                self._drop_frame.draw(surface)
                self.last_surface = surface

            else:
                new_surface = self._menu._widgets_surface

                # Ignore draw if widget is within a frame, if so, the next call made by frame.draw()
                # with surface=None is performed, but this time drop frame draws over "new_surface".
                # If widget is not within a frame, this is not necessary as the frame is not drawn over
                # and the widget is drawn at the end of all widgets
                if surface == self.last_surface and self.get_frame() is not None:
                    self.last_surface = new_surface
                    return self

                # Draw drop frame in menu widgets surface
                assert self._menu is not None, 'middle position need menu reference'
                self._drop_frame.draw(new_surface)
                self.last_surface = new_surface

        return self

    def _render_option_string(self, text: str) -> 'pygame.Surface':
        """
        Render option string surface.

        :param text: Text to render
        :return: Option string surface
        """
        color = self._selection_option_font_style['color']
        if self.readonly or self._index == -1:
            color = self._font_readonly_color
        text = text.replace('\t', ' ' * self._tab_size)
        return self._option_font.render(text, self._font_antialias, color)

    def _get_current_selected_text(self) -> str:
        """
        Return the current selected text.

        :return: Text
        """
        if self._index == -1:
            current_selected = self._placeholder
        else:
            current_selected = self.get_value()[0][0]
        return current_selected

    def _render(self) -> Optional[bool]:
        if self._option_font is None:
            return

        scroll_v = 0
        menu_height = 0 if self._menu is None else self._menu.get_height(widget=True)
        current_selected = self._get_current_selected_text()

        if not self._render_hash_changed(
                current_selected, self._selected, self._visible, self._index,
                self.readonly, self.active, self._open_bottom, scroll_v,
                menu_height, self._open_middle, len(self._items), self._rect.x,
                self._rect.y):
            return True

        title = self._render_string(self._title, self.get_font_color_status())
        current = self._render_option_string(current_selected)

        # Compute virtual inflate to be applied to current rect
        vi = 0  # Virtual inflate
        if current.get_height() < title.get_height():
            vi = (title.get_height() - current.get_height()) / 2

        current_rect_bg = current.get_rect()
        current_rect_bg.x += title.get_width() + self._selection_box_margin[0]
        current_rect_bg.y += (self._selection_box_inflate[1]) / 2 + vi + self._selection_box_margin[1]
        current_rect_bg.width = self._selection_box_width
        current_rect_bg = current_rect_bg.inflate((self._selection_box_inflate[0],
                                                   self._selection_box_inflate[1] + 2 * vi))

        # Compute delta title if height is lower than selection box
        h = title.get_height()
        delta_title_height = max(int(math.floor((current_rect_bg.height - h) / 2)), 0)

        # Create arrows
        arrow = pygame.Rect(
            title.get_width() + self._selection_box_margin[0] + self._selection_box_width - h,
            self._selection_box_arrow_margin[2] + (self._selection_box_inflate[1] + vi / 2) / 2
            + delta_title_height + self._selection_box_margin[1],
            h,
            h
        )
        w = h + self._selection_box_arrow_margin[1]

        # Check which direction it should open
        self._open_bottom = True
        if self._drop_frame is not None and self._scrollarea is not None and \
                not self._open_middle:
            rect = self._rect.copy()
            rect.width = self._selection_box_width
            rect.y += delta_title_height
            rect.x += self._title_size[0]
            rect.height += self._drop_frame.get_attribute('height')
            if rect.width != 0 and rect.height != 0:
                rect_clipped = self._scrollarea.get_world_rect().clip(rect)
                if rect.height != rect_clipped.height:
                    self._open_bottom = False
        if self._drop_frame is not None and self._open_middle and \
                self._menu is not None:
            self._drop_frame.set_scrollarea(self._menu.get_scrollarea())
            self._drop_frame._frame = None
            if not self._menu._mouse_motion_selection:
                self.force_menu_draw_focus = True
        else:
            self.force_menu_draw_focus = False

        if delta_title_height != 0:
            self.set_attribute('delta_title_height',
                               math.ceil((current_rect_bg.height - h) / 2)
                               + 2 * self._selection_box_border_width)

        arrow_up = (
            (arrow.right - w + h / 2 - h / 16, arrow.centery - h / 6 - h / 20),
            (arrow.right - w + h / 2 + h / 4 - h / 16, arrow.centery + h / 4 - h / 20),
            (arrow.right - w + h - h / 16, arrow.centery - h / 6 - h / 20)
        )
        arrow_down = (
            (arrow.right - w + h / 2 - h / 16, arrow.centery + h / 4 - h / 20),
            (arrow.right - w + h / 2 + h / 4 - h / 16, arrow.centery - h / 6 - h / 20),
            (arrow.right - w + h - h / 16, arrow.centery + h / 4 - h / 20)
        )
        if not self._open_bottom:
            if not self.active:
                arrow_right_pos = arrow_down
            else:
                arrow_right_pos = arrow_up
        else:
            if not self.active:
                arrow_right_pos = arrow_up
            else:
                arrow_right_pos = arrow_down

        self._surface = make_surface(title.get_width() + self._selection_box_margin[0]
                                     + self._selection_box_width + self._selection_box_inflate[0] / 2
                                     + self._selection_box_border_width,
                                     max(title.get_height() + self._selection_box_inflate[1],
                                         current_rect_bg.height))
        self._surface.blit(title, (0, self._selection_box_inflate[1] / 2 + delta_title_height))
        pygame.draw.rect(self._surface, self._selection_box_bgcolor, current_rect_bg)
        pygame.draw.rect(self._surface, self._selection_box_border_color, current_rect_bg,
                         self._selection_box_border_width)

        # Crop current max width
        cropped_current_w = self._selection_box_width \
                            - self._selection_box_arrow_margin[0] \
                            - self._selection_box_arrow_margin[1] \
                            - h / 2 \
                            - h / 16 \
                            - self._selection_box_text_margin
        assert cropped_current_w > 0, \
            'there is no left space for text width, try increasing selection_box_width size'
        new_current = make_surface(cropped_current_w, current.get_height())
        new_current.blit(current, (0, 0))
        # new_current.fill((0, 0, 0))
        self._surface.blit(new_current,
                           (title.get_width() + self._selection_box_margin[0]
                            + self._selection_box_text_margin,
                            self._selection_box_inflate[1] / 2 + vi - 1
                            + self._selection_box_margin[1]))
        if len(self._items) > 0:
            pygame.draw.polygon(self._surface, self._selection_box_arrow_color,
                                arrow_right_pos)

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
        Return the current value of the selected index.

        :return: Value and index as a tuple, (value, index)
        """
        if self._index == -1:
            raise ValueError('any item has been selected yet as index is -1')
        return self._items[self._index], self._index

    def _down(self) -> None:
        """
        Move current selection down.

        :return: None
        """
        if self.readonly:
            return
        if len(self._items) == 0:
            return
        if not self.active:
            return self._toggle_drop()
        if self._index == -1:
            self.set_value(len(self._items) - 1)
        else:
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
        if len(self._items) == 0:
            return
        if not self.active:
            return self._toggle_drop()
        if self._index == -1:
            self.set_value(0)
        else:
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
        Set the current value of the widget, selecting the item that matches the
        text if ``item`` is a string, or the index if ``item`` is an integer.
        This method raises ``ValueError`` if no item found.

        For example, if widget item list is ``[['a',0],['b',1],['a',2]]``:

        - *widget*.set_value('a') -> Widget selects the first item (index 0)
        - *widget*.set_value(2) -> Widget selects the third item (index 2)

        .. note::

            This method does not trigger any event (change).

        :param item: Item to select, can be a string or an integer
        :return: None
        """
        assert isinstance(item, (str, int)), 'item must be a string or an integer'

        if isinstance(item, str):
            found = False
            for i in self._items:
                if i[0] == item:
                    self._index = self._items.index(i)
                    found = True
                    break
            if not found:
                raise ValueError('no value "{}" found in drop select'.format(item))
        elif isinstance(item, int):
            assert -1 <= item < len(self._items), \
                'item index must be greater than zero and lower than the number ' \
                'of items on the drop select'
            self._index = item

        # Update options background selection
        for b_ind_x in range(len(self._option_buttons)):
            btn = self._option_buttons[b_ind_x]
            if b_ind_x == self._index:
                btn.set_background_color(self._selection_option_selected_bgcolor)
                btn.update_font({'color': self._selection_option_font_style['color_selected']})
                if not self._drop_frame.has_attribute('ignorescroll'):
                    btn.scroll_to_widget(scroll_parent=False)
            else:
                btn.set_background_color(self._selection_box_bgcolor)
                btn.update_font({'color': self._selection_option_font_style['color']})

    def update_items(self, items: Union[List[Tuple[Any, ...]], List[str]]) -> None:
        """
        Update drop select items.

        .. note::

            If the length of the list is different than the previous one, the new
            index of the select will be the first item of the list.

        :param items: New drop select items; format ``[('Item1', a, b, c...), ('Item2', d, e, f...)]``
        :return: None
        """
        assert isinstance(items, list)
        if len(items) > 0:
            check_selector_items(items)
        if self._index != -1:
            selected_item = self._items[self._index]
        else:
            selected_item = None
        self._items = items
        if selected_item is not None:
            try:
                self._index = self._items.index(selected_item)
            except ValueError:
                if self._index >= len(self._items):
                    self._index = -1
                    self._default_value = -1
        if self._drop_frame is not None:
            self._drop_frame.set_menu(None)
        self._drop_frame = None
        self.active = False

    def _check_drop_maked(self) -> None:
        """
        Checks if drop selection has been maked.

        :return: None
        """
        if self._drop_frame is None:
            raise _SelectionDropNotMakedException(
                'selection drop has not been maked yet. Call {0}.make_selection_drop()'
                'for avoiding this exception'.format(self.get_class_id())
            )

    def _toggle_drop(self) -> None:
        """
        Open drop selection.

        :return: None
        """
        self._check_drop_maked()
        if not self._selected:
            return
        if len(self._items) == 0:
            return
        self.active = not self.active
        if self.active:
            if self._drop_frame is not None:
                self._drop_frame.show()
            self.scroll_to_widget(scroll_parent=False)
        else:
            if self._drop_frame is not None:
                self._drop_frame.hide()
        if self.active and self._index != -1:
            self.set_value(self._index)

    def _compute_position_middle(self, add_offset: bool = True) -> Tuple2IntType:
        """
        Compute box position if position is in the middle.

        :param add_offset: Adds offset
        :return: Position
        """
        assert self._menu is not None, \
            'menu cannot be none if the position is in middle (open_middle)'
        self._check_drop_maked()
        if add_offset:
            offx, offy = self._menu.get_scrollarea().get_offsets()
        else:
            offx, offy = 0, 0
        w, h = self._menu.get_size()
        h -= self._menu.get_menubar().get_height()
        bw, bh = self._selection_box_width, self._drop_frame.get_attribute('height')
        assert w >= bw, \
            'selection box width ({0}) cannot be greater than menu width ({1})' \
            ''.format(bw, w)
        assert h >= bh, \
            'selection box height ({0}) cannot be greater than menu height ({1})' \
            ''.format(bh, h)
        x = (w - bw) / 2 + offx
        y = (h - bh) / 2 + offy
        return x, y

    def get_focus_rect(self) -> 'pygame.Rect':
        self._check_drop_maked()
        rect = self.get_rect(apply_padding=False, to_real_position=True)
        if self.active:
            rect.width = self._selection_box_width
            rect.x += self._title_size[0]
            rect.height += self._drop_frame.get_attribute('height') \
                           - self._drop_frame.get_attribute('extra_margin')
            if not self._open_bottom:
                rect.y -= self._drop_frame.get_attribute('height') \
                          - self._drop_frame.get_attribute('extra_margin')
            if self._open_middle:
                x, y = self._compute_position_middle(add_offset=False)
                rect.x = x + self._menu.get_position()[0]
                rect.y = y + self._menu.get_scrollarea().get_position()[1]
                rect.height -= self._rect.height
        else:
            rect.width -= self._selection_box_border_width
        return rect

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)

        if self.readonly or not self.is_visible():
            return False

        # Check scroll
        self._check_drop_maked()
        updated = self._drop_frame.update(events)
        if updated:
            return True

        for event in events:

            if event.type == pygame.KEYDOWN:  # Check key is valid
                if not check_key_pressed_valid(event):
                    continue

            # Check mouse over
            self._check_mouseover(event)

            # Events
            keydown = self._keyboard_enabled and event.type == pygame.KEYDOWN
            joy_hatmotion = self._joystick_enabled and event.type == pygame.JOYHATMOTION
            joy_axismotion = self._joystick_enabled and event.type == pygame.JOYAXISMOTION
            joy_button_down = self._joystick_enabled and event.type == pygame.JOYBUTTONDOWN

            # Left button
            if keydown and event.key == KEY_MOVE_DOWN or \
                    joy_hatmotion and event.value == JOY_LEFT or \
                    joy_axismotion and event.axis == JOY_AXIS_X and \
                    event.value < JOY_DEADZONE:
                if not self.active:
                    continue
                self._down()
                updated = True

            # Right button
            elif keydown and event.key == KEY_MOVE_UP or \
                    joy_hatmotion and event.value == JOY_RIGHT or \
                    joy_axismotion and event.axis == JOY_AXIS_X and \
                    event.value > -JOY_DEADZONE:
                if not self.active:
                    continue
                self._up()
                updated = True

            # Press enter
            elif keydown and event.key == KEY_APPLY or \
                    joy_button_down and event.button == JOY_BUTTON_SELECT:
                if self.active and self._index >= 0:
                    self._sound.play_key_add()
                    self.apply(*self._items[self._index][1:])
                if not (self.active and (not self._close_on_apply and self._index != -1)):
                    self._toggle_drop()
                updated = True

            # Press keys which active the drop but not apply
            elif keydown and (event.key == pygame.K_TAB):
                self._toggle_drop()
                updated = True

            # Close the selection
            elif keydown and (event.key == pygame.K_ESCAPE or
                              event.key == pygame.K_BACKSPACE):
                if self.active:
                    self._toggle_drop()
                updated = True

            # Click on dropselect; don't consider the mouse wheel (button 4 & 5)
            elif self.active and (
                    event.type == pygame.MOUSEBUTTONDOWN and self._mouse_enabled and
                    event.button in (1, 2, 3) or (
                            event.type == FINGERDOWN and self._touchscreen_enabled and
                            self._drop_frame is not None and
                            not self._drop_frame.get_scrollarea(inner=True).is_scrolling() and
                            self._menu is not None)
            ):
                event_pos = get_finger_pos(self._menu, event)
                if self._drop_frame.get_rect(apply_padding=False, to_real_position=True
                                             ).collidepoint(*event_pos):
                    updated = True

            # Click on dropselect; don't consider the mouse wheel (button 4 & 5)
            elif event.type == pygame.MOUSEBUTTONUP and self._mouse_enabled and \
                    event.button in (1, 2, 3) or \
                    event.type == FINGERUP and self._touchscreen_enabled and \
                    self._menu is not None and \
                    not (self._drop_frame is not None and
                         self._drop_frame.get_scrollarea(inner=True).is_scrolling()):

                # Check for mouse clicks within
                if self.active:
                    for btn in self._option_buttons:
                        btn.set_attribute('ignore_scroll_to_widget')
                        updated = btn.update(events)
                        try:
                            btn.remove_attribute('ignore_scroll_to_widget')
                        except IndexError:
                            pass
                        if updated:
                            return True

                # Get event position based on input type
                event_pos = get_finger_pos(self._menu, event)

                # If collides
                rect = self.get_rect(to_real_position=True, apply_padding=False)
                if rect.collidepoint(*event_pos):
                    # Check if mouse collides left or right as percentage, use only X coordinate
                    mouse_x, _ = event.pos
                    topleft, _ = rect.topleft
                    topright, _ = rect.topright
                    dist = mouse_x - (topleft + self._title_size[0])  # Distance from title
                    if dist > 0:  # User clicked the options, not title
                        self._toggle_drop()
                        updated = True

                else:
                    if self.active and not self.get_focus_rect().collidepoint(*event_pos):
                        self._toggle_drop()
                        updated = True

            # Check mousemove
            # elif event.type == pygame.MOUSEMOTION:
            #     for btn in self._option_buttons:
            #         btn._check_mouseover(event)

        return updated


class _SelectionDropNotMakedException(Exception):
    """
    Exception thrown if drop selection has not been maked.
    """
    pass
