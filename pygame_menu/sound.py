"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SOUND
Sound class.
"""

__all__ = [

    # Main class
    'Sound',

    # Sound types
    'SOUND_TYPE_CLICK_MOUSE',
    'SOUND_TYPE_CLICK_TOUCH',
    'SOUND_TYPE_CLOSE_MENU',
    'SOUND_TYPE_ERROR',
    'SOUND_TYPE_EVENT',
    'SOUND_TYPE_EVENT_ERROR',
    'SOUND_TYPE_KEY_ADDITION',
    'SOUND_TYPE_KEY_DELETION',
    'SOUND_TYPE_OPEN_MENU',
    'SOUND_TYPE_WIDGET_SELECTION',

    # Sound example paths
    'SOUND_EXAMPLE_CLICK_MOUSE',
    'SOUND_EXAMPLE_CLICK_TOUCH',
    'SOUND_EXAMPLE_CLOSE_MENU',
    'SOUND_EXAMPLE_ERROR',
    'SOUND_EXAMPLE_EVENT',
    'SOUND_EXAMPLE_EVENT_ERROR',
    'SOUND_EXAMPLE_KEY_ADD',
    'SOUND_EXAMPLE_KEY_DELETE',
    'SOUND_EXAMPLE_OPEN_MENU',
    'SOUND_EXAMPLE_WIDGET_SELECTION',
    'SOUND_EXAMPLES'

]

from pathlib import Path
import os.path as path
import time

from pygame import error as pygame_error
from pygame import mixer
from pygame import vernum as pygame_version

from pygame_menu._base import Base
from pygame_menu.utils import warn

from pygame_menu._types import NumberType, Dict, Any, Optional, Union, NumberInstance

try:  # pygame<2.0.0 compatibility
    from pygame import AUDIO_ALLOW_CHANNELS_CHANGE, AUDIO_ALLOW_FREQUENCY_CHANGE
except ImportError:
    AUDIO_ALLOW_CHANNELS_CHANGE, AUDIO_ALLOW_FREQUENCY_CHANGE = False, False

# Sound types
SOUND_TYPE_CLICK_MOUSE = '__pygame_menu_sound_click_mouse__'
SOUND_TYPE_CLICK_TOUCH = '__pygame_menu_sound_click_touch__'
SOUND_TYPE_CLOSE_MENU = '__pygame_menu_sound_close_menu__'
SOUND_TYPE_ERROR = '__pygame_menu_sound_error__'
SOUND_TYPE_EVENT = '__pygame_menu_sound_event__'
SOUND_TYPE_EVENT_ERROR = '__pygame_menu_sound_event_error__'
SOUND_TYPE_KEY_ADDITION = '__pygame_menu_sound_key_addition__'
SOUND_TYPE_KEY_DELETION = '__pygame_menu_sound_key_deletion__'
SOUND_TYPE_OPEN_MENU = '__pygame_menu_sound_open_menu__'
SOUND_TYPE_WIDGET_SELECTION = '__pygame_menu_sound_widget_selection__'

SOUND_TYPES = (
    SOUND_TYPE_CLICK_MOUSE,
    SOUND_TYPE_CLICK_TOUCH,
    SOUND_TYPE_CLOSE_MENU,
    SOUND_TYPE_ERROR,
    SOUND_TYPE_EVENT,
    SOUND_TYPE_EVENT_ERROR,
    SOUND_TYPE_KEY_ADDITION,
    SOUND_TYPE_KEY_DELETION,
    SOUND_TYPE_OPEN_MENU,
    SOUND_TYPE_WIDGET_SELECTION
)

# Sound example paths
__sounds_path__ = path.join(path.dirname(path.abspath(__file__)), 'resources', 'sounds', '{0}')

SOUND_EXAMPLE_CLICK_MOUSE = __sounds_path__.format('click_mouse.ogg')
SOUND_EXAMPLE_CLICK_TOUCH = SOUND_EXAMPLE_CLICK_MOUSE
SOUND_EXAMPLE_CLOSE_MENU = __sounds_path__.format('close_menu.ogg')
SOUND_EXAMPLE_ERROR = __sounds_path__.format('error.ogg')
SOUND_EXAMPLE_EVENT = __sounds_path__.format('event.ogg')
SOUND_EXAMPLE_EVENT_ERROR = __sounds_path__.format('event_error.ogg')
SOUND_EXAMPLE_KEY_ADD = __sounds_path__.format('key_add.ogg')
SOUND_EXAMPLE_KEY_DELETE = __sounds_path__.format('key_delete.ogg')
SOUND_EXAMPLE_OPEN_MENU = __sounds_path__.format('open_menu.ogg')
SOUND_EXAMPLE_WIDGET_SELECTION = __sounds_path__.format('widget_selection.ogg')

SOUND_EXAMPLES = (
    SOUND_EXAMPLE_CLICK_MOUSE,
    SOUND_EXAMPLE_CLICK_TOUCH,
    SOUND_EXAMPLE_CLOSE_MENU,
    SOUND_EXAMPLE_ERROR,
    SOUND_EXAMPLE_EVENT,
    SOUND_EXAMPLE_EVENT_ERROR,
    SOUND_EXAMPLE_KEY_ADD,
    SOUND_EXAMPLE_KEY_DELETE,
    SOUND_EXAMPLE_OPEN_MENU,
    SOUND_EXAMPLE_WIDGET_SELECTION
)

# Stores global reference that marks sounds as initialized
SOUND_INITIALIZED = [False, True]


class Sound(Base):
    """
    Sound engine class.
    
    :param allowedchanges: Convert the samples at runtime, only in pygame>=2.0.0
    :param buffer: Buffer size
    :param channels: Number of channels
    :param devicename: Device name
    :param force_init: Force mixer init with new parameters
    :param frequency: Frequency of sounds
    :param size: Size of sample
    :param sound_id: Sound ID
    :param uniquechannel: Force the channel to be unique, this is set at the object creation moment
    """
    _channel: Optional['mixer.Channel']
    _last_play: str
    _last_time: float
    _mixer_configs: Dict[str, Union[bool, int, str]]
    _sound: Dict[str, Dict[str, Any]]
    _uniquechannel: bool

    def __init__(
            self,
            allowedchanges: int = AUDIO_ALLOW_CHANNELS_CHANGE | AUDIO_ALLOW_FREQUENCY_CHANGE,
            buffer: int = 4096,
            channels: int = 2,
            devicename: str = '',
            force_init: bool = False,
            frequency: int = 22050,
            size: int = -16,
            sound_id: str = '',
            uniquechannel: bool = True
    ) -> None:
        super(Sound, self).__init__(object_id=sound_id)

        assert isinstance(allowedchanges, int)
        assert isinstance(buffer, int)
        assert isinstance(channels, int)
        assert isinstance(devicename, str)
        assert isinstance(force_init, bool)
        assert isinstance(frequency, int)
        assert isinstance(size, int)
        assert isinstance(uniquechannel, bool)

        assert buffer > 0, 'buffer size must be greater than zero'
        assert channels > 0, 'channels must be greater than zero'
        assert frequency > 0, 'frequency must be greater than zero'

        # Check if mixer is init
        mixer_missing = 'MissingModule' in str(type(mixer))
        if mixer_missing:
            if self._verbose:
                warn('pygame mixer module could not be found, NotImplementedError'
                     'has been raised. Sound support is disabled')
            SOUND_INITIALIZED[1] = False

        # Initialize sounds if not initialized
        if not mixer_missing and \
                ((mixer.get_init() is None and not SOUND_INITIALIZED[0]) or
                 force_init):

            # Set sound as initialized globally
            SOUND_INITIALIZED[0] = True

            # Check pygame version
            version_major, _, version_minor = pygame_version

            # noinspection PyBroadException
            try:
                # pygame < 1.9.5
                mixer_kwargs = {
                    'frequency': frequency,
                    'size': size,
                    'channels': channels,
                    'buffer': buffer
                }

                # pygame >= 1.9.5
                if (version_major == 1 and version_minor > 4) or version_major > 1:
                    mixer_kwargs['devicename'] = devicename

                # pygame >= 2.0.0
                if version_major > 1:
                    mixer_kwargs['allowedchanges'] = allowedchanges

                # Call to mixer
                mixer.init(**mixer_kwargs)

            except Exception as e:
                if self._verbose:
                    warn('sound error: ' + str(e))
            except pygame_error as e:
                if self._verbose:
                    warn('sound engine could not be initialized, pygame error: ' + str(e))

        # Store mixer configs
        self._mixer_configs = {
            'allowedchanges': allowedchanges,
            'buffer': buffer,
            'channels': channels,
            'devicename': devicename,
            'frequency': frequency,
            'size': size
        }

        # Channel where a sound is played
        self._channel = None
        self._uniquechannel = uniquechannel

        # Sound dict
        self._sound = {}
        for sound in SOUND_TYPES:
            self._sound[sound] = {}

        # Last played song
        self._last_play = ''
        self._last_time = 0

    def copy(self) -> 'Sound':
        """
        Return a copy of the object.

        :return: Sound copied
        """
        new_sound = Sound(uniquechannel=self._uniquechannel)
        new_sound._channel = self._channel
        for key in self._mixer_configs:
            new_sound._mixer_configs[key] = self._mixer_configs[key]
        for sound_type in self._sound.keys():
            s = self._sound[sound_type]
            if len(s) != 0:
                new_sound.set_sound(
                    sound_type=sound_type,
                    sound_file=s['path'],
                    volume=s['volume'],
                    loops=s['loops'],
                    maxtime=s['maxtime'],
                    fade_ms=s['fade_ms']
                )
        return new_sound

    def __copy__(self) -> 'Sound':
        """
        Copy method.

        :return: Return new sound
        """
        return self.copy()

    def __deepcopy__(self, memodict: Dict) -> 'Sound':
        """
        Deep-copy method.

        :param memodict: Memo dict
        :return: Return new sound
        """
        return self.copy()

    def get_channel(self) -> 'mixer.Channel':
        """
        Return the channel of the sound engine.

        :return: Sound engine channel
        """
        # noinspection PyArgumentList
        channel = mixer.find_channel()  # force only available on pygame v2
        if self._uniquechannel:  # If the channel is unique
            if self._channel is None:  # If the channel has not been set
                self._channel = channel
        else:
            self._channel = channel  # Store the available channel
        return self._channel

    def set_sound(
            self,
            sound_type: str,
            sound_file: Optional[Union[str, 'Path']],
            volume: float = 0.5,
            loops: int = 0,
            maxtime: NumberType = 0,
            fade_ms: NumberType = 0
    ) -> bool:
        """
        Link a sound file to a sound type.

        :param sound_type: Sound type
        :param sound_file: Sound file. If ``None`` disable the given sound type
        :param volume: Volume of the sound, from ``0.0`` to ``1.0``
        :param loops: Loops of the sound
        :param maxtime: Max playing time of the sound
        :param fade_ms: Fading ms
        :return: The status of the sound load, ``True`` if the sound was loaded
        """
        assert isinstance(sound_type, str)
        assert isinstance(sound_file, (str, type(None), Path))
        assert isinstance(volume, NumberInstance)
        assert isinstance(loops, int)
        assert isinstance(maxtime, NumberInstance)
        assert isinstance(fade_ms, NumberInstance)
        assert loops >= 0, 'loops count must be equal or greater than zero'
        assert maxtime >= 0, 'maxtime must be equal or greater than zero'
        assert fade_ms >= 0, 'fade_ms must be equal or greater than zero'
        assert 1 >= volume >= 0, 'volume must be between 0 and 1'

        # Check sound type is correct
        if sound_type not in SOUND_TYPES:
            raise ValueError('sound type not valid, check the manual')

        # If file is none disable the sound
        if sound_file is None or not SOUND_INITIALIZED[1]:
            self._sound[sound_type] = {}
            return False

        # Check the file exists
        sound_file = str(sound_file)
        if not path.isfile(sound_file):
            raise IOError(f'sound file "{sound_file}" does not exist')

        # Load the sound
        try:
            # noinspection PyTypeChecker
            sound_data = mixer.Sound(file=sound_file)
        except pygame_error:
            if self._verbose:
                warn(f'the sound file "{sound_file}" could not be loaded, it has been disabled')
            self._sound[sound_type] = {}
            return False

        # Configure the sound
        sound_data.set_volume(float(volume))

        # Store the sound
        self._sound[sound_type] = {
            'fade_ms': fade_ms,
            'file': sound_data,
            'length': sound_data.get_length(),
            'loops': loops,
            'maxtime': maxtime,
            'path': sound_file,
            'type': sound_type,
            'volume': volume
        }
        return True

    def load_example_sounds(self, volume: float = 0.5) -> 'Sound':
        """
        Load the example sounds provided by the package.

        :param volume: Volume of the sound, from ``0`` to ``1``
        :return: Self reference
        """
        assert isinstance(volume, NumberInstance) and 0 <= volume <= 1
        for sound in range(len(SOUND_TYPES)):
            self.set_sound(SOUND_TYPES[sound], SOUND_EXAMPLES[sound], volume=float(volume))
        return self

    def _play_sound(self, sound: Optional[Dict[str, Any]]) -> bool:
        """
        Play a sound.

        :param sound: Sound to be played
        :return: ``True`` if the sound was played
        """
        if not sound:
            return False

        # Find an available channel
        channel = self.get_channel()  # This will set the channel if it's None
        if channel is None:  # The sound can't be played because all channels are busy
            return False

        # Play the sound
        sound_time = time.time()

        # If the previous sound is the same and has not ended (max 10% overlap)
        if sound['type'] != self._last_play or \
                sound_time - self._last_time >= 0.1 * sound['length'] or self._uniquechannel:
            try:
                if self._uniquechannel:  # Stop the current channel if it's unique
                    channel.stop()
                channel.play(sound['file'],
                             loops=sound['loops'],
                             maxtime=sound['maxtime'],
                             fade_ms=sound['fade_ms']
                             )
            except pygame_error:  # Ignore errors
                pass

        # Store last execution
        self._last_play = sound['type']
        self._last_time = sound_time
        return True

    def play_click_mouse(self) -> 'Sound':
        """
        Play click mouse sound.

        :return: Self reference
        """
        self._play_sound(self._sound[SOUND_TYPE_CLICK_MOUSE])
        return self

    def play_click_touch(self) -> 'Sound':
        """
        Play click touch sound.

        :return: Self reference
        """
        self._play_sound(self._sound[SOUND_TYPE_CLICK_TOUCH])
        return self

    def play_error(self) -> 'Sound':
        """
        Play error sound.

        :return: Self reference
        """
        self._play_sound(self._sound[SOUND_TYPE_ERROR])
        return self

    def play_event(self) -> 'Sound':
        """
        Play event sound.

        :return: Self reference
        """
        self._play_sound(self._sound[SOUND_TYPE_EVENT])
        return self

    def play_event_error(self) -> 'Sound':
        """
        Play event error sound.

        :return: Self reference
        """
        self._play_sound(self._sound[SOUND_TYPE_EVENT_ERROR])
        return self

    def play_key_add(self) -> 'Sound':
        """
        Play key addition sound.

        :return: Self reference
        """
        self._play_sound(self._sound[SOUND_TYPE_KEY_ADDITION])
        return self

    def play_key_del(self) -> 'Sound':
        """
        Play key deletion sound.

        :return: Self reference
        """
        self._play_sound(self._sound[SOUND_TYPE_KEY_DELETION])
        return self

    def play_open_menu(self) -> 'Sound':
        """
        Play open Menu sound.

        :return: Self reference
        """
        self._play_sound(self._sound[SOUND_TYPE_OPEN_MENU])
        return self

    def play_close_menu(self) -> 'Sound':
        """
        Play close Menu sound.

        :return: Self reference
        """
        self._play_sound(self._sound[SOUND_TYPE_CLOSE_MENU])
        return self

    def play_widget_selection(self) -> 'Sound':
        """
        Play widget selection sound.

        :return: Self reference
        """
        self._play_sound(self._sound[SOUND_TYPE_WIDGET_SELECTION])
        return self

    def stop(self) -> 'Sound':
        """
        Stop the channel.

        :return: Self reference
        """
        channel = self.get_channel()
        if channel is None:  # The sound can't be played because all channels are busy
            return self
        try:
            channel.stop()
        except pygame_error:
            pass
        return self

    def pause(self) -> 'Sound':
        """
        Pause the channel.

        :return: Self reference
        """
        channel = self.get_channel()
        if channel is None:  # The sound can't be played because all channels are busy
            return self
        try:
            channel.pause()
        except pygame_error:
            pass
        return self

    def unpause(self) -> 'Sound':
        """
        Unpause channel.

        :return: Self reference
        """
        channel = self.get_channel()
        if channel is None:  # The sound can't be played because all channels are busy
            return self
        try:
            channel.unpause()
        except pygame_error:
            pass
        return self

    def get_channel_info(self) -> Dict[str, Any]:
        """
        Return the channel information.

        :return: Information dict e.g.: ``{'busy': 0, 'endevent': 0, 'queue': None, 'sound': None, 'volume': 1.0}``
        """
        channel = self.get_channel()
        data = {}
        if channel is None:  # The sound can't be played because all channels are busy
            return data
        data['busy'] = channel.get_busy()
        data['endevent'] = channel.get_endevent()
        data['queue'] = channel.get_queue()
        data['sound'] = channel.get_sound()
        data['volume'] = channel.get_volume()
        return data
