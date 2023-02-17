"""
pygame-menu
https://github.com/ppizarror/pygame-menu

WIDGET ADDITION EXAMPLE DOCS
See https://pygame-menu.readthedocs.io/en/latest/_source/add_widgets.html
"""

import sys

sys.path.insert(0, '../')

import pygame
import pygame_menu
from typing import List

# Init pygame
pygame.init()
surface = pygame.display.set_mode((400, 300))
pygame.display.set_caption('pygame-menu v4')

# Set pygame-menu image
icon = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU).get_surface()
pygame.display.set_icon(icon)

# Set example, only this should change
EXAMPLE = 'BUTTON'

# Create example
menu: 'pygame_menu.Menu'
widgets: List['pygame_menu.widgets.Widget']


def make_menu(
    menu_theme: 'pygame_menu.themes.Theme',
    title: str,
    center: bool = True,
    widget_font_size: int = 25
) -> 'pygame_menu.Menu':
    """
    Make menu.

    :param menu_theme: Menu theme object
    :param title: Menu title
    :param center: Center the menu
    :param widget_font_size: Theme widget font size
    :return: Menu object
    """
    menu_theme = menu_theme.copy()
    menu_theme.title_font_size = 35
    menu_theme.widget_font_size = widget_font_size

    return pygame_menu.Menu(
        center_content=center,
        column_min_width=400,
        height=300,
        onclose=pygame_menu.events.CLOSE,
        theme=menu_theme,
        title=title,
        width=400
    )


# noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
def change_background_color(selected_value, color, **kwargs):
    from random import randrange
    value_tuple, index = selected_value
    print('Change widget color to', value_tuple[0])  # selected_value format ('Color', surface, color)
    if color == (-1, -1, -1):  # Generate a random color
        color = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
    widget: 'pygame_menu.widgets.Selector' = kwargs.get('widget')
    widget.update_font({'selected_color': color})
    widget.get_selection_effect().color = color


# noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
def func(name):
    print('Hello world from', name)  # name will be 'foo'


# Init examples
if EXAMPLE == 'BUTTON':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Button')
    about_menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'About')

    menu.add.button('Exec', func, 'foo',  # Execute a function, it receives 'foo' as *arg
                    align=pygame_menu.locals.ALIGN_LEFT)
    btn = menu.add.button(about_menu.get_title(), about_menu,  # Open a sub-menu
                          shadow=True, shadow_color=(0, 0, 100))
    menu.add.button('Exit', pygame_menu.events.EXIT,  # Link to exit action
                    align=pygame_menu.locals.ALIGN_RIGHT)
    btn.select(update_menu=True)

elif EXAMPLE == 'BUTTON_BANNER':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Banner')

    image = pygame_menu.BaseImage(
        image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU
    ).scale(0.25, 0.25)
    menu.add.banner(image, pygame_menu.events.EXIT)

elif EXAMPLE == 'CLOCK':
    menu = make_menu(pygame_menu.themes.THEME_DARK, 'Clock')

    clock = menu.add.clock(font_size=25, font_name=pygame_menu.font.FONT_DIGITAL)

elif EXAMPLE == 'COLORINPUT':
    menu = make_menu(pygame_menu.themes.THEME_DARK, 'Color Entry')

    menu.add.color_input('RGB color 1: ',
                         color_type=pygame_menu.widgets.COLORINPUT_TYPE_RGB,
                         default=(255, 0, 255), font_size=18)
    menu.add.color_input('RGB color 2: ',
                         color_type=pygame_menu.widgets.COLORINPUT_TYPE_RGB,
                         input_separator='-', font_size=18)
    menu.add.color_input('HEX color 3: ',
                         color_type=pygame_menu.widgets.COLORINPUT_TYPE_HEX,
                         default='#ffaa11', font_size=18)

