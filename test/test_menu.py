"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST MENU
Menu object tests.
"""

import copy
import math
import sys
import time
import timeit

import pygame
import pytest

from pygame_menu import (
    BaseImage,
    baseimage,
    controls as ctrl,
    events,
    widgets,
)
from pygame_menu.locals import (
    ALIGN_CENTER,
    ALIGN_LEFT,
    ALIGN_RIGHT,
    CURSOR_ARROW,
    CURSOR_CROSSHAIR,
    CURSOR_HAND,
    FINGERDOWN,
    FINGERMOTION,
    INPUT_FLOAT,
    INPUT_INT,
    ORIENTATION_VERTICAL,
    SCROLLAREA_POSITION_NONE,
)
# noinspection PyProtectedMember
from pygame_menu.menu import (
    JOY_EVENT_DOWN,
    JOY_EVENT_LEFT,
    JOY_EVENT_RIGHT,
    JOY_EVENT_UP,
    Menu,
    _MenuCopyException,
    _MenuSizingException,
    _MenuWidgetOverflow,
)
from pygame_menu.themes import THEME_BLUE, THEME_DARK, THEME_DEFAULT, Theme
from pygame_menu.utils import get_cursor, set_pygame_cursor
from pygame_menu.widgets import Button, Label
from test._utils import (
    PYGAME_V2,
    TEST_THEME,
    THEME_NON_FIXED_TITLE,
    WIDGET_MOUSEOVER,
    WIDGET_TOP_CURSOR,
    MenuUtils,
    PygameEventUtils,
    reset_widgets_over,
    surface,
)

TEST_TIME_DRAW = False


def dummy_function() -> None:
    """Dummy function for callbacks in tests."""
    return


def test_mainloop_disabled():
    """Test disabled mainloop."""
    menu = MenuUtils.generic_menu(title="mainmenu")
    menu.disable()
    with pytest.raises(RuntimeError):
        menu.mainloop(surface, bgfun=dummy_function, disable_loop=True)
    menu.enable()


def test_time_draw():
    """Measure draw/update performance for stress scenarios."""
    if not TEST_TIME_DRAW:
        return

    menu = MenuUtils.generic_menu(title="EPIC")
    menu.enable()

    # Add several widgets
    add_decorator = True
    for i in range(30):
        btn = menu.add.button(title="epic", action=events.BACK)
        btn_deco = btn.get_decorator()
        if add_decorator:
            for j in range(10):
                btn_deco.add_pixel(j * 10, j * 20, (10, 10, 150))
        menu.add.vertical_margin(margin=10)
        menu.add.label(title="epic test")
        menu.add.color_input(title="color", color_type="rgb", default=(234, 33, 2))
        menu.add.selector(title="epic selector", items=[("1", "3"), ("2", "4")])
        menu.add.text_input(title="text", default="the default text")

    def draw_and_update():
        """Draw and update the menu once."""
        menu.draw(surface)
        menu.update(pygame.event.get())

    # (no decorator) no updates, 0.921
    # (no decorator) updates, 0.860
    # (no decorator) check len updates, 0.855
    # (no decorator) with surface cache, 0.10737799999999886
    # (decorator) with surface cache, 0.1033874000000008
    print(timeit.timeit(lambda: draw_and_update(), number=100))


def test_copy():
    """Test menu copy protection."""
    menu = MenuUtils.generic_menu()
    with pytest.raises(_MenuCopyException):
        copy.copy(menu)
    with pytest.raises(_MenuCopyException):
        copy.deepcopy(menu)


def test_size_constructor():
    """Test menu size constructor validation."""
    inf_size = 1000000000

    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(width=0, height=300)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(width=300, height=0)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(width=-200, height=300)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(width=inf_size, height=300)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(width=300, height=inf_size)
    with pytest.raises(ValueError):
        MenuUtils.generic_menu(width=300, height=1)


def test_position():
    """Test menu and widget positioning."""
    theme_src = TEST_THEME.copy()

    menu = MenuUtils.generic_menu(theme=theme_src)
    btn = menu.add.button("button")
    menu.center_content()

    assert menu.get_height() == 400
    assert menu.get_height(inner=True) == 345
    assert menu.get_menubar().get_height() == 55

    h = 41 if PYGAME_V2 else 42
    assert btn.get_height() == h
    assert btn.get_size()[1] == h
    assert menu.get_height(widget=True) == h

    v_pos = int((345 - h) / 2)  # available_height - widget_height
    assert menu._widget_offset[1] == v_pos
    assert btn.get_position()[1] == v_pos + 1

    # If there's too many widgets, the centering should be disabled
    for i in range(20):
        menu.add.button("button")
    assert menu._widget_offset[1] == 0

    theme = menu.get_theme()

    # Anyway, as the widget is 0, the first button position should be the height of its selection effect
    btneff = btn.get_selection_effect().get_margin()[0]
    assert btn.get_position()[1] == btneff + 1
    assert h * 21 + theme.widget_margin[1] * 20 == menu.get_height(widget=True)

    # Test menu not centered
    menu = MenuUtils.generic_menu(center_content=False, theme=theme_src)
    btn = menu.add.button("button")
    btneff = btn.get_selection_effect().get_margin()[0]
    assert btn.get_position()[1] == btneff + 1

    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(position_x=-1, position_y=0)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(position_x=0, position_y=-1)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(position_x=-1, position_y=-1)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(position_x=101, position_y=0)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(position_x=99, position_y=101)

    menu = MenuUtils.generic_menu(position_x=0, position_y=0)
    menu.set_relative_position(20, 40)

    theme = theme_src.copy()
    theme.widget_font_size = 20

    menu = Menu(
        column_min_width=380,
        columns=2,
        height=300,
        rows=4,
        theme=theme,
        title="Welcome",
        width=400,
    )

    quit1 = menu.add.button("Quit", events.EXIT)
    name1 = menu.add.text_input("Name: ", default="John Doe", maxchar=10, padding=30)
    sel1 = menu.add.selector("Difficulty: ", [("Hard", 1), ("Easy", 2)])
    sel2 = menu.add.selector("Difficulty: ", [("Hard", 1), ("Easy", 2)])
    play1 = menu.add.button("Play", events.NONE, align=ALIGN_LEFT)
    play2 = menu.add.button("Play 2", events.NONE, align=ALIGN_RIGHT)
    play2.set_float()
    hidden = menu.add.button("Hidden", font_size=100)
    hidden.hide()
    quit2 = menu.add.button("Quit", events.EXIT)
    label = menu.add.label("This label is really epic")
    label.rotate(90)
    menu.render()

    assert quit1.get_position() == (170, 5)
    assert name1.get_position() == (115, 73)
    assert sel1.get_position() == (104, 141)
    assert sel2.get_position() == (104, 179)
    assert play1.get_position() == (388, 5)
    assert play2.get_position() == (698, 5)
    assert hidden.get_position() == (0, 0)
    assert quit2.get_position() == (550, 43)
    assert label.get_position() == (556, 81)

    # Test no selectable position
    menu = MenuUtils.generic_menu(center_content=False, theme=theme_src)
    btn = menu.add.button("button")
    btn.is_selectable = False
    menu.render()
    assert btn.get_position()[1] == 1

    # Test no selectable + widget
    menu = MenuUtils.generic_menu()
    img = menu.add.image(
        baseimage.IMAGE_EXAMPLE_PYGAME_MENU,
        scale=(0.25, 0.25),
        align=ALIGN_CENTER,
    )
    btn = menu.add.button("Nice")
    margin = menu.get_theme().widget_margin[1]
    menu.render()

    assert menu.get_height(widget=True) == img.get_height() + btn.get_height() + margin
    assert (
        int((menu.get_height(inner=True) - menu.get_height(widget=True)) / 2)
        == menu._widget_offset[1]
    )

    # Test alternating float
    # b1,b2
    # b3
    # b4,b5,b6
    # b7
    menu = MenuUtils.generic_menu()
    b1 = menu.add.button("b1")
    b2 = menu.add.button("b2").set_float()
    b3 = menu.add.button("b3")
    b4 = menu.add.button("b4")
    b5 = menu.add.button("b5").set_float()
    b6 = menu.add.button("b6").set_float()
    b7 = menu.add.button("b37")

    assert b1.get_col_row_index() == (0, 0, 0)
    assert b2.get_col_row_index() == (0, 0, 1)
    assert b3.get_col_row_index() == (0, 1, 2)
    assert b4.get_col_row_index() == (0, 2, 3)
    assert b5.get_col_row_index() == (0, 2, 4)
    assert b6.get_col_row_index() == (0, 2, 5)
    assert b7.get_col_row_index() == (0, 3, 6)

    # b1,b2
    # b3,b5,b6
    # b7
    menu.remove_widget(b4)

    assert b1.get_col_row_index() == (0, 0, 0)
    assert b2.get_col_row_index() == (0, 0, 1)
    assert b3.get_col_row_index() == (0, 1, 2)
    assert b4.get_col_row_index() == (-1, -1, -1)
    assert b5.get_col_row_index() == (0, 1, 3)
    assert b6.get_col_row_index() == (0, 1, 4)
    assert b7.get_col_row_index() == (0, 2, 5)

    # b1,b2,b5,b6
    # b7
    menu.remove_widget(b3)

    assert b1.get_col_row_index() == (0, 0, 0)
    assert b2.get_col_row_index() == (0, 0, 1)
    assert b3.get_col_row_index() == (-1, -1, -1)
    assert b4.get_col_row_index() == (-1, -1, -1)
    assert b5.get_col_row_index() == (0, 0, 2)
    assert b6.get_col_row_index() == (0, 0, 3)
    assert b7.get_col_row_index() == (0, 1, 4)

    # Test position relative/absolute
    menu.set_relative_position(50, 50)
    assert menu._position == (0, 100)
    menu.set_absolute_position(50, 50)
    assert menu._position == (50, 50)

    # Test absolute position constructor
    menu = Menu("", 200, 300, position=(50, 50))
    assert menu._position == (200, 150)
    menu = Menu("", 200, 300, position=(50, 50, True))
    assert menu._position == (200, 150)
    menu = Menu("", 200, 300, position=(50, 50, False))
    assert menu._position == (50, 50)


def test_float_position():
    """Test float widget positioning behavior."""
    menu = MenuUtils.generic_menu(center_content=False)

    a = menu.add.label("nice")
    a.set_float()
    b = menu.add.label("nice")
    b.set_float()
    assert a.get_position() == b.get_position()

    z = menu.add.label("nice", float=True)
    assert a.get_position() == z.get_position()

    f = menu.add.frame_v(1000, 1000)
    f.set_float()
    assert a.get_position()[1] == f.get_position()[1]

    c = menu.add.label("nice")
    c.set_float()
    assert a.get_position() == c.get_position()
    assert c.get_position()[1] == f.get_position()[1]

    labels = [
        menu.add.label(f"Lorem ipsum #{i}", font_size=15, font_color="#000", padding=0)
        for i in range(20)
    ]
    for j in labels:
        f.pack(j)

    d = menu.add.label("nice")
    d.set_float()
    assert a.get_position() == d.get_position()
    assert len(menu.get_widgets()) == 26


def test_translate():
    """Test menu translation."""
    menu = MenuUtils.generic_menu(width=400, theme=THEME_NON_FIXED_TITLE)
    btn = menu.add.button("button")

    assert menu.get_menubar().get_height() == 55
    assert menu.get_position() == (100, 100)
    assert menu.get_scrollarea().get_position() == (100, 155)
    assert menu.get_menubar().get_position() == (100, 100)

    expected_y = 153 if PYGAME_V2 else 152
    assert btn.get_position() == (153, expected_y)
    assert btn.get_position(to_real_position=True) == (253, expected_y + 155)
    assert btn.get_position(to_absolute_position=True) == (153, expected_y)
    assert menu.get_translate() == (0, 0)

    menu.translate(0, 100)

    assert menu.get_position() == (100, 200)
    assert menu.get_scrollarea().get_position() == (100, 255)
    assert menu.get_menubar().get_position() == (100, 200)
    assert btn.get_position() == (153, expected_y)
    assert btn.get_position(to_real_position=True) == (253, expected_y + 255)
    assert btn.get_position(to_absolute_position=True) == (153, expected_y)
    assert menu.get_translate() == (0, 100)


def test_close():
    """Test menu close behavior and callbacks."""
    menu = MenuUtils.generic_menu()
    menu.disable()
    menu.set_title("1")
    menu.set_attribute("epic", False)
    menu._back()

    def close():
        """Set a flag when menu closes."""
        menu.set_attribute("epic", True)

    menu.set_onclose(close)
    assert not menu.is_enabled()
    menu.enable()
    assert not menu.get_attribute("epic")
    menu._close()
    assert menu.get_attribute("epic")

    test = [False, False]

    def closefun():
        """Mark close callback as executed."""
        test[0] = True

    menu2 = MenuUtils.generic_menu(onclose=closefun)
    menu2.set_title(2)
    menu2.enable()
    result = menu2.close()
    assert result
    assert test[0]

    def closefun_menu(m: Menu):
        """Validate close callback receives current menu."""
        test[1] = True
        assert m == menu2

    menu2.set_onclose(closefun_menu)
    menu2.enable()
    menu2.close()
    assert test[1]

    menu2.set_onclose(None)
    menu2.enable()
    result = menu2.close()
    assert not result  # NONE status don't change enabled
    assert menu2.is_enabled()

    menu2.set_onclose(events.NONE)
    result = menu2.close()
    assert not result  # NONE event don't change enabled
    assert menu2.is_enabled()

    # Add button with submenu, and open it
    assert menu2.get_current().get_title() == "2"
    menu2.add.button("to1", menu).apply()
    assert menu2.get_current().get_title() == "1"
    assert menu2.get_current() == menu

    # Set onclose 1 as reset, if close then menu should be disabled and back to '2'
    menu.set_onclose(events.RESET)
    menu.close()

    # Open again 1
    assert not menu2.is_enabled()
    menu2.enable()
    menu2.get_selected_widget().apply()
    assert menu2.get_current().get_title() == "1"

    # Set new close callback, it receives the menu and fires reset,
    # the output should be the same, except it doesn't close
    def new_close(m: Menu):
        """Reset menu from close callback."""
        assert m == menu
        m.reset(1)

    # Also, set first menu onreset to test this behavior
    reset = [False]

    def onreset(m: Menu):
        """Mark reset callback as executed."""
        assert m == menu
        reset[0] = True

    menu.set_onclose(new_close)
    menu.set_onreset(onreset)
    assert not reset[0]
    menu.close()
    assert reset[0]
    assert menu2.get_current().get_title() == "2"
    assert not menu2.is_enabled()

    # Test back event
    menu2.enable()
    menu2.get_selected_widget().apply()
    menu.set_onclose(events.BACK)
    menu.set_onreset(None)
    assert menu2.get_current() == menu
    menu2.close()
    assert menu2.get_current() == menu2

    # Test close event, this should NOT change the pointer
    menu2.enable()
    menu2.get_selected_widget().apply()
    menu.set_onclose(events.CLOSE)
    menu.set_onreset(None)
    assert menu2.get_current() == menu
    menu.close()
    assert menu2.get_current() == menu
    menu.reset(1)
    assert menu2.get_current() == menu2

    # Close if not enabled
    menu.disable()
    with pytest.raises(RuntimeError):
        menu.close()


def test_enabled():
    """Test menu enable and disable behavior."""
    menu = MenuUtils.generic_menu(onclose=events.NONE, enabled=False)
    assert not menu.is_enabled()
    menu.enable()
    assert menu.is_enabled()
    assert menu.is_enabled()

    menu.mainloop(surface, bgfun=lambda: None, disable_loop=True)
    menu._close()


def test_depth():
    """Test submenu depth tracking."""
    menu = MenuUtils.generic_menu(title="mainmenu")
    assert menu._get_depth() == 0

    menu_prev = menu
    menu_ = None
    for i in range(1, 11):
        menu_ = MenuUtils.generic_menu(title=f"submenu {i}")
        button = menu_prev.add.button("open", menu_)
        button.apply()
        menu_prev = menu_

    menu.enable()
    menu.draw(surface)

    assert menu.get_current().get_id() != menu.get_id()
    assert menu != menu_
    assert menu_._get_depth() == 10
    assert menu._get_depth() == 10

    # menu when it was opened it changed to submenu 1, when submenu 1 was opened
    # it changed to submenu 2, and so on...
    assert menu.get_title() == "mainmenu"
    assert menu.get_current().get_title() == "submenu 10"
    assert menu_.get_current().get_title() == "submenu 10"

    # Submenu 10 has not changed to any, so back will not affect it,
    # but mainmenu will reset 1 unit
    menu_._back()
    assert menu_.get_title() == "submenu 10"

    # Mainmenu has changed, go back changes from submenu 10 to 9
    assert menu._get_depth() == 9
    menu._back()
    assert menu._get_depth() == 8
    assert menu.get_title() == "mainmenu"
    assert menu.get_current().get_title() == "submenu 8"

    # Full go back (reset)
    menu.full_reset()
    assert menu._get_depth() == 0
    assert menu.get_current().get_title() == "mainmenu"


def test_get_widget():
    """Test widget retrieval, including recursive search."""
    menu = MenuUtils.generic_menu(title="mainmenu")

    widget = menu.add.text_input("test", textinput_id="some_id")
    widget_found = menu.get_widget("some_id")
    assert widget == widget_found

    # Add a widget to the deepest menu
    prev_menu = menu
    for i in range(11):
        menu_ = MenuUtils.generic_menu()
        prev_menu.add.button("menu", menu_)
        prev_menu = menu_

    # Add a deep input and selector
    deep_widget = prev_menu.add.text_input("title", textinput_id="deep_id")
    deep_selector = prev_menu.add.selector(
        "selector", [("0", 0), ("1", 1)], selector_id="deep_selector", default=1
    )

    assert menu.get_widget("deep_id", recursive=False) is None
    assert menu.get_widget("deep_id", recursive=True) == deep_widget
    assert menu.get_widget("deep_selector", recursive=True) == deep_selector


def test_add_generic_widget():
    """Test adding generic widgets to menu."""
    menu = MenuUtils.generic_menu()
    btn = menu.add.button("nice")
    w = Button("title")
    menu.add.generic_widget(w)

    with pytest.raises(ValueError):
        menu.add.generic_widget(w)

    btn._menu = None
    with pytest.raises(IndexError):
        menu.add.generic_widget(btn)

    btn._menu = menu
    menu.remove_widget(btn)
    assert btn._menu is None

    menu.add.generic_widget(btn)
    assert btn in menu.get_widgets()


def test_get_selected_widget():
    """Test selected widget state transitions."""
    menu = MenuUtils.generic_menu(title="mainmenu")

    # Test widget selection and removal
    widget = menu.add.text_input("test", default="some_id")
    assert widget == menu.get_selected_widget()
    menu.remove_widget(widget)
    assert menu.get_selected_widget() is None
    assert menu.get_index() == -1

    # Add two widgets, first widget will be selected first, but if removed the second should be selected
    widget1 = menu.add.text_input("test", default="some_id", textinput_id="epic")
    with pytest.raises(IndexError):
        menu.add.text_input("test", default="some_id", textinput_id="epic")
    widget2 = menu.add.text_input("test", default="some_id")
    assert widget1.get_menu() == menu
    assert widget1 == menu.get_selected_widget()
    menu.remove_widget(widget1)
    assert widget1.get_menu() is None
    assert widget2 == menu.get_selected_widget()
    menu.remove_widget(widget2)
    assert widget2.get_menu() is None
    assert len(menu.get_widgets()) == 0

    # Add 3 widgets, select the last one and remove it, then the selected widget must be the first
    w1 = menu.add.button("1")
    w2 = Label("2")
    menu.add.generic_widget(w2, configure_defaults=True)
    w3 = menu.add.button("3")
    assert menu.get_selected_widget() == w1
    menu.select_widget(w3)
    assert menu.get_selected_widget() == w3
    menu.remove_widget(w3)
    assert menu.get_selected_widget() == w1  # 3 was deleted, so 1 should be selected

    # Hides w1, then w2 should be selected
    w1.hide()
    assert menu.get_selected_widget() == w2

    # Un-hide w1, w2 should be keep selected
    w1.show()
    assert menu.get_selected_widget() == w2

    # Mark w1 as unselectable and remove w2, then no widget should be selected
    w1.is_selectable = False
    menu.remove_widget(w2)
    assert menu.get_selected_widget() is None
    with pytest.raises(ValueError):
        menu.select_widget(w1)

    # Mark w1 as selectable
    w1.is_selectable = True
    menu.add.generic_widget(w2)
    assert menu.get_selected_widget() == w2

    # Add a new widget that cannot be selected
    menu.add.label("not selectable")
    menu.add.label("not selectable")
    w_last = menu.add.label("not selectable", selectable=True)

    # If w2 is removed, then menu will try to select labels, but as them are not selectable it should select the last one
    w2.hide()
    assert menu.get_selected_widget() == w_last

    # Mark w1 as unselectable, then w1 is not selectable, nor w2, and labels are unselectable too
    # so the selected should be the same
    w1.is_selectable = False
    menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
    assert menu.get_selected_widget() == w_last

    # Show w2, then if DOWN is pressed again, the selected status should be 2
    w2.show()
    menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
    assert menu.get_selected_widget() == w2

    # Hide w2, pass again to w_last
    w2.hide()
    assert menu.get_selected_widget() == w_last

    # Hide w_last, then nothing is selected
    w_last.hide()
    assert menu.get_selected_widget() is None

    # Un-hide w2, then it should be selected
    w2.show()
    assert menu.get_selected_widget() == w2

    # Remove w2, then nothing should be selected
    menu.remove_widget(w2)
    assert menu.get_selected_widget() is None

    # Clear all widgets and get index
    menu._widgets = []
    menu._index = 100
    assert menu.get_selected_widget() is None

    # Destroy index
    menu._index = "0"  # type: ignore
    assert menu.get_selected_widget() is None
    assert menu._index == 0

    # Add new index
    btn = menu.add.button("epic")
    assert menu.get_selected_widget() == btn
    menu.unselect_widget()
    assert menu.get_selected_widget() is None


def test_submenu():
    """Test submenu linking and lifecycle behavior."""
    menu = MenuUtils.generic_menu()
    menu2 = MenuUtils.generic_menu()
    btn = menu.add.button("btn", menu2)

    assert btn.to_menu
    assert menu.in_submenu(menu2)
    assert not menu2.in_submenu(menu)
    assert menu2 in menu.get_submenus()
    assert menu not in menu2.get_submenus()

    # Remove menu2 from menu
    btn.update_callback(lambda: None)
    assert not btn.to_menu
    assert not menu.in_submenu(menu2)

    # Test recursive
    menu.clear()
    menu2.clear()

    with pytest.raises(ValueError):
        menu.add.button("to self", menu)
    menu.add.button("to2", menu2)
    with pytest.raises(ValueError):
        menu2.add.button("to1", menu)

    # Test duplicated submenu
    menu_d = MenuUtils.generic_menu()
    b1 = menu_d.add.button("btn", menu, button_id="1")
    b2 = menu_d.add.button("btn2", menu, button_id="2")

    assert b1._menu_hook == menu
    assert b2._menu_hook == menu

    assert b1 in menu_d._submenus[menu]
    assert b2 in menu_d._submenus[menu]

    menu_d.remove_widget("1")
    assert b1 not in menu_d._submenus[menu]
    assert b2 in menu_d._submenus[menu]
    menu_d.remove_widget("2")

    assert menu_d._submenus == {}

    # Clear menu
    menu.clear()
    assert btn._menu is None

    # Add more submenus
    menu3 = MenuUtils.generic_menu()
    ba = menu.add.button("btn12A", menu2)
    bb = menu.add.button("btn12B", menu2)
    bc = menu.add.button("btn12C", menu2)
    b23 = menu2.add.button("btn23", menu3)

    menu._test_print_widgets()
    assert menu.get_submenus() == (menu2,)
    assert menu.get_submenus(recursive=True) == (menu2, menu3)
    assert menu._submenus[menu2] == [ba, bb, bc]

    # Remove links upon submenu disappears
    menu.remove_widget(bb)
    assert menu.get_submenus() == (menu2,)
    assert menu._submenus[menu2] == [ba, bc]
    menu.remove_widget(ba)
    assert menu.get_submenus() == (menu2,)
    assert menu._submenus[menu2] == [bc]
    menu.remove_widget(bc)
    assert menu.get_submenus() == ()
    assert menu.get_submenus(recursive=True) == ()
    assert menu._submenus == {}

    # Test circular
    assert b23._menu == menu2
    menu2.clear()
    assert b23._menu is None

    menu.add.button("12", menu2)
    menu2.add.button("23", menu3)
    with pytest.raises(ValueError):
        menu3.add.button("31", menu)
    with pytest.raises(ValueError):
        menu3.add.button("31", menu2)

    # Test update action
    menu.clear()
    menu2.clear()

    b12 = menu.add.button("btn12", menu2)
    b23 = menu2.add.button("btn23", menu3)
    assert menu.get_submenus() == (menu2,)
    assert menu.get_submenus(recursive=True) == (menu2, menu3)
    assert menu._submenus == {menu2: [b12]}
    assert menu2._submenus == {menu3: [b23]}

    b12.update_callback(lambda: print("epic"))
    assert menu.get_submenus() == ()
    assert menu.get_submenus(recursive=True) == ()
    assert menu._submenus == {}
    assert menu2._submenus == {menu3: [b23]}


def test_centering():
    """Test automatic menu centering behavior."""
    theme = THEME_BLUE.copy()
    theme.widget_offset = (0, 100)
    menu = MenuUtils.generic_menu(theme=theme)
    assert menu.get_theme() == theme
    assert not menu._auto_centering

    # Outer scrollarea margin disables centering
    theme = THEME_BLUE.copy()
    theme.scrollarea_outer_margin = (0, 100)
    menu = MenuUtils.generic_menu(theme=theme)
    assert not menu._auto_centering

    # Normal
    theme = THEME_BLUE.copy()
    menu = MenuUtils.generic_menu(theme=theme)
    assert menu._auto_centering

    # Text offset
    theme = THEME_DARK.copy()
    theme.title_font_size = 35
    theme.widget_font_size = 25

    menu = Menu(
        column_min_width=400, height=300, theme=theme, title="Images", width=400
    )

    menu.add.label("Text #1")
    menu.add.vertical_margin(100)
    menu.add.label("Text #2")
    assert menu._widget_offset[1] == (33 if PYGAME_V2 else 32)


def test_getters():
    """Test basic menu getters."""
    menu = MenuUtils.generic_menu(title="mainmenu")
    assert menu.get_menubar() is not None
    assert menu.get_scrollarea() is not None

    w, h = menu.get_size()
    assert int(w) == 600
    assert int(h) == 400

    w, h = menu.get_window_size()
    assert int(w) == 600
    assert int(h) == 600


def test_generic_events():
    """Test generic keyboard, joystick, and mouse events."""
    menu = MenuUtils.generic_menu(title="mainmenu")

    event_val = [False]

    # Add a menu and a method that set a function
    def _some_event():
        """Toggle event flag and return payload."""
        event_val[0] = True
        return "the value"

    # Add some widgets
    button = None
    wid = []
    for i in range(5):
        button = menu.add.button("button", _some_event)
        wid.append(button.get_id())
    assert len(menu.get_widgets()) == 5
    assert len(menu.get_widgets(wid)) == 5

    # Create an event in pygame
    menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    assert menu.get_index() == 1

    # Move down twice
    for i in range(2):
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
    assert menu.get_index() == 4
    menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    assert menu.get_index() == 0

    # Press enter, button should trigger and call function
    assert button.apply() == "the value"
    menu.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))

    # Other
    menu.update(PygameEventUtils.key(ctrl.KEY_CLOSE_MENU, keydown=True))
    menu.update(PygameEventUtils.key(ctrl.KEY_BACK, keydown=True))

    # Check index is the same as before
    assert menu.get_index() == 0

    # Check joy
    menu.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_UP))
    assert menu.get_index() == 4
    menu.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_DOWN))
    assert menu.get_index() == 0
    menu.update(PygameEventUtils.joy_motion(1, 1))
    assert menu.get_index() == 1
    menu.update(PygameEventUtils.joy_motion(1, -1))
    assert menu.get_index() == 0
    menu.update(PygameEventUtils.joy_motion(1, -1))
    assert menu.get_index() == 4

    click_pos = button.get_rect(to_real_position=True).center
    menu.update(PygameEventUtils.mouse_click(click_pos[0], click_pos[1]))
    assert event_val[0]
    event_val[0] = False


def test_back_event():
    """Test back event handling."""
    menu = MenuUtils.generic_menu(title="mainmenu")
    assert menu._get_depth() == 0
    menu_ = MenuUtils.generic_menu(title="submenu")
    button = menu.add.button("open", menu_)
    button.apply()
    assert menu._get_depth() == 1
    menu.update(PygameEventUtils.key(ctrl.KEY_BACK, keydown=True))
    assert menu._get_depth() == 0


def test_mouse_empty_submenu():
    """Test mouse navigation when opening a smaller submenu."""
    menu = MenuUtils.generic_menu(title="mainmenu")
    menu.enable()

    submenu = MenuUtils.generic_menu()
    submenu.add.button("button", lambda: None)

    menu.add.button("button", lambda: None)
    menu.add.button("button", lambda: None)
    button = menu.add.button("button", submenu)
    menu.disable()
    with pytest.raises(RuntimeError):
        menu.draw(surface)
    menu.enable()
    menu.draw(surface)

    click_pos = button.get_rect(to_real_position=True).center
    menu.update(PygameEventUtils.mouse_click(click_pos[0], click_pos[1]))


def test_input_data():
    """Test input data gathering and validation."""
    menu = MenuUtils.generic_menu(title="mainmenu")

    menu.add.text_input("text1", textinput_id="id1", default=1)
    data = menu.get_input_data(True)
    assert data["id1"] == "1"

    menu.add.text_input(
        "text1",
        textinput_id="id2",
        default=1.5,
        input_type=INPUT_INT,
    )
    data = menu.get_input_data(True)
    assert data["id2"] == 1
    with pytest.raises(IndexError):
        menu.add.text_input("text1", textinput_id="id1", default=1)

    menu.add.text_input(
        "text1",
        textinput_id="id3",
        default=1.5,
        input_type=INPUT_FLOAT,
    )
    data = menu.get_input_data(True)
    assert data["id3"] == 1.5

    # Add input to a submenu
    submenu = MenuUtils.generic_menu()
    submenu.add.text_input("text", textinput_id="id4", default="thewidget")
    menu.add.button("submenu", submenu)
    data = menu.get_input_data(recursive=True)
    assert data["id4"] == "thewidget"

    # Add a submenu within submenu with a repeated id, menu.get_input_data
    # should raise an exception because of the repeated id, even if it's in a different submenu
    subsubmenu = MenuUtils.generic_menu()
    subsubmenu.add.text_input("text", textinput_id="id4", default="repeateddata")
    submenu.add.button("submenu", subsubmenu)
    with pytest.raises(ValueError):
        menu.get_input_data(recursive=True)


def test_columns_menu():
    """Test multi-column menu behavior."""
    # Basic invalid configurations
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(columns=0)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(columns=-1)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(rows=0)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(rows=-10)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(columns=2, rows=0)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(columns=2)  # none rows

    # Assert append more widgets than number of rows*columns
    column_menu = MenuUtils.generic_menu(columns=2, rows=4, enabled=False)

    # Check move if empty
    assert not column_menu._right()
    assert not column_menu._left()

    for _ in range(8):
        column_menu.add.button("test", events.BACK)

    with pytest.raises(RuntimeError):
        column_menu.mainloop(surface, bgfun=dummy_function, disable_loop=True)

    column_menu._move_selected_left_right(-1)
    column_menu._move_selected_left_right(1)

    column_menu.disable()
    with pytest.raises(RuntimeError):
        column_menu.draw(surface)
    column_menu.enable()
    column_menu.draw(surface)
    column_menu.disable()
    assert len(column_menu._widgets) == 8
    with pytest.raises(RuntimeError):
        column_menu.draw(surface)

    with pytest.raises(_MenuWidgetOverflow):
        column_menu.add.button("test", events.BACK)

    column_menu._update_widget_position()
    assert len(column_menu._widgets) == 8

    # Test max width
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(columns=3, rows=4, column_max_width=[500, 500, 500, 500])

    MenuUtils.generic_menu(columns=3, rows=4, column_max_width=0)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(columns=3, rows=4, column_max_width=-1)

    column_menu = MenuUtils.generic_menu(columns=3, rows=4, column_max_width=500)
    assert len(column_menu._column_max_width) == 3
    for i in range(3):
        assert column_menu._column_max_width[i] == 500

    # Test min width
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(columns=3, rows=4, column_min_width=[500, 500, 500, 500])

    MenuUtils.generic_menu(columns=3, rows=4, column_min_width=100)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(columns=3, rows=4, column_min_width=-100)

    column_menu = MenuUtils.generic_menu(columns=3, rows=4, column_min_width=500)
    assert len(column_menu._column_min_width) == 3
    for i in range(3):
        assert column_menu._column_min_width[i] == 500

    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(columns=3, rows=4, column_min_width=None)  # type: ignore

    # max width > min width
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(
            columns=2,
            rows=4,
            column_min_width=[500, 500],
            column_max_width=[100, 500],
        )
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(
            columns=2,
            rows=4,
            column_min_width=[500, 500],
            column_max_width=[500, 100],
        )
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(rows=4, column_min_width=10, column_max_width=1)

    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(columns=-1, rows=4, column_max_width=500)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(rows=0, column_max_width=500)

    MenuUtils.generic_menu(column_max_width=[500])

    # Test different rows
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(columns=2, rows=[3, 3, 3])
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(columns=2, rows=[3, -3])
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(columns=2, rows=[3])

    # Create widget positioning
    width = 600
    menu = MenuUtils.generic_menu(columns=3, rows=2, width=width)
    btn1 = menu.add.button("btn")
    btn2 = menu.add.button("btn")
    btn3 = menu.add.button("btn")
    btn4 = menu.add.button("btn")
    btn5 = menu.add.button("btn")
    btn6 = menu.add.button("btn")

    assert btn1.get_col_row_index() == (0, 0, 0)
    assert btn2.get_col_row_index() == (0, 1, 1)
    assert btn3.get_col_row_index() == (1, 0, 2)
    assert btn4.get_col_row_index() == (1, 1, 3)
    assert btn5.get_col_row_index() == (2, 0, 4)
    assert btn6.get_col_row_index() == (2, 1, 5)

    # Check size
    assert len(menu._column_widths) == 3
    for col_w in menu._column_widths:
        assert col_w == width / 3

    # Removing widget updates layout
    menu.remove_widget(btn1)
    assert btn1.get_col_row_index() == (-1, -1, -1)
    assert btn2.get_col_row_index() == (0, 0, 0)
    assert btn3.get_col_row_index() == (0, 1, 1)
    assert btn4.get_col_row_index() == (1, 0, 2)
    assert btn5.get_col_row_index() == (1, 1, 3)
    assert btn6.get_col_row_index() == (2, 0, 4)

    # Hide widget
    btn2.hide()
    menu.render()
    assert btn2.get_col_row_index() == (-1, -1, 0)
    assert btn3.get_col_row_index() == (0, 0, 1)
    assert btn4.get_col_row_index() == (0, 1, 2)
    assert btn5.get_col_row_index() == (1, 0, 3)
    assert btn6.get_col_row_index() == (1, 1, 4)

    # Show again
    btn2.show()
    menu.render()
    assert btn1.get_col_row_index() == (-1, -1, -1)
    assert btn2.get_col_row_index() == (0, 0, 0)
    assert btn3.get_col_row_index() == (0, 1, 1)
    assert btn4.get_col_row_index() == (1, 0, 2)
    assert btn5.get_col_row_index() == (1, 1, 3)
    assert btn6.get_col_row_index() == (2, 0, 4)

    # Remove button
    menu.remove_widget(btn2)
    assert btn3.get_col_row_index() == (0, 0, 0)
    assert btn4.get_col_row_index() == (0, 1, 1)
    assert btn5.get_col_row_index() == (1, 0, 2)
    assert btn6.get_col_row_index() == (1, 1, 3)

    assert len(menu._column_widths) == 2
    for col_w in menu._column_widths:
        assert col_w == width / 2

    # Add new button
    btn7 = menu.add.button("btn")
    # Layout:
    # btn3 | btn5 | btn7
    # btn4 | btn6 |

    # Select second button
    with pytest.raises(ValueError):
        menu.select_widget(btn2)
    menu.select_widget(btn4)
    assert btn4.is_selected()

    # Move right → btn6
    menu._move_selected_left_right(1)
    assert not btn4.is_selected()
    assert btn6.is_selected()
    assert not btn7.is_selected()

    # Move right → btn7
    menu._move_selected_left_right(1)
    assert not btn6.is_selected()
    assert btn7.is_selected()

    # Move right → wrap to btn3
    menu._move_selected_left_right(1)
    assert not btn7.is_selected()
    assert btn3.is_selected()

    # Set btn4 as floating, then the layout should be
    # btn3,4 | btn6
    # btn5   | btn7
    btn4.set_float()
    menu.render()
    assert btn3.get_col_row_index() == (0, 0, 0)
    assert btn4.get_col_row_index() == (0, 0, 1)
    assert btn5.get_col_row_index() == (0, 1, 2)
    assert btn6.get_col_row_index() == (1, 0, 3)
    assert btn7.get_col_row_index() == (1, 1, 4)

    # Test sizing
    # btn3   | btn6
    # btn4,5 | btn7
    btn4.set_float(False)
    btn5.set_float()
    menu.render()

    assert btn3.get_width(apply_selection=True) == 63
    for col_w in menu._column_widths:
        assert col_w == width / 2

    # Scale 4, this should not change menu column widths
    btn4.scale(5, 5)
    menu.render()
    for col_w in menu._column_widths:
        assert col_w == width / 2

    # Scale 3, this should change menu column widths
    btn3.scale(5, 1)
    btn3_sz = btn3.get_width(apply_selection=True)
    btn6_sz = btn6.get_width(apply_selection=True)
    menu.render()
    col_width1 = (width * btn3_sz) / (btn3_sz + btn6_sz)
    col_width2 = width - col_width1
    assert pytest.approx(menu._column_widths[0], rel=0.01) == math.ceil(col_width1)
    assert pytest.approx(menu._column_widths[1], rel=0.01) == math.ceil(col_width2)

    # Different rows per column
    menu = MenuUtils.generic_menu(
        columns=3,
        rows=[2, 1, 2],
        width=width,
        column_max_width=[300, None, 100],
    )
    btn1 = menu.add.button("btn")
    btn2 = menu.add.button("btn")
    btn3 = menu.add.button("btn")
    btn4 = menu.add.button("btn")
    btn5 = menu.add.button("btn")

    assert btn1.get_col_row_index() == (0, 0, 0)
    assert btn2.get_col_row_index() == (0, 1, 1)
    assert btn3.get_col_row_index() == (1, 0, 2)
    assert btn4.get_col_row_index() == (2, 0, 3)
    assert btn5.get_col_row_index() == (2, 1, 4)

    btn1.scale(10, 1)
    with pytest.raises(_MenuSizingException):
        menu.render()

    btn1.resize(300, 10)
    menu.render()
    # btn1 | btn3 | btn4
    # btn2 |      | btn5

    assert menu._column_widths == [300, 200, 100]
    assert menu._column_pos_x == [150, 400, 550]

    # Change menu max column width, this should fulfill third column to its maximum possible less than 300
    # col2 should keep its current width
    menu._column_max_width = [300, None, 300]
    menu.render()
    assert menu._column_widths == [300, 63, 238]
    assert menu._column_pos_x == [150, 331, 482]

    # Chance maximum width of third column and enlarge button 4, then
    # middle column 3 will take 600-300-100 = 200
    menu._column_max_width = [300, None, 100]
    btn5.resize(100, 10)
    menu.render()
    assert menu._column_widths == [300, 200, 100]

    # Minimum width tests
    menu = MenuUtils.generic_menu(
        columns=3,
        rows=[2, 1, 2],
        width=width,
        column_max_width=[200, None, 150],
        column_min_width=[150, 150, 150],
    )
    # btn1 | btn3 | btn4
    # btn2 |      | btn5
    btn1 = menu.add.button("btn")
    menu.add.button("btn")
    menu.add.button("btn")
    menu.add.button("btn")
    menu.add.button("btn")
    btn1.resize(200, 10)
    menu.render()  # This should scale 2 column
    assert menu._column_widths == [200, 250, 150]

    menu = MenuUtils.generic_menu(
        columns=3,
        rows=[2, 1, 2],
        width=width,
        column_max_width=[200, 150, 150],
        column_min_width=[150, 150, 150],
    )
    btn1 = menu.add.button("btn")
    btn2 = menu.add.button("btn")
    btn3 = menu.add.button("btn")
    menu.add.button("btn")
    menu.add.button("btn")
    btn1.resize(200, 10)
    btn2.resize(150, 1)
    btn3.resize(150, 1)
    menu.render()
    assert menu._column_widths == [200, 150, 150]

    menu = MenuUtils.generic_menu()
    assert menu.get_col_rows() == (1, [10000000])


def test_screen_dimension():
    """Test custom screen dimension validation."""
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(title="mainmenu", screen_dimension=1)
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(title="mainmenu", screen_dimension=(-1, 1))
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(title="mainmenu", screen_dimension=(1, -1))
    with pytest.raises(AssertionError):
        # The menu is 600x400, so using a lower screen throws an error
        MenuUtils.generic_menu(title="mainmenu", screen_dimension=(1, 1))
    menu = MenuUtils.generic_menu(title="mainmenu", screen_dimension=(888, 999))
    assert menu.get_window_size() == (888, 999)


def test_touchscreen():
    """Test touchscreen interaction behavior."""
    with pytest.raises(AssertionError):
        MenuUtils.generic_menu(
            title="mainmenu",
            touchscreen=False,
            touchscreen_motion_selection=True,
        )

    menu = MenuUtils.generic_menu(
        title="mainmenu", touchscreen=True, enabled=False, mouse_visible=False
    )

    with pytest.raises(RuntimeError):
        menu.mainloop(surface, bgfun=dummy_function)

    event_val = [False]

    def _some_event():
        """Toggle touch event flag and return payload."""
        event_val[0] = True
        return "the value"

    button = menu.add.button("button", _some_event)

    if hasattr(pygame, "FINGERUP"):
        click_pos = button.get_rect(to_real_position=True).center
        menu.enable()

        menu.update(
            PygameEventUtils.touch_click(click_pos[0], click_pos[1], normalize=False)
        )
        assert not event_val[0]

        menu.update(PygameEventUtils.touch_click(click_pos[0], click_pos[1], menu=menu))
        assert event_val[0]
        event_val[0] = False

        assert menu.get_selected_widget().get_id() == button.get_id()
        btn = menu.get_selected_widget()
        assert btn.get_selected_time() >= 0


def test_remove_widget():
    """Test widget removal from update lists."""
    menu = MenuUtils.generic_menu()
    f = menu.add.frame_h(100, 200)
    menu._update_frames.append(f)
    btn = menu.add.button("epic")
    menu._update_widgets.append(btn)

    menu.remove_widget(f)
    assert f not in menu._update_frames

    menu.remove_widget(btn)
    assert btn not in menu._update_widgets


def test_reset_value():
    """Test value reset across widgets and submenus."""
    menu = MenuUtils.generic_menu(title="mainmenu")
    menu2 = MenuUtils.generic_menu(title="other")

    color = menu.add.color_input("title", default="ff0000", color_type="hex")
    text = menu.add.text_input("title", default="epic")
    selector = menu.add.selector("title", items=[("a", 1), ("b", 2)], default=1)
    text2 = menu2.add.text_input("titlesub", default="not epic")
    menu.add.label("mylabel")
    menu.add.button("submenu", menu2)

    # Change values
    color.set_value("aaaaaa")
    text.set_value("changed")
    text2.set_value("changed2")
    selector.set_value(0)

    # Reset values
    color.reset_value()
    assert color.get_value(as_string=True) == "#ff0000"
    color.set_value("aaaaaa")

    # Check values changed
    assert color.get_value(as_string=True) == "#aaaaaa"
    assert text.get_value() == "changed"
    assert selector.get_index() == 0

    # Reset values
    menu.reset_value(recursive=True)
    assert color.get_value(as_string=True) == "#ff0000"
    assert text.get_value() == "epic"
    assert text2.get_value() == "not epic"
    assert selector.get_index() == 1


def test_mainloop_kwargs():
    """Test mainloop callback argument handling."""
    test = [False, False]

    def test_accept_menu(m: Menu):
        """Callback that expects a menu argument."""
        assert isinstance(m, Menu)
        test[0] = True

    def test_not_accept_menu():
        """Callback that does not expect arguments."""
        test[1] = True

    menu = MenuUtils.generic_menu()
    assert not test[0]
    menu.mainloop(surface, test_accept_menu, disable_loop=True)
    assert test[0]
    assert not test[1]
    menu.mainloop(surface, test_not_accept_menu, disable_loop=True)
    assert test[0]
    assert test[1]

    test = [False, 0]

    def bgfun():
        """Background callback used while waiting for events."""
        test[0] = not test[0]
        test[1] += 1
        pygame.event.post(PygameEventUtils.joy_center(inlist=False))

    menu = MenuUtils.generic_menu()
    menu.set_onupdate(menu.disable)
    menu.enable()
    menu.mainloop(surface, bgfun, wait_for_event=True)

    test = [0]
    menu = MenuUtils.generic_menu()

    def bgfun():
        """Background callback used to count frames."""
        test[0] += 1
        if test[0] == 20:
            assert test[0] == menu._stats.loop
            menu.disable()

    menu.mainloop(surface, bgfun)


def _call_invalid_menu():
    """Call Menu constructor with an invalid keyword."""
    bad = {"fake_option": True}
    Menu(height=100, width=100, title="nice", **bad)


def test_invalid_args():
    """Test invalid constructor argument handling."""
    with pytest.raises(TypeError):
        _call_invalid_menu()


def test_set_title():
    """Test title updates and offsets."""
    menu = MenuUtils.generic_menu(title="menu")
    theme = menu.get_theme()
    menubar = menu.get_menubar()

    assert menu.get_title() == "menu"
    assert menubar.get_title_offset()[0] == theme.title_offset[0]
    assert menubar.get_title_offset()[1] == theme.title_offset[1]

    menu.set_title("nice")
    assert menu.get_title() == "nice"
    assert menubar.get_title_offset()[0] == theme.title_offset[0]
    assert menubar.get_title_offset()[1] == theme.title_offset[1]

    menu.set_title("nice", offset=(9, 10))
    assert menu.get_title() == "nice"
    assert menubar.get_title_offset()[0] == 9
    assert menubar.get_title_offset()[1] == 10

    menu.set_title("nice2")
    assert menu.get_title() == "nice2"
    assert menubar.get_title_offset()[0] == theme.title_offset[0]
    assert menubar.get_title_offset()[1] == theme.title_offset[1]


def test_empty():
    """Test empty and hidden-widget menu height."""
    menu = MenuUtils.generic_menu(title="menu")
    menu.render()
    assert menu.get_height(widget=True) == 0

    # Adds a button, hide it, then the height should be 0 as well
    btn = menu.add.button("hidden")
    btn.hide()
    assert menu.get_height(widget=True) == 0

    menu._runtime_errors.throw(False, "error")


def test_beforeopen():
    """Test onbeforeopen callbacks."""
    menu = MenuUtils.generic_menu()
    menu2 = MenuUtils.generic_menu()
    test = [False]

    def onbeforeopen(menu_from: Menu, menu_to: Menu):
        """Validate source and target menus before opening."""
        assert menu_from == menu
        assert menu_to == menu2
        test[0] = True

    menu2.set_onbeforeopen(onbeforeopen)
    assert not test[0]
    menu.add.button("to2", menu2).apply()
    assert test[0]

    def onbeforeopen_select_widget(_from: Menu, _to: Menu):
        """Select a specific widget before opening submenu."""
        _to.select_widget("option2")

    menu = MenuUtils.generic_menu()
    submenu = MenuUtils.generic_menu()
    submenu.add.button("Option 1", button_id="option1")
    submenu.add.button("Option 2", button_id="option2")
    submenu.add.button("Option 3", button_id="option3")
    submenu.set_onbeforeopen(onbeforeopen_select_widget)
    btn_submenu = menu.add.button("Submenu", submenu)

    # Test applying to submenu, which should trigger onbeforeopen
    assert submenu.get_selected_widget().get_id() == "option1"
    btn_submenu.apply()
    assert submenu.get_selected_widget().get_id() == "option2"


def test_focus():
    """Test focus overlay rendering conditions."""
    menu = MenuUtils.generic_menu(title="menu", mouse_motion_selection=True)
    btn = menu.add.button("nice")

    # Test focus
    btn.active = True
    focus = menu._draw_focus_widget(surface, btn)
    assert len(focus) == 4

    if not PYGAME_V2:
        assert focus[1] == ((0, 0), (600, 0), (600, 302), (0, 302))
        assert focus[2] == ((0, 303), (262, 303), (262, 352), (0, 352))
        assert focus[3] == ((336, 303), (600, 303), (600, 352), (336, 352))
        assert focus[4] == ((0, 353), (600, 353), (600, 600), (0, 600))
    else:
        assert focus[1] == ((0, 0), (600, 0), (600, 303), (0, 303))
        assert focus[2] == ((0, 304), (262, 304), (262, 352), (0, 352))
        assert focus[3] == ((336, 304), (600, 304), (600, 352), (336, 352))
        assert focus[4] == ((0, 353), (600, 353), (600, 600), (0, 600))

    # Test cases where the focus must fail
    btn._selected = False
    assert menu._draw_focus_widget(surface, btn) is None
    btn._selected = True

    # Set active false
    btn.active = False
    assert menu._draw_focus_widget(surface, btn) is None
    btn.active = True

    btn.hide()
    assert menu._draw_focus_widget(surface, btn) is None
    btn.show()

    btn.is_selectable = False
    assert menu._draw_focus_widget(surface, btn) is None
    btn.is_selectable = True

    menu._mouse_motion_selection = False
    assert menu._draw_focus_widget(surface, btn) is None
    menu._mouse_motion_selection = True

    btn.active = True
    btn._selected = True
    assert menu._draw_focus_widget(surface, btn) is not None


def test_visible():
    """Test widget visibility and selection updates."""
    menu = MenuUtils.generic_menu(title="menu")
    btn1 = menu.add.button("nice")
    btn2 = menu.add.button("nice")
    assert btn1.is_selected()

    btn2.hide()
    menu.select_widget(btn1)

    # btn2 cannot be selected as it is hidden
    with pytest.raises(ValueError):
        menu.select_widget(btn2)
    btn2.show()
    menu.select_widget(btn2)

    # Hide buttons
    btn1.hide()
    btn2.hide()

    assert not btn1.is_selected()
    assert not btn2.is_selected()

    assert btn1.get_col_row_index() == (-1, -1, 0)
    assert btn2.get_col_row_index() == (-1, -1, 1)

    menu.remove_widget(btn1)
    assert btn1.get_col_row_index() == (-1, -1, -1)
    assert btn2.get_col_row_index() == (-1, -1, 0)

    menu.remove_widget(btn2)
    assert btn1.get_col_row_index() == (-1, -1, -1)
    assert btn2.get_col_row_index() == (-1, -1, -1)

    menu = MenuUtils.generic_menu(title="menu")
    btn = menu.add.button("button")
    assert btn.is_selected()
    btn.hide()

    # As there's no more visible widgets, index must be -1
    assert menu._index == -1
    assert not btn.is_selected()

    # Widget should be selected, and index must be 0
    btn.show()
    assert btn.is_selected()
    assert menu._index == 0

    # Hide button, and set is as unselectable
    btn.hide()
    btn.is_selectable = False
    assert menu._index == -1
    btn.show()

    # Now, as widget is not selectable, button should not be selected and index still -1
    assert not btn.is_selected()
    assert menu._index == -1

    # Set selectable again
    btn.is_selectable = True
    btn.select()
    assert menu._index == -1
    assert menu.get_selected_widget() is None
    btn.select(update_menu=True)
    assert menu.get_selected_widget() == btn


def test_decorator():
    """Test menu decorator retrieval."""
    menu = MenuUtils.generic_menu()
    dec = menu.get_decorator()
    assert dec._obj == menu


def test_events():
    """Test menu event update flow."""
    if not PYGAME_V2:
        return

    menu_top = MenuUtils.generic_menu()
    menu = MenuUtils.generic_menu(
        columns=4,
        rows=2,
        touchscreen=True,
        touchscreen_motion_selection=True,
        column_min_width=[400, 300, 400, 300],
        joystick_enabled=True,
    )
    menu_top.add.button("menu", menu).apply()

    wid_g = []
    for i in range(8):
        b = menu.add.button("test" + str(i))
        wid_g.append(b)

    # btn0 | btn2 | btn4 | btn6
    # btn1 | btn3 | btn5 | btn7
    assert menu_top.get_current() == menu

    # Arrow keys
    assert menu.get_selected_widget() == wid_g[0]
    menu_top.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert menu.get_selected_widget() == wid_g[6]
    menu_top.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    assert menu.get_selected_widget() == wid_g[7]
    menu_top.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert menu.get_selected_widget() == wid_g[1]
    menu_top.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
    assert menu.get_selected_widget() == wid_g[0]

    # Joy key
    menu_top.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_LEFT))
    assert menu.get_selected_widget() == wid_g[6]
    menu_top.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_DOWN))
    assert menu.get_selected_widget() == wid_g[7]
    menu_top.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_RIGHT))
    assert menu.get_selected_widget() == wid_g[1]
    menu_top.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_UP))
    assert menu.get_selected_widget() == wid_g[0]

    # Joy hat
    menu_top.update(PygameEventUtils.joy_motion(-10, 0))
    assert menu_top.get_current()._joy_event == JOY_EVENT_LEFT
    assert menu.get_selected_widget() == wid_g[6]
    menu_top.update(PygameEventUtils.joy_motion(0, 10))
    assert menu_top.get_current()._joy_event == JOY_EVENT_DOWN
    assert menu.get_selected_widget() == wid_g[7]
    menu_top.update(PygameEventUtils.joy_motion(10, 0))
    assert menu_top.get_current()._joy_event == JOY_EVENT_RIGHT
    assert menu.get_selected_widget() == wid_g[1]
    menu_top.update(PygameEventUtils.joy_motion(0, -10))
    assert menu_top.get_current()._joy_event == JOY_EVENT_UP
    assert menu.get_selected_widget() == wid_g[0]

    # Menu should keep a recursive state of joy
    assert menu.get_current()._joy_event != 0
    menu_top.update(PygameEventUtils.joy_center())
    assert menu.get_current()._joy_event == 0

    # Click widget
    menu_top.enable()
    menu_top.update(
        PygameEventUtils.middle_rect_click(wid_g[1], evtype=pygame.MOUSEBUTTONDOWN)
    )
    assert menu.get_selected_widget() == wid_g[1]
    menu_top.update(
        PygameEventUtils.middle_rect_click(wid_g[0], evtype=pygame.MOUSEBUTTONDOWN)
    )
    assert menu.get_selected_widget() == wid_g[0]
    menu_top.update(
        PygameEventUtils.middle_rect_click(wid_g[1], evtype=pygame.MOUSEBUTTONDOWN)
    )
    assert menu.get_selected_widget() == wid_g[1]

    # It should not change the menu selection (button up)
    assert menu_top.update(
        PygameEventUtils.middle_rect_click(wid_g[1], evtype=pygame.MOUSEBUTTONUP)
    )
    assert menu.get_selected_widget() == wid_g[1]

    # Applying button up in a non-selected widget must return false
    assert not menu.update(
        PygameEventUtils.middle_rect_click(wid_g[0], evtype=pygame.MOUSEBUTTONUP)
    )

    # Fingerdown don't change selected widget if _touchscreen_motion_selection is enabled
    assert menu._touchscreen_motion_selection
    menu.update(PygameEventUtils.middle_rect_click(wid_g[0], evtype=FINGERDOWN))

    # If touchscreen motion is disabled, then fingerdown should select the widget
    menu._touchscreen_motion_selection = False
    menu.update(PygameEventUtils.middle_rect_click(wid_g[1], evtype=FINGERDOWN))
    assert menu.get_selected_widget() == wid_g[1]
    menu._touchscreen_motion_selection = True

    # Fingermotion should select widgets as touchscreen is active
    menu.update(PygameEventUtils.middle_rect_click(wid_g[0], evtype=FINGERMOTION))
    assert menu.get_selected_widget() == wid_g[0]

    # Infinite joy
    menu_top.update(PygameEventUtils.joy_motion(0, 10))
    menu.update([pygame.event.Event(menu._joy_event_repeat)])
    assert menu._joy_event != 0

    # Now disable joy event, then event repeat should not continue
    menu._joy_event = 0
    menu.update([pygame.event.Event(menu._joy_event_repeat)])
    menu_top.update(PygameEventUtils.joy_center())
    assert menu.get_current()._joy_event == 0

    # Active widget, and click outside to disable it (only if motion selection enabled)
    wid = menu.get_selected_widget()
    wid.active = True

    # Clicking the same rect should not fire the callback
    menu_top.update(
        PygameEventUtils.middle_rect_click(wid, evtype=pygame.MOUSEBUTTONDOWN)
    )
    assert wid.active
    assert wid.is_selected()
    wid._rect.x += 500
    menu._mouse_motion_selection = True
    menu_top.update(
        PygameEventUtils.middle_rect_click(wid, evtype=pygame.MOUSEBUTTONDOWN)
    )
    assert not wid.active
    assert (
        events.MENU_LAST_WIDGET_DISABLE_ACTIVE_STATE
        in menu_top.get_last_update_mode()[0]
    )

    # Test same effect but with touchbar
    menu._mouse_motion_selection = True
    menu._touchscreen = True
    menu._touchscreen_motion_selection = True
    wid.active = True
    menu_top.update(PygameEventUtils.middle_rect_click(wid, evtype=pygame.FINGERDOWN))
    assert not wid.active
    assert (
        events.MENU_LAST_WIDGET_DISABLE_ACTIVE_STATE
        in menu_top.get_last_update_mode()[0]
    )

    # Test mouseover and mouseleave
    test = [None]

    def on_over(m, e):
        """Handle menu mouse-over events."""
        assert isinstance(m, Menu)
        assert e.type == pygame.MOUSEMOTION
        test[0] = True  # type: ignore

    def on_leave(m, e):
        """Handle menu mouse-leave events."""
        assert isinstance(m, Menu)
        assert e.type == pygame.MOUSEMOTION
        test[0] = False  # type: ignore

    menu = MenuUtils.generic_menu(width=100, height=100)
    menu.set_onmouseover(on_over)
    menu.set_onmouseleave(on_leave)

    assert test[0] is None

    rect = menu.get_rect()
    menu.update(PygameEventUtils.mouse_motion(rect.center))

    ev = PygameEventUtils.mouse_motion((50, 50))
    menu.update(ev)

    assert test[0] is False

    rect = menu.get_rect()
    ev = PygameEventUtils.mouse_click(
        rect.centerx, rect.centery, inlist=True, evtype=pygame.MOUSEMOTION
    )
    menu.update(ev)
    assert test[0] is True
    assert menu._mouseover

    ev = PygameEventUtils.mouse_motion((50, 50))
    menu.update(ev)
    assert not menu._mouseover
    assert test[0] is False

    # Test empty parameters
    menu.set_onmouseover(lambda: None)
    menu.set_onmouseleave(lambda: None)

    menu.update(
        PygameEventUtils.mouse_click(50, 50, inlist=True, evtype=pygame.MOUSEMOTION)
    )
    menu.update(
        PygameEventUtils.mouse_click(
            rect.centerx, rect.centery, inlist=True, evtype=pygame.MOUSEMOTION
        )
    )
    menu.update(
        PygameEventUtils.mouse_click(50, 50, inlist=True, evtype=pygame.MOUSEMOTION)
    )

    # Test window mouseover and mouseleave
    test = [None]

    def on_over(m):
        """Handle window mouse-over events."""
        assert isinstance(m, Menu)
        test[0] = True  # type: ignore

    def on_leave(m):
        """Handle window mouse-leave events."""
        assert isinstance(m, Menu)
        test[0] = False  # type: ignore

    menu.set_onwindowmouseover(on_over)
    menu.set_onwindowmouseleave(on_leave)

    assert test[0] is None
    menu.update(PygameEventUtils.enter_window())
    assert test[0] is True
    menu.update(PygameEventUtils.leave_window())
    assert test[0] is False

    # Test empty parameters
    menu.set_onwindowmouseover(lambda: None)
    menu.set_onwindowmouseleave(lambda: None)

    menu.update(PygameEventUtils.enter_window())
    menu._mouseover = True
    menu.update(PygameEventUtils.leave_window())
    assert menu.get_last_update_mode()[0] == events.MENU_LAST_MOUSE_LEAVE_WINDOW

    menu.update([])
    assert menu.get_last_update_mode()[0] == events.MENU_LAST_NONE

    # Test if not enabled
    menu.disable()
    with pytest.raises(RuntimeError):
        menu.update([])

    menu.enable()
    menu._disable_update = True
    assert not menu.update([])
    menu._disable_update = False

    # Test scrollbars
    menu._scrollarea.update = lambda _: True
    assert menu.update([])
    assert menu.get_last_update_mode()[0] == events.MENU_LAST_SCROLL_AREA
    menu._scrollarea.update = lambda _: False

    # Test menubar
    menu._menubar.update = lambda _: True
    assert menu.update([])
    assert menu.get_last_update_mode()[0] == events.MENU_LAST_MENUBAR
    menu._menubar.update = lambda _: False

    # Test quit
    menu._disable_exit = True
    assert menu.update([pygame.event.Event(pygame.QUIT)])
    assert menu.get_last_update_mode()[0] == events.MENU_LAST_QUIT
    assert menu.update([pygame.event.Event(events.PYGAME_WINDOWCLOSE)])
    assert menu.get_last_update_mode()[0] == events.MENU_LAST_QUIT

    # Test menu close
    menu._onclose = lambda: None
    assert menu.update(PygameEventUtils.key(ctrl.KEY_CLOSE_MENU, keydown=True))
    assert menu.get_last_update_mode()[0] == events.MENU_LAST_MENU_CLOSE


def test_theme_params():
    """Test theme parameters affecting menu behavior."""
    th = TEST_THEME.copy()

    th.title = False
    menu = MenuUtils.generic_menu(theme=th)
    assert not menu.get_menubar().is_visible()

    th.title = True
    menu = MenuUtils.generic_menu(theme=th)
    assert menu.get_menubar().is_visible()

    th.title_updates_pygame_display = True
    menu = MenuUtils.generic_menu(theme=th, title="Epic")
    menu.draw(surface)
    assert pygame.display.get_caption()[0] == menu.get_title()


def test_widget_move_index():
    """Test moving widgets by index and reference."""
    menu = MenuUtils.generic_menu(theme=TEST_THEME.copy())
    btn1 = menu.add.button("1")
    btn2 = menu.add.button("2")
    btn3 = menu.add.button("3")

    def test_order(buttons, selected):
        """Assert widget order and selection snapshot."""
        assert menu.get_selected_widget() == selected
        sel = [int(w == selected) for w in buttons]

        if PYGAME_V2:
            assert menu._test_widgets_status() == (
                (
                    (
                        "Button-" + buttons[0].get_title(),
                        (0, 0, 0, 291, 102, 17, 41, 291, 257, 291, 102),
                        (1, 0, sel[0], 1, 0, 0, 0),
                    ),
                    (
                        "Button-" + buttons[1].get_title(),
                        (0, 1, 1, 291, 153, 17, 41, 291, 308, 291, 153),
                        (1, 0, sel[1], 1, 0, 0, 0),
                    ),
                    (
                        "Button-" + buttons[2].get_title(),
                        (0, 2, 2, 291, 204, 17, 41, 291, 359, 291, 204),
                        (1, 0, sel[2], 1, 0, 0, 0),
                    ),
                )
            )
        else:
            assert menu._test_widgets_status() == (
                (
                    (
                        "Button-" + buttons[0].get_title(),
                        (0, 0, 0, 291, 100, 17, 42, 291, 255, 291, 100),
                        (1, 0, sel[0], 1, 0, 0, 0),
                    ),
                    (
                        "Button-" + buttons[1].get_title(),
                        (0, 1, 1, 291, 152, 17, 42, 291, 307, 291, 152),
                        (1, 0, sel[1], 1, 0, 0, 0),
                    ),
                    (
                        "Button-" + buttons[2].get_title(),
                        (0, 2, 2, 291, 204, 17, 42, 291, 359, 291, 204),
                        (1, 0, sel[2], 1, 0, 0, 0),
                    ),
                )
            )

    test_order((btn1, btn2, btn3), btn1)
    menu.move_widget_index(btn1)
    test_order((btn2, btn3, btn1), btn1)
    menu.move_widget_index(btn3, 0)
    test_order((btn3, btn2, btn1), btn1)
    menu.move_widget_index(btn2, btn1)
    test_order((btn3, btn1, btn2), btn1)

    with pytest.raises(AssertionError):
        menu.move_widget_index(btn2, btn2)

    menu.move_widget_index(btn1, btn2)
    test_order((btn3, btn2, btn1), btn1)

    menu.move_widget_index(None)
    test_order((btn1, btn2, btn3), btn1)

    menu.select_widget(btn2)
    test_order((btn1, btn2, btn3), btn2)

    menu.move_widget_index(None)
    assert menu.get_selected_widget() == btn2
    test_order((btn3, btn2, btn1), btn2)

    menu.move_widget_index(btn1, 0)
    with pytest.raises(AssertionError):
        menu.move_widget_index(btn1, -1)
    with pytest.raises(AssertionError):
        menu.move_widget_index(btn1, -1.5)  # type: ignore
    test_order((btn1, btn3, btn2), btn2)


def test_mouseover_widget():
    """Test mouseover and mouseleave callbacks."""
    menu = MenuUtils.generic_menu()
    btn1 = menu.add.button("1", cursor=CURSOR_ARROW, button_id="b1")
    btn2 = menu.add.button("2", cursor=CURSOR_ARROW, button_id="b2")

    # Setup
    menu.select_widget("b2")
    assert menu.get_selected_widget() == btn2
    menu.select_widget("b1")
    assert btn1.is_selected()
    assert not menu._mouse_motion_selection

    test = [False, False, False, False]  # btn1over, btn1leave, btn2over, btn2leave

    def onover1(widget, _):
        """Handle mouse-over for first button."""
        assert widget == btn1
        test[0] = not test[0]

    def onleave1(widget, _):
        """Handle mouse-leave for first button."""
        assert widget == btn1
        test[1] = not test[1]

    def onover2(widget, _):
        """Handle mouse-over for second button."""
        assert widget == btn2
        test[2] = not test[2]

    def onleave2(widget, _):
        """Handle mouse-leave for second button."""
        assert widget == btn2
        test[3] = not test[3]

    btn1.set_onmouseover(onover1)
    btn1.set_onmouseleave(onleave1)
    btn2.set_onmouseover(onover2)
    btn2.set_onmouseleave(onleave2)

    btn1.set_cursor(CURSOR_HAND)
    btn2.set_cursor(CURSOR_CROSSHAIR)

    # Test before
    assert test == [False, False, False, False]

    reset_widgets_over()
    assert WIDGET_MOUSEOVER == [None, []]

    # Get cursors
    cur_none = get_cursor()
    if cur_none is None:
        return

    set_pygame_cursor(btn1._cursor)
    cur1 = get_cursor()

    set_pygame_cursor(btn2._cursor)
    cur2 = get_cursor()

    set_pygame_cursor(cur_none)

    # Place mouse over widget 1, it should set as mouseover and trigger the events
    deco = menu.get_decorator()

    def draw_rect():
        """Paint a test rect over first button area."""
        surface.fill((255, 255, 255), btn1.get_rect(to_real_position=True))

    deco.add_callable(draw_rect, prev=False, pass_args=False)

    assert get_cursor() == cur_none
    menu.update(PygameEventUtils.mouse_motion(btn1))
    assert menu.get_selected_widget() == btn1
    assert test == [True, False, False, False]
    assert WIDGET_MOUSEOVER == [btn1, [btn1, cur_none, []]]
    assert get_cursor() == cur1

    # Place mouse away. This should force widget 1 mouseleave
    mouse_away_event = PygameEventUtils.middle_rect_click(
        (1000, 1000), evtype=pygame.MOUSEMOTION
    )
    menu.update(mouse_away_event)
    assert test == [True, True, False, False]
    assert WIDGET_MOUSEOVER == [None, []]
    assert get_cursor() == cur_none

    # Place over widget 2
    menu.update(PygameEventUtils.mouse_motion(btn2))
    assert test == [True, True, True, False]
    assert WIDGET_MOUSEOVER == [btn2, [btn2, cur_none, []]]
    assert get_cursor() == cur2

    # Place mouse away. This should force widget 1 mouseleave
    menu.update(mouse_away_event)
    assert test == [True, True, True, True]
    assert WIDGET_MOUSEOVER == [None, []]
    assert get_cursor() == cur_none

    # Test immediate switch, from 1 to 2, then from 2 to 1, then off
    test = [False, False, False, False]
    menu.update(PygameEventUtils.mouse_motion(btn1))
    assert menu.get_selected_widget() == btn1
    assert test == [True, False, False, False]
    assert WIDGET_MOUSEOVER == [btn1, [btn1, cur_none, []]]
    assert get_cursor() == cur1

    menu.update(PygameEventUtils.mouse_motion(btn2))
    assert test == [True, True, True, False]
    assert WIDGET_MOUSEOVER == [btn2, [btn2, cur_none, []]]
    assert get_cursor() == cur2

    menu.update(mouse_away_event)
    assert test == [True, True, True, True]
    assert WIDGET_MOUSEOVER == [None, []]
    assert get_cursor() == cur_none

    # Same switch test, but now with widget selection by mouse motion
    menu._mouse_motion_selection = True
    test = [False, False, False, False]
    menu.select_widget(btn2)
    assert menu.get_selected_widget() == btn2

    menu.update(PygameEventUtils.mouse_motion(btn1))
    assert menu.get_selected_widget() == btn1
    assert test == [True, False, False, False]
    assert WIDGET_MOUSEOVER == [btn1, [btn1, cur_none, []]]
    assert get_cursor() == cur1

    menu.update(PygameEventUtils.mouse_motion(btn2))
    assert menu.get_selected_widget() == btn2
    assert test == [True, True, True, False]
    assert WIDGET_MOUSEOVER == [btn2, [btn2, cur_none, []]]
    assert get_cursor() == cur2

    menu.update(mouse_away_event)
    assert test == [True, True, True, True]
    assert WIDGET_MOUSEOVER == [None, []]
    assert get_cursor() == cur_none
    assert menu.get_selected_widget() == btn2

    # Mouseover btn1, but then hide it
    menu._mouse_motion_selection = False
    test = [False, False, False, False]
    menu.update(PygameEventUtils.mouse_motion(btn1))
    assert test == [True, False, False, False]
    assert WIDGET_MOUSEOVER == [btn1, [btn1, cur_none, []]]
    assert get_cursor() == cur1

    btn1.hide()
    assert WIDGET_MOUSEOVER == [None, []]
    assert get_cursor() == cur_none

    # Test close
    menu.update(PygameEventUtils.mouse_motion(btn2))
    assert test == [True, True, True, False]
    assert WIDGET_MOUSEOVER == [btn2, [btn2, cur_none, []]]
    assert get_cursor() == cur2

    menu.disable()
    assert test == [True, True, True, True]
    assert WIDGET_MOUSEOVER == [None, []]
    assert get_cursor() == cur_none

    btn2.mouseleave(PygameEventUtils.mouse_motion(btn2))
    assert test == [True, True, True, True]
    assert WIDGET_MOUSEOVER == [None, []]
    assert get_cursor() == cur_none

    # Enable
    menu.enable()
    menu.update(PygameEventUtils.mouse_motion(btn2))
    assert test == [True, True, False, True]
    assert WIDGET_MOUSEOVER == [btn2, [btn2, cur_none, []]]
    assert get_cursor() == cur2

    # Move to hidden
    menu.update(PygameEventUtils.mouse_motion(btn1))
    assert test == [True, True, False, False]
    assert WIDGET_MOUSEOVER == [None, []]
    assert get_cursor() == cur_none

    # Unhide
    btn1.show()
    test = [False, False, False, False]
    prev_pos1 = PygameEventUtils.mouse_motion(btn1)
    menu.update(prev_pos1)
    assert test == [True, False, False, False]
    assert WIDGET_MOUSEOVER == [btn1, [btn1, cur_none, []]]

    # Move btn1 and btn2
    assert menu.get_widgets() == (btn1, btn2)
    menu.move_widget_index(btn1, btn2)
    assert menu.get_widgets() == (btn2, btn1)
    assert WIDGET_MOUSEOVER == [None, []]

    menu.update(prev_pos1)
    assert WIDGET_MOUSEOVER == [btn2, [btn2, cur_none, []]]

    # Remove btn2
    menu.remove_widget(btn2)
    assert WIDGET_MOUSEOVER == [None, []]

    # Select btn1
    menu.update(PygameEventUtils.mouse_motion(btn1))
    assert WIDGET_MOUSEOVER == [btn1, [btn1, cur_none, []]]
    assert get_cursor() == cur1

    # Change previous cursor to assert an error if mouseleave doesn't reset it
    assert cur_none == WIDGET_TOP_CURSOR[0]
    WIDGET_MOUSEOVER[1][1] = cur2
    menu.update(mouse_away_event)
    assert get_cursor() == cur_none


def test_floating_pos():
    """Test floating widget layout behavior."""
    menu = MenuUtils.generic_menu(theme=THEME_NON_FIXED_TITLE)
    btn = menu.add.button("floating")
    assert btn.get_alignment() == ALIGN_CENTER

    expc_pos = (247, 153) if PYGAME_V2 else (247, 152)
    assert btn.get_position() == expc_pos

    btn.set_float()
    assert btn.get_position() == expc_pos
    btn.set_float(menu_render=True)
    assert btn.get_position() == expc_pos

    menu = MenuUtils.generic_menu(columns=3, rows=[2, 2, 2])
    assert len(menu._column_widths) == 0
    for _ in range(6):
        menu.add.none_widget()
    assert menu._column_widths == [200, 200, 200]

    menu = MenuUtils.generic_menu(
        columns=3, rows=[2, 2, 2], column_min_width=[300, 100, 100]
    )
    assert len(menu._column_widths) == 0
    for _ in range(6):
        menu.add.none_widget()
    assert menu._column_widths == [360.0, 120.0, 120.0]

    menu = MenuUtils.generic_menu(
        columns=3, rows=[2, 2, 2], column_min_width=[600, 600, 600]
    )
    assert len(menu._column_widths) == 0
    for _ in range(6):
        menu.add.none_widget()
    assert menu._column_widths == [600, 600, 600]

    menu = MenuUtils.generic_menu(
        columns=3, rows=[2, 2, 2], column_max_width=[100, None, None]
    )
    assert len(menu._column_widths) == 0
    for _ in range(6):
        menu.add.none_widget()
    assert menu._column_widths == [100, 250, 250]


def test_surface_cache():
    """Test surface cache update flags."""
    menu = MenuUtils.generic_menu()
    assert not menu._widgets_surface_need_update
    menu.force_surface_cache_update()
    menu.force_surface_update()
    assert menu._widgets_surface_need_update


def test_baseimage_selector():
    """Test BaseImage selector integration with menu links."""
    if sys.version_info.major == 3 and sys.version_info.minor == 8:
        return

    x = 400
    y = 400

    class Sample:
        icons: list[BaseImage]
        icon: widgets.Image
        selector: widgets.Selector

        def __init__(self):
            """Build menus, icons, and selector callbacks."""
            theme = Theme(
                title_font_size=8,
                title_bar_style=widgets.MENUBAR_STYLE_SIMPLE,
                background_color=(116, 161, 122),
                title_background_color=(4, 47, 58),
                title_font_color=(38, 158, 151),
                widget_selection_effect=widgets.NoneSelection(),
            )

            self.main_menu = Menu(title="MAIN MENU", height=x, width=y, theme=theme)

            submenu1 = Menu(title="SUB MENU 1", height=x, width=y, theme=theme)
            submenu1.add.label("SUB MENU 1")

            submenu2 = Menu(title="SUB MENU 2", height=x, width=y, theme=theme)
            submenu2.add.label("SUB MENU 2")

            self.icons = [
                BaseImage(baseimage.IMAGE_EXAMPLE_PYGAME_MENU).resize(80, 80),
                BaseImage(baseimage.IMAGE_EXAMPLE_PYTHON).resize(80, 80),
            ]

            self.icon = self.main_menu.add.image(image_path=self.icons[0].copy())

            def update_icon(*args):
                """Update displayed icon from selector index."""
                icon_idx = args[0][-1]
                set_icon = self.icons[icon_idx].copy()
                set_icon.scale(2, 2)
                self.icon.set_image(set_icon)

            def open_menu(*args):
                """Open submenu linked to selector option."""
                sub = args[-1][0][1]
                sub.open()

            self.selector = self.main_menu.add.selector(
                "",
                [
                    ("Menu 1", self.main_menu.add.menu_link(submenu1)),
                    ("Menu 2", self.main_menu.add.menu_link(submenu2)),
                ],
                onchange=update_icon,
                onreturn=open_menu,
            )
            self.selector.change()

    s = Sample()
    s.main_menu.draw(surface)

    assert s.icon.get_size() == (176, 168)
    assert s.main_menu.get_title() == "MAIN MENU"

    s.selector.apply()
    assert s.icon.get_size() == (176, 168)
    assert s.main_menu.get_current().get_title() == "SUB MENU 1"

    s.selector._left()
    s.selector.apply()
    assert s.icon.get_size() == (176, 168)
    assert s.main_menu.get_current().get_title() == "SUB MENU 2"


def test_resize():
    """Test menu resize behavior."""
    theme = THEME_DEFAULT.copy()
    menu = MenuUtils.generic_menu(theme=theme)
    assert menu.get_size() == (600, 400)

    # Disable auto centering depending on the case
    menu._auto_centering = True
    theme.widget_offset = (0, 10)
    menu.resize(300, 300)
    assert not menu._auto_centering
    theme.widget_offset = (0, 0)

    menu._auto_centering = True
    theme.scrollarea_outer_margin = (0, 10)
    menu.resize(300, 300)
    assert not menu._auto_centering
    theme.widget_offset = (0, 0)

    # Test resize
    menu = MenuUtils.generic_menu(theme=theme, column_max_width=[0])
    assert menu._column_max_width_zero == [True]
    assert menu._column_max_width == [600]
    assert menu._menubar._width == 600
    assert not menu._widgets_surface_need_update
    menu.resize(300, 300)
    assert not menu._widgets_surface_need_update
    assert menu.get_size() == (300, 300)
    assert menu._column_max_width == [300]
    assert menu._menubar._width == 300

    # Render
    assert menu._widgets_surface is None
    menu.render()
    assert menu._widgets_surface is not None
    menu.resize(200, 200)
    assert menu._widgets_surface_need_update

    # Add button to resize
    menu = MenuUtils.generic_menu()

    def _resize():
        """Toggle menu width between two presets."""
        if menu.get_size()[0] == 300:
            menu.resize(600, 400)
        else:
            menu.resize(300, 300)

    btn = menu.add.button("Resize", _resize)
    assert menu.get_size()[0] == 600
    btn.apply()
    assert menu.get_size()[0] == 300

    # Resize with another surface size
    menu.resize(300, 300, (500, 500))

    # Invalid size
    with pytest.raises(ValueError):
        menu.resize(50, 10)

    # Resize but using position absolute
    menu.resize(400, 400, position=(50, 50))
    assert menu._position_relative
    assert menu._position == (100, 100)
    menu.resize(400, 400, position=(50, 50, False))
    assert not menu._position_relative
    assert menu._position == (50, 50)

    # Resize, hide scrollbars
    theme = THEME_DEFAULT.copy()
    menu = MenuUtils.generic_menu(theme=theme)
    for i in range(8):
        menu.add.button(i, bool)
    sa = menu.get_scrollarea()

    # Test with force
    assert sa.get_size(inner=True) == (580, 400)
    sa.hide_scrollbars(ORIENTATION_VERTICAL)
    assert sa.get_size(inner=True) == (600, 400)
    sa.show_scrollbars(ORIENTATION_VERTICAL)
    assert sa.get_size(inner=True) == (580, 400)

    # Disable force, this will not affect menu as after resizing the scrollbars
    # will re-show again
    sa.hide_scrollbars(ORIENTATION_VERTICAL, force=False)
    assert sa.get_size(inner=True) == (580, 400)
    sa.show_scrollbars(ORIENTATION_VERTICAL, force=False)
    assert sa.get_size(inner=True) == (580, 400)

    # Test submenu recursive resizing
    menu = MenuUtils.generic_menu(theme=theme)
    menu2 = MenuUtils.generic_menu(theme=theme)
    menu3 = MenuUtils.generic_menu(theme=theme)
    menu.add.button("btn", menu2)
    menu2.add.button("btn", menu3)
    assert menu.get_submenus(True) == (menu2, menu3)
    for m in (menu, menu2, menu3):
        assert m.get_size() == (600, 400)
    menu.resize(300, 300, recursive=True)  # Now, resize
    for m in (menu, menu2, menu3):
        assert m.get_size() == (300, 300)


def test_get_size():
    """Test menu size getters and border size calculation."""
    theme = THEME_DEFAULT.copy()
    menu = MenuUtils.generic_menu(theme=theme)
    assert menu.get_size() == (600, 400)

    for scale in [(1, 1), (2, 5), (5, 2)]:
        theme.border_color = BaseImage(baseimage.IMAGE_EXAMPLE_TILED_BORDER)
        theme.border_color.scale(*scale)
        border_size = theme.border_color.get_size()
        menu = MenuUtils.generic_menu(theme=theme)
        assert menu.get_size() == (600, 400)
        assert menu.get_size(border=True) == (
            600 + 2 * border_size[0] / 3,
            400 + 2 * border_size[1] / 3,
        )

    theme.border_width = 10
    theme.border_color = "red"
    menu = MenuUtils.generic_menu(theme=theme)
    assert menu.get_size(border=True) == (600 + 20, 400 + 20)

    theme.border_width = 10
    theme.border_color = None
    menu = MenuUtils.generic_menu(theme=theme)
    assert menu.get_size(border=True) == (600, 400)

    theme = THEME_BLUE.copy()
    theme.title = False
    theme.scrollarea_position = SCROLLAREA_POSITION_NONE
    theme.widget_selection_effect = widgets.LeftArrowSelection(arrow_right_margin=50)

    menu = Menu("Welcome", 200, 200, theme=theme)
    menu.add.button("Play")
    menu.add.button("Quit", events.EXIT)
    size = menu.get_size(widget=True)
    assert size == (136, 98)
    assert menu.resize(*size).get_size() == size


def test_border_color():
    """Test menu border color and image border handling."""
    theme = THEME_DEFAULT.copy()
    assert theme.border_color is None
    theme.border_width = 10
    theme.title_font_size = 15

    theme.border_color = "invalid"
    with pytest.raises(ValueError):
        Menu("Menu with border color", 250, 250, theme=theme)

    theme.border_color = "red"
    menu = Menu("Menu with border color", 250, 250, theme=theme)
    menu.draw(surface)

    theme.border_color = BaseImage(baseimage.IMAGE_EXAMPLE_TILED_BORDER)
    menu = Menu("Menu with border image", 250, 250, theme=theme)
    menu.draw(surface)


def test_menu_render_toggle():
    """Test render toggling performance behavior."""
    menu = MenuUtils.generic_menu(columns=3, rows=50)
    nc, nr = menu.get_col_rows()
    assert nc == 3
    assert nr == [50, 50, 50]

    # Test with rendering enabled
    n = sum(nr)  # Number of widgets to be added
    t0 = time.time()
    wdt = []  # Widgets
    for i in range(n):
        wdt.append(menu.add.label(i))
    t_on = time.time() - t0

    position_before = [w.get_position() for w in wdt]

    # Test with rendering disabled
    menu.clear()
    wdt.clear()
    menu.disable_render()
    t0 = time.time()
    for i in range(n):
        wdt.append(menu.add.label(i))
    menu.enable_render()
    menu.render()
    t_off = time.time() - t0

    assert t_on > t_off

    # Position after render must be equal!
    for i in range(n):
        assert position_before[i] == wdt[i].get_position()
    print(f'Render on: {t_on}s, off: {t_off}s')


def test_menu_widget_selected_events():
    """Test event forwarding to selected widget."""
    menu = MenuUtils.generic_menu()
    age = menu.add.text_input("Character age:")
    name = menu.add.text_input("Character name:")

    menu.update(PygameEventUtils.key(pygame.K_a, keydown=True, char="a"))
    assert age.is_selected()
    assert not name.is_selected()
    assert age.get_value() == "a"
    assert name.get_value() == ""

    menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
    assert not age.is_selected()
    assert name.is_selected()

    # Now, disable global widget selected event
    menu._widget_selected_update = False
    menu.update(PygameEventUtils.key(pygame.K_a, keydown=True, char="a"))
    assert name.get_value() == ""

    # Re-enable global widget selected event
    menu._widget_selected_update = True
    menu.update(PygameEventUtils.key(pygame.K_a, keydown=True, char="a"))
    assert name.get_value() == "a"

    # Disable local widget accept event
    name.receive_menu_update_events = False
    menu.update(PygameEventUtils.key(pygame.K_a, keydown=True, char="a"))
    assert name.get_value() == "a"

    # Enable local widget accept event
    name.receive_menu_update_events = True
    menu.update(PygameEventUtils.key(pygame.K_s, keydown=True, char="s"))
    assert name.get_value() == "as"


def test_subsurface_offset():
    """Test subsurface offset handling for draw and update."""
    main_surface = surface
    w, h = surface.get_size()
    left_surf_w = 300
    menu_w, menu_h = w - left_surf_w, h
    menu_surface = main_surface.subsurface((300, 0, menu_w, menu_h))

    menu = MenuUtils.generic_menu(
        title="Subsurface",
        width=menu_w,
        height=menu_h,
        position_x=0,
        position_y=0,
        mouse_motion_selection=True,
        surface=menu_surface,
    )

    btn_click = [False]

    def btn():
        """Mark subsurface button callback as executed."""
        btn_click[0] = True

    b1 = menu.add.button("Button", btn)
    menu._surface = None
    assert menu.get_last_surface_offset() == (0, 0)
    assert b1.get_rect(to_real_position=True).x == 94
    assert menu._surface_last is None

    menu._surface = menu_surface
    assert menu.get_last_surface_offset() == (300, 0)
    r = b1.get_rect(to_real_position=True)
    assert r.x == 394
    assert menu._surface_last is None

    menu.draw()
    assert menu._surface_last == menu_surface

    menu.draw(surface)
    assert menu._surface_last == surface

    menu._surface = surface
    assert menu.get_last_surface_offset() == (0, 0)
    surface.fill((0, 0, 0))

    menu._surface = menu_surface
    assert not btn_click[0]
    menu.update(PygameEventUtils.middle_rect_click(r))
    assert btn_click[0]

    menu.mainloop(disable_loop=True)
    assert menu._surface_last == menu_surface


def test_inheritance():
    """Test Menu inheritance behavior."""

    class SubMenu(Menu):
        def __init__(self):
            """Initialize inherited menu with one submenu button."""
            super().__init__(
                title="Test",
                width=150,
                height=200,
                theme=THEME_DARK.copy(),
            )
            help_menu = MenuUtils.generic_menu()
            self.add.button(help_menu.get_title(), help_menu)
            self.enable()

    assert len(SubMenu().get_widgets()) == 1
    main_menu = SubMenu()
    test_menu = Menu("test", 500, 400)
    assert main_menu.add.menu_link(test_menu).get_menu() == main_menu


def test_selection():
    """Test selection persistence between linked menus."""
    menu = MenuUtils.generic_menu()
    sub = MenuUtils.generic_menu()
    sub2 = MenuUtils.generic_menu()

    # Add "sub" as a link within "menu"
    sub_link = menu.add.menu_link(sub)
    btn_back = sub.add.button("Back", events.BACK)

    # Add "sub2" as a link within "sub"
    sub2_link = sub.add.menu_link(sub2)
    btn_back_2 = sub2.add.button("Back", events.BACK)

    btn = menu.add.button("No-op Button")
    btn2 = menu.add.button("Sub", sub_link.open)
    btn3 = sub.add.button("Sub2", sub2_link.open)

    menu.render()
    assert menu.get_selected_widget() == btn

    # Now, we test selection preservation on return. By default, menu does not
    # keep previous selection. So, selecting widget 2 (that opens the new menu
    # sub2), and moving back, the index should be 0
    menu.select_widget(btn2).get_selected_widget().apply()
    assert menu.get_current() == sub
    assert menu.get_current().get_selected_widget() == btn_back

    menu.get_current().select_widget(btn3).get_selected_widget().apply()
    btn_back_2.apply()
    assert menu.get_current().get_selected_widget() == btn_back

    # Now we select the btn3 and apply
    menu.get_current()._remember_selection = True
    menu.get_current().select_widget(btn3).get_selected_widget().apply()
    btn_back_2.apply()
    assert menu.get_current().get_selected_widget() == btn3

    # Disable the feature, and now see what happens if trying to select first index if menu is empty
    menu.get_current()._remember_selection = True
    btn3.apply()
    assert menu.get_current() == sub2

    sub.clear(reset=False)
    assert menu.get_current() == sub2
