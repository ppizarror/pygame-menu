"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - LABEL
Test Label widget.
"""

import pytest

from pygame_menu.locals import ALIGN_LEFT
from pygame_menu.widgets import Label
from test._utils import PYGAME_V2, MenuUtils, surface


@pytest.fixture
def menu():
    """Return a generic menu fixture."""
    return MenuUtils.generic_menu()


@pytest.mark.parametrize(
    "text,max_char,expected",
    [
        (
            # long lorem ipsum
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
                "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, "
                "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu "
                "fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in "
                "culpa qui officia deserunt mollit anim id est laborum.",
                33,
                [
                    "Lorem ipsum dolor sit amet,",
                    "consectetur adipiscing elit, sed",
                    "do eiusmod tempor incididunt ut",
                    "labore et dolore magna aliqua. Ut",
                    "enim ad minim veniam, quis",
                    "nostrud exercitation ullamco",
                    "laboris nisi ut aliquip ex ea",
                    "commodo consequat. Duis aute",
                    "irure dolor in reprehenderit in",
                    "voluptate velit esse cillum",
                    "dolore eu fugiat nulla pariatur.",
                    "Excepteur sint occaecat cupidatat",
                    "non proident, sunt in culpa qui",
                    "officia deserunt mollit anim id",
                    "est laborum.",
                ],
        ),
        (
                "This label should split.\nIn two lines",
                None,
                ["This label should split.", "In two lines"],
        ),
        (
                "This label should split, this line is really long so it should split.\nThe second line",
                40,
                [
                    "This label should split, this line is",
                    "really long so it should split.",
                    "The second line",
                ],
        ),
        (
                "This label should split, this line is really long so it should split.\nThe second line",
                -1,
                [
                    "This label should split, this line is really",
                    "long so it should split.",
                    "The second line",
                ],
        ),
        ("a\n\nb\n\nc", -1, ["a", "", "b", "", "c"]),
    ],
)
def test_label_splitting(menu, text, max_char, expected):
    """Test label splitting across lines."""
    kwargs = {}
    if max_char is not None:
        kwargs["max_char"] = max_char
    label = menu.add.label(text, **kwargs)
    assert [i.get_title() for i in label] == expected


def test_label_properties(menu):
    """Test label widget properties."""
    label = menu.add.label(
        "hello", max_char=10, margin=(3, 5), align=ALIGN_LEFT, font_size=3
    )
    w = label

    assert not w.is_selectable
    assert w.get_margin() == (3, 5)
    assert w.get_alignment() == ALIGN_LEFT
    assert w.get_font_info()["size"] == 3

    w.draw(surface)
    assert not w.update([])


def test_label_underline(menu):
    """Test label underline decorator."""
    label = menu.add.label("nice")
    assert label._decorator._total_decor() == 0

    label.add_underline((0, 0, 0), 1, 1, force_render=True)
    assert label._decorator._total_decor() == 1


def test_label_underline_flag(menu):
    """Test label underline flag."""
    label = menu.add.label("underlined", underline=True)
    assert label._last_underline[1] is not None


def test_label_title_generator(menu):
    """Test label title generator behavior."""
    label = menu.add.label("nice")

    seq = ["a", "b", "c"]
    idx = [-1]

    def gen():
        """Generate label titles."""
        idx[0] = (idx[0] + 1) % len(seq)
        return seq[idx[0]]

    label.set_title_generator(gen)

    # initial title unchanged until update()
    assert label.get_title() == "nice"
    label.render()
    assert label.get_title() == "nice"

    # generator updates
    label.update([])
    assert label.get_title() == "a"
    label.update([])
    assert label.get_title() == "b"
    label.update([])
    assert label.get_title() == "c"

    # overriding title while generator active
    label.set_title("ignored")
    label.update([])
    assert label.get_title() == "a"  # next in sequence

    # remove generator
    label.set_title_generator(None)
    assert label._title_generator is None
    label.update([])
    assert label.get_title() == "a"


def test_empty_title(menu):
    """Test empty title dimensions."""
    label = menu.add.label("")
    p = label._padding

    assert label.get_width() == p[1] + p[3]
    expected_h = p[0] + p[2] + (41 if PYGAME_V2 else 42)
    assert label.get_height() == expected_h


def test_label_value(menu):
    """Test label value API."""
    label = menu.add.label("title")

    with pytest.raises(ValueError):
        label.get_value()

    with pytest.raises(ValueError):
        label.set_value("value")

    assert not label.value_changed()
    label.reset_value()


def test_wordwrap_basic(menu):
    """Test basic label wordwrap behavior."""
    label = menu.add.label(
        "lorem ipsum dolor sit amet this was very important nice a test is required",
        wordwrap=True,
    )

    assert label.get_width() == 586
    with pytest.raises(AssertionError):
        label.get_overflow_lines()

    assert label._get_max_container_width() == 584
    assert len(label.get_lines()) == 2
    assert label._get_leading() == 41
    assert label.get_height() == 90

    # menu removed
    label.set_menu(None)
    assert label.get_width(apply_padding=False) == 0
    assert label._get_max_container_width() == 0
    label._force_render()


def test_wordwrap_max_lines(menu):
    """Test label wordwrap with max lines."""
    s = (
        "lorem ipsum dolor sit amet this was very important nice a test is required "
        "lorem ipsum dolor sit amet this was very important nice a test is required"
    )

    label = menu.add.label(s, wordwrap=True, max_nlines=3)

    assert len(label.get_lines()) == 3
    assert label.get_height() == 131
    assert label.get_overflow_lines() == ["important nice a test is required"]

    # lines + overflow reconstruct original
    assert " ".join(label.get_lines() + label.get_overflow_lines()) == s

    label.set_menu(None)
    assert label.get_overflow_lines() == []


def test_clock(menu):
    """Test clock widget."""
    clock = menu.add.clock()
    assert clock.get_title() != ""

    with pytest.raises(AssertionError):
        menu.add.clock(title_format="bad")

    assert isinstance(clock, Label)
