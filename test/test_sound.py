# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST SOUND
Test sound management.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2020 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""
from test._utils import *


class SoundTest(unittest.TestCase):

    def setUp(self):
        """
        Setup sound engine.
        """
        self.sound = pygameMenu.sound.Sound(force_init=True)
        self.sound._verbose = False

    def test_channel(self):
        """
        Test channel.
        """
        new_sound = pygameMenu.sound.Sound(uniquechannel=False)
        new_sound.get_channel()
        self.sound.get_channel_info()
        self.sound.pause()
        self.sound.unpause()
        self.sound.stop()

    def test_load_sound(self):
        """
        Test load sounds.
        """
        self.assertEqual(self.sound.set_sound(pygameMenu.sound.SOUND_TYPE_CLICK_MOUSE, None), False)
        self.assertRaises(ValueError, lambda: self.sound.set_sound('none', None))
        self.assertRaises(IOError,
                          lambda: self.sound.set_sound(pygameMenu.sound.SOUND_TYPE_CLICK_MOUSE, 'bad_file'))
        self.assertEqual(self.sound._play_sound(None), False)
        self.assertEqual(self.sound.set_sound(pygameMenu.sound.SOUND_TYPE_ERROR, pygameMenu.font.FONT_PT_SERIF), False)

    def test_example_sounds(self):
        """
        Test example sounds.
        """
        self.sound.load_example_sounds()

        self.sound.play_click_mouse()
        self.sound.play_close_menu()
        self.sound.play_error()
        self.sound.play_event()
        self.sound.play_event_error()
        self.sound.play_key_add()
        self.sound.play_key_del()
        self.sound.play_open_menu()

    def test_sound_menu(self):
        """
        Test sounds in menu.
        """
        menu = PygameMenuUtils.generic_menu()
        submenu = PygameMenuUtils.generic_menu()

        menu.add_option('submenu', submenu)
        button = menu.add_option('button', lambda: None)
        menu.set_sound(self.sound, True)
        self.assertEqual(button.sound, self.sound)

        # This will remove the sound engine
        menu.set_sound(None, True)
        self.assertNotEqual(button.sound, self.sound)
