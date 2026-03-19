"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - FRAME
Test Frame. Frame is the most complex widget as this interacts with menu, modifies
its layout and contains other widgets.
"""

import pygame
import pytest

import pygame_menu
import pygame_menu.controls as ctrl
from pygame_menu.locals import (
    ALIGN_CENTER,
    ALIGN_RIGHT,
    ORIENTATION_HORIZONTAL,
    ORIENTATION_VERTICAL,
    POSITION_CENTER,
    POSITION_SOUTH,
    POSITION_SOUTHEAST,
)
from pygame_menu.utils import get_cursor, set_pygame_cursor
from pygame_menu.widgets import Button
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented
# noinspection PyProtectedMember
from pygame_menu.widgets.widget.frame import (
    _FrameDoNotAcceptScrollarea,
    _FrameSizeException,
)
from test._utils import (
    PYGAME_V2,
    TEST_THEME,
    THEME_NON_FIXED_TITLE,
    MenuUtils,
    PygameEventUtils,
    WIDGET_MOUSEOVER,
    reset_widgets_over,
    surface,
)


@pytest.fixture
def menu():
    """Create a generic menu fixture configured with the test theme."""
    return MenuUtils.generic_menu(theme=TEST_THEME.copy())


@pytest.fixture
def scroll_menu():
    """Create a scrollable menu fixture using a non-fixed title theme."""
    return MenuUtils.generic_menu(theme=THEME_NON_FIXED_TITLE)


def test_frame_general_layout_and_packing(menu):
    """Test frame layout, packing, and widget/frame relationship updates."""
    menu.add.button("rr")

    frame = menu.add.frame_h(250, 100, background_color=(200, 0, 0))
    frame._pack_margin_warning = False
    btn = menu.add.button("nice1")
    menu.add.button("44")

    frame2 = menu.add.frame_v(50, 250, background_color=(0, 0, 200))
    frame2._pack_margin_warning = False
    btn2 = menu.add.button("nice2")
    btn3 = menu.add.button("nice3")

    frame11 = menu.add.frame_v(50, 90, background_color=(0, 200, 0))
    frame11._pack_margin_warning = False
    btn11 = menu.add.button("11")
    btn12 = menu.add.button("12")

    frame11.pack(btn11)
    frame11.pack(btn12)

    frame.pack(btn)
    frame.pack(btn2, ALIGN_CENTER, vertical_position=POSITION_CENTER)
    frame.pack(frame11, ALIGN_RIGHT, vertical_position=POSITION_SOUTH)

    frame2.pack(menu.add.button("1"))
    frame2.pack(menu.add.button("2"), align=ALIGN_CENTER)
    frame2.pack(menu.add.button("3"), align=ALIGN_RIGHT)

    for f in (frame, frame2):
        for w in f.get_widgets():
            w.get_selection_effect().zero_margin()

    menu.render()
    wid = menu.get_widgets()

    # Key index checks
    assert wid[0].get_col_row_index() == (0, 0, 0)
    assert wid[1].get_col_row_index() == (0, 1, 1)
    assert wid[7].get_col_row_index() == (0, 2, 7)
    assert wid[12].get_col_row_index() == (0, 4, 12)

    # Relationship logic
    assert btn3.get_frame() is None
    assert btn2.get_frame() == frame
    assert btn2.get_translate() == (0, 0)
    assert not btn2.is_floating()

    menu.remove_widget(btn2)
    assert btn2.get_frame() is None
    assert btn2.get_translate(virtual=True) == (0, 0)
    assert btn2.is_floating()


@pytest.mark.parametrize(
    "child_size",
    [
        (100, 400),  # too tall
        (400, 10),  # too wide
    ],
)
def test_frame_size_exceptions(menu, child_size):
    frame_numbers = menu.add.frame_h(250, 42, frame_id="frame_numbers")
    w, h = child_size
    with pytest.raises(_FrameSizeException):
        frame_numbers.pack(menu.add.frame_v(w, h))


def test_frame_size_relax(menu):
    frame_numbers = menu.add.frame_h(250, 42)
    frame_numbers.relax()
    frame_numbers.pack(menu.add.frame_v(10, 10), align=ALIGN_CENTER)
    frame_numbers.pack(menu.add.frame_v(10, 10), align=ALIGN_RIGHT)
    frame_numbers.pack(menu.add.frame_v(10, 10))


@pytest.mark.parametrize(
    "method,args",
    [
        ("rotate", (10,)),
        ("scale", (100, 100)),
        ("flip", (True, True)),
        ("set_max_width", (100,)),
        ("set_max_height", (100,)),
    ],
)
def test_frame_unsupported_transformations(menu, method, args):
    wid = menu.add.frame_v(400, 100)
    with pytest.raises(WidgetTransformationNotImplemented):
        getattr(wid, method)(*args)


def test_frame_resize_no_transform(menu):
    """Test frame resize and translation without enabling transform flags."""
    wid = menu.add.frame_v(400, 100)
    wid.set_position(1, 1)
    assert wid.get_position() == (1, 1)

    wid.translate(1, 1)
    assert wid.get_translate() == (1, 1)

    wid.resize(10, 10)
    # Only assert that resize did not enable transform flags
    assert not wid._scale[0]


def test_frame_value_behavior(menu):
    """Test frame value API behavior."""
    f = menu.add.frame_v(300, 800)
    with pytest.raises(ValueError):
        f.get_value()
    with pytest.raises(ValueError):
        f.set_value("value")
    assert not f.value_changed()
    f.reset_value()


def test_frame_draw_callbacks(menu):
    """Test frame draw callback registration and removal."""
    frame = menu.add.frame_v(200, 200)
    flag = {"called": False}

    def cb(*_):
        """Mark draw callback as executed."""
        flag["called"] = True

    cid = frame.add_draw_callback(cb)
    frame.draw(surface)
    assert flag["called"]

    flag["called"] = False
    frame.remove_draw_callback(cid)
    frame.draw(surface)
    assert not flag["called"]

    frame._draw(surface)
    frame.update([])


def test_frame_clear_and_floating(menu):
    """Test frame clear and floating-state restoration after removal."""
    f = menu.add.frame_v(200, 200)
    b1 = f.pack(menu.add.button("A"))
    b2 = f.pack(menu.add.button("B"))

    f.clear()
    assert f.get_widgets() == ()

    menu.remove_widget(f)
    assert b1.is_floating()
    assert b2.is_floating()
    assert b1.get_frame() is None
    assert b2.get_frame() is None
    assert b1.get_translate(virtual=True) == (0, 0)
    assert b2.get_translate(virtual=True) == (0, 0)


def test_frame_contains_widget(menu):
    """Test frame contains-widget checks and packing preconditions."""
    h = menu.add.frame_h(400, 300)
    btn = pygame_menu.widgets.Button("button")

    with pytest.raises(AssertionError):
        h.pack(btn)

    menu.add.configure_defaults_widget(btn)
    h.pack(btn)
    h.pack(menu.add.button("legit"))
    assert h.contains_widget(btn)


def test_mouseover_events_and_cursor(menu):
    """Test frame and child mouseover callbacks and cursor updates."""
    from pygame_menu.locals import CURSOR_HAND as HAND

    reset_widgets_over()

    f1 = menu.add.frame_v(500, 500, background_color="red", cursor=HAND)
    f2 = menu.add.frame_v(400, 300, background_color="blue", cursor=HAND)
    b1 = f1.pack(menu.add.button("1"))

    events = {"f1": False, "f2": False, "b1": False}

    def toggle(k):
        """Create a callback that toggles mouseover state flags."""

        def cb(_, __):
            """Toggle the tracked mouseover flag for a widget key."""
            events[k] = not events[k]

        return cb

    for key, widget in zip(["f1", "f2", "b1"], [f1, f2, b1]):
        widget.set_onmouseover(toggle(key))
        widget.set_onmouseleave(toggle(key))

    menu.update(PygameEventUtils.topleft_rect_mouse_motion(f1))
    assert events["f1"]

    menu.update(PygameEventUtils.topleft_rect_mouse_motion(b1))
    assert events["b1"]

    cur = get_cursor()
    # Just sanity‑check that a cursor object is set
    assert cur is not None


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_width": 400},
        {"max_height": 500},
        {"max_height": -1},
    ],
)
def test_scrollarea_invalid_constraints(scroll_menu, kwargs):
    """Test invalid scrollable frame constraints raise assertions."""
    with pytest.raises(AssertionError):
        scroll_menu.add.frame_v(300, 400, **kwargs)


def test_scrollarea_creation_and_disable(scroll_menu):
    """Test scrollarea creation and disabled-scrollarea protection."""
    f = scroll_menu.add.frame_v(300, 800, frame_id="f1")

    def create():
        """Build a scrollarea with explicit scrollbar and style settings."""
        return f.make_scrollarea(
            200,
            300,
            "red",
            "white",
            None,
            True,
            "red",
            1,
            POSITION_SOUTHEAST,
            "yellow",
            "green",
            0,
            20,
            pygame_menu._scrollarea.get_scrollbars_from_position(POSITION_SOUTHEAST),
        )

    create()

    f._accepts_scrollarea = False
    with pytest.raises(_FrameDoNotAcceptScrollarea):
        create()

    f._accepts_scrollarea = True
    f._has_title = True
    f.make_scrollarea(
        None,
        None,
        "red",
        "white",
        None,
        True,
        "red",
        1,
        POSITION_SOUTHEAST,
        "yellow",
        "green",
        0,
        20,
        pygame_menu._scrollarea.get_scrollbars_from_position(POSITION_SOUTHEAST),
    )

    sa = f._frame_scrollarea
    f.set_scrollarea(sa)


def test_scrollarea_structure(scroll_menu):
    """Test frame scrollarea parent-child structure and widget bindings."""
    img = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU)

    frame_sc = scroll_menu.add.frame_v(
        300, 400, max_height=200, background_color=img, frame_id="frame_sc"
    )
    frame_scroll = frame_sc.get_scrollarea(inner=True)

    frame2 = scroll_menu.add.frame_v(
        400, 200, background_color=(30, 30, 30), padding=25
    )
    scroll_menu.add.frame_v(300, 200, background_color=(255, 255, 0))

    btn_frame21 = frame2.pack(scroll_menu.add.button("A"))
    frame2.pack(scroll_menu.add.button("B"))
    btns = [
        frame_sc.pack(scroll_menu.add.button(f"Nice{i}", padding=10))
        for i in range(1, 6)
    ]
    btn_real = scroll_menu.add.button("Real", background_color=(255, 0, 255))

    assert frame_sc.is_scrollable
    assert not frame2.is_scrollable
    assert btns[0].get_frame() == frame_sc
    assert btns[0].get_scrollarea() == frame_scroll
    assert btn_real.get_frame() is None
    assert btn_real.get_scrollarea() == scroll_menu.get_scrollarea()
    assert btn_frame21.get_frame() == frame2
    assert frame_scroll.get_parent() == scroll_menu.get_scrollarea()


def test_scroll_value_logic(scroll_menu):
    """Test scroll value updates after keyboard navigation in scrollable frames."""
    if not PYGAME_V2:
        pytest.skip("Requires PYGAME_V2")

    frame_sc = scroll_menu.add.frame_v(300, 400, max_height=200)
    frame_scroll = frame_sc.get_scrollarea(inner=True)
    frame2 = scroll_menu.add.frame_v(400, 200)

    btn_f2 = frame2.pack(scroll_menu.add.button("F2"))
    for i in range(5):
        frame_sc.pack(scroll_menu.add.button(f"Nice{i}"))
    scroll_menu.add.button("Real")

    scroll_menu.render()
    assert scroll_menu.get_selected_widget() == btn_f2

    scroll_menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))

    assert frame_scroll.get_scroll_value_percentage(ORIENTATION_VERTICAL) >= 0
    assert (
        scroll_menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_HORIZONTAL)
        == -1
    )


def test_widget_clipping(scroll_menu):
    """Test widget clipping position changes while scrolling."""
    frame_sc = scroll_menu.add.frame_v(300, 400, max_height=200)
    frame_scroll = frame_sc.get_scrollarea(inner=True)
    btn = frame_sc.pack(scroll_menu.add.button("Target"))

    scroll_menu.render()
    r0 = btn.get_rect(to_real_position=True)

    frame_scroll.scroll_to(ORIENTATION_VERTICAL, 0.5)
    r1 = btn.get_rect(to_real_position=True)

    assert r0 != r1


def test_text_input_scroll_overflow(scroll_menu):
    """Test text input behavior and overflow handling inside scrollable frames."""
    frame_sc = scroll_menu.add.frame_v(300, 400, max_height=200)
    text = frame_sc.pack(scroll_menu.add.text_input("text: "))

    scroll_menu.select_widget(text)
    assert not text.active

    scroll_menu.update(PygameEventUtils.key(pygame.K_a, char="a", keydown=True))
    assert text.active
    assert text.get_value() == "a"

    with pytest.raises(_FrameSizeException):
        for _ in range(50):
            text.set_value(text.get_value() + "overflow")
        scroll_menu.render()


def test_multiple_selection_error(scroll_menu):
    """Test multiple selected widgets trigger render-time exception."""
    btn1 = scroll_menu.add.button("B1")
    btn2 = scroll_menu.add.button("B2")

    btn1.select()
    btn2.select()

    with pytest.raises(pygame_menu.menu._MenuMultipleSelectedWidgetsException):
        scroll_menu.render()


def test_frame_sorting_and_indices(menu):
    """Test menu widget sorting and index ranges while packing frames."""
    b0 = menu.add.button("b0")
    b1 = menu.add.button("b1")
    b2 = menu.add.button("b2")
    b3 = menu.add.button("b3")
    f1 = menu.add.frame_v(300, 800, frame_id="f1")
    f2 = menu.add.frame_v(200, 500, frame_id="f2")

    assert menu._widgets == [b0, b1, b2, b3, f1, f2]

    f1.pack(b1)
    assert menu._widgets == [b0, b2, b3, f1, b1, f2]

    f2.pack(b3)
    assert menu._widgets == [b0, b2, f1, b1, f2, b3]

    f1.pack(b2)
    assert menu._widgets == [b0, f1, b1, b2, f2, b3]

    f1.pack(f2)
    assert menu._widgets == [b0, f1, b1, b2, f2, b3]

    b4 = menu.add.button("b4")
    b5 = menu.add.button("b5")

    assert f1.get_indices() == (2, 4)
    assert f2.get_indices() == (5, 5)

    f2.pack(b5)
    assert menu._widgets == [b0, f1, b1, b2, f2, b3, b5, b4]


def test_recursive_frames(menu):
    """Test recursive frame nesting and parent linkage."""
    f_rec = []
    n = 10
    for i in range(n):
        f_rec.append(menu.add.frame_v(100, 100, frame_id=f"f_rec{i}"))
        f_rec[i].relax()
        if i > 0:
            f_rec[i - 1].pack(f_rec[i])

    for i in range(n):
        assert f_rec[i].get_indices() == (-1, -1)
        assert f_rec[i].get_frame() == (None if i == 0 else f_rec[i - 1])


def test_deeply_nested_scrollareas(menu):
    """Test deeply nested frames and inherited scrollarea behavior."""
    f1 = menu.add.frame_v(450, 400, background_color=(0, 0, 255))
    f2 = menu.add.frame_v(400, 400, max_height=300, background_color=(255, 0, 0))
    f3 = menu.add.frame_v(350, 400, max_height=200, background_color=(0, 255, 0))
    f4 = menu.add.frame_v(300, 400, max_height=100, background_color=(0, 255, 255))

    b1 = f1.pack(menu.add.button("b1"))
    f2.pack(menu.add.button("b2"))
    f3.pack(menu.add.button("b3"))
    b4 = f4.pack(menu.add.button("b4"))

    f1.pack(f2)
    f2.pack(f3)
    f3.pack(f4)

    b5 = menu.add.button("b5")

    assert b4.get_frame_depth() == 4
    assert b5.get_frame_depth() == 0

    s1 = f2.get_scrollarea(inner=True)
    s2 = f3.get_scrollarea(inner=True)

    assert f3.get_scrollarea() == s1
    assert f4.get_scrollarea() == s2
    assert s2.get_depth() == 2

    f1.hide()
    assert not b1.is_visible()
    assert not b4.is_visible()
    assert b5.is_visible()

    f1.show()
    assert b4.is_visible()


def test_title_height_and_drag(menu):
    """Test frame title height impact and draggable title support."""
    frame = menu.add.frame_v(300, 200)
    initial_h = frame.get_height()

    frame.set_title("Modern Title", title_font_size=20)
    assert frame.get_height() > initial_h

    # Draggable flag should be accepted without error
    frame.set_title("Draggable", draggable=True)


def test_resize_with_scrollable_constraints(menu):
    """Test frame resize behavior with and without scroll constraints."""
    frame = menu.add.frame_v(300, 200)
    frame.resize(400, 400)
    assert frame.get_size() == (400, 400)

    frame_scroll = menu.add.frame_v(300, 200, max_width=200, max_height=100)
    assert frame_scroll.is_scrollable

    # Modern behavior: resize with new max_* does not raise
    frame_scroll.resize(400, 400, max_width=300, max_height=200)
    assert frame_scroll.is_scrollable

    # Title-aware resizing
    frame.set_title("Title")
    frame.resize(600, 600)
    expected_h = 600 + (41 if PYGAME_V2 else 42)
    assert abs(frame.get_height() - expected_h) <= 1


def test_pack_columns():
    """Test frame packing and indices across menu columns."""
    menu = pygame_menu.Menu(columns=2, rows=1, height=500, width=600, title="Title")

    frame = menu.add.frame_h(width=250, height=100)
    label_inner = menu.add.label("Col One")
    frame.pack(label_inner)

    label_outer = menu.add.label("Col Two")

    assert frame.get_col_row_index() == (0, 0, 0)
    assert label_inner.get_col_row_index() == (0, 0, 1)
    assert label_outer.get_col_row_index() == (1, 0, 2)
    assert label_inner.get_frame() == frame


def test_sort():
    """Test frame sorting."""
    menu = MenuUtils.generic_menu()
    b0 = menu.add.button('b0')
    b1 = menu.add.button('b1')
    b2 = menu.add.button('b2')
    b3 = menu.add.button('b3')
    f1 = menu.add.frame_v(300, 800, frame_id='f1')
    f2 = menu.add.frame_v(200, 500, frame_id='f2')

    # Test basics
    assert f1.get_size() == (300, 800)
    assert f2.get_size() == (200, 500)
    assert menu._widgets == [b0, b1, b2, b3, f1, f2]
    f1.pack(b1)
    assert b1.get_frame() == f1
    assert menu._widgets == [b0, b2, b3, f1, b1, f2]
    f2.pack(b3)
    assert menu._widgets == [b0, b2, f1, b1, f2, b3]
    f1.pack(b2)
    assert menu._widgets == [b0, f1, b1, b2, f2, b3]
    f1.pack(f2)
    assert menu._widgets == [b0, f1, b1, b2, f2, b3]
    assert menu.get_selected_widget() == b0

    # Add two more buttons
    b4 = menu.add.button('b4')
    assert menu._widgets == [b0, f1, b1, b2, f2, b3, b4]
    b5 = menu.add.button('b5')
    assert menu._widgets == [b0, f1, b1, b2, f2, b3, b4, b5]

    # Test positioning
    assert f1.get_indices() == (2, 4)
    assert f2.get_indices() == (5, 5)
    f2.pack(b5)
    assert menu._widgets == [b0, f1, b1, b2, f2, b3, b5, b4]
    f1.pack(b0)
    assert menu.get_selected_widget() == b0
    assert menu._widgets == [f1, b1, b2, f2, b3, b5, b0, b4]
    f1.pack(b4)
    assert menu._widgets == [f1, b1, b2, f2, b3, b5, b0, b4]
    with pytest.raises(AssertionError):
        f1.pack(b4)
    with pytest.raises(AssertionError):
        f1.pack(b3)
    assert f2.get_frame() == f1
    assert f2.get_frame_depth() == 1
    assert b3.get_frame() == f2
    assert b3.get_frame_depth() == 2
    assert f1.get_indices() == (1, 7)
    assert f2.get_indices() == (4, 5)

    # Unpack f2
    f1.unpack(f2)
    assert menu._widgets == [f1, b1, b2, b0, b4, f2, b3, b5]
    assert f1.get_indices() == (1, 4)
    assert f2.get_indices() == (6, 7)

    # Create new frame 3, inside 2
    f3 = menu.add.frame_h(150, 200, frame_id='f3')
    f2.pack(f3)
    assert f3.get_indices() == (-1, -1)
    assert menu._widgets == [f1, b1, b2, b0, b4, f2, b3, b5, f3]
    assert b1 == f3.pack(f1.unpack(b1))
    assert menu._widgets == [f1, b2, b0, b4, f2, b3, b5, f3, b1]

    # Create container frame
    f4 = menu.add.frame_v(400, 1500, frame_id='f4')
    assert f2.get_frame() is None
    f4.pack(f2)
    assert menu._widgets == [f1, b2, b0, b4, f4, f2, b3, b5, f3, b1]
    f4.pack(f1.unpack(b2))
    assert menu._widgets == [f1, b0, b4, f4, f2, b3, b5, f3, b1, b2]

    # Sort two widgets
    assert len(menu._update_frames) == 0
    menu.move_widget_index(b2, f2)
    assert menu._widgets == [f1, b0, b4, f4, b2, f2, b3, b5, f3, b1]
    with pytest.raises(AssertionError):
        menu.move_widget_index(b2, b3)
    menu.move_widget_index(b3, b5)
    assert menu._widgets == [f1, b0, b4, f4, b2, f2, b5, b3, f3, b1]
    menu.move_widget_index(f3, b5)
    assert menu._widgets == [f1, b0, b4, f4, b2, f2, f3, b1, b5, b3]
    f3.pack(f2.unpack(b5))
    assert menu._widgets == [f1, b0, b4, f4, b2, f2, f3, b1, b5, b3]
    menu.move_widget_index(b1, b5)
    assert menu._widgets == [f1, b0, b4, f4, b2, f2, f3, b5, b1, b3]
    menu.move_widget_index(b3, f3)
    assert menu._widgets == [f1, b0, b4, f4, b2, f2, b3, f3, b5, b1]
    menu.move_widget_index(f3, b3)
    assert menu._widgets == [f1, b0, b4, f4, b2, f2, f3, b5, b1, b3]
    assert menu.get_selected_widget() == b0

    # Test advanced packing
    f4.pack(f1)
    assert menu._widgets == [f4, b2, f2, f3, b5, b1, b3, f1, b0, b4]
    f4.unpack(f2)
    assert menu._widgets == [f4, b2, f1, b0, b4, f2, f3, b5, b1, b3]
    menu.remove_widget(f4)
    assert b2.get_frame() is None
    assert f1.get_frame() is None
    assert b0.get_frame() == f1
    assert b4.get_frame() == f1
    assert menu._widgets == [f2, f3, b5, b1, b3, b2, f1, b0, b4]
    f3.pack(f1)
    assert menu._widgets == [f2, f3, b5, b1, f1, b0, b4, b3, b2]

    # Assert limits
    assert f1.get_indices() == (5, 6)
    assert f2.get_indices() == (1, 7)
    assert f3.get_indices() == (2, 4)
    assert f4.get_indices() == (-1, -1)

    f2.pack(b2)
    assert menu._widgets == [f2, f3, b5, b1, f1, b0, b4, b3, b2]
    assert f1.get_indices() == (5, 6)
    assert f2.get_indices() == (1, 8)
    assert f3.get_indices() == (2, 4)
    assert f4.get_indices() == (-1, -1)

    f2.pack(f3.unpack(f1))
    assert menu._widgets == [f2, f3, b5, b1, b3, b2, f1, b0, b4]
    f2.pack(f2.unpack(f3))
    assert menu._widgets == [f2, b3, b2, f1, b0, b4, f3, b5, b1]
    assert f1.get_indices() == (4, 5)
    assert f2.get_indices() == (1, 6)
    assert f3.get_indices() == (7, 8)

    # Unpack f3 and move to first
    f2.unpack(f3)
    menu.move_widget_index(f3, f2)
    assert menu._widgets == [f3, b5, b1, f2, b3, b2, f1, b0, b4]
    assert f1.get_indices() == (7, 8)
    assert f2.get_indices() == (4, 6)
    assert f3.get_indices() == (1, 2)

    # Remove b5
    menu.remove_widget(b5)
    assert b5 not in f1.get_widgets()
    assert b5.get_menu() == b5.get_frame()

    # Add again b5, this time this widget is not within menu
    f3.pack(b5)
    with pytest.raises(AssertionError):
        f3.pack(f4)
    assert f4.get_menu() is None
    f3.pack(f2.unpack(b3))
    assert f3.get_widgets(unpack_subframes=False) == (b1, b5, b3)
    menu.move_widget_index(b1, b3)
    assert f3.get_widgets(unpack_subframes=False) == (b3, b1, b5)

    assert f2.get_indices() == (4, 5)
    assert f1.get_indices() == (6, 7)
    menu.remove_widget(b4)
    assert f2.get_indices() == (4, 5)
    assert f1.get_indices() == (6, 6)

    menu.move_widget_index(b3, b1)
    assert f3.get_widgets(unpack_subframes=False) == (b1, b5, b3)
    with pytest.raises(AssertionError):
        menu.move_widget_index(b1, 5)
    with pytest.raises(AssertionError):
        menu.move_widget_index(b1, 1)
    menu.move_widget_index(b3, 1)
    f3.pack(b4)
    assert f3.get_widgets(unpack_subframes=False) == (b3, b1, b5, b4)
    assert menu._widgets == [f3, b3, b1, f2, b2, f1, b0]

    # Sort two frames, considering non-menu widgets
    menu.move_widget_index(f3, f2)
    assert menu._widgets == [f2, b2, f1, b0, f3, b3, b1]
    assert f3.get_widgets(unpack_subframes=False) == (b3, b1, b5, b4)

    # Rollback
    menu.move_widget_index(f3, f2)
    assert menu._widgets == [f3, b3, b1, f2, b2, f1, b0]

    # Add non-menu to last frame within frame
    f1.pack(f3.unpack(b4))
    assert f3.get_widgets(unpack_subframes=False) == (b3, b1, b5)
    assert f1.get_widgets(unpack_subframes=False) == (b0, b4)

    # Move again
    menu.move_widget_index(f3, f2)
    assert menu._widgets == [f2, b2, f1, b0, f3, b3, b1]
    menu.move_widget_index(f3, f2)
    assert menu._widgets == [f3, b3, b1, f2, b2, f1, b0]

    # Move, but 3 frame in same levels
    f2.unpack(f1)
    assert menu.get_selected_widget() == b0
    menu.move_widget_index(f1, f3)
    assert menu._widgets == [f1, b0, f3, b3, b1, f2, b2]
    menu.move_widget_index(f2, f3)
    assert menu._widgets == [f1, b0, f2, b2, f3, b3, b1]
    menu.move_widget_index(f2, f3)
    assert menu._widgets == [f1, b0, f3, b3, b1, f2, b2]
    menu.move_widget_index(f3, f2)
    assert menu._widgets == [f1, b0, f2, b2, f3, b3, b1]
    menu.move_widget_index(None)
    assert menu._widgets == [f3, b3, b1, f2, b2, f1, b0]
    assert menu.get_selected_widget() == b0

    # Add really long nested frames
    f_rec = []
    n = 10
    for i in range(n):
        f_rec.append(menu.add.frame_v(100, 100, frame_id=f'f_rec{i}'))
        f_rec[i].relax()
        if i >= 1:
            f_rec[i - 1].pack(f_rec[i])

    # Check indices
    for i in range(n):
        assert f_rec[i].get_indices() == (-1, -1)
        assert f_rec[i].get_frame() is None if i == 0 else f_rec[i - 1]

    assert menu._widgets == [f3, b3, b1, f2, b2, f1, b0, *f_rec]

    # Test frame with none menu as first
    assert f1.get_widgets() == (b0, b4)
    f1.pack(f1.unpack(b0))
    assert f1.get_widgets() == (b4, b0)
    assert menu._widgets == [f3, b3, b1, f2, b2, f1, b0, *f_rec]

    # Move widgets
    menu.move_widget_index(f2, f_rec[0])
    assert menu._widgets == [f3, b3, b1, *f_rec, f2, b2, f1, b0]
    menu.move_widget_index(f3, f_rec[0])
    assert menu._widgets == [*f_rec, f3, b3, b1, f2, b2, f1, b0]
    menu.move_widget_index(f3, f2)
    assert menu._widgets == [*f_rec, f2, b2, f3, b3, b1, f1, b0]
    menu.move_widget_index(f3, f_rec[0])
    assert menu._widgets == [f3, b3, b1, *f_rec, f2, b2, f1, b0]

    # Add button to deepest frame
    f_rec[-1].pack(f3.unpack(b3))
    assert menu.get_selected_widget() == b0
    for i in range(n):
        assert f_rec[i].get_indices() == (3 + i, 3 + i)
    menu.select_widget(b3)
    for w in [b1, b0, b2, b3]:
        menu._down()
        assert menu.get_selected_widget() == w

    #  Unpack button from recursive
    f3.pack(f_rec[-1].unpack(b3))
    for i in range(n):
        assert f_rec[i].get_indices() == (-1, -1)
    for w in [b1, b0, b2, b3]:
        menu._down()
        assert menu.get_selected_widget() == w
    for w in [b2, b0, b1, b3]:
        menu._up()
        assert menu.get_selected_widget() == w

    menu._test_print_widgets()


def test_scrollarea():
    """Test scrollarea frame."""
    menu = MenuUtils.generic_menu(theme=THEME_NON_FIXED_TITLE)
    with pytest.raises(AssertionError):
        menu.add.frame_v(300, 400, max_width=400)
    with pytest.raises(AssertionError):
        menu.add.frame_v(300, 400, max_height=500)
    with pytest.raises(AssertionError):
        menu.add.frame_v(300, 400, max_height=-1)
    img = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU)
    frame_sc = menu.add.frame_v(300, 400, max_height=200, background_color=img, frame_id='frame_sc')
    frame_scroll = frame_sc.get_scrollarea(inner=True)
    frame2 = menu.add.frame_v(400, 200, background_color=(30, 30, 30), padding=25)
    menu.add.frame_v(300, 200, background_color=(255, 255, 0))
    assert menu.get_selected_widget() is None
    btn_frame21 = frame2.pack(menu.add.button('Button frame nosc'))
    btn_frame22 = frame2.pack(menu.add.button('Button frame nosc 2'))
    btn = frame_sc.pack(menu.add.button('Nice', lambda: print('Clicked'), padding=10))
    btn2 = frame_sc.pack(menu.add.button('Nice2', lambda: print('Clicked'), padding=10))
    btn3 = frame_sc.pack(menu.add.button('Nice3', lambda: print('Clicked'), padding=10))
    btn4 = frame_sc.pack(menu.add.button('Nice4', lambda: print('Clicked'), padding=10))
    btn5 = frame_sc.pack(menu.add.button('Nice5', lambda: print('Clicked'), padding=10))
    btn_real = menu.add.button('Normal button', lambda: print('Clicked'), background_color=(255, 0, 255))

    # First, test structure
    #   btn    \
    #   btn2   |
    #   btn3   | frame_sc scrollarea enabled
    #   btn4   |
    #   btn5   /
    #   btn_frame21 (x) \ frame2 no scrollarea <-- selected by default
    #   btn_frame22     /
    #   btn_real
    assert frame_sc.is_scrollable
    assert not frame2.is_scrollable
    assert btn.get_frame() == frame_sc
    assert btn2.get_frame() == frame_sc
    assert btn.get_scrollarea() == frame_sc.get_scrollarea(inner=True)
    assert btn_real.get_frame() is None
    assert btn_real.get_scrollarea() == menu.get_scrollarea()
    assert btn_frame21.get_frame() == frame2
    assert btn_frame22.get_frame() == frame2
    assert btn_frame21.is_selected()
    assert frame_scroll.get_parent() == menu.get_scrollarea()

    btn_frame21.active = True
    menu._mouse_motion_selection = True
    assert menu._draw_focus_widget(surface, btn_frame21) == (
        {1: ((0, 0), (600, 0), (600, 158 if PYGAME_V2 else 158), (0, 158 if PYGAME_V2 else 158)),
         2: ((0, 159 if PYGAME_V2 else 159), (114, 159 if PYGAME_V2 else 159),
             (114, 207 if PYGAME_V2 else 208), (0, 207 if PYGAME_V2 else 208)),
         3: ((390, 159 if PYGAME_V2 else 159), (600, 159 if PYGAME_V2 else 159),
             (600, 207 if PYGAME_V2 else 208), (390, 207 if PYGAME_V2 else 208)),
         4: ((0, 208 if PYGAME_V2 else 209), (600, 208 if PYGAME_V2 else 209), (600, 600), (0, 600))}
    )
    btn_frame21.active = False

    # Test scrollareas position
    vpos = 0.721
    vpos2 = 0.56
    vpos3 = 0.997
    vpos4 = 0
    if PYGAME_V2:
        assert menu.get_selected_widget() == btn_frame21
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(vpos)
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_HORIZONTAL) == -1
        assert frame_scroll.get_scroll_value_percentage(ORIENTATION_VERTICAL) == 0
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
        assert menu.get_selected_widget() == btn_frame22
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(vpos)
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_HORIZONTAL) == -1
        assert frame_scroll.get_scroll_value_percentage(ORIENTATION_VERTICAL) == 0
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == vpos4
        assert frame_scroll.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(vpos2)
        assert menu.get_selected_widget() == btn5
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == vpos4
        assert frame_scroll.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(vpos2)
        assert menu.get_selected_widget() == btn4
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == vpos4
        assert frame_scroll.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(vpos2)
        assert menu.get_selected_widget() == btn3
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == vpos4
        assert frame_scroll.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(0.305)
        assert menu.get_selected_widget() == btn2
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == vpos4
        assert frame_scroll.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(0)
        assert menu.get_selected_widget() == btn
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(vpos3)
        assert frame_scroll.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(0)
        assert menu.get_selected_widget() == btn_real
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == vpos4
        assert frame_scroll.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(vpos2)
        assert menu.get_selected_widget() == btn5
    else:
        menu.select_widget(btn5)

    # Test active within scroll
    btn5.active = True
    assert menu._draw_focus_widget(surface, btn5) == (
        {1: ((0, 0), (600, 0), (600, 287 if PYGAME_V2 else 285), (0, 287 if PYGAME_V2 else 285)),
         2: ((0, 288 if PYGAME_V2 else 286), (137, 288 if PYGAME_V2 else 286), (137, 347), (0, 347)),
         3: ((237, 288 if PYGAME_V2 else 286), (600, 288 if PYGAME_V2 else 286), (600, 347), (237, 347)),
         4: ((0, 348), (600, 348), (600, 600), (0, 600))}
    )
    btn5.active = False
    btn.select(update_menu=True)

    assert btn.get_rect(to_real_position=True) == pygame.Rect(138, 156, 82, 61 if PYGAME_V2 else 62)
    assert frame_scroll.get_absolute_view_rect() == pygame.Rect(138, 156, 284, 192)

    # Move inner scroll by 10%
    frame_scroll.scroll_to(ORIENTATION_VERTICAL, 0.1)
    assert frame_scroll.get_absolute_view_rect() == pygame.Rect(138, 156, 284, 192)
    assert btn.get_rect(to_real_position=True) == pygame.Rect(138, 156, 82, 41 if PYGAME_V2 else 42)

    # Move menu scroll by 10%
    menu.get_scrollarea().scroll_to(ORIENTATION_VERTICAL, 0.1)
    assert frame_scroll.get_absolute_view_rect() == pygame.Rect(138, 155, 284, 165)
    assert btn.get_rect(to_real_position=True) == pygame.Rect(138, 155, 82, 14 if PYGAME_V2 else 15)

    # Move menu scroll by 50%
    menu.get_scrollarea().scroll_to(ORIENTATION_VERTICAL, 0.5)
    assert frame_scroll.get_absolute_view_rect() == pygame.Rect(138, 155, 284, 46 if PYGAME_V2 else 44)
    assert btn.get_rect(to_real_position=True) == pygame.Rect(138, 155, 0, 0)

    menu.get_scrollarea().scroll_to(ORIENTATION_VERTICAL, 1)
    assert frame_scroll.get_absolute_view_rect() == pygame.Rect(0, 155, 0, 0)
    assert btn.get_rect(to_real_position=True) == pygame.Rect(0, 155, 0, 0)

    menu.get_scrollarea().scroll_to(ORIENTATION_VERTICAL, 0)
    frame_scroll.scroll_to(ORIENTATION_VERTICAL, 0)
    assert btn.get_rect(to_real_position=True) == pygame.Rect(138, 156, 82, 61 if PYGAME_V2 else 62)
    assert frame_scroll.get_absolute_view_rect() == pygame.Rect(138, 156, 284, 192)

    # Remove btn
    menu.remove_widget(btn)
    assert not btn.is_selected()
    assert btn.get_menu() is None

    # Hide button 5
    btn5.hide()

    # Add textinput to frame
    # First, test structure
    #   btn2   \  <-- selected by default
    #   btn3   | frame_sc scrollarea enabled
    #   btn4   |
    #   btn5   |
    #   text   /
    #   btn_frame21 (x) \ frame2 no scrollarea
    #   btn_frame22     /
    #   btn_real
    text = frame_sc.pack(menu.add.text_input('text: '))
    assert text.get_position() == (8, 187 if PYGAME_V2 else 190)
    assert text.get_translate(virtual=True) == (-138, 182 if PYGAME_V2 else 185)
    assert text.get_translate() == (0, 0)

    # Test text events within frame
    menu.select_widget(btn2)
    menu.select_widget(text)
    assert not text.active
    assert text.get_value() == ''
    menu.update(PygameEventUtils.key(pygame.K_a, char='a', keydown=True))
    assert text.active
    assert text.get_value() == 'a'
    for i in range(10):
        menu.update(PygameEventUtils.key(pygame.K_a, char='a', keydown=True))
    menu.draw(surface)
    menu.update(PygameEventUtils.key(pygame.K_a, char='a', keydown=True))  # the last one to be added
    with pytest.raises(pygame_menu.widgets.widget.frame._FrameSizeException):
        menu.mainloop(surface)
    text.set_value('')
    assert text.active
    menu.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert not text.active

    # Set widgets as floating
    #   btn4,text, btn2  \
    #   btn3             | frame_sc scrollarea enabled
    #   btn6             /
    #   btn_frame21 (x) \ frame2 no scrollarea
    #   btn_frame22     /
    #   btn_real
    btn4.set_float()
    text.set_float()
    btn6 = frame_sc.pack(menu.add.button('btn6'))
    if PYGAME_V2:
        assert menu._test_widgets_status() == (
            (('Frame',
              (0, 0, 0, 138, 1, 304, 192, 138, 156, 138, 1),
              (0, 0, 0, 1, 1, 0, 0),
              (1, 6)),
             ('Button-Nice2',
              (0, 0, 1, 0, 0, 99, 61, 138, 156, 0, 155),
              (1, 0, 0, 1, 0, 1, 1)),
             ('Button-Nice3',
              (0, 0, 2, 0, 61, 99, 61, 138, 217, 0, 216),
              (1, 0, 0, 1, 0, 1, 1)),
             ('Button-Nice4',
              (0, 0, 3, 0, 0, 99, 61, 138, 156, 0, 155),
              (1, 1, 0, 1, 0, 1, 1)),
             ('Button-Nice5',
              (-1, -1, 4, -148, 172, 99, 61, 138, 156, -148, 327),
              (1, 0, 0, 0, 0, 1, 1)),
             ('TextInput-text: ',
              (0, 0, 5, 0, 0, 87, 49, 138, 156, 0, 155),
              (1, 1, 1, 1, 0, 1, 1),
              ''),
             ('Button-btn6',
              (0, 0, 6, 0, 122, 80, 49, 138, 278, 0, 277),
              (1, 0, 0, 1, 0, 1, 1)),
             ('Frame',
              (0, 1, 7, 90, 193, 400, 200, 90, 348, 90, 193),
              (0, 0, 0, 1, 0, 0, 0),
              (8, 9)),
             ('Button-Button frame nosc',
              (0, 1, 8, 115, 218, 275, 49, 115, 373, 115, 218),
              (1, 0, 0, 1, 0, 1, 1)),
             ('Button-Button frame nosc 2',
              (0, 1, 9, 115, 267, 300, 49, 115, 422, 115, 267),
              (1, 0, 0, 1, 0, 1, 1)),
             ('Frame',
              (0, 2, 10, 140, 393, 300, 200, 0, 155, 140, 393),
              (0, 0, 0, 1, 0, 0, 0),
              (-1, -1)),
             ('Button-Normal button',
              (0, 3, 11, 178, 593, 224, 49, 0, 155, 178, 593),
              (1, 0, 0, 1, 0, 0, 0)))
        )

    # Test widget unpacking within scrollarea
    assert btn6.get_scrollarea() == frame_sc.get_scrollarea(inner=True)
    frame_sc.unpack(btn6)
    assert btn6.get_scrollarea() == menu.get_scrollarea()

    # Translate widget within scrollarea
    btn3.translate(250, 100)
    menu.render()
    assert btn3.get_translate() == (250, 100)

    # Add another scrollarea within scrollarea
    w = frame_sc.clear()
    for v in w:
        menu.remove_widget(v)
    assert btn6 not in w
    menu.remove_widget(btn6)
    if PYGAME_V2:
        assert menu._test_widgets_status() == (
            (('Frame',
              (0, 0, 0, 138, 1, 304, 192, 0, 155, 138, 1),
              (0, 0, 0, 1, 1, 0, 0),
              (-1, -1)),
             ('Frame',
              (0, 1, 1, 90, 193, 400, 200, 90, 155, 90, 193),
              (0, 0, 0, 1, 0, 0, 0),
              (2, 3)),
             ('Button-Button frame nosc',
              (0, 1, 2, 115, 218, 275, 49, 115, 159, 115, 218),
              (1, 0, 1, 1, 0, 1, 1)),
             ('Button-Button frame nosc 2',
              (0, 1, 3, 115, 267, 300, 49, 115, 208, 115, 267),
              (1, 0, 0, 1, 0, 1, 1)),
             ('Frame',
              (0, 2, 4, 140, 393, 300, 200, 140, 334, 140, 393),
              (0, 0, 0, 1, 0, 0, 0),
              (-1, -1)),
             ('Button-Normal button',
              (0, 3, 5, 178, 593, 224, 49, 0, 155, 178, 593),
              (1, 0, 0, 1, 0, 0, 0)))
        )

    btn1 = frame_sc.pack(menu.add.button('btn1'))
    btn2 = frame_sc.pack(menu.add.button('btn2'))
    btn3 = pygame_menu.widgets.Button('btn3')
    menu.add.configure_defaults_widget(btn3)
    frame_sc.pack(btn3)
    frame_rnoscroll = menu.add.frame_v(150, 100, background_color=(160, 0, 60), frame_id='rno')
    btn4 = frame_rnoscroll.pack(menu.add.button('btn4', button_id='nice'))
    frame_rscroll = menu.add.frame_v(200, 500, max_height=100, background_color=(60, 60, 60), frame_id='r')
    frame_sc.pack(frame_rscroll)
    frame_sc.pack(frame_rnoscroll)
    bnice = menu.add.button('nice', font_color=(255, 255, 255))
    btn5 = frame_rscroll.pack(bnice)
    frame_sc.translate(-50, 0)

    # btn1                    \
    # btn2                    |
    # btn3                    | frame_sc, frame_scroll
    # btn5  > frame_rscroll   |
    # btn4  > frame_rnoscroll /
    # btn_frame21 (x) \ frame2 no scrollarea
    # btn_frame22     /
    # btn_real
    assert btn1.get_scrollarea() == frame_scroll
    assert btn2.get_scrollarea() == frame_scroll
    assert btn3.get_scrollarea() == frame_scroll
    assert frame_rscroll.get_scrollarea() == frame_scroll
    assert btn5.get_scrollarea().get_parent() == frame_scroll
    assert frame_rnoscroll.get_scrollarea() == frame_scroll
    assert btn5.get_scrollarea() == frame_rscroll.get_scrollarea(inner=True)
    assert btn4.get_scrollarea() == frame_scroll
    assert frame_rscroll.get_size() == (204, 92)
    assert frame_sc.get_scrollarea(inner=True) == frame_scroll
    assert frame_rscroll.get_scrollarea() == frame_scroll
    assert frame_rscroll.get_scrollarea(inner=True).get_parent() == frame_rscroll.get_scrollarea()

    # Normal frame with inner frames
    frame_out = menu.add.frame_v(400, 900, background_color=(0, 200, 0))
    nice1 = frame_out.pack(menu.add.button('Nice1'))
    frame_out_rnoscroll = menu.add.frame_v(150, 100, background_color=(160, 0, 60))
    nice2 = frame_out_rnoscroll.pack(menu.add.button('Nice2'))
    frame_out_rnoscroll2 = menu.add.frame_v(150, 100, background_color=(20, 50, 140))
    nice3 = frame_out_rnoscroll2.pack(menu.add.button('Nice3'))
    frame_out_rnoscroll_rscroll = menu.add.frame_v(200, 500, max_height=100, background_color=(60, 60, 60))
    nice4 = frame_out_rnoscroll_rscroll.pack(menu.add.button('Nice4'))
    frame_out.pack(frame_out_rnoscroll)
    frame_out.pack(frame_out_rnoscroll2)
    frame_out.pack(frame_out_rnoscroll_rscroll)
    assert nice2.get_scrollarea() == menu.get_scrollarea()

    assert nice1 in frame_out.get_widgets()
    assert nice3 in frame_out.get_widgets()
    assert nice4 in frame_out.get_widgets()

    # frame_sc.translate(-50, 0)

    def draw_rect() -> None:
        """
        Draw absolute rect on surface for testing purposes.
        """
        # surface.fill((160, 0, 0), frame_scroll.get_absolute_view_rect())
        # surface.fill((60, 0, 60), btn.get_scrollarea().to_real_position(btn.get_rect(), visible=True))
        # surface.fill((255, 255, 255), btn.get_rect(to_real_position=True))
        # surface.fill((0, 255, 0), nice4.get_rect(to_real_position=True))
        # surface.fill((0, 255, 255), btn4.get_rect(to_real_position=True))
        return

    menu.get_decorator().add_callable(draw_rect, prev=False, pass_args=False)

    # Scroll down each subelement
    frame_sc.scrollh(1)
    frame_sc.scrollv(1)
    frame_rscroll.scrollv(1)
    frame_out_rnoscroll_rscroll.scrollv(1)
    menu.select_widget(btn_real)

    if PYGAME_V2:
        for v in [0.292, 0.335, 0.419, 0.535, 0.002, 0.002, 0.002, 0.002, 0.002, 0.002, 0.247]:
            menu._up()
            assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(v)
    assert menu.get_selected_widget() == btn_real

    frame_sc.scrollh(1)
    frame_sc.scrollv(1)
    frame_rscroll.scrollv(1)
    frame_out_rnoscroll_rscroll.scrollv(1)

    # Now up
    if PYGAME_V2:
        for v in [0.222, 0.180, 0.002, 0.002, 0.002, 0.002, 0.535, 0.535, 0.535, 0.535, 0.496]:
            menu._down()
            assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(v)
    assert menu.get_selected_widget() == btn_real

    # Select two widgets
    btn_frame21.select()
    menu._test_print_widgets()

    # Check selection
    with pytest.raises(pygame_menu.menu._MenuMultipleSelectedWidgetsException):
        menu.render()
    menu.render()
    assert menu.get_selected_widget() == btn_frame21


def test_scrollarea_frame_within_scrollarea():
    """Test scrollarea frame within scrollarea's."""
    menu = MenuUtils.generic_menu(theme=THEME_NON_FIXED_TITLE)
    f1 = menu.add.frame_v(450, 400, background_color=(0, 0, 255), frame_id='f1')
    f2 = menu.add.frame_v(400, 400, max_height=300, background_color=(255, 0, 0), frame_id='f2')
    f3 = menu.add.frame_v(350, 400, max_height=200, background_color=(0, 255, 0), frame_id='f3')
    f4 = menu.add.frame_v(300, 400, max_height=100, background_color=(0, 255, 255), frame_id='f4')

    f4._pack_margin_warning = False

    # Get scrollarea's
    s0 = menu.get_scrollarea()
    s1 = f2.get_scrollarea(inner=True)
    s2 = f3.get_scrollarea(inner=True)
    s3 = f4.get_scrollarea(inner=True)

    vm = f2.pack(menu.add.vertical_margin(25, margin_id='margin'))
    b1 = f1.pack(menu.add.button('btn1', button_id='b1'), margin=(25, 0))
    b2 = f2.pack(menu.add.button('btn2', button_id='b2'), margin=(25, 0))
    b3 = f3.pack(menu.add.button('btn3', button_id='b3'), margin=(25, 0))
    b4 = f4.pack(menu.add.button('btn4', button_id='b4'), margin=(25, 0))

    # Pack frames
    f1.pack(f2)
    f2.pack(f3)
    f3.pack(f4)

    # Add last button
    b5 = menu.add.button('btn5', button_id='b5')

    # Test positioning
    #
    # .------------f1-----------.
    # | btn1                 s0 |
    # | .----------f2---------. |
    # | | <25px>           s1 ^ |
    # | | btn2                | |
    # | | .--------f3-------. | |
    # | | | btn3         s2 ^ | |
    # | | | .------f4-----. | | |
    # | | | | btn4     s3 ^ | | |
    # | | | |             v | | |
    # | | | .-------------. v | |
    # | | .-----------------. v |
    # | .---------------------. |
    # .-------------------------.
    # btn5
    assert b1.get_frame_depth() == 1
    assert b2.get_frame_depth() == 2
    assert b3.get_frame_depth() == 3
    assert b4.get_frame_depth() == 4
    assert b5.get_frame_depth() == 0

    assert menu._update_frames == [f4, f3, f2]

    assert not f1.is_scrollable
    assert f2.is_scrollable
    assert f3.is_scrollable
    assert f4.is_scrollable

    assert s0.get_parent() is None
    assert f1.get_scrollarea() == s0
    assert f2.get_scrollarea() == s0
    assert f3.get_scrollarea() == s1
    assert f4.get_scrollarea() == s2

    assert s0.get_depth() == 0
    assert s1.get_depth() == 1
    assert s2.get_depth() == 2
    assert s3.get_depth() == 3

    if PYGAME_V2:
        assert s0.get_absolute_view_rect() == pygame.Rect(0, 155, 580, 345)
        assert s1.get_absolute_view_rect() == pygame.Rect(73, 208, 384, 292)
        assert s2.get_absolute_view_rect() == pygame.Rect(73, 282, 334, 192)
        assert s3.get_absolute_view_rect() == pygame.Rect(73, 331, 284, 92)

        assert s0.get_parent_position() == (0, 0)
        assert s1.get_parent_position() == (0, 154)
        assert s2.get_parent_position() == (73, 208)
        assert s3.get_parent_position() == (73, 282)

    def draw_rect() -> None:
        """
        Draw absolute rect on surface for testing purposes.
        """
        # surface.fill((0, 0, 0), s3.get_absolute_view_rect())
        return

    menu.get_decorator().add_callable(draw_rect, prev=False, pass_args=False)

    assert menu.get_selected_widget() == b1
    assert f1.get_indices() == (1, 2)
    assert f2.get_indices() == (4, 5)
    assert f3.get_indices() == (6, 7)
    assert f4.get_indices() == (8, 8)

    # Scroll all to bottom, test movement
    f2.scrollv(1)
    f3.scrollv(1)
    f4.scrollv(1)
    if PYGAME_V2:
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(0.01)
        menu._down()
        assert menu.get_selected_widget() == b5
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(0.99)
        assert f2.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(0.99)
        assert f3.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(1)
        assert f4.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(0.993)
        menu._down()
        assert menu.get_selected_widget() == b4
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(0)
        assert f2.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(0)
        assert f3.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(0)
        assert f3.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(0)
        assert menu._test_widgets_status() == (
            (('Frame',
              (0, 0, 0, 65, 1, 450, 400, 65, 156, 65, 1),
              (0, 0, 0, 1, 0, 0, 0),
              (1, 2)),
             ('Button-btn1',
              (0, 0, 1, 98, 5, 80, 49, 98, 160, 98, 5),
              (1, 0, 0, 1, 0, 1, 1)),
             ('Frame',
              (0, 0, 2, 73, 54, 404, 292, 73, 209, 73, 54),
              (0, 0, 0, 1, 1, 1, 1),
              (4, 5)),
             ('VMargin', (0, 0, 3, 0, 0, 0, 25, 0, 0, 0, 0), (0, 0, 0, 1, 0, 1, 2)),
             ('Button-btn2',
              (0, 0, 4, 25, 25, 80, 49, 98, 234, 25, 180),
              (1, 0, 0, 1, 0, 1, 2)),
             ('Frame',
              (0, 0, 5, 0, 74, 354, 192, 73, 283, 0, 229),
              (0, 0, 0, 1, 1, 1, 2),
              (6, 7)),
             ('Button-btn3',
              (0, 0, 6, 25, 0, 80, 49, 98, 283, 98, 209),
              (1, 0, 0, 1, 0, 1, 3)),
             ('Frame',
              (0, 0, 7, 0, 49, 304, 92, 73, 332, 73, 258),
              (0, 0, 0, 1, 1, 1, 3),
              (8, 8)),
             ('Button-btn4',
              (0, 0, 8, 25, 0, 80, 49, 98, 332, 98, 283),
              (1, 0, 1, 1, 0, 1, 4)),
             ('Button-btn5',
              (0, 1, 9, 250, 401, 80, 49, 0, 155, 250, 401),
              (1, 0, 0, 1, 0, 0, 0)))
        )

    def check_all_visible() -> None:
        """
        Check all widgets are visible.
        """
        assert f1.is_visible()
        assert b1.is_visible()
        assert b1.is_visible(check_frame=False)
        assert f2.is_visible()
        assert b2.is_visible()
        assert b2.is_visible(check_frame=False)
        assert f3.is_visible()
        assert b3.is_visible()
        assert b3.is_visible(check_frame=False)
        assert f4.is_visible()
        assert b4.is_visible()
        assert b4.is_visible(check_frame=False)
        assert b5.is_visible()
        assert b5.is_visible(check_frame=False)

    # Test hide
    f1.hide()
    assert menu.get_selected_widget() == b5
    assert not f1.is_visible()
    assert not b1.is_visible()
    assert b1.is_visible(check_frame=False)
    assert not f2.is_visible()
    assert not b2.is_visible()
    assert not f3.is_visible()
    assert not b3.is_visible()
    assert not f4.is_visible()
    assert not b4.is_visible()
    assert b5.is_visible()

    f1.show()
    assert menu.get_selected_widget() == b5
    check_all_visible()

    f2.hide()
    assert f1.is_visible()
    assert b1.is_visible()
    assert not f2.is_visible()
    assert not b2.is_visible()
    assert not f3.is_visible()
    assert not b3.is_visible()
    assert not f4.is_visible()
    assert not b4.is_visible()
    assert b5.is_visible()

    f2.show()
    check_all_visible()
    f3.hide()
    assert f1.is_visible()
    assert b1.is_visible()
    assert f2.is_visible()
    assert b2.is_visible()
    assert not f3.is_visible()
    assert not b3.is_visible()
    assert not f4.is_visible()
    assert not b4.is_visible()
    assert b5.is_visible()

    f3.show()
    check_all_visible()
    f4.hide()
    assert f1.is_visible()
    assert b1.is_visible()
    assert f2.is_visible()
    assert b2.is_visible()
    assert f3.is_visible()
    assert b3.is_visible()
    assert not f4.is_visible()
    assert not b4.is_visible()
    assert b5.is_visible()

    f4.show()
    check_all_visible()
    menu.get_scrollarea().scroll_to(ORIENTATION_VERTICAL, 0.562)

    # Move widgets
    menu.select_widget(b4)
    assert menu.get_selected_widget() == b4
    assert menu.get_widgets() == (f1, b1, f2, vm, b2, f3, b3, f4, b4, b5)
    menu.move_widget_index(f1, b5)
    assert menu.get_selected_widget() == b4
    assert menu.get_widgets() == (b5, f1, b1, f2, vm, b2, f3, b3, f4, b4)

    # Test scroll on up
    f3.scrollv(0)
    menu._down()
    assert menu.get_selected_widget() == b3
    assert f3.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(0 if PYGAME_V2 else 0.005)
    if PYGAME_V2:
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(0.562)

    f2.scrollv(0)
    menu._down()
    assert menu.get_selected_widget() == b2
    assert f2.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(0)
    if PYGAME_V2:
        assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(0.562)

    menu._down()
    menu._down()
    assert menu.get_selected_widget() == b5

    # Check all widgets are non-floating
    for w in menu.get_widgets():
        assert not w.is_floating()

    # Pack all widgets within the deepest frame
    f4.unpack(b4)
    with pytest.raises(AssertionError):
        f4.pack(f1.unpack(f1))
    f4.pack(f1.unpack(b1))
    menu.remove_widget(vm)
    assert vm not in f2.get_widgets()
    f4.pack(f2.unpack(b2))
    f4.pack(f3.unpack(b3))
    f4.pack(b4)
    f4.pack(b5)
    b5.set_float()
    f4w = f4.get_widgets()
    for w in f4w:
        assert w.is_floating()
        assert w.get_position() == f4w[0].get_position()
    assert menu.get_selected_widget() == b5
    assert f4.get_widgets() == (b1, b2, b3, b4, b5)

    # Unfloat widgets
    f4.unfloat()
    menu.select_widget(b1)
    for w in [b5, b4, b3, b2, b1]:
        menu._down()
        assert menu.get_selected_widget() == w

    for w in [b2, b3, b4, b5, b1]:
        menu._up()
        assert menu.get_selected_widget() == w

    menu._test_print_widgets()

    # Remove f4 from menu
    menu.remove_widget(f4)
    assert menu._update_frames == [f3, f2]


