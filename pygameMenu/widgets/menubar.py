# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

MENUBAR
MenuBar class to display menu title.

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

import pygame as _pygame
import pygame.gfxdraw as _gfxdraw
from pygameMenu.widgets.widget import Widget
import pygameMenu.controls as _ctrl


# noinspection PyTypeChecker
class MenuBar(Widget):
    """
    MenuBar widget.
    """

    def __init__(self,
                 label,
                 width,
                 back_box=False,
                 onchange=None,
                 onreturn=None,
                 *args,
                 **kwargs
                 ):
        """
        Description of the specific paramaters (see Widget class for generic ones):

        :param label: Title of the menu
        :type label: basestring
        :param width: Width of the menu bar (generally width of the menu dialog)
        :type width: int
        :param back_box: Draw a back-box button on header
        :type back_box: bool
        :param onchange: Callback when changing the selector
        :type onchange: function, NoneType
        :param onreturn: Callback when pressing return button
        :type onreturn: function, NoneType
        :param args: Optional arguments for callbacks
        :param kwargs: Optional keyword-arguments for callbacks
        """
        assert isinstance(label, str)
        assert isinstance(width, (int, float))
        assert isinstance(back_box, bool)

        # MenuBar has no ID
        super(MenuBar, self).__init__(onchange=onchange,
                                      onreturn=onreturn,
                                      args=args,
                                      kwargs=kwargs
                                      )

        self._backbox = back_box
        self._backbox_pos = None  # type: tuple
        self._backbox_rect = None  # type: _pygame.rect.RectType
        self._label = label
        self._offsetx = 0
        self._offsety = 0
        self._polygon_pos = None  # type: tuple
        self._width = width

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

        _gfxdraw.filled_polygon(surface, self._polygon_pos, self._font_color)

        if self.mouse_enabled and self._backbox:
            _pygame.draw.rect(surface, self._font_selected_color, self._backbox_rect, 1)
            _pygame.draw.polygon(surface, self._font_selected_color, self._backbox_pos)

        surface.blit(self._surface,
                     (5 + self._rect.topleft[0] + self._offsetx,
                      self._rect.topleft[1] + self._offsety))

    def get_title(self):
        """
        Return the title of the menu.

        :return: Title
        :rtype: basestring
        """
        return self._label

    def _render(self):
        """
        See upper class doc.
        """
        self._surface = self.render_string(self._label, self._font_selected_color)

        # Usually done in get_rect(), but can not be called here because it call _render() itself
        self._rect.width, self._rect.height = self._surface.get_size()

        self._polygon_pos = (
            (self._rect.x, self._rect.y),
            (self._rect.x + self._width, self._rect.y),
            (self._rect.x + self._width, self._rect.y + self._rect.height * 0.6),
            (self._rect.x + self._rect.width + 30, self._rect.y + self._rect.height * 0.6),
            (self._rect.x + self._rect.width + 10, self._rect.y + self._rect.height + 5),
            (self._rect.x, self._rect.y + self._rect.height + 5)
        )

        cross_size = self._polygon_pos[2][1] - self._polygon_pos[1][1] - 6
        self._backbox_rect = _pygame.Rect(self._polygon_pos[1][0] - cross_size - 3,
                                          self._polygon_pos[1][1] + 3,
                                          cross_size, cross_size)

        self._backbox_pos = (
            (self._backbox_rect.left + 5, self._backbox_rect.centery),
            (self._backbox_rect.centerx, self._backbox_rect.top + 5),
            (self._backbox_rect.centerx, self._backbox_rect.centery - 2),
            (self._backbox_rect.right - 5, self._backbox_rect.centery - 2),
            (self._backbox_rect.right - 5, self._backbox_rect.centery + 2),
            (self._backbox_rect.centerx, self._backbox_rect.centery + 2),
            (self._backbox_rect.centerx, self._backbox_rect.bottom - 5),
            (self._backbox_rect.left + 5, self._backbox_rect.centery)
        )

    def set_title(self, title, offsetx=0, offsety=0):
        """
        Set menu title.

        :param title: Menu title
        :type title: str
        :param offsetx: Offset x-position of title (px)
        :type offsetx: int
        :param offsety: Offset y-position of title (px)
        :type offsety: int
        :return: None
        """
        assert isinstance(title, str)
        assert isinstance(offsetx, int)
        assert isinstance(offsety, int)

        self._label = title
        self._offsety = offsety
        self._offsetx = offsetx

    def update(self, events):
        """
        See upper class doc.
        """
        updated = False
        for event in events:  # type: _pygame.event.EventType

            if self.mouse_enabled and event.type == _pygame.MOUSEBUTTONUP:
                if self._backbox_rect and self._backbox_rect.collidepoint(*event.pos):
                    self.sound.play_click_mouse()
                    self.apply()
                    updated = True

            elif self.joystick_enabled and event.type == _pygame.JOYBUTTONDOWN:
                if event.button == _ctrl.JOY_BUTTON_BACK:
                    self.sound.play_key_del()
                    self.apply()
                    updated = True

        return updated
