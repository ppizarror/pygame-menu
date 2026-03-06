"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGETS
Test general widget properties.
"""

import copy

import pygame
import pytest

import pygame_menu
from pygame_menu.locals import (
    POSITION_CENTER,
    POSITION_EAST,
    POSITION_NORTH,
    POSITION_NORTHEAST,
    POSITION_NORTHWEST,
    POSITION_SOUTH,
    POSITION_SOUTHEAST,
    POSITION_SOUTHWEST,
    POSITION_WEST,
)
from pygame_menu.widgets import Button, Label
from pygame_menu.widgets.core.widget import AbstractWidgetManager, Widget
from test._utils import (
    PYGAME_V2,
    TEST_THEME,
    MenuUtils,
    PygameEventUtils,
    surface,
    test_reset_surface,
)


@pytest.fixture(autouse=True)
def setup_widgets_test() -> None:
    """
    Setup widgets test.
    """
    test_reset_surface()


@pytest.mark.parametrize(
    "method_call",
    [
        lambda wm: wm._theme,
        lambda wm: wm._add_submenu(None, None),
        lambda wm: wm._filter_widget_attributes({}),
        lambda wm: wm._configure_widget(None),
        lambda wm: wm._check_kwargs({}),
        lambda wm: wm._append_widget(None),
        lambda wm: wm.configure_defaults_widget(None),
    ],
)
def test_abstract_widget_manager(method_call) -> None:
    """
    Test abstract widget manager raises NotImplementedError for all abstract methods.
    """
    wm = AbstractWidgetManager()
    with pytest.raises(NotImplementedError):
        method_call(wm)


def test_abstract_widget() -> None:
    """
    Test an abstract widget.
    """
    w = Widget()

    w.readonly = True
    w.change()

    w.lock_position = True
    w.set_position(1, 1)
    assert w.get_position() == (0, 0)

    with pytest.raises(NotImplementedError):
        w._render()
    with pytest.raises(NotImplementedError):
        w._draw(surface)
    with pytest.raises(NotImplementedError):
        w._apply_font()
    with pytest.raises(NotImplementedError):
        w.update([])

    assert w._get_menu_widgets() == []
    assert w._get_menu_update_widgets() == []

    w._selected = True
    assert w.get_selected_time() > 0


def test_kwargs() -> None:
    """
    Test kwargs addition.
    """

    def function_kwargs(*args, **kwargs) -> None:
        """
        Button callback.
        """
        assert len(args) == 0
        kwargs_k = list(kwargs.keys())
        assert kwargs_k[0] == "test"
        assert kwargs_k[1] == "widget"

    menu = MenuUtils.generic_menu()
    with pytest.raises(ValueError):
        menu.add.button("btn", function_kwargs, test=True)
    btn = menu.add.button(
        "btn", function_kwargs, test=True, accept_kwargs=True, padding=10
    )
    assert len(btn._kwargs) == 1
    with pytest.raises(KeyError):
        btn.add_self_to_kwargs("test")
    assert len(btn._kwargs) == 1
    btn.add_self_to_kwargs()
    assert len(btn._kwargs) == 2
    assert btn._kwargs["widget"] == btn
    btn.apply()


def test_copy() -> None:
    """
    Test widget copy.
    """
    widget = pygame_menu.widgets.Widget()
    with pytest.raises(pygame_menu.widgets.core.widget._WidgetCopyException):
        copy.copy(widget)
    with pytest.raises(pygame_menu.widgets.core.widget._WidgetCopyException):
        copy.deepcopy(widget)


def test_onselect() -> None:
    """
    Test onselect widgets.
    """
    menu = MenuUtils.generic_menu()
    test = [None]

    def on_select(selected, widget, _) -> None:
        """
        Callback.
        """
        if selected:
            test[0] = widget

    # Button
    assert test[0] is None
    btn = menu.add.button("nice", onselect=on_select)  # The first to be selected
    assert test[0] == btn

    btn2 = menu.add.button("nice", onselect=on_select)
    assert test[0] == btn
    btn2.is_selectable = False
    btn2.select(update_menu=True)
    assert test[0] == btn
    btn2.is_selectable = True
    btn2.select(update_menu=True)
    assert test[0] == btn2
    btn.scale(1, 1)

    # Color
    color = menu.add.color_input("nice", "rgb", onselect=on_select)
    color.select(update_menu=True)
    assert test[0] == color

    # Image
    image = menu.add.image(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
        onselect=on_select,
        font_color=(2, 9),
    )
    image.select(update_menu=True)
    assert test[0] == color
    image.is_selectable = True
    image.select(update_menu=True)
    assert test[0] == image

    # Label
    label = menu.add.label("label", onselect=on_select)
    label.is_selectable = True
    label.select(update_menu=True)
    assert test[0] == label

    # None, it cannot be selected
    none = menu.add.none_widget()
    none.select(update_menu=True)
    assert test[0] == label

    # Selector
    selector = menu.add.selector("nice", ["nice", "epic"], onselect=on_select)
    selector.select(update_menu=True)
    assert test[0] == selector

    # Textinput
    text = menu.add.text_input("nice", onselect=on_select)
    text.select(update_menu=True)
    assert test[0] == text

    # Vmargin
    vmargin = menu.add.vertical_margin(10)
    vmargin.select(update_menu=True)
    assert test[0] == text


def test_non_ascii() -> None:
    """
    Test non-ascii.
    """
    menu = MenuUtils.generic_menu()
    m = MenuUtils.generic_menu(title="Ménu")
    m.clear()
    menu.add.button("0", pygame_menu.events.NONE)
    menu.add.button("Test", pygame_menu.events.NONE)
    menu.add.button("Menú", pygame_menu.events.NONE)
    menu.add.color_input("Cólor", "rgb")
    text = menu.add.text_input("Téxt")
    menu.add.label("Téxt")
    menu.add.selector("Sélect".encode("latin1"), [("a", "a")])
    menu.enable()
    menu.draw(surface)

    # Text text input
    text.set_value("ą, ę, ś, ć, ż, ź, ó, ł, ń")
    assert text.get_value() == "ą, ę, ś, ć, ż, ź, ó, ł, ń"
    text.set_value("")
    text.update(PygameEventUtils.key(pygame.K_l, char="ł", keydown=True))
    assert text.get_value() == "ł"


@pytest.mark.parametrize(
    "color_input,expected_output",
    [
        ((255, 255, 255), (255, 255, 255, 255)),
        ("#ff00ff", (255, 0, 255, 255)),
        ("#f0f", (255, 0, 255, 255)),
    ],
)
def test_background(color_input, expected_output) -> None:
    """
    Test widget background with parametrized colors.
    """
    menu = MenuUtils.generic_menu()
    w = menu.add.label("Text")

    if isinstance(color_input, tuple) and len(color_input) == 3:
        w.set_background_color(color_input, (10, 10))
        w.draw(surface)
        assert w._background_inflate[0] == 10
        assert w._background_inflate[1] == 10
    else:
        w.set_background_color(color_input)

    assert w._background_color == expected_output
    w.draw(surface)


def test_background_baseimage() -> None:
    """
    Test widget background with BaseImage.
    """
    menu = MenuUtils.generic_menu()
    w = menu.add.label("Text")

    w.set_background_color((255, 255, 255), (10, 10))
    assert w._background_color == (255, 255, 255, 255)
    w.draw(surface)
    w.set_background_color(
        pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    )
    w.draw(surface)


def test_max_width_height() -> None:
    """
    Test widget max width/height.
    """
    label = Label("my label is really long yeah, it should be scaled in the width")
    label.set_font(
        pygame_menu.font.FONT_OPEN_SANS,
        25,
        (255, 255, 255),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
    )
    label.render()

    # The padding is zero, also the selection box and all transformations
    assert label.get_width() == 686
    assert label.get_height() == 35
    assert label.get_size()[0] == 686
    assert label.get_size()[1] == 35

    # Add padding, this will increase the width of the widget
    label.set_padding(58)
    assert label.get_width() == 802

    # Apply scaling
    label.scale(0.5, 0.5)
    assert label.get_width() == 401
    label.scale(0.5, 0.5)
    assert label.get_width() == 401
    assert label.get_padding()[0] == 28
    assert label.get_padding(transformed=False)[0] == 58

    # Set size
    label.resize(450, 100)
    assert label.get_width() == 448
    assert label.get_height() == 99

    # Set size back
    label.scale(1, 1)
    label.set_padding(0)
    assert label.get_width() == 686
    assert label.get_height() == 35

    # Test max width
    label.scale(2, 2)
    label.set_padding(52)
    label.set_max_width(250)
    assert not label._scale[0]  # max width disables scale
    assert label.get_width() == 249
    assert label.get_height() == 35 + 52 * 2

    # Apply the same, but this time height is scaled
    label.set_max_width(250, scale_height=True)
    assert label.get_height() == 113

    # Set max height, this will disable max width
    label.set_max_height(100)
    assert label._max_width[0] is None
    assert label.get_height() == 99

    # Scale, disable both max width and max height
    label.set_max_width(100)
    label.set_max_height(100)
    label.scale(1.5, 1.5)
    assert label._max_width[0] is None
    assert label._max_height[0] is None
    assert label._scale[0]

    # Set scale back
    label.scale(1, 1)
    label.set_padding(0)
    assert label.get_width() == 686
    assert label.get_height() == 35


def test_visibility() -> None:
    """
    Test widget visibility.
    """
    menu = MenuUtils.generic_menu()
    w = menu.add.label("Text")
    last_hash = w._last_render_hash
    w.hide()
    assert not w.is_visible()
    assert w._last_render_hash != last_hash
    last_hash = w._last_render_hash
    w.show()
    assert w.is_visible()
    assert w._last_render_hash != last_hash

    w = Button("title")
    menu.add.generic_widget(w)
    w.hide()


@pytest.mark.parametrize(
    "position",
    [
        POSITION_NORTHWEST,
        POSITION_NORTH,
        POSITION_NORTHEAST,
        POSITION_EAST,
        POSITION_SOUTHEAST,
        POSITION_SOUTH,
        POSITION_SOUTHWEST,
        POSITION_WEST,
        POSITION_CENTER,
    ],
)
def test_font_shadow_positions(position) -> None:
    """
    Test widget font shadow on all positions.
    """
    menu = MenuUtils.generic_menu()
    w = menu.add.label("Text")
    w.set_font_shadow(position=position)


def test_font() -> None:
    """
    Test widget font.
    """
    menu = MenuUtils.generic_menu()

    w = menu.add.label("Text")  # type: Label
    with pytest.raises(AssertionError):
        w.update_font({})
    w.update_font({"color": (255, 0, 0)})

    # Default color
    w._selected = False
    assert w.get_font_color_status() == w._font_color

    # Readonly color
    w.readonly = True
    assert w.get_font_color_status() == w._font_readonly_color

    # Read only + selected color
    w._selected = True
    assert w.get_font_color_status() == w._font_readonly_selected_color

    # Selected only color
    w.readonly = False
    assert w.get_font_color_status() == w._font_selected_color

    # Default color
    w._selected = False
    assert w.get_font_color_status() == w._font_color


@pytest.mark.parametrize(
    "padding_input,expected_output",
    [
        (25, (25, 25, 25, 25)),
        ((25, 50, 75, 100), (25, 50, 75, 100)),
        ((25, 50), (25, 50, 25, 50)),
        ((25, 75, 50), (25, 75, 50, 75)),
    ],
)
def test_padding_valid(padding_input, expected_output) -> None:
    """
    Test widget padding with valid inputs.
    """
    menu = MenuUtils.generic_menu()
    w = menu.add.button(0, pygame_menu.events.NONE, padding=padding_input)
    assert w.get_padding() == expected_output


@pytest.mark.parametrize(
    "invalid_padding",
    [
        -1,
        "a",
        (0, 0, 0, 0, 0),
        (0, 0, -1, 0),
        (0, 0, "a", 0),
    ],
)
def test_padding_invalid(invalid_padding) -> None:
    """
    Test widget padding with invalid inputs.
    """
    menu = MenuUtils.generic_menu()
    with pytest.raises(Exception):
        menu.add.button(0, pygame_menu.events.NONE, padding=invalid_padding)


def test_draw_callback() -> None:
    """
    Test drawing callback.
    """
    menu = MenuUtils.generic_menu()

    def call(widget, _) -> None:
        """
        Callback.
        """
        widget.set_attribute("attr", True)

    btn = menu.add.button("btn")
    call_id = btn.add_draw_callback(call)
    assert not btn.get_attribute("attr", False)
    menu.draw(surface)
    assert btn.get_attribute("attr", False)
    btn.remove_draw_callback(call_id)
    with pytest.raises(IndexError):
        btn.remove_draw_callback(call_id)  # Already removed
    menu.disable()


def test_update_callback() -> None:
    """
    Test update callback.
    """

    def update(event, widget, _) -> None:
        """
        Callback.
        """
        assert isinstance(event, list)
        widget.set_attribute("attr", True)

    menu = MenuUtils.generic_menu(theme=TEST_THEME.copy())
    btn = menu.add.button("button", lambda: print("Clicked"))
    call_id = btn.add_update_callback(update)
    assert not btn.get_attribute("attr", False)
    click_pos = btn.get_rect(to_real_position=True).center
    deco = menu.get_decorator()

    def draw_rect() -> None:
        """
        Draw absolute rect on surface for testing purposes.
        """
        surface.fill((0, 255, 0), btn.get_rect(to_real_position=True))

    deco.add_callable(draw_rect, prev=False, pass_args=False)
    click_pos_absolute = btn.get_rect(to_absolute_position=True).center
    assert click_pos != click_pos_absolute
    assert (
        menu.get_scrollarea()._view_rect
        == menu.get_scrollarea().get_absolute_view_rect()
    )
    assert btn.get_scrollarea() == menu.get_current().get_scrollarea()

    if PYGAME_V2:
        assert btn.get_rect() == pygame.Rect(253, 153, 94, 41)
        assert btn.get_rect(to_real_position=True) == pygame.Rect(253, 308, 94, 41)
    else:
        assert btn.get_rect() == pygame.Rect(253, 152, 94, 42)
        assert btn.get_rect(to_real_position=True) == pygame.Rect(253, 307, 94, 42)

    assert len(menu._update_frames) == 0
    assert len(menu.get_current()._update_frames) == 0
    btn.update(
        PygameEventUtils.mouse_click(click_pos[0], click_pos[1])
    )  # MOUSEBUTTONUP
    assert btn.get_attribute("attr", False)
    btn.set_attribute("attr", False)
    btn.remove_update_callback(call_id)
    with pytest.raises(IndexError):
        btn.remove_update_callback(call_id)
    assert not btn.get_attribute("attr", False)
    btn.update(PygameEventUtils.mouse_click(click_pos[0], click_pos[1]))
    assert not btn.get_attribute("attr", False)

    def update2(event, widget, _) -> None:
        """
        Callback.
        """
        assert isinstance(event, list)
        widget.set_attribute("epic", "bass")

    btn.add_update_callback(update2)
    assert not btn.has_attribute("epic")
    btn.draw(surface)
    assert not btn.has_attribute("epic")
    btn.update(PygameEventUtils.mouse_click(click_pos[0], click_pos[1]))
    assert btn.has_attribute("epic")
    btn.remove_attribute("epic")
    with pytest.raises(IndexError):
        btn.remove_attribute("epic")
    assert not btn.has_attribute("epic")


@pytest.mark.parametrize(
    "border_width,border_color,border_inflate",
    [
        (-1, "black", (1, 1)),  # Invalid negative width
        (1.5, "black", (1, 1)),  # Invalid float width
        (1, (0, 0, 0), (-1, -1)),  # Invalid negative inflate
    ],
)
def test_border_invalid(border_width, border_color, border_inflate) -> None:
    """
    Test widget border with invalid parameters.
    """
    menu = MenuUtils.generic_menu()
    with pytest.raises(AssertionError):
        menu.add.button(
            "",
            border_width=border_width,
            border_color=border_color,
            border_inflate=border_inflate,
        )


def test_border_valid() -> None:
    """
    Test widget border with valid parameters.
    """
    menu = MenuUtils.generic_menu()
    btn = menu.add.button(
        "", border_width=1, border_color=(0, 0, 0), border_inflate=(1, 1)
    )
    assert btn._border_width == 1
    assert btn._border_color == (0, 0, 0, 255)
    assert btn._border_inflate == (1, 1)
    assert (
        btn._border_position
        == pygame_menu.widgets.core.widget.WIDGET_BORDER_POSITION_FULL
    )


@pytest.mark.parametrize(
    "position",
    [
        POSITION_NORTH,
        POSITION_SOUTH,
        POSITION_EAST,
        POSITION_WEST,
    ],
)
def test_border_positions(position) -> None:
    """
    Test widget border on different positions.
    """
    menu = MenuUtils.generic_menu()
    btn = menu.add.button(
        "", border_width=1, border_color="black", border_inflate=(1, 1)
    )
    btn.set_border(1, "black", (1, 1), position)
    btn._draw_border(surface)


def test_border_invalid_position() -> None:
    """
    Test widget border with invalid position.
    """
    menu = MenuUtils.generic_menu()
    with pytest.raises(AssertionError):
        btn = menu.add.button(
            "", border_width=1, border_color=(0, 0, 0), border_inflate=(1, 1)
        )
        btn.set_border(1, "black", (1, 1), POSITION_SOUTHEAST)


def test_border_edge_cases() -> None:
    """
    Test widget border edge cases.
    """
    menu = MenuUtils.generic_menu()
    btn = menu.add.button(
        "", border_width=1, border_color=(0, 0, 0), border_inflate=(1, 1)
    )
    btn._draw_border(surface)

    # Invalid border position list
    btn._border_position = [POSITION_SOUTHEAST]
    with pytest.raises(RuntimeError):
        btn._draw_border(surface)

    # None border
    btn._border_position = pygame_menu.widgets.core.widget.WIDGET_BORDER_POSITION_NONE
    btn._draw_border(surface)

    # Invalid border position string
    btn._border_position = "invalid"
    with pytest.raises(RuntimeError):
        btn._draw_border(surface)


def test_scale_maxwidth_height() -> None:
    """
    Test the interaction between scale, max width and max height.
    """
    menu = MenuUtils.generic_menu()
    btn = menu.add.button("button")

    btn.scale(1, 1)
    btn.scale(2, 3)

    assert btn._scale[0]
    assert btn._scale[1] == 2
    assert btn._scale[2] == 3

    # Now, set max width
    btn.set_max_width(150)
    assert not btn._scale[0]

    btn.set_max_height(150)
    assert not btn._scale[0]
    assert btn._max_width[0] is None

    btn.scale(2, 2)
    assert btn._max_height[0] is None
    assert btn._scale[0]
    assert btn._scale[1] == 2
    assert btn._scale[2] == 2


def test_widget_floating_zero() -> None:
    """
    Test widgets with zero position if floated.
    """
    menu = MenuUtils.generic_menu(title="Example menu")
    img = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU)
    img.scale(0.3, 0.3)
    image_widget = menu.add.image(image_path=img.copy())
    image_widget.set_border(1, "black")
    image_widget.set_float(origin_position=True)
    menu.render()

    # Test position
    assert image_widget.get_position() == (8, 60)

    # Image translate
    image_widget.translate(100, 100)
    assert image_widget.get_position() == (8, 60)

    # Render, then update the position
    menu.render()
    assert image_widget.get_position() == (108, 160)

    image_widget.translate(-50, 0)
    menu.render()
    assert image_widget.get_position() == (-42, 60)


def test_widget_center_overflow_ignore_scrollbar_thickness() -> None:
    """
    Test widget centering if overflow ignores scrollbar thickness.
    """
    theme = TEST_THEME.copy()

    menu = MenuUtils.generic_menu(width=320, theme=theme)
    for i in range(5):
        menu.add.button(f"Option{i + 1}")
        menu.add.button("Quit", pygame_menu.events.EXIT)

    pos_before = menu.get_selected_widget().get_position()
    theme.widget_alignment_ignore_scrollbar_thickness = True
    menu.render()
    pos_after = menu.get_selected_widget().get_position()

    # If we ignore scrollbar thickness in position, the difference
    # should be equal to half the scrollbar thickness (because centering)
    scrollbar_thickness = menu._get_scrollbar_thickness()
    assert pos_after[0] - pos_before[0] == scrollbar_thickness[1] / 2  # x
    assert pos_after[1] == pos_before[1]  # y