def test_menu_support():
    """Test frame menu support."""
    # Test frame movement
    theme = TEST_THEME.copy()
    theme.widget_margin = (0, 0)
    theme.widget_font_size = 20
    menu = MenuUtils.generic_menu(columns=3, rows=2, theme=theme)

    # btn0 | f1(btn2,btn3,btn4,btn5) | f2(btn7,
    #      |                         |    btn8,
    #      |                         |    f3(btn9,btn10))
    # btn1 |           btn6          | f4(btn11,btn12,btn13)
    btn0 = menu.add.button('btn0')
    btn1 = menu.add.button('btn1')
    f1 = menu.add.frame_h(200, 50, frame_id='f1')
    btn2 = menu.add.button('btn2 ')
    btn3 = menu.add.button('btn3 ')
    btn4 = menu.add.button('btn4 ')
    btn5 = menu.add.button('btn5 ')
    btn6 = menu.add.button('btn6')
    f2 = menu.add.frame_v(200, 132, background_color=(100, 0, 0), frame_id='f2')
    f3 = menu.add.frame_h(200, 50, background_color=(0, 0, 100), frame_id='f3')
    f4 = menu.add.frame_h(260, 50, frame_id='f4')
    btn7 = menu.add.button('btn7')
    btn8 = menu.add.button('btn8')
    btn9 = menu.add.button('btn9 ')
    btn10 = menu.add.button('btn10')
    btn11 = menu.add.button('btn11 ')
    btn12 = menu.add.button('btn12 ')
    btn13 = menu.add.button('btn13')
    f1.pack((btn2, btn3, btn4, btn5))
    f3.pack((btn9, btn10))
    f2.pack((btn7, btn8, f3), align=pygame_menu.locals.ALIGN_CENTER)
    f4.pack((btn11, btn12, btn13))

    menu._test_print_widgets()

    # Test min max indices
    assert f1.get_indices() == (3, 6)
    assert f2.get_indices() == (9, 11)
    assert f3.get_indices() == (12, 13)
    assert f4.get_indices() == (15, 17)

    # Check positioning
    assert btn0.get_col_row_index() == (0, 0, 0)
    assert btn1.get_col_row_index() == (0, 1, 1)
    assert f1.get_col_row_index() == (1, 0, 2)
    assert btn6.get_col_row_index() == (1, 1, 7)
    assert f2.get_col_row_index() == (2, 0, 8)
    assert f4.get_col_row_index() == (2, 1, 14)

    assert not f1.is_scrollable
    assert not f2.is_scrollable
    assert not f3.is_scrollable
    assert menu._test_widgets_status() == (
        (('Button-btn0',
          (0, 0, 0, 13, 82, 42, 28, 13, 237, 13, 82),
          (1, 0, 1, 1, 0, 0, 0)),
         ('Button-btn1',
          (0, 1, 1, 13, 110, 42, 28, 13, 265, 13, 110),
          (1, 0, 0, 1, 0, 0, 0)),
         ('Frame',
          (1, 0, 2, 84, 82, 200, 50, 84, 237, 84, 82),
          (0, 0, 0, 1, 0, 0, 0),
          (3, 6)),
         ('Button-btn2 ',
          (1, 0, 3, 84, 82, 47, 28, 84, 237, 84, 82),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Button-btn3 ',
          (1, 0, 4, 131, 82, 47, 28, 131, 237, 131, 82),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Button-btn4 ',
          (1, 0, 5, 178, 82, 47, 28, 178, 237, 178, 82),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Button-btn5 ',
          (1, 0, 6, 225, 82, 47, 28, 225, 237, 225, 82),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Button-btn6',
          (1, 1, 7, 163, 132, 42, 28, 163, 287, 163, 132),
          (1, 0, 0, 1, 0, 0, 0)),
         ('Frame',
          (2, 0, 8, 351, 82, 200, 132, 351, 237, 351, 82),
          (0, 0, 0, 1, 0, 0, 0),
          (9, 11)),
         ('Button-btn7',
          (2, 0, 9, 430, 82, 42, 28, 430, 237, 430, 82),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Button-btn8',
          (2, 0, 10, 430, 110, 42, 28, 430, 265, 430, 110),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Frame',
          (2, 0, 11, 351, 138, 200, 50, 351, 293, 351, 138),
          (0, 0, 0, 1, 0, 1, 1),
          (12, 13)),
         ('Button-btn9 ',
          (2, 0, 12, 351, 138, 47, 28, 351, 293, 351, 138),
          (1, 0, 0, 1, 0, 1, 2)),
         ('Button-btn10',
          (2, 0, 13, 398, 138, 53, 28, 398, 293, 398, 138),
          (1, 0, 0, 1, 0, 1, 2)),
         ('Frame',
          (2, 1, 14, 321, 214, 260, 50, 321, 369, 321, 214),
          (0, 0, 0, 1, 0, 0, 0),
          (15, 17)),
         ('Button-btn11 ',
          (2, 1, 15, 321, 214, 58, 28, 321, 369, 321, 214),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Button-btn12 ',
          (2, 1, 16, 379, 214, 58, 28, 379, 369, 379, 214),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Button-btn13',
          (2, 1, 17, 437, 214, 53, 28, 437, 369, 437, 214),
          (1, 0, 0, 1, 0, 1, 1)))
    )

    # Arrow keys
    assert menu.get_selected_widget() == btn0
    menu.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert menu.get_selected_widget() == btn2
    menu.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert menu.get_selected_widget() == btn3
    menu.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert menu.get_selected_widget() == btn4
    menu.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert menu.get_selected_widget() == btn5
    menu.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert menu.get_selected_widget() == btn7
    menu.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert menu.get_selected_widget() == btn0
    menu.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert menu.get_selected_widget() == btn10
    menu.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert menu.get_selected_widget() == btn9
    menu.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert menu.get_selected_widget() == btn5
    menu.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert menu.get_selected_widget() == btn4
    menu.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert menu.get_selected_widget() == btn3
    menu.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert menu.get_selected_widget() == btn2
    menu.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert menu.get_selected_widget() == btn0
    for bt in (btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn0, btn1):
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
        assert menu.get_selected_widget() == bt
    for bt in (btn6, btn11, btn12, btn13, btn1):
        menu.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_RIGHT))
        assert menu.get_selected_widget() == bt
    for bt in (btn0, btn13, btn12, btn11, btn10, btn9, btn8, btn7, btn6, btn5, btn4, btn3, btn2, btn1, btn0):
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        assert menu.get_selected_widget() == bt
    menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    assert menu.get_selected_widget() == btn1
    for bt in (btn13, btn12, btn11, btn6, btn1):
        menu.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_LEFT))
        assert menu.get_selected_widget() == bt

    # Check mouse events
    for bt in (btn0, btn13, btn12, btn11, btn10, btn9, btn8, btn7, btn6, btn5, btn4, btn3, btn2, btn1, btn0):
        menu.update(PygameEventUtils.middle_rect_click(bt, evtype=pygame.MOUSEBUTTONDOWN))
        assert menu.get_selected_widget() == bt

    # btn0 | f1(btn2,btn3,btn4,btn5) | f2(btn7,
    #      |                         |    btn8)
    # btn1 |            btn6         | f4(btn11,btn12,btn13)+(floating9,10)
    menu.select_widget(btn0)
    assert len(f2._widgets) == 3
    assert len(f3._widgets) == 2
    menu.remove_widget(f3)
    assert len(f2._widgets) == 2
    assert len(f3._widgets) == 0
    assert menu._test_widgets_status() == (
        (('Button-btn0',
          (0, 0, 0, 13, 82, 42, 28, 13, 237, 13, 82),
          (1, 0, 1, 1, 0, 0, 0)),
         ('Button-btn1',
          (0, 1, 1, 13, 110, 42, 28, 13, 265, 13, 110),
          (1, 0, 0, 1, 0, 0, 0)),
         ('Frame',
          (1, 0, 2, 84, 82, 200, 50, 84, 237, 84, 82),
          (0, 0, 0, 1, 0, 0, 0),
          (3, 6)),
         ('Button-btn2 ',
          (1, 0, 3, 84, 82, 47, 28, 84, 237, 84, 82),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Button-btn3 ',
          (1, 0, 4, 131, 82, 47, 28, 131, 237, 131, 82),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Button-btn4 ',
          (1, 0, 5, 178, 82, 47, 28, 178, 237, 178, 82),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Button-btn5 ',
          (1, 0, 6, 225, 82, 47, 28, 225, 237, 225, 82),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Button-btn6',
          (1, 1, 7, 163, 132, 42, 28, 163, 287, 163, 132),
          (1, 0, 0, 1, 0, 0, 0)),
         ('Frame',
          (2, 0, 8, 351, 82, 200, 132, 351, 237, 351, 82),
          (0, 0, 0, 1, 0, 0, 0),
          (9, 10)),
         ('Button-btn7',
          (2, 0, 9, 430, 82, 42, 28, 430, 237, 430, 82),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Button-btn8',
          (2, 0, 10, 430, 110, 42, 28, 430, 265, 430, 110),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Frame',
          (2, 1, 11, 321, 214, 260, 50, 321, 369, 321, 214),
          (0, 0, 0, 1, 0, 0, 0),
          (12, 14)),
         ('Button-btn11 ',
          (2, 1, 12, 321, 214, 58, 28, 321, 369, 321, 214),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Button-btn12 ',
          (2, 1, 13, 379, 214, 58, 28, 379, 369, 379, 214),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Button-btn13',
          (2, 1, 14, 437, 214, 53, 28, 437, 369, 437, 214),
          (1, 0, 0, 1, 0, 1, 1)),
         ('Button-btn9 ',
          (2, 0, 15, 427, 82, 47, 28, 427, 237, 427, 82),
          (1, 1, 0, 1, 0, 0, 0)),
         ('Button-btn10',
          (2, 0, 16, 424, 82, 53, 28, 424, 237, 424, 82),
          (1, 1, 0, 1, 0, 0, 0)))
    )

    menu.select_widget(btn0)
    for i in range(14):
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    assert menu.get_selected_widget() == btn0
    for i in range(14):
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
    assert menu.get_selected_widget() == btn0


