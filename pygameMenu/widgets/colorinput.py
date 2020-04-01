# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

COLOR INPUT
Color input class, Widget created in top of TextInput that provides a textbox
for entering and previewing colors in RGB and HEX format.

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

from pygameMenu.widgets.textinput import TextInput
import pygameMenu.locals as _locals


# noinspection PyTypeChecker
class ColorInput(TextInput):
    """
    Color input widget.
    """

    def __init__(self,
                 label='',
                 colorinput_id='',
                 color_type='rgb',
                 input_comma=',',
                 input_underline='_',
                 cursor_color=(0, 0, 0),
                 onchange=None,
                 onreturn=None,
                 repeat_keys_initial_ms=450,
                 repeat_keys_interval_ms=80,
                 repeat_mouse_interval_ms=100,
                 **kwargs
                 ):
        """
        Description of the specific paramaters (see Widget class for generic ones):

        :param label: Input label text
        :type label: basestring
        :param colorinput_id: ID of the text input
        :type colorinput_id: basestring
        :param color_type: Type of color input (rgb, hex)
        :type color_type: basestring
        :param input_comma: Divisor between RGB channels
        :type input_comma: basestring
        :param input_underline: Character drawn under each number input
        :type input_underline: basestring
        :param cursor_color: Color of cursor
        :type cursor_color: tuple
        :param onchange: Callback when changing the selector
        :type onchange: function, NoneType
        :param onreturn: Callback when pressing return button
        :type onreturn: function, NoneType
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :type repeat_keys_initial_ms: float, int
        :param repeat_keys_interval_ms: Interval between key press repetition when held
        :type repeat_keys_interval_ms: float, int
        :param repeat_mouse_interval_ms: Interval between mouse events when held
        :type repeat_mouse_interval_ms: float, int
        :param kwargs: Optional keyword-arguments for callbacks
        """
        assert isinstance(label, str)
        assert isinstance(colorinput_id, str), 'ID must be a string'
        assert isinstance(color_type, str), 'color_type must be a string'
        assert isinstance(input_comma, str), 'input_comma must be a string'
        assert isinstance(input_underline, str), 'input_underline must be a string'
        assert isinstance(cursor_color, tuple)
        assert isinstance(repeat_keys_initial_ms, int)
        assert isinstance(repeat_keys_interval_ms, int)
        assert isinstance(repeat_mouse_interval_ms, int)

        if len(input_comma) != 1:
            raise ValueError('input_comma must be a single char')
        if len(input_comma) == 0:
            raise ValueError('input_comma cannot be empty')

        _maxchar = 0
        color_type = color_type.lower()
        if color_type == 'rgb':
            _maxchar = 11  # RRR,GGG,BBB
            valid_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', input_comma]
        elif color_type == 'hex':
            _maxchar = 7  # #XXYYZZ
            valid_chars = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F', '#', '0', '1', '2', '3', '4',
                           '5', '6', '7', '8', '9']
        else:
            raise ValueError('color type must be "rgb" or "hex"')

        _input_type = _locals.INPUT_TEXT
        _maxwidth = 0
        _password = False
        super(ColorInput, self).__init__(label=label,
                                         textinput_id=colorinput_id,
                                         input_type=_input_type,
                                         input_underline=input_underline,
                                         cursor_color=cursor_color,
                                         enable_copy_paste=False,
                                         enable_selection=False,
                                         history=0,
                                         maxchar=_maxchar,
                                         maxwidth=_maxwidth,  # Disabled
                                         onchange=onchange,
                                         onreturn=onreturn,
                                         password=_password,
                                         repeat_keys_initial_ms=repeat_keys_initial_ms,
                                         repeat_keys_interval_ms=repeat_keys_interval_ms,
                                         repeat_mouse_interval_ms=repeat_mouse_interval_ms,
                                         valid_chars=valid_chars,
                                         kwargs=kwargs,
                                         )
