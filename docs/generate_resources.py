"""
pygame-menu
https://github.com/ppizarror/pygame-menu

GENERATE RESOURCES
Generate resources for docs.
"""

__all__ = ['save_font_image', 'generate_fonts_doc']

import pygame
import pygame_menu

pygame.init()


def save_font_image(
    font_name: str,
    text: str,
    filename: str,
    font_size: int = 50,
    image_height: int = 26
) -> None:
    """
    Generate a font image and save as a png.

    :param font_name: Font name
    :param text: Text to render
    :param filename: File to save the font
    :param font_size: Font size
    :param image_height: Image size in px
    """
    assert isinstance(font_size, int)
    assert isinstance(image_height, int)
    assert font_size > 0 and image_height > 0
    font = pygame_menu.font.get_font(font_name, font_size)
    surf = font.render(text, True, (0, 0, 0))
    h, w = surf.get_height(), surf.get_width()
    new_width = int(w * (float(image_height) / h))
    surf2 = pygame.transform.smoothscale(surf, (new_width, image_height))
    pygame.image.save(surf2, filename)


def generate_fonts_doc() -> None:
    """
    Generate images for all fonts.
    """
    text = 'pygame menu'
    save_font_image(pygame_menu.font.FONT_8BIT, text, '_static/font_8bit.png')
    save_font_image(pygame_menu.font.FONT_BEBAS, text, '_static/font_bebas.png')
    save_font_image(pygame_menu.font.FONT_COMIC_NEUE, text, '_static/font_comic_neue.png')
    save_font_image(pygame_menu.font.FONT_DIGITAL, text, '_static/font_digital.png')
    save_font_image(pygame_menu.font.FONT_FIRACODE, text, '_static/font_firacode.png')
    save_font_image(pygame_menu.font.FONT_FIRACODE_BOLD, text, '_static/font_firacode_bold.png')
    save_font_image(pygame_menu.font.FONT_FIRACODE_BOLD_ITALIC, text, '_static/font_firacode_bold_italic.png')
    save_font_image(pygame_menu.font.FONT_FIRACODE_ITALIC, text, '_static/font_firacode_italic.png')
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