def test_mouseover():
    """Test frame mouse support."""
    menu = MenuUtils.generic_menu(theme=THEME_NON_FIXED_TITLE)
    reset_widgets_over()
    assert WIDGET_MOUSEOVER == [None, []]

    f1 = menu.add.frame_v(500, 500, background_color='red',
                          cursor=pygame_menu.locals.CURSOR_HAND, frame_id='f1')
    menu.add.vertical_margin(100, margin_id='vbottom')
    f1.pack(menu.add.vertical_margin(100, margin_id='vtop'))

    f2 = menu.add.frame_v(400, 300, background_color='blue',
                          cursor=pygame_menu.locals.CURSOR_HAND, frame_id='f2')
    b1 = f1.pack(menu.add.button('1', button_id='b1', cursor=pygame_menu.locals.CURSOR_ARROW))
    f1.pack(f2)
    b2 = f2.pack(menu.add.button('2', button_id='b2', cursor=pygame_menu.locals.CURSOR_ARROW))

    f3 = f2.pack(menu.add.frame_v(100, 100, background_color='green',
                                  cursor=pygame_menu.locals.CURSOR_HAND, frame_id='f3'))
    b3 = f3.pack(menu.add.button('3', button_id='b3', cursor=pygame_menu.locals.CURSOR_ARROW))

    f1._id__repr__ = True
    f2._id__repr__ = True
    f3._id__repr__ = True

    # Get cursors
    cur_none = get_cursor()
    if cur_none is None:
        return
    set_pygame_cursor(pygame_menu.locals.CURSOR_ARROW)
    cur_arrow = get_cursor()
    set_pygame_cursor(pygame_menu.locals.CURSOR_HAND)
    cur_hand = get_cursor()
    set_pygame_cursor(cur_none)

    if PYGAME_V2:
        assert menu._test_widgets_status() == (
            (('Frame',
              (0, 0, 0, 40, 1, 500, 500, 40, 155, 40, 1),
              (0, 0, 0, 1, 0, 0, 0),
              (2, 3)),
             ('VMargin', (0, 0, 1, 0, 0, 0, 100, 0, 0, 0, 0), (0, 0, 0, 1, 0, 1, 1)),
             ('Button-1',
              (0, 0, 2, 48, 105, 33, 49, 48, 191, 48, 105),
              (1, 0, 1, 1, 0, 1, 1)),
             ('Frame',
              (0, 0, 3, 48, 154, 400, 300, 48, 240, 48, 154),
              (0, 0, 0, 1, 0, 1, 1),
              (4, 5)),
             ('Button-2',
              (0, 0, 4, 56, 158, 33, 49, 56, 244, 56, 158),
              (1, 0, 0, 1, 0, 1, 2)),
             ('Frame',
              (0, 0, 5, 56, 207, 100, 100, 56, 293, 56, 207),
              (0, 0, 0, 1, 0, 1, 2),
              (6, 6)),
             ('Button-3',
              (0, 0, 6, 64, 211, 33, 49, 64, 297, 64, 211),
              (1, 0, 0, 1, 0, 1, 3)),
             ('VMargin', (0, 1, 7, 0, 0, 0, 100, 0, 0, 0, 0), (0, 0, 0, 1, 0, 0, 0)))
        )

    # Setup
    assert b1.is_selected()
    assert not menu._mouse_motion_selection
    menu._test_print_widgets()

    test = [False, False, False, False, False, False]  # f1, b1, f2, b2, f3, b3
    print_events = False

    def onf1(widget, _) -> None:
        """
        f1 event.
        """
        assert widget == f1
        test[0] = not test[0]
        if print_events:
            print(f"{'Enter' if test[0] else 'Leave'} f1")

    def onb1(widget, _) -> None:
        """
        b1 event.
        """
        assert widget == b1
        test[1] = not test[1]
        if print_events:
            print(f"{'Enter' if test[1] else 'Leave'} b1")

    def onf2(widget, _) -> None:
        """
        f2 event.
        """
        assert widget == f2
        test[2] = not test[2]
        if print_events:
            print(f"{'Enter' if test[2] else 'Leave'} f2")

    def onb2(widget, _) -> None:
        """
        b2 event.
        """
        assert widget == b2
        test[3] = not test[3]
        if print_events:
            print(f"{'Enter' if test[3] else 'Leave'} b2")

    def onf3(widget, _) -> None:
        """
        f3 event.
        """
        assert widget == f3
        test[4] = not test[4]
        if print_events:
            print(f"{'Enter' if test[4] else 'Leave'} f3")

    def onb3(widget, _) -> None:
        """
        b3 event.
        """
        assert widget == b3
        test[5] = not test[5]
        if print_events:
            print(f"{'Enter' if test[5] else 'Leave'} b3")

    f1.set_onmouseover(onf1)
    f1.set_onmouseleave(onf1)
    b1.set_onmouseover(onb1)
    b1.set_onmouseleave(onb1)

    f2.set_onmouseover(onf2)
    f2.set_onmouseleave(onf2)
    b2.set_onmouseover(onb2)
    b2.set_onmouseleave(onb2)

    f3.set_onmouseover(onf3)
    f3.set_onmouseleave(onf3)
    b3.set_onmouseover(onb3)
    b3.set_onmouseleave(onb3)

    # Start moving mouse
    #
    # .------------f1-----------.
    # | vop <100px>             |
    # | b1                      |
    # | .----------f2---------. |
    # | | b2                  | |
    # | | .--------f3-------. | |
    # | | | b3              | | |
    # | | .-----------------. | |
    # | .---------------------. |
    # .-------------------------.
    # vbottom <100px>
    assert get_cursor() == cur_none
    menu.update(PygameEventUtils.topleft_rect_mouse_motion(f1))
    assert test == [True, False, False, False, False, False]
    assert WIDGET_MOUSEOVER == [f1, [f1, cur_none, []]]
    assert get_cursor() == cur_hand

    # Move to b1 inside f1
    menu.update(PygameEventUtils.topleft_rect_mouse_motion(b1))
    assert test == [True, True, False, False, False, False]
    assert WIDGET_MOUSEOVER == [b1, [b1, cur_hand, [f1, cur_none, []]]]
    assert get_cursor() == cur_arrow

    # Move to f2, inside f1
    menu.update(PygameEventUtils.topleft_rect_mouse_motion(f2))
    assert test == [True, False, True, False, False, False]  # out from b1
    assert WIDGET_MOUSEOVER == [f2, [f2, cur_hand, [f1, cur_none, []]]]
    assert get_cursor() == cur_hand

    # Move to b2, inside f2+f1
    menu.update(PygameEventUtils.topleft_rect_mouse_motion(b2))
    assert test == [True, False, True, True, False, False]
    assert WIDGET_MOUSEOVER == [b2, [b2, cur_hand, [f2, cur_hand, [f1, cur_none, []]]]]
    assert get_cursor() == cur_arrow

    # Move to f3
    menu.update(PygameEventUtils.topleft_rect_mouse_motion(f3))
    assert test == [True, False, True, False, True, False]  # out from b2
    assert WIDGET_MOUSEOVER == [f3, [f3, cur_hand, [f2, cur_hand, [f1, cur_none, []]]]]
    assert get_cursor() == cur_hand

    # Move to b3, inside f3+f2+f1
    menu.update(PygameEventUtils.topleft_rect_mouse_motion(b3))
    assert test == [True, False, True, False, True, True]
    assert WIDGET_MOUSEOVER == [b3, [b3, cur_hand, [f3, cur_hand, [f2, cur_hand, [f1, cur_none, []]]]]]
    assert get_cursor() == cur_arrow

    # From b3, move mouse out from window
    menu.update(PygameEventUtils.leave_window())
    assert test == [False, False, False, False, False, False]
    assert WIDGET_MOUSEOVER == [None, []]
    assert get_cursor() == cur_none

    # Move from out to inner widget (b3), this should call f1->f2->f3->b3
    menu.update(PygameEventUtils.topleft_rect_mouse_motion(b3))
    assert test == [True, False, True, False, True, True]
    assert WIDGET_MOUSEOVER == [b3, [b3, cur_hand, [f3, cur_hand, [f2, cur_hand, [f1, cur_none, []]]]]]
    assert get_cursor() == cur_arrow

    # Move from b3->f2, this should call b3, f3 but not call f2 as this is actually over
    menu.update(PygameEventUtils.topleft_rect_mouse_motion(f2))
    assert test == [True, False, True, False, False, False]
    assert WIDGET_MOUSEOVER == [f2, [f2, cur_hand, [f1, cur_none, []]]]
    assert get_cursor() == cur_hand

    # Move from f2->b1, this should call f2
    menu.update(PygameEventUtils.topleft_rect_mouse_motion(b1))
    assert test == [True, True, False, False, False, False]
    assert WIDGET_MOUSEOVER == [b1, [b1, cur_hand, [f1, cur_none, []]]]
    assert get_cursor() == cur_arrow

    # Move from b1 to outside the menu
    menu.update(PygameEventUtils.topleft_rect_mouse_motion((1, 1)))
    assert test == [False, False, False, False, False, False]
    assert WIDGET_MOUSEOVER == [None, []]
    assert get_cursor() == cur_none

    # Move from out to b2, this should call f1->f2->b2
    menu.update(PygameEventUtils.topleft_rect_mouse_motion(b2))
    assert test == [True, False, True, True, False, False]
    assert WIDGET_MOUSEOVER == [b2, [b2, cur_hand, [f2, cur_hand, [f1, cur_none, []]]]]
    assert menu.get_mouseover_widget() == b2
    assert get_cursor() == cur_arrow

    # Unpack b2
    f2.unpack(b2)
    if test != [False, False, False, False, False, False]:
        return
    assert WIDGET_MOUSEOVER == [None, []]
    assert get_cursor() == cur_none

    # Check b2
    menu.scroll_to_widget(b2)
    menu.update(PygameEventUtils.topleft_rect_mouse_motion(b2))
    assert test == [False, False, False, True, False, False]
    assert WIDGET_MOUSEOVER == [b2, [b2, cur_none, []]]
    assert get_cursor() == cur_arrow


