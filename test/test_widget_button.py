"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - BUTTON
Test Button widget.
"""

import pygame
import pytest

import pygame_menu
from pygame_menu.widgets import Button, HighlightSelection
from pygame_menu.widgets.core.widget import WIDGET_SHADOW_TYPE_ELLIPSE
from test._utils import PYGAME_V2, MenuUtils, PygameEventUtils, surface


@pytest.fixture
def menu():
    """Provides a fresh generic menu for each test."""
    return MenuUtils.generic_menu()


@pytest.fixture
def submenu():
    """Provides a second menu for testing sub-menu navigation."""
    return MenuUtils.generic_menu()


@pytest.fixture
def callback_flag():
    """A mutable flag to verify if a callback was executed."""
    return {"called": False, "value": None}


@pytest.mark.parametrize(
    "invalid_input",
    [
        1,
        "a",
        True,
        pygame,
        surface,
        1.1,
        [1, 2, 3],
        (1, 2, 3),
        pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES),
    ],
)
def test_button_raises_error_on_invalid_callback(menu, invalid_input):
    """Test that invalid callback raises an error."""
    with pytest.raises(ValueError):
        menu.add.button("btn", invalid_input)


def test_button_raises_error_on_recursive_menu(menu):
    """A menu cannot add a button that points back to itself (infinite loop)."""
    with pytest.raises(ValueError):
        menu.add.button("bt", menu)


@pytest.mark.parametrize(
    "valid_input",
    [lambda: None, pygame_menu.events.NONE, pygame_menu.events.PYGAME_QUIT, None],
)
def test_button_accepts_valid_callbacks(menu, valid_input):
    """Test that valid callbacks are accepted."""
    btn = menu.add.button("btn", valid_input)
    assert btn is not None


def test_button_callback_execution_with_args(callback_flag):
    """Test that callback execution with args is accepted."""

    def cb(t=False):
        """Store callback execution state and passed value."""
        callback_flag["called"] = True
        callback_flag["value"] = t

    btn = Button("epic", t=True, onreturn=cb)
    btn.apply()

    assert callback_flag["called"] is True
    assert callback_flag["value"] is True


def test_button_kwargs_logic(menu):
    """Test that kwargs are accepted."""

    def cb_check(**kwargs):
        """Validate kwargs forwarded to callback."""
        assert kwargs.get("key") is True

    # Test explicit kwarg passing
    btn = Button("test", onreturn=cb_check, key=True)
    btn.apply()

    # Test through menu factory
    btn2 = menu.add.button("test2", cb_check, accept_kwargs=True, key=True)
    btn2.apply()


def test_button_underline_decoration(menu):
    """Test that underline decoration is accepted."""
    btn = menu.add.button("underline_me", pygame_menu.events.NONE)

    btn.add_underline((255, 0, 0), 2, 2, force_render=True)
    assert btn._decorator._total_decor() == 1

    btn.remove_underline()
    assert btn._decorator._total_decor() == 0


def test_button_navigation_to_submenu(menu, submenu):
    """Test that navigation to submenu is accepted."""
    btn_to_sub = menu.add.button("go", submenu)
    menu.full_reset()

    # Trigger selection/apply
    btn_to_sub.update(PygameEventUtils.keydown(pygame_menu.controls.KEY_APPLY))
    assert menu.get_current() == submenu


def test_button_empty_title_geometry(menu):
    """Test that empty title geometry is accepted."""
    btn = menu.add.button("")
    p = btn._padding
    # Pygame version affects vertical alignment slightly
    expected_h = p[0] + p[2] + (41 if PYGAME_V2 else 42)

    assert btn.get_width() == p[1] + p[3]
    assert btn.get_height() == expected_h


def test_button_shadow_generation(menu):
    """Test that shadow generation is accepted."""
    btn = menu.add.button("shadow_test")
    btn.shadow(shadow_width=10, color="black")

    # Before drawing, surface is usually None
    btn.draw(surface)

    shadow_surf = btn._shadow["surface"]
    assert shadow_surf is not None
    # Shadow surface should be widget size + 2*width
    assert shadow_surf.get_width() == btn.get_width() + 20


def test_button_url_behavior(menu):
    """Test that url behavior is accepted."""
    btn = menu.add.url("https://google.com", "Search")
    assert btn.get_title() == "Search"

    with pytest.raises(AssertionError):
        menu.add.url("not-a-url")


def test_banner_widget_properties(menu):
    """Banners are specialized buttons typically used for images."""
    img = pygame.Surface((100, 50))
    custom_effect = HighlightSelection()

    btn = menu.add.banner(img, padding=10, selection_effect=custom_effect)

    assert abs(btn.get_height() - img.get_height()) <= 1
    assert btn._padding == (10, 10, 10, 10)
    assert isinstance(btn.get_selection_effect(), HighlightSelection)


def test_button_multiline_wordwrap(menu):
    """Test multiline wordwrap behavior."""
    text = "word " * 20
    # Limit to 2 lines even if text is longer
    btn = menu.add.button(text, wordwrap=True, max_nlines=2)

    assert len(btn.get_lines()) == 2
    assert len(btn.get_overflow_lines()) > 0


def test_update_callback_rejects_invalid(menu):
    """Test rejection callback rejects invalid input."""
    btn = menu.add.button("b1", lambda: None)
    for invalid in [menu, 1, [1, 2, 3], (1, 2, 3)]:
        with pytest.raises(AssertionError):
            btn.update_callback(invalid)  # type: ignore


def test_button_readonly_behavior(menu):
    """Test readonly behavior."""
    applied = []

    def cb():
        """Track callback invocation."""
        applied.append(True)

    btn = menu.add.button("x", cb)
    assert btn.apply() is None  # normal call returns None

    btn.readonly = True
    assert btn.apply() is None  # still allowed
    # callback *does* run on apply()
    assert applied == [True]

    # but readonly blocks event-driven apply()
    applied.clear()
    event = PygameEventUtils.keydown(pygame_menu.controls.KEY_APPLY)
    assert btn.update(event) is False
    assert applied == []

    # KEY_APPLY must not trigger apply() when readonly
    event = PygameEventUtils.keydown(pygame_menu.controls.KEY_APPLY)
    assert btn.update(event) is False


def test_button_resize_flip_and_limits(menu):
    """Test resize and flip behavior."""
    btn = menu.add.button("resize", pygame_menu.events.NONE)

    btn.resize(1, 1)
    btn.set_max_height(None)
    btn.set_max_width(None)
    btn.flip(True, True)

    assert btn._flip == (True, True)


def test_button_active_selected_consistency(menu):
    """Test active selection consistency behavior."""
    btn = menu.add.button("active", pygame_menu.events.NONE)

    btn.active = True
    btn._selected = False
    btn.draw(surface)

    # Drawing a non-selected active button must deactivate it
    assert btn.active is False


def test_button_change_calls_onchange(menu):
    """Test change behavior."""
    btn = menu.add.button("x", pygame_menu.events.NONE)
    called = []

    btn._onchange = lambda: called.append(True)
    assert btn.change() is None
    assert called == [True]


def test_button_event_constants(menu):
    """Test button event constants behavior."""
    # PYGAME_QUIT and WINDOWCLOSE must map to menu._exit
    btn = menu.add.button("quit", pygame_menu.events.PYGAME_QUIT)
    assert btn._onreturn == menu._exit

    btn = menu.add.button("close", pygame_menu.events.PYGAME_WINDOWCLOSE)
    assert btn._onreturn == menu._exit

    # NONE must disable callback
    btn = menu.add.button("none", pygame_menu.events.NONE)
    assert btn._onreturn is None

    # No callback provided → also None
    btn = menu.add.button("none2")
    assert btn._onreturn is None


def test_button_invalid_kwarg_rejected(menu):
    """Test button invalid kwarg rejected."""

    def cb(**_):
        """Dummy callback for kwarg validation."""
        pass

    # accept_kwargs=False but kwarg provided → error
    with pytest.raises(ValueError):
        menu.add.button("bad", cb, key=True)


def test_button_remove_widget(menu):
    """Test removing button widget from menu."""
    btn = menu.add.button("x")
    menu.remove_widget(btn)

    # Removing twice must raise
    with pytest.raises(ValueError):
        menu.remove_widget(btn)


def test_button_shadow_full_behavior(menu):
    """Test full shadow behavior, including re-enable and invalid radius cases."""
    btn = menu.add.button("shadow", pygame_menu.events.NONE)

    # Enable shadow
    btn.shadow(shadow_width=20, color="black")
    assert btn._shadow["enabled"] is True
    assert btn._shadow["properties"][4] == (0, 0, 0)

    # Disable shadow with alpha color
    btn.shadow(shadow_width=0, color=(250, 250, 30, 40))
    assert btn._shadow["enabled"] is False
    assert btn._shadow["properties"][4] == (250, 250, 30)
    assert btn._shadow["surface"] is None

    # Disable shadow with RGB
    btn.shadow(shadow_width=0, color=(250, 250, 100))
    assert btn._shadow["enabled"] is False
    assert btn._shadow["properties"][4] == (250, 250, 100)

    # Re-enable and verify surface size
    btn.shadow(shadow_width=20, color="black")
    btn.draw(surface)
    s = btn._shadow["surface"].get_size()
    assert s[0] == btn.get_width() + 40
    assert s[1] == btn.get_height() + 40

    # Scaling must invalidate shadow surface
    btn.scale(2, 2)
    assert btn._shadow["surface"] is None
    btn.draw(surface)
    s2 = btn._shadow["surface"].get_size()
    assert s2[0] == btn.get_width() + 40
    assert s2[1] == btn.get_height() + 40

    # Ellipse shadow
    btn2 = menu.add.button("ellipse")
    btn2.shadow(WIDGET_SHADOW_TYPE_ELLIPSE, 50)
    btn2.draw(surface)

    # Invalid corner radius disables shadow
    btn2.shadow(corner_radius=4000)
    assert btn2._shadow["enabled"] is True
    btn2.draw(surface)
    assert btn2._shadow["enabled"] is False


def test_button_value_methods(menu):
    """Test button value API behavior."""
    btn = menu.add.button("button")

    with pytest.raises(ValueError):
        btn.get_value()

    with pytest.raises(ValueError):
        btn.set_value("value")

    assert btn.value_changed() is False
    btn.reset_value()


def test_multiline_inside_frame_rewrap(menu):
    """Test multiline button rewrap when packed into and unpacked from a frame."""
    s = (
        "lorem ipsum dolor sit amet this was very important nice a test is required "
        "lorem ipsum dolor sit amet this was very important nice a test is required"
    )

    btn = menu.add.button(s, wordwrap=True, max_nlines=3)
    assert len(btn.get_lines()) == 3
    assert btn.get_overflow_lines() == ["important nice a test is required"]

    # Inside frame → rewrap to container width
    frame = menu.add.frame_h(200, 200)
    frame.pack(btn)

    assert len(btn.get_overflow_lines()) > 3  # many wrapped lines

    # Removing from frame restores original wrap
    frame.unpack(btn)
    assert btn.get_overflow_lines() == ["important nice a test is required"]


def test_banner_respects_user_cursor(menu):
    """Test banner respects user-provided cursor."""
    surf = pygame.Surface((50, 50))
    btn = menu.add.banner(surf, cursor=pygame.SYSTEM_CURSOR_CROSSHAIR)
    assert btn._cursor == pygame.SYSTEM_CURSOR_CROSSHAIR


def test_banner_float_behavior(menu):
    """Test banner float behavior."""
    surf = pygame.Surface((30, 30))
    btn = menu.add.banner(surf, float=True)
    assert btn.is_floating()


def test_banner_apply_via_event(menu):
    """Test banner apply via keyboard event."""
    applied = {"ok": False}

    def cb():
        """Mark banner callback as called."""
        applied["ok"] = True

    surf = pygame.Surface((60, 60))
    menu.add.banner(surf, cb)

    event = PygameEventUtils.keydown(pygame_menu.controls.KEY_APPLY)
    menu.update(event)

    assert applied["ok"] is True


def test_controller_behavior(menu):
    """Test controller."""
    from random import randrange
    from pygame_menu.controls import Controller

    custom = Controller()
    counter = {"n": 0}

    def apply(event, _):
        """Handle key events through custom controller and count accepted keys."""
        if event.key in (pygame.K_a, pygame.K_b, pygame.K_c):
            menu.get_scrollarea().update_area_color(
                (randrange(0, 255), randrange(0, 255), randrange(0, 255))
            )
            counter["n"] += 1
            return True
        return False

    custom.apply = apply

    btn = menu.add.button("My button", lambda: None)
    btn.set_controller(custom)

    menu.update(PygameEventUtils.keydown(pygame.K_d))
    assert counter["n"] == 0

    menu.update(PygameEventUtils.keydown(pygame.K_a))
    menu.update(PygameEventUtils.keydown(pygame.K_b))
    menu.update(PygameEventUtils.keydown(pygame.K_c))
    assert counter["n"] == 3

    # Joystick select must trigger update()
    assert btn.update(
        PygameEventUtils.joy_button(pygame_menu.controls.JOY_BUTTON_SELECT)
    )
