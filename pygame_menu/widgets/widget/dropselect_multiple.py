"""
pygame-menu
https://github.com/ppizarror/pygame-menu

DROPSELECT MULTIPLE
Drop select where multiple options can be selected at the same time.

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

__all__ = ['DropSelectMultiple']

import pygame

from pygame_menu.font import FontType
from pygame_menu.utils import assert_color, assert_vector
from pygame_menu.widgets.widget.button import Button
from pygame_menu.widgets.widget.dropselect import DropSelect

from pygame_menu._types import Tuple, Union, List, Any, Optional, CallbackType, \
    ColorType, ColorInputType, Tuple2IntType, Tuple3IntType, PaddingType, \
    Tuple2NumberType, CursorInputType


# noinspection PyMissingOrEmptyDocstring
class DropSelectMultiple(DropSelect):
    """
    Drop select multiple is a drop select which can select many options at the
    same time. This drops a vertical frame if requested.

    The items of the DropSelectMultiple are:

    .. code-block:: python

        items = [('Item1', a, b, c...), ('Item2', d, e, f...), ('Item3', g, h, i...)]

    The callbacks receive the current selected items (tuple) and the indices (tuple), where
    ``selected_item=widget.get_value()`` and ``selected_index=widget.get_index()``:

    .. code-block:: python

        onchange((selected_item, selected_index), **kwargs)
        onreturn((selected_item, selected_index), **kwargs)

    For example, if ``selected_index=[0, 2]`` then ``selected_item=[('Item1', a, b, c...), ('Item3', g, h, i...)]``.

    .. note::

        DropSelectMultiple only implements translation.

    :param title: Drop select title
    :param items: Items of the drop select
    :param dropselect_id: ID of the drop select
    :param default: Index(es) of default item(s) to display. If ``None`` no item is selected
    :param max_selected: Max items to be selected. If ``0`` there's no limit
    :param onchange: Callback when changing the drop select item
    :param onreturn: Callback when pressing return on the selected item
    :param onselect: Function when selecting the widget
    :param open_middle: If ``True`` the selection box is opened in the middle of the menu
    :param placeholder: Text shown if no option is selected yet
    :param placeholder_add_to_selection_box: If ``True`` adds the placeholder button to the selection box
    :param placeholder_selected: Text shown if option is selected. Accepts the number of selected options
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
    :param selection_option_active_bgcolor: Active option(s) background color; active options is the currently active (by user)
    :param selection_option_active_font_color: Active option(s) font color
    :param selection_option_border_color: Option border color
    :param selection_option_border_width: Option border width
    :param selection_option_cursor: Option cursor. If ``None`` use the same cursor as the widget
    :param selection_option_font: Option font. If ``None`` use the same font as the widget
    :param selection_option_font_color: Option font color
    :param selection_option_font_size: Option font size. If ``None`` use the 100% of the widget font size
    :param selection_option_padding: Selection padding. See padding styling
    :param selection_option_selected_bgcolor: Selected option(s) background color
    :param selection_option_selected_box: Draws a box in the selected option(s)
    :param selection_option_selected_box_border: Box border width in px
    :param selection_option_selected_box_color: Box color
    :param selection_option_selected_box_height: Height of the selection box relative to the options height
    :param selection_option_selected_box_margin: Option box margin (left, right, vertical) in px
    :param selection_option_selected_font_color: Selected option(s) font color
    :param kwargs: Optional keyword arguments
    """
    _max_selected: int
    _placeholder_selected: str
    _selected_indices: List[int]
    _selection_option_active_bgcolor: ColorType
    _selection_option_active_font_color: ColorType
    _selection_option_selected_box: bool
    _selection_option_selected_box_color: ColorType
    _selection_option_selected_box_width: int

    def __init__(
            self,
            title: Any,
            items: Union[List[Tuple[Any, ...]], List[str]],
            dropselect_id: str = '',
            default: Optional[Union[int, List[int]]] = None,
            max_selected: int = 0,
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: CallbackType = None,
            open_middle: bool = False,
            placeholder: str = 'Select an option',
            placeholder_add_to_selection_box: bool = True,
            placeholder_selected: str = '{0} selected',
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
            selection_option_active_bgcolor: ColorInputType = (188, 227, 244),
            selection_option_active_font_color: ColorInputType = (0, 0, 0),
            selection_option_border_color: ColorInputType = (220, 220, 220),
            selection_option_border_width: int = 1,
            selection_option_cursor: CursorInputType = None,
            selection_option_font: Optional[FontType] = None,
            selection_option_font_color: ColorInputType = (0, 0, 0),
            selection_option_font_size: Optional[int] = None,
            selection_option_padding: PaddingType = 5,
            selection_option_selected_bgcolor: ColorInputType = (142, 247, 141),
            selection_option_selected_box: bool = True,
            selection_option_selected_box_border: int = 1,
            selection_option_selected_box_color: ColorInputType = (150, 150, 150),
            selection_option_selected_box_height: float = 0.5,
            selection_option_selected_box_margin: Tuple3IntType = (0, 5, 0),
            selection_option_selected_font_color: ColorInputType = (0, 0, 0),
            *args,
            **kwargs
    ) -> None:
        super(DropSelectMultiple, self).__init__(
            dropselect_id=dropselect_id,
            items=items,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            open_middle=open_middle,
            placeholder=placeholder,
            placeholder_add_to_selection_box=placeholder_add_to_selection_box,
            selection_box_arrow_color=selection_box_arrow_color,
            selection_box_arrow_margin=selection_box_arrow_margin,
            selection_box_bgcolor=selection_box_bgcolor,
            selection_box_border_color=selection_box_border_color,
            selection_box_border_width=selection_box_border_width,
            selection_box_height=selection_box_height,
            selection_box_inflate=selection_box_inflate,
            selection_box_margin=selection_box_margin,
            selection_box_text_margin=selection_box_text_margin,
            selection_box_width=selection_box_width,
            selection_infinite=selection_infinite,
            selection_option_border_color=selection_option_border_color,
            selection_option_border_width=selection_option_border_width,
            selection_option_cursor=selection_option_cursor,
            selection_option_font=selection_option_font,
            selection_option_font_color=selection_option_font_color,
            selection_option_font_size=selection_option_font_size,
            selection_option_padding=selection_option_padding,
            selection_option_selected_bgcolor=selection_option_selected_bgcolor,
            selection_option_selected_font_color=selection_option_selected_font_color,
            title=title,
            **kwargs
        )

        # Asserts
        assert isinstance(placeholder_selected, str)
        assert isinstance(selection_option_selected_box, bool)
        assert isinstance(selection_option_selected_box_border, int) and \
               selection_option_selected_box_border > 0
        assert_vector(selection_option_selected_box_margin, 3, int)
        assert isinstance(selection_option_selected_box_height, (int, float))
        assert 0 < selection_option_selected_box_height <= 1, \
            'height factor must be between 0 and 1'
        assert isinstance(max_selected, int) and max_selected >= 0

        # Configure parent
        self._args = args or []
        self._close_on_apply = False
        self._max_selected = max_selected
        self._selection_option_left_space = True
        self._selection_option_left_space_height_factor = selection_option_selected_box_height
        self._selection_option_left_space_margin = selection_option_selected_box_margin

        # Set style
        self._placeholder_selected = placeholder_selected
        self._selection_option_active_bgcolor = assert_color(selection_option_active_bgcolor)
        self._selection_option_active_font_color = assert_color(selection_option_active_font_color)
        self._selection_option_selected_box = selection_option_selected_box
        self._selection_option_selected_box_color = assert_color(selection_option_selected_box_color)
        self._selection_option_selected_box_width = selection_option_selected_box_border

        self.set_default_value(default)

    def get_index(self) -> List[int]:
        """
        Get selected index(es).

        :return: Selected index
        """
        return self._selected_indices.copy()

    def _render_option_string(self, text: str) -> 'pygame.Surface':
        color = self._selection_option_font_style['color']
        if self.readonly or \
                len(self._selected_indices) == 0 or \
                self._max_selected != 0 and len(self._selected_indices) == self._max_selected:
            color = self._font_readonly_color
        text = text.replace('\t', ' ' * self._tab_size)
        return self._option_font.render(text, self._font_antialias, color)

    def _click_option(self, index: int, btn: 'Button') -> None:
        btn.set_attribute('ignore_scroll_to_widget')
        self.set_value(index)
        self._process_index()
        if self._index != -1:
            self.change(*self._items[self._index][1:])
        if self._close_on_apply:
            self.active = False
            if self._drop_frame is not None:
                self._drop_frame.hide()
        btn.remove_attribute('ignore_scroll_to_widget')

    def _apply_font(self) -> None:
        prev_selection_box_width = self._selection_box_width
        super(DropSelectMultiple, self)._apply_font()
        if prev_selection_box_width == 0:
            f1 = self._render_option_string(self._placeholder)
            f2 = self._render_option_string(self._placeholder_selected.format(999))
            h = self._render_string(self._title, self.get_font_color_status()).get_height()
            self._selection_box_width = int(max(f1.get_width(), f2.get_width())
                                            + self._selection_box_arrow_margin[0]
                                            + self._selection_box_arrow_margin[1]
                                            + h - h / 4
                                            + 2 * self._selection_box_border_width)

    def _get_current_selected_text(self) -> str:
        if len(self._selected_indices) == 0:
            current_selected = self._placeholder
        else:
            current_selected = self._placeholder_selected.format(len(self._selected_indices))
        return current_selected

    def get_value(self) -> Tuple[List[Union[Tuple[Any, ...], str]], List[int]]:
        selected_items = []
        for j in self._selected_indices:
            selected_items.append(self._items[j])
        return selected_items, self.get_index()

    def get_total_selected(self) -> int:
        """
        Return the total number of selected items.

        :return: Number of selected items
        """
        return len(self._selected_indices)

    def set_default_value(self, default: Optional[Union[int, List[int]]]) -> 'DropSelectMultiple':
        if default is None:
            default = []
        if isinstance(default, int):
            default = [default]
        for i in default:
            assert isinstance(i, int) and 0 <= i < len(self._items), \
                'each default index must be an integer between 0 and the number ' \
                'of elements ({0})' \
                ''.format(len(self._items) - 1)
        self._default_value = default.copy()
        self._selected_indices = default.copy()
        if self._drop_frame is not None:
            self._drop_frame.set_menu(None)
        self._drop_frame = None
        self.active = False
        self.render()
        return self

    def update_items(self, items: Union[List[Tuple[Any, ...]], List[str]]) -> None:
        """
        Update drop select multiple items. This method updates the current index,
        but removes the selected indices.

        .. note::

            If the length of the list is different than the previous one, the new
            index of the select will be the first item of the list.

        :param items: New drop select items; format ``[('Item1', a, b, c...), ('Item2', d, e, f...)]``
        :return: None
        """
        super(DropSelectMultiple, self).update_items(items)
        self._default_value = []
        self._selected_indices = []

    def _process_index(self) -> None:
        """
        Process current index, add to selected or remove if present.

        :return: None
        """
        if self._index == -1:
            return
        if self._index in self._selected_indices:
            self._selected_indices.remove(self._index)
        else:
            if self._max_selected == 0 or len(self._selected_indices) < self._max_selected:
                self._selected_indices.append(self._index)
                self._selected_indices.sort()
            else:
                self._sound.play_event_error()
        self._update_buttons()

    def reset_value(self) -> 'DropSelectMultiple':
        self._index = -1
        self._selected_indices = self._default_value.copy()
        self._update_buttons()
        return self

    def set_value(self, item: Union[str, int], process_index: bool = False) -> None:
        """
        Set the current value of the widget, selecting the item that matches
        the text if ``item`` is a string, or the index if ``item`` is an integer.
        This method raises ``ValueError`` if no item found.

        For example, if widget item list is ``[['a',0],['b',1],['a',2]]``:

        - *widget*.set_value('a') -> Widget selects the first item (index 0)
        - *widget*.set_value(2) -> Widget selects the third item (index 2)

        This method only changes the active index, for adding the new item to the
        selected indices set ``process_index=True``.

        .. note::

            This method does not trigger any event (change).

        :param item: Item to select, can be a string or an integer
        :param process_index: Adds/Removes the index from the selected indices list
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
                raise ValueError('no value "{}" found in drop select multiple'.format(item))
        elif isinstance(item, int):
            assert -1 <= item < len(self._items), \
                'item index must be greater than zero and lower than the number ' \
                'of items on the drop select multiple'
            self._index = item

        if process_index:
            self._process_index()

        # Update options background selection
        self._update_buttons()

    def _update_buttons(self) -> None:
        """
        Update buttons.

        :return: None
        """
        for b_ind_x in range(len(self._option_buttons)):
            btn = self._option_buttons[b_ind_x]
            if b_ind_x == self._index:
                btn.set_background_color(self._selection_option_active_bgcolor)
                btn.update_font({'color': self._selection_option_active_font_color})
                btn.scroll_to_widget(scroll_parent=False)
            elif b_ind_x in self._selected_indices:
                btn.set_background_color(self._selection_option_selected_bgcolor)
                btn.update_font({'color': self._selection_option_font_style['color_selected']})
            else:
                btn.set_background_color(self._selection_box_bgcolor)
                btn.update_font({'color': self._selection_option_font_style['color']})
            deco = btn.get_decorator()
            if btn.has_attribute('deco_on'):
                if b_ind_x in self._selected_indices:
                    deco.enable(btn.get_attribute('deco_on'))
                    deco.disable(btn.get_attribute('deco_off'))
                else:
                    deco.disable(btn.get_attribute('deco_on'))
                    deco.enable(btn.get_attribute('deco_off'))

    def make_selection_drop(self, **kwargs) -> 'DropSelectMultiple':
        super(DropSelectMultiple, self).make_selection_drop(**kwargs)
        # Add button decorations
        for btn in self._option_buttons:
            deco = btn.get_decorator()
            total_height = btn.get_height(apply_padding=False)
            dh = btn.get_attribute('left_space_height')
            x, y = btn.get_position()
            off = deco.add_rectangle(x - dh - self._selection_option_left_space_margin[1],
                                     y + (total_height - dh) / 2,
                                     dh, dh, self._selection_option_selected_box_color,
                                     self._selection_option_selected_box_width,
                                     use_center_positioning=False)
            on = deco.add_rectangle(x - dh - self._selection_option_left_space_margin[1],
                                    y + (total_height - dh) / 2,
                                    dh, dh, self._selection_option_selected_box_color,
                                    use_center_positioning=False)
            deco.disable(on)
            btn.set_attribute('deco_on', on)
            btn.set_attribute('deco_off', off)
        return self

    def apply(self, *args) -> Any:
        self._process_index()
        super(DropSelectMultiple, self).apply()

    def change(self, *args) -> Any:
        super(DropSelectMultiple, self).change()
