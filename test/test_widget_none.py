"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - NONE
Test NoneWidget, HMargin, VFill, VMargin and MenuLink widgets.
"""

import math

import pytest

import pygame_menu
import pygame_menu.controls as ctrl
from pygame_menu.widgets import NoneSelection, NoneWidget
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented
from test._utils import MenuUtils, PygameEventUtils, surface


def test_none_widget_behavior():
    menu = MenuUtils.generic_menu()

    widgets = [
        NoneWidget(),
        menu.add.vertical_margin(10),
        menu.add.horizontal_margin(10),
        menu.add.vertical_fill(10),
    ]

    for wid in widgets:
        wid.set_margin(9, 9)
        assert wid.get_margin() == (0, 0)

        wid.set_padding(9)
        assert wid.get_padding() == (0, 0, 0, 0)

        wid.set_background_color((1, 1, 1))
        wid._draw_background_color(surface)
        assert wid._background_color is None

        no_sel = NoneSelection()
        wid.set_selection_effect(no_sel)
        assert wid.get_selection_effect() != no_sel

        wid.set_title("none")
        assert wid.get_title() == ""

        r = wid.get_rect(inflate=(10, 10))
        assert r.x == 0
        assert r.y == 0

        assert not wid.is_selectable
        assert wid.is_visible()

        wid.apply()
        wid.change()

        wid.set_font("myfont", 0, (1, 1, 1), (1, 1, 1), (1, 1, 1), (0, 0, 0), (0, 0, 0))
        wid.update_font({"name": ""})
        wid._apply_font()
        assert wid._font is None

        surf = wid._render_string("nice", (1, 1, 1))
        assert surf.get_width() == 0
        assert surf.get_height() == 0

        wid._apply_transforms()

        wid.hide()
        assert not wid.is_visible()
        wid.show()
        assert wid.is_visible()

        with pytest.raises(ValueError):
            wid.get_value()

        surf = wid.get_surface()
        assert surf.get_width() == 0
        assert surf.get_height() == 0

        wid.set_position(1, 1)
        assert wid.get_position() == (0, 0)

        with pytest.raises(WidgetTransformationNotImplemented):
            wid.translate(1, 1)
        assert wid.get_translate() == (0, 0)

        with pytest.raises(WidgetTransformationNotImplemented):
            wid.rotate(10)
        assert wid._angle == 0

        with pytest.raises(WidgetTransformationNotImplemented):
            wid.resize(10, 10)
        assert wid._scale[0] is False
        assert wid._scale[1] == 1
        assert wid._scale[2] == 1

        with pytest.raises(WidgetTransformationNotImplemented):
            wid.scale(100, 100)
        assert wid._scale[0] is False
        assert wid._scale[1] == 1
        assert wid._scale[2] == 1

        with pytest.raises(WidgetTransformationNotImplemented):
            wid.flip(True, True)
        assert wid._flip == (False, False)

        with pytest.raises(WidgetTransformationNotImplemented):
            wid.set_max_width(100)
        assert wid._max_width[0] is None

        with pytest.raises(WidgetTransformationNotImplemented):
            wid.set_max_height(100)
        assert wid._max_height[0] is None

        wid.select()
        assert not wid.is_selected()
        assert not wid.is_selectable

        wid.set_sound(None)
        assert wid._sound is not None

        wid.set_border(1, (0, 0, 0), (0, 0))
        assert wid._border_width == 0
        assert wid.get_selected_time() == 0

        def my_event():
            return

        wid.set_onchange(my_event)
        assert wid._onchange is None
        wid.set_onmouseover(my_event)
        assert wid._onmouseover is None
        wid.set_onmouseleave(my_event)
        assert wid._onmouseleave is None
        wid.set_onselect(my_event)
        assert wid._onselect is None
        wid.set_onreturn(my_event)
        assert wid._onreturn is None

        wid.mouseleave()
        wid.mouseover()
        wid._mouseover = True
        wid._check_mouseover()
        assert wid._mouseover is False


def test_draw_update_callbacks():
    wid = NoneWidget()

    draw_flag = [False]

    def _draw(*_):
        draw_flag[0] = True

    draw_id = wid.add_draw_callback(_draw)
    assert isinstance(draw_id, str)

    wid.draw(surface)
    assert draw_flag[0] is True

    draw_flag[0] = False
    wid.remove_draw_callback(draw_id)

    with pytest.raises(IndexError):
        wid.remove_draw_callback(draw_id)

    wid.draw(surface)
    assert draw_flag[0] is False

    update_flag = [False]

    def _update(*_):
        update_flag[0] = True

    update_id = wid.add_update_callback(_update)
    assert isinstance(update_id, str)

    assert wid.update(surface) is False
    assert update_flag[0] is True

    update_flag[0] = False
    wid.remove_update_callback(update_id)

    with pytest.raises(IndexError):
        wid.remove_update_callback(update_id)

    wid.update(surface)
    assert update_flag[0] is False


def test_hmargin():
    w = pygame_menu.widgets.HMargin(999)
    w._render()

    assert w.get_rect().width == 999
    assert w.get_rect().height == 0
    assert not w.update([])
    assert w._font_size == 0
    assert w.get_margin() == (0, 0)

    w.draw(surface)

    menu = MenuUtils.generic_menu()
    w2 = menu.add.horizontal_margin(999)
    assert w2.get_rect().width == 999
    assert w2.get_rect().height == 0


def test_vfill():
    menu = MenuUtils.generic_menu()
    b = menu.add.button("nice")
    bh = b.get_height()

    assert menu.get_height(widget=True) == bh
    assert menu.get_size(widget=True) == b.get_size()

    vf1 = menu.add.vertical_fill()
    assert vf1.get_width() == 0
    assert vf1.get_height() == menu.get_height(inner=True) - bh - 1
    assert menu.get_height(inner=True) - 1 == menu.get_height(widget=True)

    vf2 = menu.add.vertical_fill()
    assert vf1.get_height() == vf2.get_height() + 1

    menu = MenuUtils.generic_menu()
    b1 = menu.add.button(1)
    vf1 = menu.add.vertical_fill()
    menu.add.button(2)
    vf2 = menu.add.vertical_fill()
    menu.add.button(3)
    vf3 = menu.add.vertical_fill()
    menu.add.button(4)

    assert vf1.get_width() == 0
    assert vf1.get_height() == vf2.get_height()
    assert vf2.get_height() == vf3.get_height() + 1

    prev_height = vf1.get_height()

    added = []
    for i in range(5, 10):
        added.append(menu.add.button(i))

    assert vf1.get_height() == 0
    assert vf2.get_height() == 0
    assert vf3.get_height() == 0

    for b in added:
        menu.remove_widget(b)

    assert vf1.get_height() == prev_height

    total = vf1.get_height() + vf2.get_height() + vf3.get_height()
    vf2.hide()
    total_after = vf1.get_height() + vf3.get_height()

    assert vf1.get_height() == vf3.get_height() + 1
    assert abs(total - total_after) <= 1

    vf2.show()
    assert total == vf1.get_height() + vf2.get_height() + vf3.get_height()

    vf1_prev = vf1.get_height()
    b1_height = math.ceil(b1.get_height() / 3)

    b1.hide()
    assert abs(vf1.get_height() - (vf1_prev + b1_height)) <= 1

    b1.show()
    assert vf1.get_height() == vf1_prev

    menu = MenuUtils.generic_menu()
    b = menu.add.button(1)
    v = menu.add.vertical_fill(10)

    assert v.get_height() == menu.get_height(inner=True) - b.get_height() - 1

    for i in range(20):
        menu.add.button(i)

    assert v.get_height() == 10

    menu = MenuUtils.generic_menu(
        theme=pygame_menu.Theme(widget_alignment=pygame_menu.locals.ALIGN_LEFT)
    )

    vf1 = menu.add.vertical_fill()
    assert menu.get_size(widget=True) == (0, vf1.get_height())
    assert vf1.get_height() == menu.get_height(inner=True) - 1

    b = menu.add.button("nice")
    assert menu.get_size(widget=True) == (
        b.get_width(),
        b.get_height() + vf1.get_height(),
    )

    vf2 = menu.add.vertical_fill()
    assert menu.get_size(widget=True) == (
        b.get_width(),
        b.get_height() + vf1.get_height() + vf2.get_height(),
    )


def test_vmargin():
    menu = MenuUtils.generic_menu()
    w = menu.add.vertical_margin(999)
    w._render()

    assert w.get_rect().width == 0
    assert w.get_rect().height == 999
    assert not w.update([])
    assert w._font_size == 0
    assert w.get_margin() == (0, 0)

    w.draw(surface)


def test_menu_link():
    menu = MenuUtils.generic_menu()
    menu1 = MenuUtils.generic_menu(title="Menu1", theme=pygame_menu.themes.THEME_BLUE)
    menu1.add.button("Back", pygame_menu.events.BACK)

    menu2 = MenuUtils.generic_menu(title="Menu2", theme=pygame_menu.themes.THEME_ORANGE)
    menu2.add.button("Back", pygame_menu.events.BACK)

    menu3 = MenuUtils.generic_menu(title="Menu3", theme=pygame_menu.themes.THEME_GREEN)
    menu3.add.button("Back", pygame_menu.events.BACK)

    btn1 = menu.add.button("menu1", menu1)
    btn2 = menu.add.button("menu2", menu2)
    btn3 = menu.add.button("menu3", menu3)

    btn1.hide()
    btn2.hide()
    btn3.hide()

    assert menu.get_current() is menu
    btn1.apply()
    assert menu.get_current() is menu1

    menu.full_reset()
    assert menu.get_current() is menu

    link = menu.add.menu_link(menu2)
    link.open()
    assert menu.get_current() is menu2

    menu.full_reset()
    assert menu.get_current() is menu

    assert not link.is_visible()
    link.hide()
    assert not link.is_visible()
    link.show()
    assert not link.is_visible()

    with pytest.raises(ValueError):
        menu.add.menu_link(menu)

    with pytest.raises(ValueError):
        menu.add.menu_link(True)  # type: ignore

    def open_link(*args):
        _link = args[-1]
        assert isinstance(_link, pygame_menu.widgets.MenuLink)
        _link.open()

    sel = menu.add.selector(
        "Change menu ",
        [
            ("Menu 1", menu.add.menu_link(menu1)),
            ("Menu 2", menu.add.menu_link(menu2)),
            ("Menu 3", menu.add.menu_link(menu3)),
        ],
        onreturn=open_link,
        style=pygame_menu.widgets.SELECTOR_STYLE_FANCY,
    )

    sel.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))


def test_value_errors():
    menu = MenuUtils.generic_menu()
    menu2 = MenuUtils.generic_menu()

    widgets = [
        menu.add.none_widget(),
        menu.add.vertical_margin(1),
        menu.add.horizontal_margin(1),
        menu.add.menu_link(menu2),
    ]

    for w in widgets:
        with pytest.raises(ValueError):
            w.get_value()
        with pytest.raises(ValueError):
            w.set_value("value")
        with pytest.raises(ValueError):
            w.set_default_value("value")

        assert not w.value_changed()
        w.reset_value()


def test_shadow():
    menu = MenuUtils.generic_menu()
    w = menu.add.vertical_margin(1)

    w.shadow(10, 10)
    assert not w._shadow["enabled"]
