# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - USE SCROLLBAR WIDGET
Shows how the ScrollBar can be used on a surface.

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

import os
import pygame
import pygameMenu.config as _cfg
import pygameMenu.locals as _locals
from pygameMenu.widgets import ScrollBar


def make_world(width, height):
    world = pygame.Surface((width, height))
    world.fill((200, 200, 200))

    color = [70, 20, 20]
    maxx = len(list(range(100, width, 200)))
    maxy = len(list(range(100, height, 200)))
    numberx = 0
    for x in range(100, width, 200):
        numbery = 0
        for y in range(100, height, 200):
            if numberx in (0, maxx - 1) or numbery in (0, maxy - 1):
                # White circles to delimite world boundaries
                pygame.draw.circle(world, (255, 255, 255), (x, y), 100, 10)
            else:
                pygame.draw.circle(world, color, (x, y), 100, 10)
                if color[0] + 15 < 255:
                    color[0] += 15
                elif color[1] + 15 < 255:
                    color[1] += 15
                else:
                    color[2] += 15
            numbery += 1
        numberx += 1

    return world


def h_changed(value):
    print("Horizontal position changed:", value)


def v_changed(value):
    print("Vertical position changed:", value)


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

    scr_size = (400, 600)
    screen = pygame.display.set_mode(scr_size)
    world = make_world(int(scr_size[0] * 4), scr_size[1] * 3)
    screen.fill((120, 90, 130))

    pygame.display.set_caption("ScrollBar")
    thick = 20

    # Horizontal ScrollBar
    sb_h = ScrollBar(scr_size[0] - thick,
                     (50, world.get_width() - scr_size[0] + thick),
                     _locals.ORIENTATION_HORIZONTAL,
                     2,
                     (200, 200, 200),
                     thick,
                     (240, 240, 240),
                     onchange=h_changed)
    sb_h.set_shadow(enabled=True,
                    color=_cfg.MENU_SHADOW_COLOR,
                    position=_locals.POSITION_SOUTHEAST,
                    offset=_cfg.MENU_SHADOW_OFFSET)
    sb_h.set_controls(False, True)
    sb_h.set_position(0, scr_size[1] - thick)
    sb_h.set_page_step(scr_size[0] - thick)

    # Vertical ScrollBar
    sb_v = ScrollBar(scr_size[1] - thick,
                     (0, world.get_height() - scr_size[1] + thick),
                     _locals.ORIENTATION_VERTICAL,
                     2,
                     (200, 200, 200),
                     thick,
                     (240, 240, 240),
                     onchange=v_changed)
    sb_v.set_shadow(enabled=True,
                    color=_cfg.MENU_SHADOW_COLOR,
                    position=_locals.POSITION_SOUTHEAST,
                    offset=_cfg.MENU_SHADOW_OFFSET)
    sb_v.set_controls(False, True)
    sb_v.set_position(scr_size[0] - thick, 0)
    sb_v.set_page_step(scr_size[1] - thick)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------

    while True:
        event = pygame.event.wait()

        if event.type is pygame.QUIT:
            break

        if event.type is pygame.KEYDOWN and event.key == pygame.K_h:
            sb_h.set_value(100)

        if event.type is pygame.KEYDOWN and event.key == pygame.K_v:
            sb_v.set_value(200)

        sb_h.update([event])
        sb_h.draw(screen)
        sb_v.update([event])
        sb_v.draw(screen)

        trunc_world_orig = (sb_h.get_value(), sb_v.get_value())
        trunc_world = (scr_size[0] - thick, scr_size[1] - thick)

        screen.blit(world, (0, 0), (trunc_world_orig, trunc_world))
        pygame.display.update()


if __name__ == '__main__':
    main()
