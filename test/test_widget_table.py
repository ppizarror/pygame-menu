"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - TABLE
Test Table widget.
"""

import pygame
import pytest
import pygame_menu

from pygame_menu import locals as pgm_locals
from pygame_menu.widgets import Label, SurfaceWidget
from test._utils import PYGAME_V2, MenuUtils, surface


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


@pytest.mark.skipif(not PYGAME_V2, reason="Requires Pygame V2")
def test_table():
    """Test all table."""
    menu = MenuUtils.generic_menu()
    btn = menu.add.button("1")
    table = menu.add.table("table", background_color="red")
    assert table.is_rectangular()
    assert table.get_inner_size() == (0, 0)
    assert table.get_size(apply_padding=False) == (0, 0)
    with pytest.raises(RuntimeError):
        table.pack(btn)

    # Test add rows
    row1 = table.add_row([1, 2, 3], row_background_color="blue", cell_align=pygame_menu.locals.ALIGN_CENTER)
    assert table.is_rectangular()
    assert row1.get_size() == (51, 41)
    assert table.get_size(apply_padding=False) == (51, 41)
    row2 = table.add_row([10, 20, 30], row_background_color="green", cell_padding=10)
    assert row1.get_size() == (162, 41)
    assert row2.get_size() == (162, 61)
    assert table.get_size(apply_padding=False) == (162, 102)
    table.draw(surface)
    assert table.is_rectangular()

    # Test get cell
    assert table.get_cell(2, 1) == row1.get_widgets(unpack_subframes=False)[1]
    assert table.get_cell(1, 2) == row2.get_widgets(unpack_subframes=False)[0]
    with pytest.raises(AssertionError):
        table.get_cell(0, 0)
    with pytest.raises(AssertionError):
        table.get_cell(0, 1)
    with pytest.raises(AssertionError):
        table.get_cell(1, 0)
    c1 = table.get_cell(1, 1)
    assert c1 == row1.get_widgets(unpack_subframes=False)[0]

    # Test cell properties
    assert c1.get_attribute("align") == pygame_menu.locals.ALIGN_CENTER
    assert c1.get_attribute("border_color") == (0, 0, 0, 255)
    assert c1.get_attribute("border_position") == pygame_menu.widgets.core.widget.WIDGET_FULL_BORDER
    assert c1.get_attribute("border_width") == 1
    assert c1.get_attribute("column") == 1
    assert c1.get_attribute("padding") == (0, 0, 0, 0)
    assert c1.get_attribute("row") == 1
    assert c1.get_attribute("table") == table
    assert c1.get_attribute("vertical_position") == pygame_menu.locals.POSITION_NORTH

    # Update cell
    c5 = table.update_cell_style(2, 2)
    assert c5._background_color is None
    assert c5.get_attribute("background_color") == (0, 255, 0, 255)

    table.update_cell_style(2, 2, background_color="white")
    assert c5._background_color == (255, 255, 255, 255)

    table.update_cell_style(3, 1, background_color="cyan")
    assert c5.get_padding() == (10, 10, 10, 10)
    table.update_cell_style(2, 2, padding=0)
    assert c5.get_padding() == (0, 0, 20, 0)  # vertical position north
    table.update_cell_style(2, 2, vertical_position=pygame_menu.locals.POSITION_CENTER)
    assert c5.get_padding() == (10, 0, 10, 0)  # vertical position north
    table.update_cell_style(2, 2, vertical_position=pygame_menu.locals.POSITION_SOUTH)
    assert c5.get_padding() == (20, 0, 0, 0)  # vertical position north
    table.update_cell_style(1, 1, font_color="white")
    table.draw(surface)
    assert table.get_size() == (158, 110)
    table.update_cell_style(2, 2, padding=50)
    assert table.get_size() == (258, 190)

    # Test align
    c2 = table.get_cell(2, 1)
    assert c2.get_size() == (134, 41)
    assert c2.get_padding() == (0, 58, 0, 59)
    table.update_cell_style(2, 1, align=pygame_menu.locals.ALIGN_LEFT)
    assert c2.get_size() == (134, 41)
    assert c2.get_padding() == (0, 117, 0, 0)
    table.update_cell_style(2, 1, align=pygame_menu.locals.ALIGN_RIGHT)
    assert c2.get_padding() == (0, 0, 0, 117)
    assert c2.get_attribute("border_width") == 1
    table.update_cell_style(2, 1, border_width=0)
    assert c2.get_attribute("border_width") == 0
    table.draw(surface)

    # Test hide
    assert c2.is_visible()
    table.hide()
    table.draw(surface)
    assert not c2.is_visible()
    table.show()
    assert c2.is_visible()

    # Add and remove row
    assert table.get_size() == (258, 190)
    row3 = table.add_row([12])
    assert not table.is_rectangular()
    assert row1.get_total_packed() == 3
    assert row3.get_total_packed() == 1
    assert table.get_size() == (258, 231)
    table.remove_row(row3)
    assert table.get_size() == (258, 190)

    # Add new row with an image
    table.update_cell_style(2, 2, padding=0)
    b_image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU)
    b_image.scale(0.1, 0.1)
    row3 = table.add_row(["image", b_image, "ez"])
    assert isinstance(row3.get_widgets()[1], pygame_menu.widgets.Image)

    # Remove table from menu
    menu.remove_widget(table)

    # Add sub-table
    menu.add.generic_widget(table)
    table2 = menu.add.table(font_size=10)
    table2row1 = table2.add_row([1, 2])
    table2.add_row([3, 4])

    assert btn in menu.get_widgets()

    row4 = table.add_row(["sub-table", table2, btn], cell_align=pygame_menu.locals.ALIGN_CENTER,
                         cell_vertical_position=pygame_menu.locals.POSITION_CENTER)
    table.update_cell_style(2, 4, background_color="white")
    assert btn not in menu.get_widgets()
    assert btn.get_frame() == row4
    assert table2.get_frame() == row4
    assert table2.get_frame_depth() == 2
    assert table2row1.get_widgets()[0].get_frame() == table2row1
    assert table2row1.get_widgets()[0].get_frame_depth() == 4

    # Try to add an existing row as a new row
    with pytest.raises(AssertionError):
        table.add_row([row1])
    with pytest.raises(AssertionError):
        table.add_row([table2row1.get_widgets()[0]])

    # Update padding
    assert table.get_size() == (265, 201)
    table.set_padding(0)
    assert table.get_size() == (249, 193)

    # Add surface
    new_surface = pygame.Surface((40, 40))
    new_surface.fill((255, 192, 203))
    inner_surface = pygame.Surface((20, 20))
    inner_surface.fill((75, 0, 130))
    new_surface.blit(inner_surface, (10, 10))
    row5 = table.add_row([new_surface, "epic", new_surface],
                         cell_border_position=pygame_menu.locals.POSITION_SOUTH)

    assert isinstance(row5.get_widgets()[0], pygame_menu.widgets.SurfaceWidget)
    assert isinstance(row5.get_widgets()[1], pygame_menu.widgets.Label)
    assert isinstance(row5.get_widgets()[2], pygame_menu.widgets.SurfaceWidget)
    assert table.get_size() == (249, 234)

    # Create table with fixed surface for testing sizing
    table3 = menu.add.table(background_color="purple")
    table3._draw_cell_borders(surface)
    with pytest.raises(AssertionError):
        table3.remove_row(row1)  # Empty table
    table3.add_row([new_surface])
    with pytest.raises(AssertionError):
        table3.remove_row(row1)  # Empty table
    assert table3.get_margin() == (0, 0)
    assert table3.get_size() == (56, 48)
    table3.set_padding(False)
    assert table3.get_size() == (40, 40)

    # Test others
    surf_same_table = pygame.Surface((10, 200))
    surf_same_table.fill((0, 0, 0))
    surf_widget = menu.add.surface(surf_same_table)

    # Create frame
    menu._test_print_widgets()
    frame = menu.add.frame_v(300, 300, background_color="yellow", padding=0)
    frame.pack(surf_widget)
    menu.remove_widget(surf_widget)

    assert table._translate_virtual == (0, 0)
    frame.pack(table, align=pygame_menu.locals.ALIGN_CENTER, vertical_position=pygame_menu.locals.POSITION_CENTER)
    assert table._translate_virtual == (25, 33)

    # Add to scrollable frame
    frame2 = menu.add.frame_v(300, 400, max_height=300, background_color="brown")
    menu.remove_widget(frame)
    frame2.pack(table)

    # Add scrollable frame to table
    menu._test_print_widgets()
    frame3 = menu.add.frame_v(200, 200, max_width=100, max_height=100, background_color="cyan")
    assert frame3 in menu._update_frames
    row6 = table.add_row([frame3, table3], cell_border_width=0)
    row6_widgs = row6.get_widgets(unpack_subframes=False)
    assert frame3 in menu._update_frames
    assert row6.get_widgets(unpack_subframes=False)[1] == table3
    assert table.get_cell(*table.get_cell_column_row(table3)) == table3

    # Remove row6, this should remove table3 from update frames as well
    table.remove_row(row6)
    assert frame3 not in menu._update_frames

    # Check value
    with pytest.raises(ValueError):
        table.get_value()

    # Remove table from scrollable frame
    assert row6.get_total_packed() == 2
    row7 = table.add_row(row6)
    assert row6 != row7
    assert row6_widgs == row7.get_widgets(unpack_subframes=False)
    assert row6.get_total_packed() == 0
    assert frame3 in menu._update_frames

    # Unpack table from frame
    frame2.unpack(table)
    assert frame3 in menu._update_frames
    assert table.is_floating()
    table.set_float(False)
    menu._test_print_widgets()

    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_METAL)
    img.scale(0.2, 0.2)
    table.add_row(img)

    # Test single position
    table.update_cell_style(1, 1, border_position=pygame_menu.locals.POSITION_SOUTH)

    # Test update using -1 column/row
    assert len(table.update_cell_style(-1, 1)) == 3
    assert len(table.update_cell_style(-1, 7)) == 1
    assert len(table.update_cell_style(1, -1)) == 7
    assert len(table.update_cell_style(-1, -1)) == 18
    assert len(table.update_cell_style(1, [1, -1])) == 7
    assert len(table.update_cell_style(1, [1, 1])) == 1
    assert len(table.update_cell_style([1, -1], [1, -1])) == 18
    with pytest.raises(AssertionError):
        assert len(table.update_cell_style([1, 7], [1, -1])) == 18
    assert len(table.update_cell_style([1, 2], 1)) == 2
    assert not table.update([])