elif EXAMPLE == 'DROPSELECT':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Drop Select')

    selector_epic = menu.add.dropselect(
        title='Is pygame-menu epic?',
        items=[('Yes', 0),
               ('Absolutely Yes', 1)],
        font_size=16,
        selection_option_font_size=20
    )
    selector_sum = menu.add.dropselect(
        title='What is the value of π?',
        items=[('3 (Engineer)', 0),
               ('3.1415926535897932384626433832795028841971693993751058209', 1),
               ('4', 2),
               ('I don\'t know what is π', 3)],
        font_size=16,
        selection_box_width=173,
        selection_option_padding=(0, 5),
        selection_option_font_size=20
    )
    selector_country = menu.add.dropselect(
        title='Pick a country',
        items=[('Argentina', 'ar'),
               ('Australia', 'au'),
               ('Bolivia', 'bo'),
               ('Chile', 'ch'),
               ('China', 'cn'),
               ('Finland', 'fi'),
               ('France', 'fr'),
               ('Germany', 'de'),
               ('Italy', 'it'),
               ('Japan', 'jp'),
               ('Mexico', 'mx'),
               ('Peru', 'pe'),
               ('United States', 'us')],
        font_size=20,
        default=3,
        open_middle=True,  # Opens in the middle of the menu
        selection_box_height=5,
        selection_box_width=212,
        selection_infinite=True,
        selection_option_font_size=20
    )

elif EXAMPLE == 'DROPSELECT_MULTIPLE':
    menu = make_menu(pygame_menu.themes.THEME_GREEN, 'Drop Select Multiple', center=False)
    menu.add.vertical_margin(75)

    selector = menu.add.dropselect_multiple(
        title='Pick 3 colors',
        items=[('Black', (0, 0, 0)),
               ('Blue', (0, 0, 255)),
               ('Cyan', (0, 255, 255)),
               ('Fuchsia', (255, 0, 255)),
               ('Green', (0, 255, 0)),
               ('Red', (255, 0, 0)),
               ('White', (255, 255, 255)),
               ('Yellow', (255, 255, 0))],
        font_size=23,
        max_selected=3,
        selection_option_font_size=23
    )

elif EXAMPLE == 'FRAME':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Frames', widget_font_size=18)
    menu.get_theme().widget_selection_effect.zero_margin()

    frame = menu.add.frame_v(250, 150, background_color=(50, 50, 50), padding=0)
    frame_title = menu.add.frame_h(250, 29, background_color=(180, 180, 180), padding=0)
    frame_content = menu.add.frame_v(250, 120, padding=0)
    frame.pack(frame_title)
    frame.pack(frame_content)

    frame_title.pack(menu.add.label('Settings', padding=0), margin=(2, 2))
    frame_title.pack(
        menu.add.button('Close', pygame_menu.events.EXIT, padding=(0, 5),
                        background_color=(100, 100, 100)),
        align=pygame_menu.locals.ALIGN_RIGHT, margin=(2, 2))
    frame_content.pack(
        menu.add.label('Pick a number', font_color=(150, 150, 150)),
        align=pygame_menu.locals.ALIGN_CENTER)
    frame_numbers = menu.add.frame_h(250, 41, padding=0)
    frame_content.pack(frame_numbers)
    for i in range(9):
        frame_numbers.pack(
            menu.add.button(i, font_color=(5 * i, 11 * i, 13 * i),
                            padding=(0, 5), font_size=30),
            align=pygame_menu.locals.ALIGN_CENTER)
    frame_content.pack(menu.add.vertical_margin(15))
    frame_content.pack(
        menu.add.toggle_switch('Nice toggle', False, width=100,
                               font_color=(150, 150, 150), padding=0),
        align=pygame_menu.locals.ALIGN_CENTER)