def test_title():
    """Test frame title."""
    menu = MenuUtils.generic_menu(theme=THEME_NON_FIXED_TITLE)

    pad = 5
    frame = menu.add.frame_v(300, 200, background_color=(170, 170, 170), padding=pad, frame_id='f1')
    frame.set_cursor(pygame_menu.locals.CURSOR_HAND)
    frame._class_id__repr__ = True
    assert frame.get_scroll_value_percentage(ORIENTATION_VERTICAL) == -1
    frame_prev_rect = frame.get_rect()

    # with pytest.raises(ValueError): frame.get_title()
    frame._accepts_title = False
    with pytest.raises(pygame_menu.widgets.widget.frame._FrameDoNotAcceptTitle):
        frame.set_title('title')
    with pytest.raises(pygame_menu.widgets.widget.frame._FrameDoNotAcceptTitle):
        frame.add_title_button('none', None)
    with pytest.raises(pygame_menu.widgets.widget.frame._FrameDoNotAcceptTitle):
        frame.add_title_generic_button(None)  # type: ignore
    with pytest.raises(pygame_menu.widgets.widget.frame._FrameDoNotAcceptTitle):
        frame.remove_title()
    frame._accepts_title = True
    assert frame.get_size() == (300, 200)
    assert frame.get_title() == ''
    frame.set_onmouseover(lambda: print('over frame 1'))
    frame.set_onmouseleave(lambda: print('leave frame 1'))

    # Add a title
    assert frame not in menu._update_frames
    assert frame._title_height() == 0
    frame.set_title(
        'epic',
        padding_outer=3,
        title_font_size=20,
        padding_inner=(0, 3),
        title_font_color='white',
        title_alignment=pygame_menu.locals.ALIGN_CENTER
    )
    frame_title = frame.set_title(
        'epic',
        padding_outer=3,
        title_font_size=20,
        padding_inner=(0, 3),
        title_font_color='white',
        title_alignment=pygame_menu.locals.ALIGN_CENTER
    )
    frame_title.set_onmouseover(lambda: print('over title frame 1'))
    frame_title.set_onmouseleave(lambda: print('leave title frame 1'))
    assert frame in menu._update_frames  # Even if not scrollable
    assert frame._title_height() == 34
    assert frame._has_title
    assert frame.get_size() == (300, 234)
    assert frame.get_position() == (150 + pad, 73 + pad)
    assert len(frame._frame_title.get_widgets()) == 1  # The title itself
    assert frame._frame_title.get_widgets()[0].get_size() == (38, 28)
    assert frame._frame_title.get_widgets()[0].get_title() == 'epic'
    assert frame.get_title() == 'epic'
    assert frame._title_height() == 34
    assert frame.get_position() == (150 + pad, 73 + pad)
    assert frame._frame_title.get_position() == (156, 76)
    menu.render()
    assert frame.get_position() == (150 + pad, 56 + pad)
    assert frame._frame_title.get_position() == (156, 59)
    frame.pack(menu.add.button('Button', background_color='green'))

    # Test frame cannot set to itself
    with pytest.raises(AssertionError):
        frame_title.set_frame(frame_title)
    # Add button to title
    test = [False]

    def click_button(**kwargs) -> None:
        """
        Click button.
        """
        f = kwargs.pop('frame')
        b = kwargs.pop('button')
        assert f == frame
        assert isinstance(b, Button)
        test[0] = not test[0]
        # print('clicked')

    btn1 = frame.add_title_button(pygame_menu.widgets.FRAME_TITLE_BUTTON_CLOSE, click_button)
    btn2 = frame.add_title_button(pygame_menu.widgets.FRAME_TITLE_BUTTON_MAXIMIZE, click_button)
    btn3 = frame.add_title_button(pygame_menu.widgets.FRAME_TITLE_BUTTON_MINIMIZE, click_button)
    with pytest.raises(ValueError):
        frame.add_title_button('none', click_button)
    with pytest.raises(IndexError):
        frame.get_index(btn1)
    assert frame._frame_title.get_index(btn1) == 1
    assert frame._frame_title.get_index(btn2) == 2
    assert frame._frame_title.get_index(btn3) == 3
    assert not test[0]
    # menu.update(PygameEventUtils.middle_rect_click(btn1))
    # assert test[0]
    # menu.update(PygameEventUtils.middle_rect_click(btn2))
    # assert not test[0]
    # menu.update(PygameEventUtils.middle_rect_click(btn3))
    # assert test[0]

    # Scrollable widget
    # menu.add.vertical_margin(50)
    frame2 = menu.add.frame_v(300, 200, max_height=100, background_color='red', padding=pad, frame_id='f2')
    frame2._class_id__repr__ = True
    frame2.set_onmouseover(lambda: print('over frame 2'))
    frame2.set_onmouseleave(lambda: print('leave frame 2'))
    frame2_title = frame2.set_title('title',
                                    padding_outer=3,
                                    title_font_size=20,
                                    padding_inner=(0, 3),
                                    cursor=pygame_menu.locals.CURSOR_CROSSHAIR,
                                    title_font_color='white',
                                    title_alignment=pygame_menu.locals.ALIGN_CENTER,
                                    draggable=True)
    frame2_title.set_onmouseover(lambda: print('over title frame 2'))
    frame2_title.set_onmouseleave(lambda: print('leave title frame 2'))
    btn4 = frame2.add_title_button(pygame_menu.widgets.FRAME_TITLE_BUTTON_CLOSE, None)
    assert btn4.get_frame() == frame2._frame_title

    assert frame2.get_position() == (135, 235)
    assert frame2.get_size() == (310, 124)
    assert frame2._frame_title.get_position() == (141, 238)
    assert frame2._frame_title.get_size() == (304, 28)
    assert frame2.get_translate() == (0, 0)

    # Test events
    assert not frame2._frame_title.has_attribute('drag')
    menu.update(PygameEventUtils.middle_rect_click(frame2._frame_title))
    assert frame2._frame_title.has_attribute('drag')
    assert not frame2._frame_title.get_attribute('drag')
    menu.update(PygameEventUtils.middle_rect_click(frame2._frame_title, evtype=pygame.MOUSEBUTTONDOWN))
    assert frame2._frame_title.get_attribute('drag')
    menu.update(PygameEventUtils.mouse_motion(frame2._frame_title, rel=(10, 0)))
    assert frame2.get_translate() == (10, 0)
    menu.update(PygameEventUtils.mouse_motion(frame2._frame_title, rel=(0, -500)))
    assert frame2.get_translate() == (10, -235)  # Apply top limit
    menu.render()

    # Test drag with position way over the item
    menu.update(PygameEventUtils.mouse_motion(frame2._frame_title, rel=(0, 100), delta=(0, -100)))
    assert frame2.get_translate() == (10, -235)  # Apply top limit restriction

    menu.update(PygameEventUtils.middle_rect_click(frame2._frame_title))
    assert not frame2._frame_title.get_attribute('drag')

    # Test hide
    assert frame2._frame_title.is_visible()
    assert btn4.is_visible()
    frame2.hide()
    assert not frame2.is_visible()
    assert not frame2._frame_title.is_visible()
    assert not btn4.is_visible()
    frame2.show()
    assert frame2.is_visible()
    assert frame2._frame_title.is_visible()
    assert btn4.is_visible()

    # Remove title from frame 1
    frame.remove_title()
    assert frame._title_height() == 0
    assert frame not in menu._update_frames
    assert not frame._has_title

    menu.render()
    assert frame.get_rect().width == frame_prev_rect.width
    assert frame.get_rect().height == frame_prev_rect.height

    # Move frame 1 to bottom
    menu.update(PygameEventUtils.middle_rect_click(frame2._frame_title, evtype=pygame.MOUSEBUTTONDOWN))
    assert frame2._frame_title.get_attribute('drag')
    menu.render()
    menu.update(PygameEventUtils.mouse_motion(frame2._frame_title, rel=(0, 350)))
    assert frame2.get_translate() == (10, 115)
    menu.render()
    menu.update(PygameEventUtils.mouse_motion(frame2._frame_title, rel=(0, 100)))
    assert frame2.get_translate() == (10, 115)

    # Test more title gradients
    frame2.set_title('title', background_color=((10, 36, 106), (166, 202, 240), True, True))
    frame2.set_title('title', background_color=((10, 36, 106), (166, 202, 240), True, False))
    frame2.set_title('title', background_color=((10, 36, 106), (166, 202, 240), False, False))

    frame2.set_frame(frame_title)
    frame2.set_scrollarea(frame2.get_scrollarea())


