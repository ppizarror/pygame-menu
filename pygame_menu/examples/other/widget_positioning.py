"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - WIDGET POSITIONING
Test widget positioning example.
"""

import pygame_menu
from pygame_menu.examples import create_example_window

# Create the surface
surface = create_example_window('Example - Widget Positioning', (640, 480))

# Create a custom theme
my_theme = pygame_menu.themes.THEME_DARK.copy()
my_theme.title = False  # Hide the menu title

menu = pygame_menu.Menu(
    height=480,  # Use full-screen
    theme=my_theme,
    title='',
    center_content=False,
    width=640
)

w = menu.add.label('My App')
w.set_background_color('#333333', inflate=(30, 0))
w.set_float()

w = menu.add.label('Lorem ipsum', font_name=pygame_menu.font.FONT_OPEN_SANS_ITALIC, font_size=25)
w.rotate(90)
w.translate(300, 160)

# Button options
menu.add.button('Main Menu', lambda: print(f'My method')).set_float().translate(-200,60)

# Bottom scrollable text
f = menu.add.frame_v(
    width=200,
    height=500,
    max_height=100,
    background_color='#6b6e5e',
    border_color='#36372f',
    border_width=1
)
f.set_float()
f.translate(220, 390)
labels = [menu.add.label(f'  Lorem ipsum #{i}', font_size=15, font_color='#000000', padding=0) for i in range(20)]
for j in labels:
    f.pack(j)
    menu.render()
menu.render()

# Button options
menu.add.button('Main Menu 2', lambda: print(f'My method')).set_float().translate(-200,60)

if __name__ == '__main__':
    menu.mainloop(surface)
