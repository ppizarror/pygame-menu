# Pygame Menu
Python library that can create a Menu on Pygame, Supports:

1. Textual menus
2. Textual menus + buttons
3. Lists of values (that i called **Selectors**) that can trigger functions when pressing Return or changing the value
4. Button menus

Examples:
##### Normal Button menu
<p align="center">
<img src="https://github.com/ppizarror/ppizarror.github.io/blob/master/resources/images/pygame-menu/cap1.PNG?raw=true" width="40%px" height="40%px">
</p>

##### Text menu
<p align="center">
<img src="https://github.com/ppizarror/ppizarror.github.io/blob/master/resources/images/pygame-menu/cap2.PNG?raw=true" width="40%px" height="40%px">
</p>

##### Small submenu
<p align="center">
<img src="https://github.com/ppizarror/ppizarror.github.io/blob/master/resources/images/pygame-menu/cap3.PNG?raw=true" width="40%px" height="40%px">
</p>

## Import

Import of this library is similar as pygame:
```python
import pygameMenu                # This imports classes and other things
from pygameMenu.locals import *  # Import constants (like actions)
```

Obviously you need <a href="http://www.pygame.org/download.shtml">Pygame</a> to run this.

## Usage

### Creating menus

- **Menu**

    > This class creates a Menu
    >  
    > ```python
    > pygameMenu.Menu(surface, window_width, window_height, font, title, *args) # -> Menu object
    > ```
    >
    > Parameters are the following:
    >
    > | Param | Description | Type |
    > | :-: | :--| :--:|
    > |  surface |  	 Pygame surface object | Surface
    > |  window_width|     Window width size (px)| int|
    > |  window_height|    Window height size (px) |int|
    > |  font | Font file direction|str|
    > |  title | Title of the menu (main title)|str
    > |  enabled| Menu is enabled by default or not|bool
    > | bgfun| Background drawing function (only if menu pause app) | function|
    > | color_selected|Color of selected item|tuple
    > |  dopause| Pause game|bool
    > |  draw_region_x| Drawing position of element inside menu (x-axis)|int|
    > |  draw_region_y| Drawing position of element inside menu (y-axis)|int|
    > | draw_select| Draw a rectangle around selected item (bool)|bool|
    > |  font_color| Color of font|tuple|
    > |  font_size| Font size|int|
    > |  font_size_title| Font size of the title|int|
    > | font_title| Alternative font of the title (file direction)|str|
    > |  menu_alpha| Alpha of background (0=transparent, 100=opaque) | int|
    > |  menu_centered| Text centered menu|bool|
    > |  menu_color| Menu color|tuple|
    > |  menu_color_title| Background color of title|tuple|
    > | menu_height| Height of menu (px)|int|
    > |  menu_width| Width of menu (px)|int|
    > |  onclose| Event that applies when closing menu|function, PymenuAction|
    > |  option_margin| Margin of each element in menu (px)|int|
    > | option_shadow| Indicate if a shadow is drawn on each option|bool|
    > | rect_width| Border with of rectangle around selected item|int|
    > | title_offsetx| Offset x-position of title (px)|int|
    > | title_offsety| Offset y-position of title (px)|int|


- **TextMenu**

    > This class creates a textual menu
    > ```python
    > pygameMenu.TextMenu(surface, window_width, window_height, font, title, *args) # -> TextMenu object
    > ```
    >
    > This class inherites from Menu, so the parameters are the same, except the following extra parameters:
    >
    >
    > | Param | Description | Type |
    > | :-: | :--| :--:|
    > |text_centered| Indicate if text is centered| bool|
    > |text_color| Text color|tuple|
    > |text_fontsize| Text font size| int
    > |text_margin| Line margin| int
    > |draw_text_region_x| X-Axis drawing region of the text| int|

### Add options and entries to Menus

**Menu** and **TextMenu** have the next functions:

- <i>add_option(self, element_name, element, *args)</i>: Adds an *option* to the Menu

    | Param | Description | Type |
    | :-: | :--| :--:|
    |element_name| String on menu entry| str|
    |element_name| Menu object (Menu, function or Menu-Event) supported |_PymenuAction, function, Menu|
    |*args| Additional arguments | -|
    
    
    Example:
    ```python
    help_menu = pygameMenu.TextMenu(surface,window_width=W_SIZE, window_height=H_SIZE,
                                    font=pygameMenu.fonts.FONT_FRANCHISE,
                                    onclose=PYGAME_MENU_DISABLE_CLOSE,
                                    title='Help', dopause=False,                        
                                    menu_color_title=(120, 45, 30),
                                    menu_color=(30, 50, 107))
    help_menu.add_option('Return to Menu', PYGAME_MENU_BACK) # Add option
    ```
     
    Another example:
    ```python
    menu = pygameMenu.Menu(surface,window_width=W_SIZE, window_height=H_SIZE,
                           font=pygameMenu.fonts.FONT_NEVIS,
                           title='Main Menu', title_offsety=5,
                           menu_alpha=90, enabled=False,
                           bgfun=mainmenu_background)
    menu.add_option(timer_menu.get_title(), timer_menu)  # Add timer submenu
    menu.add_option(help_menu.get_title(), help_menu)    # Add help submenu
    menu.add_option(about_menu.get_title(), about_menu)  # Add about submenu
    menu.add_option('Exit', PYGAME_MENU_EXIT)            # Add exit function
    ```

- <i>add_selector(self, title, values, onchange, onreturn, **kwargs)</i>: Add a *selector* to menu: several options with values and two functions that execute when changing the selector (left/right) and pressing *Return key* on the element.

    | Param | Description | Type |
    | :-: | :--| :--:|
    |title| String on menu entry| str|
    |values| Value list, list of tuples|list
    |onchange| Function that executes when change the value of selector| function|
    |onreturn| Function that executes when pressing return button on selected item | function|
    |**kwargs| Additional arguments | -|
    
    Example:
    ```python
    def change_color_bg(c, **kwargs):
        """
        Change background color
        
        :param c: Color tuple
        """
        if c == (-1, -1, -1):  # If random color
            c = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
        if kwargs['write_on_console']:
            print('New bg color: ({0},{1},{2})'.format(*c))
        COLOR_BACKGROUND[0] = c[0]
        COLOR_BACKGROUND[1] = c[1]
        COLOR_BACKGROUND[2] = c[2]
        
    timer_menu = pygameMenu.Menu(...)
    
    # Add selector
    timer_menu.add_selector('Change bgcolor',
                            # Values of selector, call to change_color_bg
                            [('Random', (-1, -1, -1)),  # Random color
                             ('Default', (128, 0, 128)),
                             ('Black', (0, 0, 0)),
                             ('Blue', COLOR_BLUE)],
                            None, # onchange
                            change_color_bg, # onreturn
                            write_on_console=True # Optional change_color_bg param)
                            
    timer_menu.add_option('Reset timer', reset_timer)
    timer_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
    timer_menu.add_option('Close Menu', PYGAME_MENU_CLOSE)
    ```

### Menu events

Supported events are the same:

| Event | Description |
| :-:|:--|
|PYGAME_MENU_BACK | Go back on menu|
| PYGAME_MENU_CLOSE | Close menu|
|PYGAME_MENU_EXIT | Close application
| PYGAME_MENU_DISABLE_CLOSE | Disable close menu|
| PYGAME_MENU_RESET | Reset menu |

## Licence
This project is licenced under GPLv3 (GNU General Public License, version 3) [https://www.gnu.org/licenses/gpl-3.0.html].

## Author
Author: Pablo Pizarro, 2017.


