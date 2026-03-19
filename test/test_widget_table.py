"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - TABLE
Test Table widget.
"""

import pygame
import pytest

from pygame_menu import locals as pgm_locals
from pygame_menu.widgets import Label, SurfaceWidget
from test._utils import PYGAME_V2, MenuUtils


@pytest.fixture
def menu():
    """Provides a fresh generic menu for table testing."""
    return MenuUtils.generic_menu()


@pytest.fixture
def table(menu):
    """Provides a table widget attached to a menu."""
    return menu.add.table("test_table", background_color="red")


@pytest.mark.skipif(not PYGAME_V2, reason="Requires Pygame V2")
def test_table_initialization(menu, table):
    """Test table initialization."""
    btn = menu.add.button("1")

    assert table.is_rectangular()
    assert table.get_inner_size() == (0, 0)
    assert table.get_size(apply_padding=False) == (0, 0)

    with pytest.raises(RuntimeError):
        table.pack(btn)


@pytest.mark.skipif(not PYGAME_V2, reason="Requires Pygame V2")
def test_row_addition_and_sizing(table):
    """Test table row addition and sizing."""
    row1 = table.add_row(
        [1, 2, 3], row_background_color="blue", cell_align=pgm_locals.ALIGN_CENTER
    )
    assert row1.get_size() == (51, 41)

    row2 = table.add_row([10, 20, 30], row_background_color="green", cell_padding=10)
    assert row1.get_size() == (162, 41)
    assert row2.get_size() == (162, 61)
    assert table.get_size(apply_padding=False) == (162, 102)


@pytest.mark.skipif(not PYGAME_V2, reason="Requires Pygame V2")
def test_cell_access_and_styling(table):
    """Test table cell access and style updates."""
    table.add_row([1, 2, 3])
    table.add_row([10, 20, 30])

    with pytest.raises(AssertionError):
        table.get_cell(0, 0)

    c1 = table.get_cell(1, 1)
    assert c1.get_attribute("column") == 1
    assert c1.get_attribute("row") == 1

    table.update_cell_style(1, 1, background_color="white", padding=50)
    assert c1._background_color == (255, 255, 255, 255)
    assert table.get_size()[0] >= 100


@pytest.mark.skipif(not PYGAME_V2, reason="Requires Pygame V2")
def test_visibility_toggle(table):
    """Test table visibility toggling."""
    table.add_row([1, 2, 3])
    c = table.get_cell(1, 1)

    assert c.is_visible()
    table.hide()
    assert not c.is_visible()
    table.show()
    assert c.is_visible()


@pytest.mark.skipif(not PYGAME_V2, reason="Requires Pygame V2")
def test_complex_nesting(menu, table):
    """Test nested tables and widget frame relationships."""
    sub = menu.add.table(font_size=10)
    sub_row1 = sub.add_row([1, 2])

    btn = menu.add.button("Inside")

    row = table.add_row(
        ["sub", sub, btn],
        cell_align=pgm_locals.ALIGN_CENTER,
        cell_vertical_position=pgm_locals.POSITION_CENTER,
    )

    assert btn.get_frame() == row
    assert sub.get_frame() == row
    assert sub.get_frame_depth() == 2
    assert sub_row1.get_widgets()[0].get_frame_depth() == 4
    assert btn not in menu.get_widgets()


@pytest.mark.skipif(not PYGAME_V2, reason="Requires Pygame V2")
def test_surface_and_images(table):
    """Test table rows containing surfaces and labels."""
    surf = pygame.Surface((40, 40))
    surf.fill((255, 192, 203))

    row = table.add_row([surf, "Label"])
    assert isinstance(row.get_widgets()[0], SurfaceWidget)
    assert isinstance(row.get_widgets()[1], Label)


@pytest.mark.skipif(not PYGAME_V2, reason="Requires Pygame V2")
@pytest.mark.parametrize(
    "col, row_idx, expected",
    [
        (-1, 1, 3),
        (1, -1, 4),
        (-1, -1, 12),
    ],
)
def test_bulk_cell_updates(table, col, row_idx, expected):
    """Test bulk cell style updates using wildcard row and column selectors."""
    for _ in range(4):
        table.add_row([1, 2, 3])

    updated = table.update_cell_style(col, row_idx, background_color="cyan")
    assert len(updated) == expected


@pytest.mark.skipif(not PYGAME_V2, reason="Requires Pygame V2")
def test_row_removal(table):
    """Test table row removal."""
    table.add_row([1, 2, 3])
    r2 = table.add_row([4, 5, 6])

    assert table.get_size()[1] > 0

    table.remove_row(r2)

    assert r2 not in table._rows


@pytest.mark.skipif(not PYGAME_V2, reason="Requires Pygame V2")
def test_frame_packing(menu, table):
    """Test packing table widgets into frames."""
    frame = menu.add.frame_v(300, 300, background_color="yellow", padding=0)
    frame.pack(
        table,
        align=pgm_locals.ALIGN_CENTER,
        vertical_position=pgm_locals.POSITION_CENTER,
    )

    assert table._translate_virtual != (0, 0)

    frame2 = menu.add.frame_v(300, 400, max_height=300, background_color="brown")
    menu.remove_widget(frame)
    frame2.pack(table)

    assert table.is_floating()
    table.set_float(False)
    assert not table.is_floating()


@pytest.mark.skipif(not PYGAME_V2, reason="Requires Pygame V2")
def test_scrollable_frame_interactions(menu, table):
    """Test table interactions with scrollable frames and update lists."""
    table.add_row([1])

    frame3 = menu.add.frame_v(
        200, 200, max_width=100, max_height=100, background_color="cyan"
    )
    table3 = menu.add.table(background_color="purple")
    table3.add_row([pygame.Surface((40, 40))])

    row = table.add_row([frame3, table3], cell_border_width=0)
    assert table.get_cell(*table.get_cell_column_row(table3)) == table3

    table.remove_row(row)

    assert frame3 not in menu._update_frames


@pytest.mark.skipif(not PYGAME_V2, reason="Requires Pygame V2")
def test_value_api(table):
    """Test table value API."""
    with pytest.raises(ValueError):
        table.get_value()
    with pytest.raises(ValueError):
        table.set_value("value")

    assert not table.value_changed()
    table.reset_value()


@pytest.mark.skipif(not PYGAME_V2, reason="Requires Pygame V2")
def test_update_empty(table):
    """Test table update with empty event list."""
    assert table.update([]) is False
