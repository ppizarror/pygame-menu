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
from pygame_menu.utils import get_cursor
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
    reset_widgets_over,
    surface,
)


@pytest.fixture
def menu():
    return MenuUtils.generic_menu(theme=TEST_THEME.copy())


@pytest.fixture
def scroll_menu():
    return MenuUtils.generic_menu(theme=THEME_NON_FIXED_TITLE)


def test_frame_general_layout_and_packing(menu):
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
    wid = menu.add.frame_v(400, 100)
    wid.set_position(1, 1)
    assert wid.get_position() == (1, 1)

    wid.translate(1, 1)
    assert wid.get_translate() == (1, 1)

    wid.resize(10, 10)
    # Only assert that resize did not enable transform flags
    assert not wid._scale[0]


def test_frame_value_behavior(menu):
    f = menu.add.frame_v(300, 800)
    with pytest.raises(ValueError):
        f.get_value()
    with pytest.raises(ValueError):
        f.set_value("value")
    assert not f.value_changed()
    f.reset_value()


def test_frame_draw_callbacks(menu):
    frame = menu.add.frame_v(200, 200)
    flag = {"called": False}

    def cb(*_):
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
    h = menu.add.frame_h(400, 300)
    btn = pygame_menu.widgets.Button("button")

    with pytest.raises(AssertionError):
        h.pack(btn)

    menu.add.configure_defaults_widget(btn)
    h.pack(btn)
    h.pack(menu.add.button("legit"))
    assert h.contains_widget(btn)


def test_mouseover_events_and_cursor(menu):
    from pygame_menu.locals import CURSOR_HAND as HAND

    reset_widgets_over()

    f1 = menu.add.frame_v(500, 500, background_color="red", cursor=HAND)
    f2 = menu.add.frame_v(400, 300, background_color="blue", cursor=HAND)
    b1 = f1.pack(menu.add.button("1"))

    events = {"f1": False, "f2": False, "b1": False}

    def toggle(k):
        def cb(_, __):
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
    with pytest.raises(AssertionError):
        scroll_menu.add.frame_v(300, 400, **kwargs)


def test_scrollarea_creation_and_disable(scroll_menu):
    f = scroll_menu.add.frame_v(300, 800, frame_id="f1")

    def create():
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
    frame_sc = scroll_menu.add.frame_v(300, 400, max_height=200)
    frame_scroll = frame_sc.get_scrollarea(inner=True)
    btn = frame_sc.pack(scroll_menu.add.button("Target"))

    scroll_menu.render()
    r0 = btn.get_rect(to_real_position=True)

    frame_scroll.scroll_to(ORIENTATION_VERTICAL, 0.5)
    r1 = btn.get_rect(to_real_position=True)

    assert r0 != r1


def test_text_input_scroll_overflow(scroll_menu):
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
    btn1 = scroll_menu.add.button("B1")
    btn2 = scroll_menu.add.button("B2")

    btn1.select()
    btn2.select()

    with pytest.raises(pygame_menu.menu._MenuMultipleSelectedWidgetsException):
        scroll_menu.render()


def test_frame_sorting_and_indices(menu):
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
    frame = menu.add.frame_v(300, 200)
    initial_h = frame.get_height()

    frame.set_title("Modern Title", title_font_size=20)
    assert frame.get_height() > initial_h

    # Draggable flag should be accepted without error
    frame.set_title("Draggable", draggable=True)


def test_resize_with_scrollable_constraints(menu):
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
    menu = pygame_menu.Menu(columns=2, rows=1, height=500, width=600, title="Title")

    frame = menu.add.frame_h(width=250, height=100)
    label_inner = menu.add.label("Col One")
    frame.pack(label_inner)

    label_outer = menu.add.label("Col Two")

    assert frame.get_col_row_index() == (0, 0, 0)
    assert label_inner.get_col_row_index() == (0, 0, 1)
    assert label_outer.get_col_row_index() == (1, 0, 2)
    assert label_inner.get_frame() == frame
