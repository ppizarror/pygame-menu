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


# noinspection PyTypeChecker
class ColorInput(TextInput):
    """
    Color input widget.
    """

    def __init__(self,
                 label='',
                 colorrgb_id='',
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
        :param colorrgb_id: ID of the text input
        :type colorrgb_id: basestring
        :param input_underline: Character drawn under each number input (rgb channels)
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
        assert isinstance(colorrgb_id, str)
        assert isinstance(input_underline, str)
        assert isinstance(cursor_color, tuple)
        assert isinstance(repeat_keys_initial_ms, int)
        assert isinstance(repeat_keys_interval_ms, int)
        assert isinstance(repeat_mouse_interval_ms, int)

        super(ColorInput, self).__init__(label='',
                                         textinput_id='',
                                         input_type=_locals.INPUT_TEXT,
                                         input_underline='',
                                         cursor_color=(0, 0, 0),
                                         enable_selection=False,
                                         history=0,
                                         maxchar=0,
                                         maxwidth=0,
                                         maxwidth_dynamically_update=True,
                                         onchange=None,
                                         onreturn=None,
                                         password=False,
                                         password_char='*',
                                         repeat_keys_initial_ms=450,
                                         repeat_keys_interval_ms=80,
                                         repeat_mouse_interval_ms=100,
                                         selection_color=(30, 30, 30),
                                         text_ellipsis='...',
                                         kwargs=kwargs)
