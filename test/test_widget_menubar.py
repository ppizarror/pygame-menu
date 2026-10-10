"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - MENUBAR
Test MenuBar widget.
"""

import pygame
import pytest

import pygame_menu
import pygame_menu.controls as ctrl
from pygame_menu.locals import (
    POSITION_EAST,
    POSITION_NORTH,
    POSITION_SOUTH,
    POSITION_SOUTHWEST,
    POSITION_WEST,
)
from pygame_menu.widgets import (
    MENUBAR_STYLE_ADAPTIVE,
    MENUBAR_STYLE_NONE,
    MENUBAR_STYLE_SIMPLE,
    MENUBAR_STYLE_TITLE_ONLY,
    MENUBAR_STYLE_TITLE_ONLY_DIAGONAL,
    MENUBAR_STYLE_UNDERLINE,
    MENUBAR_STYLE_UNDERLINE_TITLE,
    MenuBar,
)
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented
from pygame_menu.widgets.widget.menubar import _MODE_CLOSE
from test._utils import MenuUtils, PygameEventUtils, surface


@pytest.fixture
def menu():
    """Return a generic menu fixture."""
    return MenuUtils.generic_menu()


@pytest.mark.parametrize(
    "mode",
    [
        MENUBAR_STYLE_ADAPTIVE,
        MENUBAR_STYLE_NONE,
        MENUBAR_STYLE_SIMPLE,
        MENUBAR_STYLE_UNDERLINE,
        MENUBAR_STYLE_UNDERLINE_TITLE,
        MENUBAR_STYLE_TITLE_ONLY,
        MENUBAR_STYLE_TITLE_ONLY_DIAGONAL,
    ],
)
def test_menubar_modes(menu, mode):
    """Test menubar widget modes."""
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True, mode=mode)
    menu.add.generic_widget(mb)
    menu.draw(surface)


def test_menubar_backbox_border_width(menu):
    """Test menubar backbox border width."""
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True)
    mb.set_backbox_border_width(2)

    with pytest.raises(AssertionError):
        mb.set_backbox_border_width(1.5)  # type: ignore
    with pytest.raises(AssertionError):
        mb.set_backbox_border_width(0)
    with pytest.raises(AssertionError):
        mb.set_backbox_border_width(-1)

    assert mb._backbox_border_width == 2


def test_menubar_unknown_mode(menu):
    """Test menubar unknown mode handling."""
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True, mode="unknown")  # type: ignore
    with pytest.raises(ValueError):
        mb.set_menu(menu)


def test_menubar_scrollbar_displacements(menu):
    """Test menubar scrollbar displacements."""
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True, mode=MENUBAR_STYLE_ADAPTIVE)

    assert mb.get_scrollbar_style_change(POSITION_SOUTH) == (0, (0, 0))
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (0, (0, 0))
    assert mb.get_scrollbar_style_change(POSITION_WEST) == (0, (0, 0))
    assert mb.get_scrollbar_style_change(POSITION_NORTH) == (0, (0, 0))

    mb.set_menu(menu)
    mb._render()

    assert mb.get_scrollbar_style_change(POSITION_SOUTHWEST) == (0, (0, 0))


def test_menubar_displacements_with_title_only():
    """Test displacements with title-only menubar."""
    theme = pygame_menu.themes.THEME_DEFAULT.copy()
    theme.title_bar_style = MENUBAR_STYLE_TITLE_ONLY

    menu = MenuUtils.generic_menu(theme=theme, title="my title")
    mb = menu.get_menubar()

    assert mb.get_scrollbar_style_change(POSITION_SOUTH) == (0, (0, 0))
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (0, (0, 0))
    assert mb.get_scrollbar_style_change(POSITION_WEST) == (-55, (0, 55))
    assert mb.get_scrollbar_style_change(POSITION_NORTH) == (0, (0, 55))


def test_menubar_displacements_with_close_button():
    """Test displacements with close button enabled."""
    theme = pygame_menu.themes.THEME_DEFAULT.copy()
    theme.title_bar_style = MENUBAR_STYLE_TITLE_ONLY
    theme.widget_border_inflate = (0, 0)

    menu = MenuUtils.generic_menu(
        theme=theme,
        title="my title",
        onclose=pygame_menu.events.CLOSE,
        touchscreen=True,
    )

    mb = menu.get_menubar()

    assert mb.get_scrollbar_style_change(POSITION_SOUTH) == (0, (0, 0))
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (-33, (0, 33))
    assert mb.get_scrollbar_style_change(POSITION_WEST) == (-55, (0, 55))
    assert mb.get_scrollbar_style_change(POSITION_NORTH) == (0, (0, 55))

    mb.hide()
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (0, (0, 0))

    mb.show()
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (-33, (0, 33))

    mb.set_float(True)
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (0, (0, 0))

    mb.set_float(False)
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (-33, (0, 33))

    mb.fixed = False
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (0, (0, 0))


def test_menubar_events(menu):
    """Test menubar event handling."""
    theme = pygame_menu.themes.THEME_DEFAULT.copy()
    theme.title_bar_style = MENUBAR_STYLE_TITLE_ONLY
    menu = MenuUtils.generic_menu(theme=theme, title="my title")
    menu.enable()
    mb = menu.get_menubar()

    assert not mb.update(PygameEventUtils.middle_rect_click(mb._rect))

    assert not mb.update(PygameEventUtils.middle_rect_click(mb._backbox_rect))

    assert not mb.update(
        PygameEventUtils.middle_rect_click(
            mb._backbox_rect, evtype=pygame.FINGERUP, menu=menu
        )
    )

    assert not mb.update(
        PygameEventUtils.middle_rect_click(
            mb._backbox_rect, evtype=pygame.MOUSEBUTTONDOWN
        )
    )

    assert mb.update(PygameEventUtils.joy_button(ctrl.JOY_BUTTON_BACK))

    mb.readonly = True
    assert not mb.update(PygameEventUtils.joy_button(ctrl.JOY_BUTTON_BACK))
    mb.readonly = False


@pytest.mark.parametrize(
    "method,args",
    [
        ("rotate", (10,)),
        ("resize", (10, 10)),
        ("scale", (100, 100)),
        ("flip", (True, True)),
        ("set_max_width", (100,)),
        ("set_max_height", (100,)),
    ],
)
def test_menubar_invalid_transforms(method, args):
    """Test unsupported menubar transforms."""
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True)

    with pytest.raises(WidgetTransformationNotImplemented):
        getattr(mb, method)(*args)


def test_menubar_transform_state():
    """Test menubar transform state after invalid transforms."""
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True)

    with pytest.raises(WidgetTransformationNotImplemented):
        mb.rotate(10)
    assert mb._angle == 0

    with pytest.raises(WidgetTransformationNotImplemented):
        mb.resize(10, 10)
    assert mb._scale[:3] == [False, 1, 1]

    with pytest.raises(WidgetTransformationNotImplemented):
        mb.scale(100, 100)
    assert mb._scale[:3] == [False, 1, 1]

    with pytest.raises(WidgetTransformationNotImplemented):
        mb.flip(True, True)
    assert mb._flip == (False, False)

    with pytest.raises(WidgetTransformationNotImplemented):
        mb.set_max_width(100)
    assert mb._max_width[0] is None

    with pytest.raises(WidgetTransformationNotImplemented):
        mb.set_max_height(100)
    assert mb._max_height[0] is None


def test_menubar_empty_title():
    """Test menubar empty title size."""
    mb = MenuBar("", 500, (0, 0, 0), back_box=True)
    p = mb._padding

    assert mb.get_width() == p[1] + p[3]
    assert mb.get_height() == p[0] + p[2]


def test_menubar_value_api():
    """Test menubar value API."""
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True)

    with pytest.raises(ValueError):
        mb.get_value()

    with pytest.raises(ValueError):
        mb.set_value("value")

    assert not mb.value_changed()
    mb.reset_value()


def test_menubar_backbox_created(menu):
    """Test backbox creation when enabled."""
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True)
    mb.set_menu(menu)

    mb._render()

    assert mb._backbox_rect is not None
    assert mb._backbox_pos is not None


def test_menubar_backbox_disabled(menu):
    """Test backbox is not created when disabled."""
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=False)
    mb.set_menu(menu)

    mb._render()

    assert mb._backbox_rect is None


def test_menubar_close_mode_backbox(menu):
    """Test close mode backbox generation."""
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True)
    mb.set_menu(menu)

    mb._render()

    assert mb._box_mode == _MODE_CLOSE
    assert mb._backbox_pos is not None


def test_menubar_title_offset():
    """Test title offset getter."""
    mb = MenuBar("Menu", 500, (0, 0, 0), offsetx=10, offsety=20)

    assert mb.get_title_offset() == (10, 20)


def test_menubar_set_title_returns_self():
    """Test set_title returns self."""
    mb = MenuBar("Menu", 500, (0, 0, 0))

    assert mb.set_title("New title") is mb


def test_menubar_set_title_updates_title():
    """Test set_title updates stored title."""
    mb = MenuBar("Menu", 500, (0, 0, 0))

    mb.set_title("Updated")

    assert mb._title == "Updated"


def test_menubar_get_title_offset_casts_int():
    """Test title offsets are returned as integers."""
    mb = MenuBar("Menu", 500, (0, 0, 0))

    mb._offsetx = 10.8
    mb._offsety = 15.2

    assert mb.get_title_offset() == (10, 15)


def test_menubar_scrollbar_change_hidden(menu):
    """Test hidden menubar has no scrollbar displacement."""
    mb = MenuBar("Menu", 500, (0, 0, 0))
    mb.set_menu(menu)

    mb.hide()

    assert mb.get_scrollbar_style_change(POSITION_EAST) == (0, (0, 0))


def test_menubar_scrollbar_change_modify_scrollarea_disabled(menu):
    """Test disabled scrollarea modification returns no displacement."""
    mb = MenuBar(
        "Menu",
        500,
        (0, 0, 0),
        modify_scrollarea=False,
    )
    mb.set_menu(menu)

    assert mb.get_scrollbar_style_change(POSITION_EAST) == (0, (0, 0))


def test_menubar_set_padding_returns_self():
    """Test set_padding returns self."""
    mb = MenuBar("Menu", 500, (0, 0, 0))

    assert mb.set_padding(1, 2, 3, 4) is mb


def test_menubar_set_border_returns_self():
    """Test set_border returns self."""
    mb = MenuBar("Menu", 500, (0, 0, 0))

    assert mb.set_border(1) is mb


def test_menubar_set_selection_effect_returns_self():
    """Test set_selection_effect returns self."""
    mb = MenuBar("Menu", 500, (0, 0, 0))

    assert mb.set_selection_effect(None) is mb


def test_menubar_backbox_visibility_disabled():
    """Test backbox visibility when backbox is disabled."""
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=False)

    assert not mb._backbox_visible()


def test_menubar_get_height_hidden():
    """Test hidden menubar height is zero."""
    mb = MenuBar("Menu", 500, (0, 0, 0))

    mb.hide()

    assert mb.get_height() == 0


def test_menubar_get_height_floating():
    """Test floating menubar height is zero."""
    mb = MenuBar("Menu", 500, (0, 0, 0))

    mb.set_float(True)

    assert mb.get_height() == 0


def test_menubar_set_title_rerender(menu):
    """Test title update after menubar is attached to a menu."""
    mb = MenuBar("Menu", 500, (0, 0, 0))
    mb.set_menu(menu)

    mb.set_title("New title")

    assert mb._title == "New title"


def test_menubar_invalid_title_offset_types():
    """Test invalid title offset types."""
    mb = MenuBar("Menu", 500, (0, 0, 0))

    with pytest.raises(AssertionError):
        mb.set_title("Menu", offsetx="bad")  # type: ignore

    with pytest.raises(AssertionError):
        mb.set_title("Menu", offsety="bad")  # type: ignore


def test_menubar_backbox_border_width_update():
    """Test backbox border width update."""
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True)

    mb.set_backbox_border_width(5)

    assert mb._backbox_border_width == 5
