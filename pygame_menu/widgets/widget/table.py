"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TABLE
The table widget is a Frame which packs widgets in a structured way.

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

__all__ = ['Table']

import pygame

from pygame_menu.baseimage import BaseImage
from pygame_menu.font import FontType, assert_font
from pygame_menu.locals import ORIENTATION_VERTICAL, ALIGN_LEFT, ALIGN_CENTER, \
    ORIENTATION_HORIZONTAL, POSITION_NORTH, POSITION_CENTER, POSITION_SOUTH, \
    ALIGN_RIGHT, POSITION_WEST, POSITION_EAST
from pygame_menu.utils import assert_alignment, assert_color, uuid4, parse_padding, \
    assert_position, assert_vector
from pygame_menu.widgets.core.widget import Widget, WidgetBorderPositionType, \
    WIDGET_FULL_BORDER, WIDGET_BORDER_POSITION_NONE
from pygame_menu.widgets.widget.frame import Frame
from pygame_menu.widgets.widget.image import Image
from pygame_menu.widgets.widget.label import Label
from pygame_menu.widgets.widget.surface import SurfaceWidget

from pygame_menu._types import List, Union, ColorInputType, Optional, Tuple, \
    VectorInstance, PaddingType, Dict, NumberType, Vector2IntType

CellType = Union['Widget', str, int, float, bool, 'BaseImage', 'pygame.Surface']
ColumnInputType = Union[Tuple[CellType, ...], List[CellType]]