def test_resize():
    """Test resize."""
    menu = MenuUtils.generic_menu()

    # No title, no scrollable
    frame = menu.add.frame_v(300, 200, background_color=(170, 170, 170), frame_id='f1')
    assert frame.get_size() == (300, 200)

    # Resize
    frame.resize(400, 400)
    assert frame.get_size() == (400, 400)

    # No title, scrollable to non-scrollable
    frame2 = menu.add.frame_v(300, 200, background_color=(170, 170, 170), frame_id='f2', max_width=200,
                              max_height=100)
    assert frame2.get_size() == (204, 112)
    frame2.resize(400, 400)  # Now it's not scrollable
    assert not frame2.is_scrollable
    assert frame2.get_size() == (400, 400)
    with pytest.raises(AssertionError):
        frame2.resize(400, 400, max_width=300, max_height=200)
    # No title, scrollable to scrollable
    frame3 = menu.add.frame_v(300, 200, background_color=(170, 170, 170), frame_id='f3', max_width=200,
                              max_height=100)
    assert frame3.is_scrollable
    frame3.resize(400, 400, max_width=300, max_height=300)
    assert frame3.get_size() == (320, 320)
    assert frame3.is_scrollable

    # Title, no scrollable
    frame4 = menu.add.frame_v(300, 200, background_color=(170, 170, 170), frame_id='f4')
    frame4title = frame4.set_title('generic title')
    btn1 = frame4.add_title_button(pygame_menu.widgets.FRAME_TITLE_BUTTON_CLOSE, lambda: print(''))
    btn2 = frame4.add_title_button(pygame_menu.widgets.FRAME_TITLE_BUTTON_MINIMIZE, lambda: print(''))
    frame4title_widgets = frame4._frame_title.get_widgets()
    label = frame4title_widgets[0]
    assert frame4title_widgets == (label, btn1, btn2)

    frame4.resize(600, 600)
    new_frame4title_widgets = frame4._frame_title.get_widgets()
    label = new_frame4title_widgets[0]
    assert frame4.get_size() == (600, 641 if PYGAME_V2 else 642)  # Plus title height
    assert frame4title != frame4._frame_title
    assert new_frame4title_widgets == (label, btn1, btn2)
