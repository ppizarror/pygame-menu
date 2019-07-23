# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SOUND
Sound class.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2019 Pablo Pizarro R. @ppizarror

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

# Import pygame and base audio mixer
from pygame import mixer as _mixer
import pygame as _pygame

# Get sounds folder
import os.path as _path

__actualpath = str(_path.abspath(_path.dirname(__file__))).replace('\\', '/')
__sounddir = '{0}/sounds/{1}.ttf'


class Sound(object):
    """
    Sound class.
    """

    def __init__(self, frequency=22050, size=-16, channels=2, buffer=4096, devicename=None,
                 allowedchanges=_pygame.AUDIO_ALLOW_FREQUENCY_CHANGE | _pygame.AUDIO_ALLOW_CHANNELS_CHANGE):
        """
        Constructor.

        :param frequency: Frequency of sounds
        :type frequency: int
        :param size: Size of sample
        :type size: int
        :param channels: Number of channels by default
        :type channels: int
        :param buffer: Buffer size
        :type buffer: int
        :param devicename: Device name
        :type devicename: NoneType, basestring
        :param allowedchanges: Convert the samples at runtime
        :type allowedchanges: bool
        """

        # Initialize sounds if not initialized
        if _mixer.get_init() is None:
            _mixer.init(frequency=frequency,
                        size=size,
                        channels=channels,
                        buffer=buffer,
                        devicename=devicename,
                        allowedchanges=allowedchanges)

        # Channel where a sound is played
        self._channel = None

    def set_sound(self, sound, file, loops=0, maxtime=0, fade_ms=0):
        """
        Set a particular sound.

        :param sound: Sound type.
        :type sound: basestring
        :param file: Sound file
        :type file: basestring
        :param loops: Loops of the sound
        :type loops: int
        :param maxtime: Max playing time of the sound
        :type maxtime: int, float
        :param fade_ms: Fading ms
        :type fade_ms: int, float
        :return: None
        """
        assert isinstance(sound, str)
        assert isinstance(file, str)
        assert isinstance(loops, int)
        assert isinstance(maxtime, (int, float))
        assert isinstance(fade_ms, (int, float))

    def _play_sound(self, sound):
        """
        Play a sound.

        :param sound: Sound to be played
        :type sound: pygame.mixer.Sound, NoneType
        :return: None
        """

        # If sound is None then the active channel is None and returns
        if sound is None:
            self._channel = None
            return

        # Find an avaiable channel
        self._channel = _mixer.find_channel()
        if self._channel is None:  # The sound can't be played because all channels are busy
            return

        # Play the sound
        (volume, file, loops, maxtime, fade_ms) = sound
        self._channel.stop()
        self._channel.set_volume(volume, loops=loops, maxtime=maxtime, fade_ms=fade_ms)
        self._channel.play(file)
