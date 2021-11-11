"""
pygame-menu
https://github.com/ppizarror/pygame-menu

DROPSELECT MULTIPLE
Drop select where multiple options can be selected at the same time.
"""

__all__ = [

    # Main Class
    'DropSelectMultiple',
    'DropSelectMultipleManager',

    # Constants
    'DROPSELECT_MULTIPLE_SFORMAT_LIST_COMMA',
    'DROPSELECT_MULTIPLE_SFORMAT_LIST_HYPHEN',
    'DROPSELECT_MULTIPLE_SFORMAT_TOTAL',

    # Type
    'DropSelectMultipleSFormatType'

]

import pygame
import pygame_menu

from abc import ABC
from pygame_menu.font import FontType
from pygame_menu.locals import POSITION_NORTHWEST, POSITION_SOUTHEAST
from pygame_menu.utils import assert_color, assert_vector, is_callable
from pygame_menu.widgets.core.widget import AbstractWidgetManager, Widget
from pygame_menu.widgets.widget.button import Button
from pygame_menu.widgets.widget.dropselect import DropSelect

from pygame_menu._types import Tuple, Union, List, Any, Optional, CallbackType, \
    ColorType, ColorInputType, Tuple2IntType, Tuple3IntType, PaddingType, \
    Tuple2NumberType, CursorInputType, NumberType, Literal, Callable

DROPSELECT_MULTIPLE_SFORMAT_LIST_COMMA = 'comma-list'
DROPSELECT_MULTIPLE_SFORMAT_LIST_HYPHEN = 'hyphen-list'
DROPSELECT_MULTIPLE_SFORMAT_TOTAL = 'total'