# noinspection PyMissingOrEmptyDocstring
class Table(Frame):
    """
    Table is a frame which can pack widgets in a structured way.

    .. note::

        Table only implements translation transformation.

    .. note::

        Table cannot be selected. Thus, it does not receive any selection effect.

    :param table_id: ID of the table
    """
    _rows: List['Frame']
    default_cell_align: str
    default_cell_border_color: ColorInputType
    default_cell_border_position: WidgetBorderPositionType
    default_cell_border_width: int
    default_cell_padding: PaddingType
    default_cell_vertical_position: str
    default_row_background_color: Optional[ColorInputType]

    def __init__(
            self,
            table_id: str = ''
    ) -> None:
        super(Table, self).__init__(
            width=1,
            height=1,
            orientation=ORIENTATION_VERTICAL,
            frame_id=table_id
        )

        # Internals
        self._rows = []

        # Frame behaviour
        self._accepts_scrollarea = False
        self._accepts_title = False

        # Set size
        self._frame_size = (0, 0)
        self._height = 0
        self._real_rect = pygame.Rect(0, 0, 0, 0)
        self._width = 0

        # Default cell properties
        self.default_cell_align = ALIGN_LEFT
        self.default_cell_border_color = (0, 0, 0)
        self.default_cell_border_position = WIDGET_FULL_BORDER
        self.default_cell_border_width = 1
        self.default_cell_padding = 0
        self.default_cell_vertical_position = POSITION_NORTH
        self.default_row_background_color = None

        # Finals
        self.relax()

    def pack(self, *args, **kwargs) -> None:
        raise RuntimeError('{0} cannot pack external widgets'.format(self.get_class_id()))

    def remove_row(self, row: 'Frame') -> None:
        """
        Removes row from the table.

        :param row: Row frame
        :return: None
        """
        self.unpack(row)

    def unpack(self, row: 'Frame') -> None:
        assert row != self, 'table cannot unpack itself'
        assert len(self._widgets) > 0, 'table is empty'
        assert row in self._rows and row.get_id() in self._widgets.keys(), \
            'row {0} does not exist on {1}'.format(row.get_class_id(), self.get_class_id())
        wid = row.get_id()
        assert row._frame == self, 'widget frame differs from current'
        row._frame = None
        row._translate_virtual = (0, 0)
        del self._widgets[wid]
        try:
            del self._pos[wid]
        except KeyError:
            pass
        self._rows.remove(row)
        self._menu_render()
        self._update_row_sizing()

        # Remove scrollable from rows
        if self._menu is not None:
            total_removed = 0
            menu_update_frames = self._get_menu_update_frames()
            for w in row.get_widgets(unpack_subframes=False):
                if isinstance(w, Frame):
                    if w in menu_update_frames:
                        menu_update_frames.remove(w)
                        total_removed += 1
            if total_removed > 0:
                self.sort_menu_update_frames()

    @staticmethod
    def _check_cell_style(
            align: str,
            background_color: ColorInputType,
            border_color: ColorInputType,
            border_position: WidgetBorderPositionType,
            border_width: int,
            padding: PaddingType,
            vertical_position: str
    ) -> None:
        """
        Assert cell style.

        :param align: Horizontal align of each cell. See :py:mod:`pygame_menu.locals`
        :param background_color: Background color
        :param border_color: Border color of each cell
        :param border_position: Border position of each cell. Valid only: north, south, east, and west. See :py:mod:`pygame_menu.locals`
        :param border_width: Border width in px of each cell
        :param padding: Cell padding according to CSS rules. General shape: (top, right, bottom, left)
        :param vertical_position: Vertical position of each cell. Only valid: north, center, and south. See :py:mod:`pygame_menu.locals`
        :return: None
        """
        # Alignment
        assert_alignment(align)

        # Background color
        if background_color is not None:
            assert_color(background_color)

        # Padding
        parse_padding(padding)

        # Vertical position
        assert_position(vertical_position)
        assert vertical_position in (POSITION_NORTH, POSITION_CENTER, POSITION_SOUTH), \
            'cell vertical position must be NORTH, CENTER, or SOUTH'

        # Border color
        assert isinstance(border_width, int) and border_width >= 0
        if border_color is not None:
            assert_color(border_color)

        # Border position
        assert isinstance(border_position, (str, VectorInstance))
        if isinstance(border_position, str):
            border_position = [border_position]

        # Border positioning
        for pos in border_position:
            assert pos in (POSITION_NORTH, POSITION_SOUTH, POSITION_EAST, POSITION_WEST), \
                'only north, south, east, and west border positions are valid, ' \
                'but received "{0}"'.format(pos)

    def add_row(
            self,
            cells: Union[ColumnInputType, 'Widget'],
            cell_align: Optional[str] = None,
            cell_border_color: Optional[ColorInputType] = None,
            cell_border_position: Optional[WidgetBorderPositionType] = None,
            cell_border_width: Optional[int] = None,
            cell_font: Optional[FontType] = None,
            cell_font_color: Optional[ColorInputType] = None,
            cell_font_size: Optional[int] = None,
            cell_padding: PaddingType = None,
            cell_vertical_position: Optional[str] = None,
            row_background_color: Optional[ColorInputType] = None
    ) -> 'Frame':
        """
        Add row to table.

        .. note::

            By default, if ``None`` each cell style uses the table defaults "cell"
            styles.

        .. note::

            By default, the cell font is the same as the table font style.

        :param cells: Cells to add. This can be a tuple or list of widgets, string, numbers, boolean values or images. Also a Frame row can be added
        :param cell_align: Horizontal align of each cell. See :py:mod:`pygame_menu.locals`
        :param cell_border_color: Border color of each cell
        :param cell_border_position: Border position of each cell. Valid only: north, south, east, and west. See :py:mod:`pygame_menu.locals`
        :param cell_border_width: Border width in px of each cell
        :param cell_font: Font name or path
        :param cell_font_color: Font color
        :param cell_font_size: Font size
        :param cell_padding: Padding of each cell according to CSS rules. General shape: (top, right, bottom, left)
        :param cell_vertical_position: Vertical position of each cell. Only valid: north, center, and south. See :py:mod:`pygame_menu.locals`
        :param row_background_color: Row background color
        :return:
        """
        assert self.configured, 'table must be configured before adding rows'

        # Use defaults
        if cell_align is None:
            cell_align = self.default_cell_align
        if cell_border_color is None:
            cell_border_color = self.default_cell_border_color
        if cell_border_position is None:
            cell_border_position = self.default_cell_border_position
        if cell_border_width is None:
            cell_border_width = self.default_cell_border_width
        if cell_font is None:
            cell_font = self._font_name
        if cell_font_color is None:
            cell_font_color = self._font_color
        if cell_font_size is None:
            cell_font_size = self._font_size
        if cell_padding is None:
            cell_padding = self.default_cell_padding
        if cell_vertical_position is None:
            cell_vertical_position = self.default_cell_vertical_position
        if row_background_color is None:
            row_background_color = self.default_row_background_color

        # If cells is a previous table row
        if isinstance(cells, Frame) and cells.has_attribute('is_row'):
            row_cells = list(cells.get_widgets(unpack_subframes=False))
            cells.clear()
            cells = row_cells
        if isinstance(cells, Widget):
            cells = [cells]

        assert isinstance(cells, VectorInstance)

        # Check cell styles
        self._check_cell_style(
            align=cell_align,
            background_color=row_background_color,
            border_color=cell_border_color,
            border_position=cell_border_position,
            border_width=cell_border_width,
            padding=cell_padding,
            vertical_position=cell_vertical_position
        )
        cell_padding = parse_padding(cell_padding)
        if cell_border_color is not None:
            cell_border_color = assert_color(cell_border_color)
        if isinstance(cell_border_position, str):
            cell_border_position = [cell_border_position]

        # Check positioning
        if cell_border_width == 0:
            cell_border_position = WIDGET_BORDER_POSITION_NONE

        if row_background_color is not None:
            row_background_color = assert_color(row_background_color)

        # Create frame row
        row = Frame(1, 1, ORIENTATION_HORIZONTAL,
                    frame_id=self._id + '+cell-row-' + uuid4(short=True))
        row._accepts_scrollarea = False
        row._accepts_title = False
        row._menu_can_be_none_pack = True
        row._update__repr___(self)
        row.configured = True
        row.relax()
        row.set_background_color(row_background_color)
        row.set_menu(self._menu)
        row.set_scrollarea(self._scrollarea)
        row.set_attribute('is_row')
        # row.set_frame(self) This cannot be executed as row is packed within

        # Create widgets
        row_cells: List['Widget'] = []
        cell: 'Widget'
        j = 0
        for c in cells:
            if isinstance(c, (str, int, float, bool)):
                cell = Label(c, label_id=self._id + '+cell-label-' + uuid4(short=True))
                cell.set_font(
                    antialias=self._font_antialias,
                    background_color=None,
                    color=cell_font_color,
                    font=cell_font,
                    font_size=cell_font_size,
                    readonly_color=self._font_readonly_color,
                    readonly_selected_color=self._font_readonly_selected_color,
                    selected_color=self._font_selected_color
                )
                cell.set_padding(0)
                cell.set_tab_size(self._tab_size)
            elif isinstance(c, BaseImage):
                cell = Image(
                    c, image_id=self._id + '+cell-image-' + uuid4(short=True)
                )
            elif isinstance(c, pygame.Surface):
                cell = SurfaceWidget(
                    c, surface_id=self._id + '+cell-surface-' + uuid4(short=True)
                )
            else:
                assert isinstance(c, Widget)
                cell = c

            # Configure cell
            cell.set_attribute('align', cell_align)
            cell.set_attribute('background_color', row_background_color)
            cell.set_attribute('border_color', cell_border_color)
            cell.set_attribute('border_position', cell_border_position)
            cell.set_attribute('border_width', cell_border_width)
            cell.set_attribute('column', j + 1)
            cell.set_attribute('padding', cell_padding)
            cell.set_attribute('row', len(self._rows) + 1)
            cell.set_attribute('row_frame', row)
            cell.set_attribute('table', self)
            cell.set_attribute('vertical_position', cell_vertical_position)
            cell.set_float(False)
            cell._update__repr___(self)
            cell.configured = True

            # If cell within a menu, remove from it
            if cell.get_menu() is not None:
                try:
                    cell.get_menu().remove_widget(cell)
                except ValueError:
                    pass

            # Check the cell frame is None
            assert cell.get_frame() != self, \
                '{0} cannot be added as it already exists in table' \
                ''.format(cell.get_class_id())
            assert cell.get_frame() is None, \
                '{0} is already packed in {1}, it cannot be added to {2}' \
                ''.format(cell.get_class_id(), cell.get_frame().get_class_id(),
                          self.get_class_id())

            # If cell is frame and scrollable
            if isinstance(cell, Frame) and self._menu is not None:
                menu_update_frames = self._get_menu_update_frames()
                if cell not in menu_update_frames:
                    menu_update_frames.append(cell)
                    self.sort_menu_update_frames()

            # Add to cells
            row_cells.append(cell)
            j += 1

        # Pack cells to row
        for c in row_cells:
            row.pack(c)

        # Pack row to self
        super(Table, self).pack(row)
        self._rows.append(row)

        # Update size
        self._update_row_sizing()

        return row

    def _get_column_width_row_height(self) -> Tuple[Dict[int, int], Dict['Frame', int]]:
        """
        Return column width and row height.

        :return: Column width and row height dict
        """
        column_widths: Dict[int, int] = {}  # column/width
        row_heights: Dict['Frame', int] = {}  # row/height

        for f in self._rows:
            col = 0  # Column
            max_height = 0  # Max row height
            for w in f.get_widgets(unpack_subframes=False):
                width = w.get_width(apply_padding=False)
                # Add inner padding
                pad = w.get_attribute('padding')  # top, right, bottom, left
                width += pad[1] + pad[3]
                if col not in column_widths.keys():
                    column_widths[col] = width
                else:
                    column_widths[col] = max(width, column_widths[col])
                col += 1
                height = w.get_height(apply_padding=False)
                height += pad[0] + pad[2]
                max_height = max(max_height, height)
            row_heights[f] = max_height

        return column_widths, row_heights

    # def set_frame(self, frame: 'pygame_menu.widgets.Frame') -> 'Table':
    #     super(Frame, self).set_frame(frame)
    #     for f in self._rows:
    #         f.set_frame(frame)
    #     return self

    def _update_row_sizing(self) -> None:
        """
        Update row sizing.

        :return: None
        """
        column_widths, row_heights = self._get_column_width_row_height()

        total_width = 0
        # Sum each column to get max row width
        for w in column_widths.values():
            total_width += w

        # Compute each row height and update padding
        total_height = 0
        for f in self._rows:
            f.resize(total_width, row_heights[f])
            total_height += row_heights[f]

            col = 0
            for w in f.get_widgets(unpack_subframes=False):
                w_w = w.get_width(apply_padding=False)
                w_h = w.get_height(apply_padding=False)
                w_pad = w.get_attribute('padding')  # top, right, bottom, left
                w_align = w.get_attribute('align')
                w_vpos = w.get_attribute('vertical_position')
                w_total_height = row_heights[f]
                w_total_width = column_widths[col]

                # Default paddings
                pad_top = w_pad[0]
                pad_right = w_pad[1]
                pad_bottom = w_pad[2]
                pad_left = w_pad[3]

                # Subtract padding to max width/height
                w_total_height -= (pad_top + pad_bottom)
                w_total_width -= (pad_left + pad_right)

                # Compute horizontal align
                delta_w = w_total_width - w_w
                assert delta_w >= 0, 'delta width cannot be negative'
                if w_align == ALIGN_LEFT:
                    pad_right += delta_w
                elif w_align == ALIGN_CENTER:
                    pad_left += int(delta_w / 2)
                    pad_right += int(delta_w / 2)
                elif w_align == ALIGN_RIGHT:
                    pad_left += delta_w

                # Compute vertical position
                delta_h = w_total_height - w_h
                assert delta_h >= 0, 'delta height cannot be negative'
                if w_vpos == POSITION_NORTH:
                    pad_bottom += delta_h
                elif w_vpos == POSITION_CENTER:
                    pad_top += int(delta_h / 2)
                    pad_bottom += int(delta_h / 2)
                elif w_vpos == POSITION_SOUTH:
                    pad_top += delta_h

                # Update cell padding
                w.set_padding((pad_top, pad_right, pad_bottom, pad_left))

                # Check if the padding closes the width
                dx = column_widths[col] - w.get_width()
                dy = row_heights[f] - w.get_height()
                if dx == 1:
                    pad_left += 1
                if dx >= 2:
                    pad_right += (dx - 1)
                if dy == 1:
                    pad_top += 1
                if dy >= 2:
                    pad_bottom += (dy - 1)
                w.set_padding((pad_top, pad_right, pad_bottom, pad_left))

                col += 1

        # Update current rect
        self.resize(total_width + self._padding[1] + self._padding[3],
                    total_height + self._padding[0] + self._padding[2])

    def on_remove_from_menu(self) -> 'Frame':
        self.update_indices()
        return self

    @staticmethod
    def get_cell_column_row(cell: 'Widget') -> Tuple[int, int]:
        """
        Return the column/row within table layout for the given widget.

        :param cell: Widget (cell) to get the column/row position
        :return: Column/Row
        """
        assert cell.has_attribute('column') and cell.has_attribute('row'), \
            '{0} does not have the table attributes'.format(cell.get_class_id())
        return cell.get_attribute('column'), cell.get_attribute('row')

    def _draw_cell_borders(self, surface: 'pygame.Surface') -> None:
        """
        Draw cell border.

        :param surface: Surface to draw the cell border
        :return: None
        """
        if len(self._rows) == 0:
            return

        # Get first row position
        x, y = self._rows[0].get_position()

        column_widths, row_heights = self._get_column_width_row_height()
        total_height = 0
        r = 0
        for row in self._rows:
            r += 1
            col = 0
            total_width = 0
            for w in row.get_widgets(unpack_subframes=False):
                border_color = w.get_attribute('border_color')
                border_position = w.get_attribute('border_position')
                border_width = w.get_attribute('border_width')

                # Create drawing rect
                subtract_border = (-border_width) if r == len(self._rows) else 0
                rect = pygame.Rect(total_width + x,
                                   total_height + y,
                                   column_widths[col],
                                   row_heights[row] + subtract_border)
                total_width += column_widths[col]
                col += 1

                # Draw the border
                if border_position == WIDGET_BORDER_POSITION_NONE or \
                        border_width == 0:
                    continue
                for pos in border_position:
                    if pos == POSITION_NORTH:
                        start, end = rect.topleft, rect.topright
                    elif pos == POSITION_SOUTH:
                        start, end = rect.bottomleft, rect.bottomright
                    elif pos == POSITION_EAST:
                        start, end = rect.topright, rect.bottomright
                    elif pos == POSITION_WEST:
                        start, end = rect.topleft, rect.bottomleft
                    else:
                        raise RuntimeError('invalid border position "{0}"'.format(pos))
                    pygame.draw.line(
                        surface,
                        border_color,
                        start,
                        end,
                        border_width
                    )

            total_height += row_heights[row]

    def get_cell(self, column: int, row: int) -> 'Widget':
        """
        Get cell widget at column/row position.

        :param column: Cell column position (counting from 1)
        :param row: Cell row position (counting from 1)
        :return: Cell widget object
        """
        assert isinstance(row, int) and row >= 1, \
            'row index must be an integer equal or greater than 1'
        assert isinstance(column, int) and column >= 1, \
            'column index must be an integer equal or greater than 1'
        assert row <= len(self._rows), \
            'row index ({0}) cannot exceed the number of rows ({1})' \
            ''.format(row, len(self._rows))
        f = self._rows[row - 1]
        w = f.get_widgets(unpack_subframes=False)
        assert column <= len(w), \
            'column index ({0}) cannot exceed the number of columns ({1}) of row {2}' \
            ''.format(column, len(w), row)
        return w[column - 1]

    def is_rectangular(self) -> bool:
        """
        Returns ``True`` if the table is rectangular, that is, each row have the
        same number of columns.

        :return: Bool
        """
        if len(self._rows) == 0:
            return True
        c = self._rows[0].get_total_packed()
        for f in self._rows:
            if f.get_total_packed() != c:
                return False
        return True

    def update_cell_style(
            self,
            column: Union[int, Vector2IntType],
            row: Union[int, Vector2IntType],
            align: Optional[str] = None,
            background_color: Optional[ColorInputType] = None,
            border_color: Optional[ColorInputType] = None,
            border_position: Optional[WidgetBorderPositionType] = None,
            border_width: Optional[int] = None,
            font: Optional[FontType] = None,
            font_color: Optional[ColorInputType] = None,
            font_size: Optional[int] = None,
            padding: Optional[PaddingType] = None,
            vertical_position: Optional[str] = None
    ) -> Union['Widget', List['Widget']]:
        """
        Update cell style. If a parameter is ``None`` the default cell property
        will be used.

        :param column: Cell column position (counting from 1). If -1 update all column from the given row. Also a 2-item list/tuple is accepted (from, to), ``to=-1`` is also accepted (last)
        :param row: Cell row position (counting from 1). If ``-1`` update all rows from the given column. Also a 2-item list/tuple is accepted (from, to), ``to=-1`` is also accepted (last)
        :param align: Horizontal align of each cell. See :py:mod:`pygame_menu.locals`
        :param background_color: Background color
        :param border_color: Border color of each cell
        :param border_position: Border position of each cell. Valid only: north, south, east, and west. See :py:mod:`pygame_menu.locals`
        :param border_width: Border width in px of each cell
        :param font: Font name or path
        :param font_color: Font color
        :param font_size: Font size
        :param padding: Cell padding according to CSS rules. General shape: (top, right, bottom, left)
        :param vertical_position: Vertical position of each cell. Only valid: north, center, and south. See :py:mod:`pygame_menu.locals`
        :return: Cell widget
        """
        if row == -1 or isinstance(row, VectorInstance):
            max_rows = len(self._rows)
            if row == -1:
                row = []
                for i in range(max_rows):
                    row.append(i + 1)
            else:
                assert_vector(row, 2, int)
                row_k = list(row)
                if row_k[1] == -1:
                    row_k[1] = len(self._rows)
                assert 1 <= row_k[0] <= row_k[1] <= max_rows, \
                    '(from, to) of rows vector must be increasing and between 1-{0}' \
                    ''.format(max_rows)
                row = [row_k[0]]
                for i in range(row_k[1] - row_k[0]):
                    row.append(row_k[0] + (i + 1))
            if isinstance(column, VectorInstance) and column != [1, -1]:
                assert self.is_rectangular(), \
                    'only rectangular tables (same number of columns for each row) ' \
                    'accept a variable column different than -1 or [1, -1], but ' \
                    'received "{0}"'.format(column)
            updated_wid = []
            for i in row:
                w = self.update_cell_style(
                    column=column,
                    row=i,
                    align=align,
                    background_color=background_color,
                    border_color=border_color,
                    border_position=border_position,
                    border_width=border_width,
                    font=font,
                    font_color=font_color,
                    font_size=font_size,
                    padding=padding,
                    vertical_position=vertical_position
                )
                if not isinstance(w, list):
                    w = [w]
                for k in w:
                    updated_wid.append(k)
            return updated_wid
        if column == -1 or isinstance(column, VectorInstance):
            assert isinstance(row, int) and 1 <= row <= len(self._rows), \
                'row index ({0}) cannot exceed the number of rows ({1})' \
                ''.format(row, len(self._rows))
            max_columns = self._rows[row - 1].get_total_packed()
            if column == -1:
                column = []
                for i in range(max_columns):
                    column.append(i + 1)
            else:
                assert_vector(column, 2, int)
                column_k = list(column)
                if column_k[1] == -1:
                    column_k[1] = max_columns
                assert 1 <= column_k[0] <= column_k[1] <= max_columns, \
                    '(from, to) of column vector must be increasing and between 1-{0} for row {1}' \
                    ''.format(max_columns, row)
                column = [column_k[0]]
                for i in range(column_k[1] - column_k[0]):
                    column.append(column_k[0] + (i + 1))
            updated_wid = []
            for i in column:
                w = self.update_cell_style(
                    column=i,
                    row=row,
                    align=align,
                    background_color=background_color,
                    border_color=border_color,
                    border_position=border_position,
                    border_width=border_width,
                    font=font,
                    font_color=font_color,
                    font_size=font_size,
                    padding=padding,
                    vertical_position=vertical_position
                )
                if not isinstance(w, list):
                    w = [w]
                for k in w:
                    updated_wid.append(k)
            return updated_wid
        cell = self.get_cell(column, row)
        r = self._rows[row - 1]

        if align is None:
            align = cell.get_attribute('align')
        if background_color is None:
            background_color = cell.get_attribute('background_color')
        if border_color is None:
            border_color = cell.get_attribute('border_color')
        if border_position is None:
            border_position = cell.get_attribute('border_position')
        if border_width is None:
            border_width = cell.get_attribute('border_width')
        if padding is None:
            padding = cell.get_attribute('padding')
        if vertical_position is None:
            vertical_position = cell.get_attribute('vertical_position')

        self._check_cell_style(
            align=align,
            background_color=background_color,
            border_color=border_color,
            border_position=border_position,
            border_width=border_width,
            padding=padding,
            vertical_position=vertical_position
        )
        if background_color is not None:
            background_color = assert_color(background_color)
        if border_color is not None:
            border_color = assert_color(border_color)
        padding = parse_padding(padding)

        # Update background color
        if background_color != r._background_color:
            cell.set_background_color(background_color)
        else:
            cell.set_background_color(None)

        # Update font
        if font_color is None:
            font_color = cell._font_color
        assert_color(font_color)
        if font is None:
            font = cell._font_name
        assert_font(font)
        if font_size is None:
            font_size = cell._font_size

        try:
            cell.update_font({
                'color': font_color,
                'name': font
            })
        except AssertionError:
            pass

        try:
            if isinstance(font_size, int) and font_size > 0:
                cell.update_font({'size': font_size})
        except AssertionError:
            pass

        if isinstance(border_position, str):
            border_position = [border_position]

        # Update cell
        cell.set_attribute('align', align)
        cell.set_attribute('background_color', background_color)
        cell.set_attribute('border_color', border_color)
        cell.set_attribute('border_position', border_position)
        cell.set_attribute('border_width', border_width)
        cell.set_attribute('padding', padding)
        cell.set_attribute('vertical_position', vertical_position)

        self._update_row_sizing()
        self._render()
        self.force_menu_surface_update()
        return cell

    # noinspection PyProtectedMember
    def set_scrollarea(self, scrollarea: Optional['pygame_menu._scrollarea.ScrollArea']) -> None:
        super(Table, self).set_scrollarea(scrollarea)
        for f in self._rows:
            f.set_scrollarea(scrollarea)

    def set_position(self, x: NumberType, y: NumberType) -> 'Table':
        super(Table, self).set_position(x, y)
        x = self._rect.x
        y = self._rect.y
        for f in self._rows:
            f.set_position(x, y)
            for w in f.get_widgets(unpack_subframes=False):
                w.set_position_relative_to_frame()
            f.update_position()
        return self

    def draw(self, surface: 'pygame.Surface') -> 'Table':
        if not self.is_visible():
            return self
        super(Table, self).draw(surface)
        self._draw_cell_borders(self.last_surface)