elif EXAMPLE == 'FRAME_TITLE':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Frame + Title', widget_font_size=18)
    menu.get_theme().widget_selection_effect.zero_margin()

    frame = menu.add.frame_v(400, 800, background_color=(50, 50, 50), padding=0,
                             max_width=300, max_height=100)
    frame.set_title('My Frame App', title_font_color='white', padding_inner=(2, 5))

    frame.pack(menu.add.dropselect(
        title='Is pygame-menu epic?',
        items=[('Yes', 0),
               ('Absolutely Yes', 1)],
        font_color='white',
        font_size=16,
        selection_option_font_size=20
    ))
    for i in range(20):
        frame.pack(menu.add.button(i, font_color='white', button_id=f'b{i}'))

    # Don't copy
    menu.select_widget('b0')

elif EXAMPLE == 'IMAGE':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Image')

    image_path = pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU
    menu.add.image(image_path, angle=10, scale=(0.15, 0.15))
    menu.add.image(image_path, angle=-10, scale=(0.15, 0.15))

elif EXAMPLE == 'MENU_LINK':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Menu Links')
    menu1 = make_menu(pygame_menu.themes.THEME_ORANGE, 'Menu 1')
    menu2 = make_menu(pygame_menu.themes.THEME_GREEN, 'Menu 2')
    menu3 = make_menu(pygame_menu.themes.THEME_SOLARIZED, 'Menu 3')


    def open_link(*args) -> None:
        """
        Opens link.
        """
        link: 'pygame_menu.widgets.MenuLink' = args[-1]
        link.open()


    # Create the links
    link1 = menu.add.menu_link(menu1)
    link2 = menu.add.menu_link(menu2)
    link3 = menu.add.menu_link(menu3)

    # Add a selection object, which opens the links
    sel = menu.add.selector('Change menu ', [
        ('Menu 1', link1),
        ('Menu 2', link2),
        ('Menu 3', link3)
    ], onreturn=open_link)

elif EXAMPLE == 'LABEL':
    menu = make_menu(pygame_menu.themes.THEME_BLUE, 'Label')

    HELP = 'Press ESC to enable/disable Menu ' \
           'Press ENTER to access a Sub-Menu or use an option ' \
           'Press UP/DOWN to move through Menu ' \
           'Press LEFT/RIGHT to move through Selectors.'
    menu.add.label(HELP, max_char=-1, font_size=20)

elif EXAMPLE == 'PROGRESSBAR':
    menu = make_menu(pygame_menu.themes.THEME_DARK, 'Progress Bar', widget_font_size=18)

    progress1 = menu.add.progress_bar('My Progress', default=75.6)
    progress2 = menu.add.progress_bar('Pygame-menu epicness?', default=99.9)

elif EXAMPLE == 'RANGESLIDER':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Range Slider', widget_font_size=18)

    # Single value
    menu.add.range_slider('Choose a number', 50, (0, 100), 1,
                          rangeslider_id='range_slider',
                          value_format=lambda x: str(int(x)))

    # Range
    menu.add.range_slider('Pick a range', (7, 10), (1, 10), 1)

    # Discrete value
    range_values_discrete = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F'}
    menu.add.range_slider('Pick a letter', 0, list(range_values_discrete.keys()),
                          slider_text_value_enabled=False,
                          value_format=lambda x: range_values_discrete[x])

    # Numeric discrete range
    menu.add.range_slider('Pick a discrete range', (2, 4), [0, 1, 2, 3, 4, 5], 1)

elif EXAMPLE == 'SELECTOR':
    menu = make_menu(pygame_menu.themes.THEME_ORANGE, 'Selector')

    items = [('Default', (255, 255, 255)),
             ('Black', (0, 0, 0)),
             ('Blue', (0, 0, 255)),
             ('Random', (-1, -1, -1))]
    selector = menu.add.selector(
        title='Current color:\t',
        items=items,
        onreturn=change_background_color,  # User press "Return" button
        onchange=change_background_color  # User changes value with left/right keys
    )
    selector.add_self_to_kwargs()  # Callbacks will receive widget as parameter
    selector2 = menu.add.selector(
        title='New color:',
        items=items,
        style=pygame_menu.widgets.SELECTOR_STYLE_FANCY
    )

