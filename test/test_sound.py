"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST SOUND
Test sound management.
"""

__all__ = ['SoundTest']

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
        self.assertEqual(len(new_sound.get_channel_info()), 5)

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
