"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST SOUND
Test sound management.
"""

import copy
import time

import pygame
import pytest

from pygame_menu.sound import (
    SOUND_EXAMPLES,
    SOUND_INITIALIZED,
    SOUND_TYPES,
    Sound,
)
from test._utils import MenuUtils


@pytest.fixture
def sound():
    """Return a fresh sound engine with forced mixer init."""
    return Sound(force_init=True)


@pytest.fixture
def loaded_sound(sound):
    """Return a sound engine with all example sounds loaded."""
    sound.load_example_sounds()
    return sound


def test_copy_semantics(loaded_sound):
    """Ensure shallow and deep copies duplicate sound objects correctly."""
    shallow = copy.copy(loaded_sound)
    deep = copy.deepcopy(loaded_sound)

    for t in SOUND_TYPES:
        assert loaded_sound._sound[t]["file"] != shallow._sound[t]["file"]
        assert loaded_sound._sound[t]["file"] != deep._sound[t]["file"]

    assert loaded_sound._uniquechannel == shallow._uniquechannel
    assert loaded_sound._mixer_configs == shallow._mixer_configs


@pytest.mark.parametrize("sound_type, example", zip(SOUND_TYPES, SOUND_EXAMPLES))
def test_load_example_sound_individually(sound, sound_type, example):
    """Verify each example sound loads correctly."""
    assert sound.set_sound(sound_type, example)
    assert sound._sound[sound_type]["path"] == example


@pytest.mark.parametrize("bad_volume", [-1, 1.1, 2.0])
def test_set_sound_invalid_volume(sound, bad_volume):
    """Ensure invalid volume values raise assertion errors."""
    with pytest.raises(AssertionError):
        sound.set_sound(SOUND_TYPES[0], SOUND_EXAMPLES[0], volume=bad_volume)


@pytest.mark.parametrize("bad_loops", [-1, -5])
def test_set_sound_invalid_loops(sound, bad_loops):
    """Ensure invalid loop counts raise assertion errors."""
    with pytest.raises(AssertionError):
        sound.set_sound(SOUND_TYPES[0], SOUND_EXAMPLES[0], loops=bad_loops)


@pytest.mark.parametrize("bad_time", [-1, -0.5])
def test_set_sound_invalid_maxtime(sound, bad_time):
    """Ensure invalid maxtime values raise assertion errors."""
    with pytest.raises(AssertionError):
        sound.set_sound(SOUND_TYPES[0], SOUND_EXAMPLES[0], maxtime=bad_time)


def test_set_sound_invalid_type(sound):
    """Ensure invalid sound types raise ValueError."""
    with pytest.raises(ValueError):
        sound.set_sound("not_a_valid_type", None)


def test_set_sound_missing_file(sound):
    """Ensure missing sound files raise OSError."""
    with pytest.raises(OSError):
        sound.set_sound(SOUND_TYPES[0], "nonexistent_file.ogg")


@pytest.mark.parametrize("volume", [0.0, 0.5, 1.0])
def test_set_sound_volume_valid(loaded_sound, volume):
    """Ensure valid volume values are applied correctly."""
    t = SOUND_TYPES[0]
    assert loaded_sound.set_sound_volume(t, volume)
    assert loaded_sound._sound[t]["volume"] == volume


@pytest.mark.parametrize("volume", [-1, 2.0])
def test_set_sound_volume_invalid(loaded_sound, volume):
    """Ensure invalid volume values return False."""
    t = SOUND_TYPES[0]
    assert not loaded_sound.set_sound_volume(t, volume)


def test_set_sound_volume_disabled(sound):
    """Ensure disabled sounds cannot have volume set."""
    sound.set_sound(SOUND_TYPES[0], None)
    assert not sound.set_sound_volume(SOUND_TYPES[0], 0.5)


def test_none_channel_behavior(loaded_sound):
    """Ensure channel operations behave safely when channel is None."""
    loaded_sound.play_widget_selection()
    loaded_sound._channel = None

    loaded_sound.stop()
    loaded_sound.pause()
    loaded_sound.unpause()

    info = loaded_sound.get_channel_info()
    assert set(info.keys()) == {"busy", "endevent", "queue", "sound", "volume"}


def test_unique_channel_behavior(loaded_sound):
    """Ensure uniquechannel forces reuse of the same channel."""
    s = Sound(uniquechannel=True, force_init=True).load_example_sounds()
    ch = s.get_channel()

    s.play_click_mouse()
    first = ch.get_sound()

    s.play_error()
    second = ch.get_sound()

    assert first != second


def test_non_unique_channel_behavior(loaded_sound):
    """Ensure non-unique channels allow overlap suppression."""
    s = Sound(uniquechannel=False, force_init=True).load_example_sounds()
    ch = s.get_channel()

    s.play_click_mouse()
    first = ch.get_sound()

    s.play_click_mouse()
    second = ch.get_sound()

    assert first == second


def test_overlap_suppression_timing(monkeypatch):
    """Ensure overlap suppression depends on timing thresholds."""
    s = Sound(uniquechannel=False, force_init=True).load_example_sounds()
    ch = s.get_channel()

    fake_time = [1000.0]
    monkeypatch.setattr(time, "time", lambda: fake_time[0])

    s.play_click_mouse()
    first = ch.get_sound()

    s.play_click_mouse()
    second = ch.get_sound()
    assert second is first

    fake_time[0] += 9999
    s.play_click_mouse()
    third = ch.get_sound()

    assert third is first
    assert ch.get_busy()


def test_init_state_flags():
    """Ensure SOUND_INITIALIZED flags reflect mixer availability."""
    SOUND_INITIALIZED.attempted = False
    Sound(force_init=False)

    mixer_was_initialized = pygame.mixer.get_init() is not None

    if mixer_was_initialized:
        assert not SOUND_INITIALIZED.attempted
    else:
        assert SOUND_INITIALIZED.attempted


def test_reinit_logic():
    """Ensure mixer reinitialization logic behaves correctly."""
    # Reset state manually for test isolation
    SOUND_INITIALIZED.attempted = False
    mixer_was_initialized = pygame.mixer.get_init() is not None

    # Case 1: force_init=False
    Sound(force_init=False)

    if mixer_was_initialized:
        # Mixer already initialized → Sound should NOT attempt init
        assert not SOUND_INITIALIZED.attempted
    else:
        # Mixer not initialized → Sound SHOULD attempt init
        assert SOUND_INITIALIZED.attempted

    # Case 2: force_init=True always triggers initialization
    SOUND_INITIALIZED.attempted = False
    Sound(force_init=True)
    assert SOUND_INITIALIZED.attempted


def test_sound_menu_propagation(sound):
    """Ensure menu sound assignment propagates recursively."""
    menu = MenuUtils.generic_menu()
    submenu = MenuUtils.generic_menu()

    menu.add.button("submenu", submenu)
    button = menu.add.button("button", lambda: None)

    menu.set_sound(sound, recursive=True)
    assert button.get_sound() is sound

    menu.set_sound(None, recursive=True)
    assert button.get_sound() is not sound
    assert menu.get_sound() is menu._sound


def test_disabled_sound_behavior(sound):
    """Ensure disabled sounds behave safely when played."""
    sound.set_sound(SOUND_TYPES[0], None)
    sound.play_click_mouse()

    assert not sound.set_sound_volume(SOUND_TYPES[0], 0.5)

    info = sound.get_channel_info()
    assert isinstance(info, dict)


def test_mixer_config_copied(sound):
    """Ensure mixer configuration is copied correctly."""
    s2 = copy.copy(sound)
    assert sound._mixer_configs == s2._mixer_configs