DropSelectMultipleSFormatType = Union[Literal[DROPSELECT_MULTIPLE_SFORMAT_TOTAL,
                                              DROPSELECT_MULTIPLE_SFORMAT_LIST_COMMA,
                                              DROPSELECT_MULTIPLE_SFORMAT_LIST_HYPHEN],
                                      Callable[[List[str]], str]]


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

        DropSelectMultiple accepts the same transformations as :py:class:`pygame_menu.widgets.DropSelect`.

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
    :param placeholder_selected: Text shown if option is selected. Accepts the formatted option from ``selection_placeholder_format``
    :param scrollbar_color: Scrollbar color
    :param scrollbar_cursor: Cursor of the scrollbars if mouse is placed over. By default is ``None``
    :param scrollbar_shadow: Indicate if a shadow is drawn on each scrollbar
    :param scrollbar_shadow_color: Color of the shadow of each scrollbar
    :param scrollbar_shadow_offset: Offset of the scrollbar shadow in px
    :param scrollbar_shadow_position: Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
    :param scrollbar_slider_color: Color of the sliders
    :param scrollbar_slider_hover_color: Color of the slider if hovered or clicked
    :param scrollbar_slider_pad: Space between slider and scrollbars borders in px
    :param scrollbar_thick: Scrollbar thickness in px
    :param scrollbars: Scrollbar position. See :py:mod:`pygame_menu.locals`
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
    :param selection_placeholder_format: Format of the string replaced in ``placeholder_selected``. Can be a predefined string type ("total", "comma-list", "hyphen-list", or any other string which will join the list) or a function that receives the list of selected items and returns a string
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
    _selection_placeholder_format: DropSelectMultipleSFormatType

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
            scrollbar_color: ColorInputType = (235, 235, 235),
            scrollbar_cursor: CursorInputType = None,
            scrollbar_shadow: bool = False,
            scrollbar_shadow_color: ColorInputType = (0, 0, 0),
            scrollbar_shadow_offset: int = 2,
            scrollbar_shadow_position: str = POSITION_NORTHWEST,
            scrollbar_slider_color: ColorInputType = (200, 200, 200),
            scrollbar_slider_hover_color: ColorInputType = (170, 170, 170),
            scrollbar_slider_pad: NumberType = 0,
            scrollbar_thick: int = 20,
            scrollbars: str = POSITION_SOUTHEAST,
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
            selection_placeholder_format: DropSelectMultipleSFormatType = DROPSELECT_MULTIPLE_SFORMAT_TOTAL,
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
            scrollbar_color=scrollbar_color,
            scrollbar_cursor=scrollbar_cursor,
            scrollbar_shadow=scrollbar_shadow,
            scrollbar_shadow_color=scrollbar_shadow_color,
            scrollbar_shadow_offset=scrollbar_shadow_offset,
            scrollbar_shadow_position=scrollbar_shadow_position,
            scrollbar_slider_color=scrollbar_slider_color,
            scrollbar_slider_hover_color=scrollbar_slider_hover_color,
            scrollbar_slider_pad=scrollbar_slider_pad,
            scrollbar_thick=scrollbar_thick,
            scrollbars=scrollbars,
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
        self._selection_placeholder_format = selection_placeholder_format

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
            return self._placeholder

        # Apply selected format
        if self._selection_placeholder_format == DROPSELECT_MULTIPLE_SFORMAT_TOTAL:
            return self._placeholder_selected.format(len(self._selected_indices))

        list_items = self._get_selected_items_list_str()
        if self._selection_placeholder_format == DROPSELECT_MULTIPLE_SFORMAT_LIST_COMMA:
            return self._placeholder_selected.format(','.join(list_items))

        elif self._selection_placeholder_format == DROPSELECT_MULTIPLE_SFORMAT_LIST_HYPHEN:
            return self._placeholder_selected.format('-'.join(list_items))

        elif isinstance(self._selection_placeholder_format, str):
            return self._placeholder_selected.format(self._selection_placeholder_format.join(list_items))

        elif is_callable(self._selection_placeholder_format):
            try:
                o = self._selection_placeholder_format(list_items)
            except TypeError:
                raise ValueError('selection placeholder function receives only 1 '
                                 'argument (a list of the selected items string)'
                                 ' and must return a string')
            assert isinstance(o, str), \
                f'output from selection placeholder format function must be a ' \
                f'string (List[str]=>str), not {type(o)} type ({o} returned)'
            return self._placeholder_selected.format(o)

        else:
            raise ValueError('invalid selection placeholder format type')

    def _get_selected_items_list_str(self) -> List[str]:
        """
        Return the selected items list of strings.

        :return: List string of selected items
        """
        sel_items = []
        for i in self._selected_indices:
            sel_items.append(self._items[i][0])
        return sel_items

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
        if default is None or default == -1:
            default = []
        if isinstance(default, int):
            default = [default]
        for i in default:
            assert isinstance(i, int) and 0 <= i < len(self._items), \
                f'each default index must be an integer between 0 and the number ' \
                f'of elements ({len(self._items) - 1})'
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
            index of the select will be the ``-1``, that is, same as the unselected
            status.

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
        self._render()
        return self

    def value_changed(self) -> bool:
        if len(self._default_value) != len(self._selected_indices):
            return True
        for v in self._selected_indices:
            if v not in self._default_value:
                return True
        return False

    def set_value(self, item: Union[str, int], process_index: bool = False) -> None:
        """
        Set the current value of the widget, selecting the item that matches
        the text if ``item`` is a string, or the index if ``item`` is an integer.
        This method raises ``ValueError`` if no item found.

        For example, if widget item list is ``[['a', 0], ['b', 1], ['a', 2]]``:

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
                raise ValueError(f'no value "{item}" found in drop select multiple')
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

    def _make_selection_drop(self) -> 'DropSelectMultiple':
        super(DropSelectMultiple, self)._make_selection_drop()
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


class DropSelectMultipleManager(AbstractWidgetManager, ABC):
    """
    DropSelectMultiple manager.
    """

    def dropselect_multiple(
            self,
            title: Any,
            items: Union[List[Tuple[Any, ...]], List[str]],
            default: Optional[Union[int, List[int]]] = None,
            dropselect_multiple_id: str = '',
            max_selected: int = 0,
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            open_middle: bool = False,
            placeholder: str = 'Select an option',
            placeholder_add_to_selection_box: bool = True,
            placeholder_selected: str = '{0} selected',
            selection_placeholder_format: DropSelectMultipleSFormatType = DROPSELECT_MULTIPLE_SFORMAT_TOTAL,
            **kwargs
    ) -> 'pygame_menu.widgets.DropSelectMultiple':
        """
        Add a dropselect multiple to the Menu: Drop select multiple is a drop
        select which can select many options at the same time. This drops a
        vertical frame if requested.

        The items of the DropSelectMultiple are:

        .. code-block:: python

            items = [('Item1', a, b, c...), ('Item2', d, e, f...), ('Item3', g, h, i...)]

        The callbacks receive the current selected items (tuple) and the indices
        (tuple), where ``selected_item=widget.get_value()`` and
        ``selected_index=widget.get_index()``:

        .. code-block:: python

            onchange((selected_item, selected_index), **kwargs)
            onreturn((selected_item, selected_index), **kwargs)

        For example, if ``selected_index=[0, 2]`` then ``selected_item=[('Item1', a, b, c...), ('Item3', g, h, i...)]``.

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
            - ``float``                         (bool) - If ``True`` the widget don't contributes width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled
            - ``tab_size``                      (int) – Width of a tab character

        kwargs for modifying selection box/option style (Optional)
            - ``scrollbar_color``                       (tuple, list, str, int, :py:class:`pygame.Color`) – Scrollbar color
            - ``scrollbar_cursor``                      (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the scrollbars if the mouse is placed over
            - ``scrollbar_shadow_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the shadow of each scrollbar
            - ``scrollbar_shadow_offset``               (int) – Offset of the scrollbar shadow in px
            - ``scrollbar_shadow_position``             (str) – Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
            - ``scrollbar_shadow``                      (bool) – Indicate if a shadow is drawn on each scrollbar
            - ``scrollbar_slider_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the sliders
            - ``scrollbar_slider_hover_color``          (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the slider if hovered or clicked
            - ``scrollbar_slider_pad``                  (int, float) – Space between slider and scrollbars borders in px
            - ``scrollbar_thick``                       (int) – Scrollbar thickness in px
            - ``scrollbars``                            (str) – Scrollbar position. See :py:mod:`pygame_menu.locals`
            - ``selection_box_arrow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Selection box arrow color
            - ``selection_box_arrow_margin``            (tuple) – Selection box arrow margin (left, right, vertical) in px
            - ``selection_box_bgcolor``                 (tuple, list, str, int, :py:class:`pygame.Color`) – Selection box background color
            - ``selection_box_border_color``            (tuple, list, str, int, :py:class:`pygame.Color`) – Selection box border color
            - ``selection_box_border_width``            (int) – Selection box border width
            - ``selection_box_height``                  (int) – Selection box height, counted as how many options are packed before showing scroll
            - ``selection_box_inflate``                 (tuple) – Selection box inflate on x-axis and y-axis in px
            - ``selection_box_margin``                  (tuple, list) – Selection box on x-axis and y-axis (x, y) margin from title in px
            - ``selection_box_text_margin``             (int) – Selection box text margin (left) in px
            - ``selection_box_width``                   (int) – Selection box width in px. If ``0`` compute automatically to fit placeholder
            - ``selection_infinite``                    (bool) – If ``True`` selection can rotate through bottom/top
            - ``selection_option_active_bgcolor``       (tuple, list, str, int, :py:class:`pygame.Color`) – Active option(s) background color; active options is the currently active (by user)
            - ``selection_option_active_font_color``    (tuple, list, str, int, :py:class:`pygame.Color`) – Active option(s) font color
            - ``selection_option_border_color``         (tuple, list, str, int, :py:class:`pygame.Color`) – Option border color
            - ``selection_option_border_width``         (int) – Option border width
            - ``selection_option_font_color``           (tuple, list, str, int, :py:class:`pygame.Color`) – Option font color
            - ``selection_option_font_size``            (int, None) – Option font size. If ``None`` use the 75% of the widget font size
            - ``selection_option_font``                 (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Option font. If ``None`` use the same font as the widget
            - ``selection_option_padding``              (int, float, tuple, list) – Selection padding. See padding styling
            - ``selection_option_selected_bgcolor``     (tuple, list, str, int, :py:class:`pygame.Color`) – Selected option background color
            - ``selection_option_selected_box_border``  (int) – Box border width in px
            - ``selection_option_selected_box_color``   (tuple, list, str, int, :py:class:`pygame.Color`) – Box color
            - ``selection_option_selected_box_height``  (int, float) – Height of the selection box relative to the options height
            - ``selection_option_selected_box_margin``  (tuple, list) – Option box margin (left, right, vertical) in px
            - ``selection_option_selected_box``         (bool) – Draws a box in the selected option(s)
            - ``selection_option_selected_font_color``  (tuple, list, str, int, :py:class:`pygame.Color`) – Selected option font color

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Drop select title
        :param items: Item list of the drop select; format ``[('Item1', a, b, c...), ('Item2', d, e, f...)]``
        :param default: Index(es) of default item(s) to display. If ``None`` no item is selected
        :param dropselect_multiple_id: ID of the dropselect multiple
        :param max_selected: Max items to be selected. If ``0`` there's no limit
        :param onchange: Callback when changing the drop select item
        :param onreturn: Callback when pressing return on the selected item
        :param onselect: Function when selecting the widget
        :param open_middle: If ``True`` the selection box is opened in the middle of the menu
        :param placeholder: Text shown if no option is selected yet
        :param placeholder_add_to_selection_box: If ``True`` adds the placeholder button to the selection box
        :param placeholder_selected: Text shown if option is selected. Accepts the number of selected options
        :param selection_placeholder_format: Format of the string replaced in ``placeholder_selected``. Can be a predefined string type ("total", "comma-list", "hyphen-list", or any other string which will join the list) or a function that receives the list of selected items and returns a string
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.DropSelectMultiple`
        """
        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        # Get selection box properties
        selection_box_arrow_color = kwargs.pop('selection_box_arrow_color',
                                               self._theme.widget_box_arrow_color)
        selection_box_arrow_margin = kwargs.pop('selection_box_arrow_margin',
                                                self._theme.widget_box_arrow_margin)
        selection_box_bgcolor = kwargs.pop('selection_box_bgcolor',
                                           self._theme.widget_box_background_color)
        selection_box_border_color = kwargs.pop('selection_box_border_color',
                                                self._theme.widget_box_border_color)
        selection_box_border_width = kwargs.pop('selection_box_border_width',
                                                self._theme.widget_box_border_width)
        selection_box_height = kwargs.pop('selection_box_height', 3)
        selection_box_inflate = kwargs.pop('selection_box_inflate',
                                           self._theme.widget_border_inflate)
        selection_box_margin = kwargs.pop('selection_box_margin',
                                          self._theme.widget_box_margin)
        selection_box_text_margin = kwargs.pop('selection_box_text_margin',
                                               self._theme.widget_box_arrow_margin[0])
        selection_box_width = kwargs.pop('selection_box_width', 0)
        selection_infinite = kwargs.pop('selection_infinite', False)
        selection_option_active_bgcolor = kwargs.pop('selection_option_active_bgcolor',
                                                     (188, 227, 244))
        selection_option_active_font_color = kwargs.pop('selection_option_active_font_color',
                                                        (0, 0, 0))
        selection_option_border_color = kwargs.pop('selection_option_border_color',
                                                   self._theme.scrollbar_color)
        selection_option_border_width = kwargs.pop('selection_option_border_width',
                                                   self._theme.widget_box_border_width)
        # selection_option_cursor = kwargs.pop('selection_option_cursor', None)
        selection_option_font = kwargs.pop('selection_option_font', None)
        selection_option_font_color = kwargs.pop('selection_option_font_color', (0, 0, 0))
        selection_option_font_size = kwargs.pop('selection_option_font_size', None)
        selection_option_padding = kwargs.pop('selection_option_padding', (2, 5))
        selection_option_selected_bgcolor = kwargs.pop('selection_option_selected_bgcolor',
                                                       (142, 247, 141))
        selection_option_selected_box = kwargs.pop('selection_option_selected_box', True)
        selection_option_selected_box_border = kwargs.pop('selection_option_selected_box_border',
                                                          self._theme.widget_box_border_width)
        selection_option_selected_box_color = kwargs.pop('selection_option_selected_box_color',
                                                         self._theme.widget_box_arrow_color)
        selection_option_selected_box_height = kwargs.pop('selection_option_selected_box_height',
                                                          0.5)
        selection_option_selected_box_margin = kwargs.pop('selection_option_selected_box_margin',
                                                          (0, self._theme.widget_box_arrow_margin[1],
                                                           self._theme.widget_box_arrow_margin[2]))
        selection_option_selected_font_color = kwargs.pop('selection_option_selected_font_color',
                                                          (0, 0, 0))

        # Get selection box scrollbar properties
        scrollbar_color = kwargs.pop('scrollbar_color', self._theme.scrollbar_color)
        scrollbar_cursor = kwargs.pop('scrollbar_cursor', self._theme.scrollbar_cursor)
        scrollbar_shadow_color = kwargs.pop('scrollbar_shadow_color',
                                            self._theme.scrollbar_shadow_color)
        scrollbar_shadow_offset = kwargs.pop('scrollbar_shadow_offset',
                                             self._theme.scrollbar_shadow_offset)
        scrollbar_shadow_position = kwargs.pop('scrollbar_shadow_position',
                                               self._theme.scrollbar_shadow_position)
        scrollbar_shadow = kwargs.pop('scrollbar_shadow', self._theme.scrollbar_shadow)
        scrollbar_slider_color = kwargs.pop('scrollbar_slider_color',
                                            self._theme.scrollbar_slider_color)
        scrollbar_slider_hover_color = kwargs.pop('scrollbar_slider_hover_color',
                                                  self._theme.scrollbar_slider_hover_color)
        scrollbar_slider_pad = kwargs.pop('scrollbar_slider_pad',
                                          self._theme.scrollbar_slider_pad)
        scrollbar_thick = kwargs.pop('scrollbar_thick', self._theme.scrollbar_thick)
        scrollbars = kwargs.pop('scrollbars', self._theme.scrollarea_position)

        widget = DropSelectMultiple(
            default=default,
            dropselect_id=dropselect_multiple_id,
            items=items,
            max_selected=max_selected,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            open_middle=open_middle,
            placeholder=placeholder,
            placeholder_add_to_selection_box=placeholder_add_to_selection_box,
            placeholder_selected=placeholder_selected,
            scrollbar_color=scrollbar_color,
            scrollbar_cursor=scrollbar_cursor,
            scrollbar_shadow=scrollbar_shadow,
            scrollbar_shadow_color=scrollbar_shadow_color,
            scrollbar_shadow_offset=scrollbar_shadow_offset,
            scrollbar_shadow_position=scrollbar_shadow_position,
            scrollbar_slider_color=scrollbar_slider_color,
            scrollbar_slider_hover_color=scrollbar_slider_hover_color,
            scrollbar_slider_pad=scrollbar_slider_pad,
            scrollbar_thick=scrollbar_thick,
            scrollbars=scrollbars,
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
            selection_option_active_bgcolor=selection_option_active_bgcolor,
            selection_option_active_font_color=selection_option_active_font_color,
            selection_option_border_color=selection_option_border_color,
            selection_option_border_width=selection_option_border_width,
            # selection_option_cursor=selection_option_cursor,
            selection_option_font=selection_option_font,
            selection_option_font_color=selection_option_font_color,
            selection_option_font_size=selection_option_font_size,
            selection_option_padding=selection_option_padding,
            selection_option_selected_bgcolor=selection_option_selected_bgcolor,
            selection_option_selected_box=selection_option_selected_box,
            selection_option_selected_box_border=selection_option_selected_box_border,
            selection_option_selected_box_color=selection_option_selected_box_color,
            selection_option_selected_box_height=selection_option_selected_box_height,
            selection_option_selected_box_margin=selection_option_selected_box_margin,
            selection_option_selected_font_color=selection_option_selected_font_color,
            selection_placeholder_format=selection_placeholder_format,
            title=title,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget
