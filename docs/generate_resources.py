# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

GENERATE RESOURCES
Generate resources for docs.

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

import pygame_menu
import pygame

pygame.init()


def save_font_image(font_name, text, filename, font_size=50, image_height=26):
    """
    Generate a font image and save as a png.

    :param font_name: Font name
    :type font_name: str
    :param text: Text to render
    :type text: str
    :param filename: File to save the font
    :type filename: str
    :param font_size: Font size
    :type font_size: int
    :param image_height: Image size in px
    :type image_height: int
    """
    assert isinstance(font_size, int)
    assert isinstance(image_height, int)
    assert font_size > 0 and image_height > 0
    font = pygame_menu.font.get_font(font_name, font_size)
    surf = font.render(text, True, (0, 0, 0))  # type: pygame.Surface
    h, w = surf.get_height(), surf.get_width()
    new_width = int(w * (float(image_height) / h))
    surf2 = pygame.transform.smoothscale(surf, (new_width, image_height))
    pygame.image.save(surf2, filename)


def generate_fonts_doc():
    """
    Generate images for all fonts.

    :return: None
    """
    text = 'pygame menu'
    save_font_image(pygame_menu.font.FONT_8BIT, text, '_static/font_8bit.png')
    save_font_image(pygame_menu.font.FONT_BEBAS, text, '_static/font_bebas.png')
    save_font_image(pygame_menu.font.FONT_COMIC_NEUE, text, '_static/font_comic_neue.png')
    save_font_image(pygame_menu.font.FONT_FRANCHISE, text, '_static/font_franchise.png')
    save_font_image(pygame_menu.font.FONT_HELVETICA, text, '_static/font_helvetica.png')
    save_font_image(pygame_menu.font.FONT_MUNRO, text, '_static/font_munro.png')
    save_font_image(pygame_menu.font.FONT_NEVIS, text, '_static/font_nevis.png')
    save_font_image(pygame_menu.font.FONT_OPEN_SANS, text, '_static/font_open_sans.png')
    save_font_image(pygame_menu.font.FONT_OPEN_SANS_BOLD, text, '_static/font_open_sans_bold.png')
    save_font_image(pygame_menu.font.FONT_OPEN_SANS_ITALIC, text, '_static/font_open_sans_italic.png')
    save_font_image(pygame_menu.font.FONT_OPEN_SANS_LIGHT, text, '_static/font_open_sans_light.png')
    save_font_image(pygame_menu.font.FONT_PT_SERIF, text, '_static/font_pt_serif.png')


if __name__ == '__main__':
    generate_fonts_doc()
