# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

LABEL
Label class, to add simple text to the menu.

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

from pygameMenu.widgets.widget import Widget


class Label(Widget):
    """
    Label widget.
    """

    def __init__(self, label, label_id=''):
        """
        Description of the specific parameters (see Widget class for generic ones):

        :param label: Text of the button
        :type label: basestring
        :param label_id: Button ID
        :type label_id: basestring
        """
        assert isinstance(label, str)
        super(Label, self).__init__(widget_id=label_id)
        self._label = label
        self.is_selectable = False

    def _apply_font(self):
        """
        See upper class doc.
        """
        pass

    def draw(self, surface):
        """
        See upper class doc.
        """
        self._render()
        surface.blit(self._surface, self._rect.topleft)

    def draw_selected_rect(self, *args, **kwargs):
        """
        See upper class doc.
        """
        pass  # Nothing to select

    def _render(self):
        """
        See upper class doc.
        """
        self._surface = self.render_string(self._label, self._font_color)

    def update(self, events):
        """
        See upper class doc.
        """
        return False
