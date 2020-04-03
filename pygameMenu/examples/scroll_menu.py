# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - LONG SCROLLING MENU
Shows scrolling in menu.

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
from pygameMenu.scrollarea import ScrollArea


def make_world(width, height):
    world = pygame.Surface((width, height))  # pylint: disable-msg=E1121
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


def main():
    """
    Main function
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

    scr_size = (400, 600)
    screen = pygame.display.set_mode(scr_size)
    world = make_world(scr_size[0] * 3, scr_size[1] * 4)

    screen.fill((120, 90, 130))

    pygame.display.set_caption("ScrollArea")
    bg = pygame.Surface(scr_size).convert()

    sp = ScrollArea(world,
                    scr_size[0],
                    scr_size[1],
                    shadow=True)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:
        event = pygame.event.wait()

        if event.type is pygame.QUIT:
            break

        sp.update([event])
        sp.draw(bg)

        screen.blit(bg, (0, 0))

        pygame.display.update()


if __name__ == '__main__':
    main()