elif EXAMPLE == 'SURFACE':
    menu = make_menu(pygame_menu.themes.THEME_SOLARIZED, 'Surface')

    new_surface = pygame.Surface((160, 160))
    new_surface.fill((255, 192, 203))
    inner_surface = pygame.Surface((80, 80))
    inner_surface.fill((75, 0, 130))
    new_surface.blit(inner_surface, (40, 40))
    menu.add.surface(new_surface)

elif EXAMPLE == 'TABLE':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Tables')

    table = menu.add.table(table_id='my_table', font_size=20)
    table.default_cell_padding = 5
    table.default_row_background_color = 'white'
    table.add_row(['First item', 'Second item', 'Third item'],
                  cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)
    table.add_row(['A', 'B', 1])
    table.add_row(['α', 'β', 'γ'], cell_align=pygame_menu.locals.ALIGN_CENTER)

elif EXAMPLE == 'TABLE_ADVANCED':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Advanced Table')

    table = menu.add.table(font_size=20)
    table.default_cell_padding = 5
    table.default_cell_align = pygame_menu.locals.ALIGN_CENTER
    table.default_row_background_color = 'white'
    table.add_row(['A', 'B', 'C'],
                  cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)

    # Sub-table
    table_2 = menu.add.table(font_size=20)
    table_2.default_cell_padding = 20
    table_2.add_row([1, 2])
    table_2.add_row([3, 4])

    # Sub image
    image = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU)
    image.scale(0.25, 0.25)

    # Add the sub-table and the image
    table.add_row([table_2, '', image],
                  cell_vertical_position=pygame_menu.locals.POSITION_CENTER)
    table.update_cell_style(1, 2, padding=0)  # Disable padding for cell column 1, row 2 (table_2)
    table.update_cell_style(2, 2, border_position=pygame_menu.locals.POSITION_SOUTH)
    table.update_cell_style(3, 2, border_position=(pygame_menu.locals.POSITION_SOUTH,
                                                   pygame_menu.locals.POSITION_EAST))

elif EXAMPLE == 'TEXTINPUT':
    menu = make_menu(pygame_menu.themes.THEME_GREEN, 'Text Entry')

    menu.add.text_input('First name: ', default='John')
    menu.add.text_input('Last name: ', default='Doe', maxchar=10, input_underline='_')
    menu.add.text_input('Password: ', input_type=pygame_menu.locals.INPUT_INT, password=True)

elif EXAMPLE == 'TOGGLESWITCH':
    menu = make_menu(pygame_menu.themes.THEME_SOLARIZED, 'Switches')

    menu.add.toggle_switch('First Switch', False, toggleswitch_id='first_switch')
    menu.add.toggle_switch('Other Switch', True, toggleswitch_id='second_switch',
                           state_text=('Apagado', 'Encendido'), state_text_font_size=18)

elif EXAMPLE == 'URL':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Url', widget_font_size=18)

    menu.add.url('https://github.com/ppizarror/pygame-menu')
    menu.add.url('https://github.com/ppizarror/pygame-menu', 'The best menu ever')
    menu.add.url('https://pygame-menu.readthedocs.io/en/master/', 'pygame-menu documentation')

elif EXAMPLE == 'VERTICALFILL':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Vertical fill')

    menu.add.vertical_fill()
    menu.add.button('Button 1')
    menu.add.vertical_fill()
    menu.add.button('Button 2')
    menu.add.vertical_fill()

elif EXAMPLE == 'VERTICALMARGIN':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Vertical spacer')

    menu.add.label('Text #1')
    menu.add.vertical_margin(100)
    menu.add.label('Text #2')

else:
    raise ValueError(f'unknown example "{EXAMPLE}"')

# Execute menu
menu.mainloop(surface)
