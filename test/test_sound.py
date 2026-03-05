"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST SOUND
Test sound management.
"""

__all__ = ['SoundTest']

from pathlib import Path
from test._utils import MenuUtils, BaseTest
import copy

import pygame_menu


class SoundTest(BaseTest):

    def setUp(self) -> None:
        """
        Setup sound engine.
        """
        self.sound = pygame_menu.sound.Sound(force_init=True)

    def test_copy(self) -> None:
        """
        Test sound copy.
        """
        sound_src = pygame_menu.sound.Sound()
        sound_src.load_example_sounds()

        sound = copy.copy(sound_src)
        sound_deep = copy.deepcopy(sound_src)

        # Check if sounds are different
        t = pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE
        self.assertNotEqual(sound_src._sound[t]['file'], sound._sound[t]['file'])
        self.assertNotEqual(sound_src._sound[t]['file'], sound_deep._sound[t]['file'])
        self.assertEqual(sound_src._uniquechannel, sound._uniquechannel)

    def test_none_channel(self) -> None:
        """
        Test none channel.
        """
        new_sound = pygame_menu.sound.Sound(uniquechannel=False)
        new_sound.load_example_sounds()
        new_sound.play_widget_selection()
        new_sound._channel = None
        new_sound.stop()
        new_sound.pause()
        new_sound.unpause()
        new_sound.play_error()
        info = new_sound.get_channel_info()
        self.assertEqual(len(info), 5)
        self.assertEqual(set(info.keys()), {'busy', 'endevent', 'queue', 'sound', 'volume'})

    def test_channel(self) -> None:
        """
        Test channel.
        """
        new_sound = pygame_menu.sound.Sound(uniquechannel=False)
        new_sound.get_channel()
        self.sound.get_channel_info()
        self.sound.pause()
        self.sound.unpause()
        self.sound.stop()

    def test_load_sound(self) -> None:
        """
        Test load sounds.
        """
        self.assertFalse(self.sound.set_sound(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, None))
        self.assertRaises(ValueError, lambda: self.sound.set_sound('none', None))
        self.assertRaises(IOError, lambda: self.sound.set_sound(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, 'bad_file'))
        self.assertFalse(self.sound._play_sound(None))
        self.assertFalse(self.sound.set_sound(pygame_menu.sound.SOUND_TYPE_ERROR, pygame_menu.font.FONT_PT_SERIF))

        with self.assertRaises(AssertionError):
            self.sound.set_sound(
                pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE,
                pygame_menu.sound.SOUND_EXAMPLE_CLICK_MOUSE,
                volume=2.0
            )

        with self.assertRaises(AssertionError):
            self.sound.set_sound(
                pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE,
                pygame_menu.sound.SOUND_EXAMPLE_CLICK_MOUSE,
                loops=-1
            )

        p = Path(pygame_menu.sound.SOUND_EXAMPLE_CLICK_MOUSE)
        self.assertTrue(self.sound.set_sound(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, p))

    def test_example_sounds(self) -> None:
        """
        Test example sounds.
        """
        self.sound.load_example_sounds()

        self.sound.play_click_mouse()
        self.sound.play_click_touch()
        self.sound.play_close_menu()
        self.sound.play_error()
        self.sound.play_event()
        self.sound.play_event_error()
        self.sound.play_key_add()
        self.sound.play_key_del()
        self.sound.play_open_menu()

    def test_sound_menu(self) -> None:
        """
        Test sounds in menu.
        """
        menu = MenuUtils.generic_menu()
        submenu = MenuUtils.generic_menu()

        menu.add.button('submenu', submenu)
        button = menu.add.button('button', lambda: None)
        menu.set_sound(self.sound, True)
        self.assertEqual(button.get_sound(), self.sound)

        # This will remove the sound engine
        menu.set_sound(None, True)
        self.assertNotEqual(button.get_sound(), self.sound)
        self.assertEqual(menu.get_sound(), menu._sound)

    def test_set_sound_volume(self) -> None:
        """
        Test sound volume.
        """
        self.sound.load_example_sounds()
        self.assertTrue(self.sound.set_sound_volume(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, 0.5))
        self.assertEqual(self.sound._sound[pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE]['volume'], 0.5)
        self.assertFalse(self.sound.set_sound_volume('bad_sound', 0.5))
        self.assertTrue(self.sound.set_sound_volume(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, 1.0))
        self.assertEqual(self.sound._sound[pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE]['volume'], 1.0)
        self.assertTrue(self.sound.set_sound_volume(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, 0.0))
        self.assertEqual(self.sound._sound[pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE]['volume'], 0.0)
        self.assertFalse(self.sound.set_sound_volume(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, 2.0))

    def test_init_state_flags(self):
        from pygame_menu.sound import SOUND_INITIALIZED

        # Fresh state after creating a new Sound with force_init=False
        pygame_menu.sound.Sound(force_init=False)
        self.assertTrue(SOUND_INITIALIZED.attempted)
        self.assertTrue(SOUND_INITIALIZED.available)

    def test_reinit_logic(self):
        from pygame_menu.sound import SOUND_INITIALIZED
        import pygame

        # Reset state manually for test isolation
        SOUND_INITIALIZED.attempted = False

        mixer_was_initialized = pygame.mixer.get_init() is not None

        # Case 1: force_init=False
        pygame_menu.sound.Sound(force_init=False)

        if mixer_was_initialized:
            # Mixer already initialized → Sound should NOT attempt init
            self.assertFalse(SOUND_INITIALIZED.attempted)
        else:
            # Mixer not initialized → Sound SHOULD attempt init
            self.assertTrue(SOUND_INITIALIZED.attempted)

        # Case 2: force_init=True always triggers initialization
        SOUND_INITIALIZED.attempted = False
        pygame_menu.sound.Sound(force_init=True)
        self.assertTrue(SOUND_INITIALIZED.attempted)

    def test_unique_channel_behavior(self):
        s = pygame_menu.sound.Sound(uniquechannel=True, force_init=True)
        s.load_example_sounds()

        ch = s.get_channel()

        # Play first sound
        s.play_click_mouse()
        first_sound = ch.get_sound()

        # Play second sound immediately — should replace the first
        s.play_error()
        second_sound = ch.get_sound()

        self.assertNotEqual(first_sound, second_sound)

    def test_overlap_suppression(self):
        s = pygame_menu.sound.Sound(uniquechannel=False, force_init=True)
        s.load_example_sounds()

        ch = s.get_channel()

        # Play once
        s.play_click_mouse()
        first = ch.get_sound()

        # Play again immediately — should be suppressed
        s.play_click_mouse()
        second = ch.get_sound()

        self.assertEqual(first, second)

    def test_disabled_sound_behavior(self):
        s = pygame_menu.sound.Sound(force_init=True)

        # Disable a sound
        s.set_sound(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, None)

        # Should not crash or play
        s.play_click_mouse()

        # Volume setting should fail
        self.assertFalse(s.set_sound_volume(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, 0.5))

        # Channel info should still be valid
        info = s.get_channel_info()
        self.assertIsInstance(info, dict)

    def test_mixer_config_copied(self):
        s = pygame_menu.sound.Sound(force_init=True)
        s2 = copy.copy(s)

        self.assertEqual(s._mixer_configs, s2._mixer_configs)
