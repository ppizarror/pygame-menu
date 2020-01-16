<h1 align="center">
  <img alt="Pygame Menu" src="https://res.ppizarror.com/other/python.png" width="200px" height="200px" />
  <br /><br />
  Pygame Menu</h1>

<p align="center">Menu for pygame, simple, lightweight and easy to use</p>

<div align="left">
<a href="https://ppizarror.com"><img alt="@ppizarror" src="https://img.shields.io/badge/author-Pablo%20Pizarro%20R.-lightgray.svg" /></a>
<a href="https://opensource.org/licenses/MIT/"><img alt="License MIT" src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
<a href="https://www.python.org/downloads/"><img alt="Python 2.7+/3.4+" src="https://img.shields.io/badge/python-2.7+ / 3.4+-red.svg" /></a>
<a href="https://www.pygame.org/"><img alt="Pygame 1.9.4+" src="https://img.shields.io/badge/pygame-1.9.4+-orange.svg" /></a>
<a href="https://pypi.org/project/pygame-menu/"><img alt="PyPi package" src="https://badge.fury.io/py/pygame-menu.svg" /></a>
<br />
<a href="https://codecov.io/gh/ppizarror/pygame-menu"><img src="https://codecov.io/gh/ppizarror/pygame-menu/branch/master/graph/badge.svg" /></a>
<a href="https://travis-ci.org/ppizarror/pygame-menu"><img src="https://travis-ci.org/ppizarror/pygame-menu.svg?branch=master" /></a>
<a href="https://lgtm.com/projects/g/ppizarror/pygame-menu/alerts/"><img alt="Total alerts" src="https://img.shields.io/lgtm/alerts/g/ppizarror/pygame-menu.svg?logo=lgtm&logoWidth=18" /></a>
<a href="https://lgtm.com/projects/g/ppizarror/pygame-menu/context:python"><img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/ppizarror/pygame-menu.svg?logo=lgtm&logoWidth=18" /></a>
</div><br />

Python library that can create a simple menu for pygame application, supports:

1. Textual menus
2. Buttons
3. Lists of values (selectors) that can trigger functions when pressing return or changing the value
4. Input text

Examples:

#### Normal button menu

<p align="center">
    <img src="https://res.ppizarror.com/images/pygame-menu/example1.gif" width="60%" >
</p>

#### Textual menus

<p align="center">
    <img src="https://res.ppizarror.com/images/pygame-menu/example2.gif" width="60%"  >
</p>

#### Mouse support

<p align="center">
    <img src="https://res.ppizarror.com/images/pygame-menu/example3.gif" width="60%" >
</p>

#### Different inputs

<p align="center">
    <img src="https://res.ppizarror.com/images/pygame-menu/example4.gif" width="60%" >
</p>

## Install

Pygame-menu can be installed via pip. Simply run:

```bash
pip install pygame-menu
```

Currently python 2.7+ and 3.4+ (3.4, 3.5, 3.6, 3.7) are supported.

## Import

Import of this library is similar as pygame:

```python
import pygameMenu
```

## Library structure

| Module | Description |
| :--: | :--: |
| *pygameMenu.config* | Default configuration of Menus |
| *pygameMenu.controls* | Control definition, constants, etc. |
| *pygameMenu.events* | Events definition, constants, etc. |
| *pygameMenu.font* | Menu font management |
| *pygameMenu.locals* | Menu constants |
| *pygameMenu.Menu* | Menu class |
| *pygameMenu.sound* | Sound management |
| *pygameMenu.TextMenu* | TextMenu class |
| *pygameMenu.version* | Version of the library |

## Usage

### Creating menus

- **Menu**

    This class creates a menu.

    ```python
    pygameMenu.Menu(surface, window_width, window_height, font, title, *args) # -> Menu object
    ```

    Parameters are the following:

    | Param | Description | Type | Default |
    | :--: | :-- | :--: | :--: |
    | surface | Pygame surface object | Pygame Surface | - |
    | window_width | Window width size (px)| int | - |
    | window_height | Window height size (px) |int | - |
    | font | Font file dir | str | - |
    | title | Title of the menu (main title) | str | - |
    | back_box | Draw a back-box button on header | bool | True |
    | bgfun | Background drawing function (only if menupause app) | function | None |
    | color_selected | Color of selected item | tuple | MENU_SELECTEDCOLOR |
    | dopause | Pause game | bool | True |
    | draw_region_x | Drawing position of element inside menu (x-axis) as percentage | int | MENU_DRAW_X |
    | draw_region_y | Drawing position of element inside menu (y-axis) as percentage | int | MENU_DRAW_Y |
    | draw_select | Draw a rectangle around selected item (bool) | bool | MENU_SELECTED_DRAW |
    | enabled | Menu is enabled by default or not | bool | True |
    | font_color | Color of font | tuple | MENU_FONT_COLOR |
    | font_size | Font size of menu widgets | int | MENU_FONT_SIZE |
    | font_size_title | Font size of the title | int | MENU_FONT_SIZE_TITLE |
    | font_title | Alternative font of the title | str | None |
    | fps | Fps limit of the menu, 0: no limit | int,float | 0 |
    | joystick_enabled | Enable joystick support | bool | True |
    | menu_alpha | Alpha of background (0=tansparent, 100=opaque) | int | MENU_ALPHA |
    | menu_color | Menu color | tuple | MENU_BGCOLOR |
    | menu_color_title | Background color of title | tuple | MENU_TITLE_BG_COLOR |
    | menu_height | Height of menu (px) | int | MENU_HEIGHT |
    | menu_width | Width of menu (px) | int | MENU_WIDTH |
    | mouse_enabled | Enable mouse support | bool | True |
    | mouse_visible | Mouse visible or not, if not *mouse_enabled* wil be disabled | True |
    | onclose | Event that applies when closing menufunction | PymenuAction | None |
    | option_margin | Margin of each element in menu (px) | int | MENU_OPTION_MARGIN |
    | option_shadow | Indicate if a shadow is drawn on ech option | bool | MENU_OPTION_SHADOW |
    | option_shadow_offset | Offset of option text shadow | int | MENU_SHADOW_OFFSET |
    | option_shadow_position | Position of shadow | string | MENU_SHADOW_POSITION |
    | rect_width | Border with of rectangle around a seleted item | int | MENU_SELECTED_WIDTH |
    | title_offsetx | Offset x-position of title (px) | int | 0 |
    | title_offsety | Offset y-position of title (px) | int | 0 |
    | widget_alignment | Default widget alignment | string | locals.ALIGN_CENTER |

    Check widget alignment and shadow position possible values in [configuration](https://github.com/ppizarror/pygame-menu#configuration-values).

- **TextMenu**

     This class creates a textual menu.

    ```python
    pygameMenu.TextMenu(surface, window_width, window_height, font, title, *args) # -> TextMenu object
    ```

    This class inherites from Menu, so the parameters are the same, except the following extra parameters:  

    | Param | Description | Type | Default |
    | :--: | :-- | :--: | :--: |
    | draw_text_region_x | X-Axis drawing region of the text | int | TEXT_DRAW_X |
    | text_align | Text default alignment | string | locals.ALIGN_LEFT |
    | text_color | Text color | tuple | TEXT_FONT_COLOR |
    | text_fontsize | Text font size | int | MENU_FONT_TEXT_SIZE |
    | text_margin | Line margin | int | TEXT_MARGIN |

### Adding options and entries to menus

**Menu** and **TextMenu** have the next functions:

- *add_option(element_name, element, \*args)*

    Adds an *option* to the menu (buttons).

    | Param | Description | Type | Default |
    | :--: | :-- | :--: | :--: |
    | element_name | String on menu entry | str | *Required* |
    | element | Menu object (Menu, function or Menu-Event) supported | PymenuAction, function, Menu | *Required* |
    | *args | Additional arguments | - | - |
    | **kwargs | Additional keyword-arguments | - | - |

    Additional keyword arguments:

    | Param | Description | Type | Default |
    | :--: | :-- | :--: | :--: |
    | align | Button alignment | str | locals.ALIGN_CENTER |
    | font_size | Font size widget (overrides Menu default) | int | Menu *font_size* default |
    | option_id | Option identifier | str | "" |

    Check possible alignment in [configuration](https://github.com/ppizarror/pygame-menu#configuration-values).

    Example:

    ```python
    def fun():
        pass

    help_menu = pygameMenu.TextMenu(surface, window...)
    help_menu.add_option('Simple button', fun, align=pygameMenu.locals.ALIGN_LEFT)
    help_menu.add_option('Return to Menu', pygameMenu.events.MENU_BACK)
    ```

    Another example:

    ```python
    menu = pygameMenu.Menu(surface, window...)
    menu.add_option(timer_menu.get_title(), timer_menu)         # Adds timer submenu
    menu.add_option(help_menu.get_title(), help_menu)           # Adds help submenu
    menu.add_option(about_menu.get_title(), about_menu)         # Adds about submenu
    menu.add_option('Exit', pygameMenu.events.MENU_EXIT)        # Adds exit function
    ```

- *add_selector(title, values, selector_id, default, align, onchange, onreturn, \*\*kwargs)*

    Add a *selector* to the menu: several options with values and two functions that are executed when the selector is changed left/right (**onchange**) or *Return key* is pressed on the element (**onreturn**).

    | Param | Description | Type | Default |
    | :--: | :-- | :--: | :--: |
    | title | String on menu entry | str | *Required* |
    | values | Value list, list of tuples | list | *Required* |
    | selector_id | Selector identification | str | "" |
    | default | Default index of the displayed option | int | 0 |
    | align | Widget alignment | str | locals.ALIGN_CENTER |
    | font_size | Font size widget (overrides Menu default) | int | Menu *font_size* default |
    | onchange | Function that executes when change the value of selector | function | None |
    | onreturn | Function that executes when pressing return button on selected item | function | None |
    | **kwargs | Additional arguments | - | - |

    Check possible alignment in [configuration](https://github.com/ppizarror/pygame-menu#configuration-values).

    Example:

    ```python
    def change_color_bg(value, c=None, **kwargs):
        """
        Change background color.
        """
        color, _ = value
        if c == (-1, -1, -1):  # If random color
            c = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
        if kwargs['write_on_console']:
            print('New background color: {0} ({1},{2},{3})'.format(color, *c))
        COLOR_BACKGROUND[0] = c[0]
        COLOR_BACKGROUND[1] = c[1]
        COLOR_BACKGROUND[2] = c[2]

    def reset_timer():
        """
        Reset timer function.
        """
        ...

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
                            write_on_console=True # Optional change_color_bg param
                            )

    timer_menu.add_option('Reset timer', reset_timer)
    timer_menu.add_option('Return to Menu', pygameMenu.events.MENU_BACK)
    timer_menu.add_option('Close Menu', pygameMenu.events.MENU_CLOSE)
    ```

- *add_text_input(title, textinput_id, default, input_type, input_underline, maxchar, maxwidth, align, enable_selection, onchange, onreturn, \*\*kwargs)*

    Add a *text input* to menu: several options with values and two functions that execute when updating the text in the text entry and pressing *Return key* on the element.

    | Param | Description | Type | Default |
    | :--: | :-- | :--: | :--: |
    | title | Label string on menu entry | str | *Required* |
    | textinput_id | Text input identificator | str | "" |
    | default | Default value to display | str | "" |
    | input_type | Data type of the input | str | locals.INPUT_TEST |
    | input_underline | Char underline of the input | str | "" |
    | maxchar | Maximum length of string, if 0 there's no limit | int | 0 |
    | maxwidth | Maximum size of the text widget, if 0 there's no limit | int | 0 |
    | align | Text input alignment | str | locals.ALIGN_CENTER |
    | font_size | Font size widget (overrides Menu default) | int | Menu *font_size* default |
    | enable_selection | Enables text selection | bool |
    | password | Input is displayed as a password | bool | False |
    | onchange | Function that executes when change the value of text input | function | None |
    | onreturn | Function that executes when pressing return button | function | None |
    | **kwargs | Additional arguments | - | - |

    Check possible alignment or data type in [configuration](https://github.com/ppizarror/pygame-menu#configuration-values).

    Example:

    ```python
    def check_name_test(value):
        """
        This function tests the text input widget.
        :param value: The widget value
        :return: None
        """
        print('User name: {0}'.format(value))

    settings_menu = pygameMenu.Menu(...)

    # Add text input
    settings_menu.add_text_input('First name: ', default='John', onreturn=check_name_test)
    settings_menu.add_text_input('Last name: ', default='Rambo', maxchar=10)
    settings_menu.add_text_input('Some long text: ', maxwidth=15)

    settings_menu.add_option('Return to main menu', pygameMenu.events.MENU_BACK)
    ```

- *add_line(text)*

    Adds a new line on **TextMenu** object.

    Example:

    ```python
    HELP = ['Press ESC to enable/disable Menu',
            'Press ENTER to access a Sub-Menu or use an option',
            'Press UP/DOWN to move through Menu',
            'Press LEFT/RIGHT to move through Selectors']

    menu_help = pygameMenu.TextMenu(...)
    for line in HELP:
        menu_help.add_line(line) # Add line
    ...

    menu_help.add_option('Return to Menu', pygameMenu.events.MENU_BACK)
    ```

- *clear()*

    Full reset and clear all the widgets.

    ```python
    menu = pygameMenu.Menu(...)
    menu.clear()
    ```

- *disable(closelocked)*

    Disable Menu (doest check events and draw on surface). If *closelocked* is *True* all the locked pened submenus are closed too.

    ```python
    menu = pygameMenu.Menu(...)
    menu.disable()
    ```

- *draw()*

    Draw Menu on surface.

    ```python
    menu = pygameMenu.Menu(...)
    menu.disable()
    ```

- *enable()*

    Enable Menu (can check events and draw).

    ```python
    menu = pygameMenu.Menu(...)
    menu.enable()
    ```

- *full_reset()*

    Reset the menu back to the origin.

    ```python
    menu = pygameMenu.Menu(...)
    menu.full_reset()
    ```

- *get_fps()*

    Get the current frames per second of the Menu.

    ```python
    fps = main_menu.get_fps() # -> 60.0
    ```

- *get_input_data(recursive=False, depth=0)*

    Get input data from a menu. The results are given as a dict object, keys are the ID of each element.
    If recursive, the data will contain inputs from sub-menus; *depth* defines the depth of each input. It's used only as a informative value by now.

    ```python
    menu = pygameMenu.Menu(...)
    menu.get_input_data() # -> {'id1': value, 'id2': value}
    ```

- *get_position()*

    Returns menu position as a tuple *(x1, y1, x2, y2)*, where *(x1, y1)* is the top-left position and *(x2, y2)* is the bottom-right position.

    ```python
    menu = pygameMenu.Menu(...)
    menu.get_position() # -> (50, 100, 500, 500)
    ```

- *get_title()*

    Get the title of the menu.

    ```python
    menu = pygameMenu.Menu(..., title='Menu title', ...)
    menu.get_title() # -> 'Menu title'
    ```

- *get_widget(widget_id, recursive=False)*

    Get widget object from its ID.

    ```python
    menu = pygameMenu.Menu(...)
    menu.get_widget('id1') # -> <pygameMenu.widgets.textinput.TextInput object at 0x10ac2db38>
    ```

- *is_disabled()*

    Check if the menu is disabled.

    ```python
    menu = pygameMenu.Menu(...)
    menu.disable()
    menu.is_disabled() # -> True
    ```

- *is_enabled()*

    Check if the menu is enabled.

    ```python
    menu = pygameMenu.Menu(...)
    menu.disable()
    menu.is_enabled() # -> False
    ```

- *mainloop(events=None)*

    Main loop of menu, on this function Menu can handle exceptions and draw. If parameter **dopause** is enabled then Menu pauses application and checks Events.

    ```python
    menu = pygameMenu.Menu(...)

    # Main aplication
    while True:

        # Application events
        events = pygame.event.get()

        # Menu loop (If onpause is enabled then an infinite-loop is triggered on this line)
        menu.mainloop(events)
    ```

- *reset(total)*

    Reset the menu (back) a certain number of times (*total*).

    ```python
    menu = pygameMenu.Menu(...)
    menu.reset(1) # Back
    ```

- *set_fps(fps, recursive=True)*

    Set the fps limit of the menu, if *recursive* is True the limit is applied to all submenus.

    ```python
    menu = pygameMenu.Menu(...)
    menu.set_fps(30, True)
    ```

- *set_sound(sound, recursive=False)*

    Adds a sound engine to the menu, if *recursive* the sound is applied to all submenus.

    ```python
    sound = pygameMenu.sound.Sound()
    ...

    menu = pygameMenu.Menu(...)
    menu.set_sound(sound, True)
    ```

### Menu events

| Event | Description |
| :--: | :-- |
| BACK | Go back on menu|
| CLOSE | Close menu|
| DISABLE_CLOSE | Disable close menu|
| EXIT | Close application
| RESET | Reset menu |

This events must be imported from *pygameMenu.events*.

### Sounds

A basic sound engine can be created using *Sound* class imported from *pygameMenu.sound*. The sound engine can be customized setting a sound file to several sounds defined by a type. For example, buttons or keys.

- **Sound**

    This class creates a basic sound engine.

    ```python
    pygameMenu.sound.Sound(uniquechannel, frequency, size, channels, buffer, devicename, allowedchanges)
    ```

    Parameters are the following:

    | Param | Description | Type | Default |
    | :--: | :-- | :--: | :--: |
    | uniquechannel | Force the channel to be unique, this is setted at the moment of creation of the object | bool | True |
    | frequency | Frequency of sounds | int | 22050 |
    | size | Size of sample | int | -16 |
    | channels | Number of channels by default | int | 2 |
    | buffer | Buffer size | int | 4096 |
    | devicename | Device name | str | "" |
    | allowedchanges | Convert the samples at runtime | int | 0 |

- *get_channel()*

    Get the channel of the sound engine.

    ```python
    sound = pygameMenu.sound.Sound(...)
    sound.get_channel() # -> <Channel object at 0x0000023AC8EA2CF0>
    ```

- *get_channel_info()*

    Get the current channel information of the sound engine.

    ```python
    sound = pygameMenu.sound.Sound(...)
    sound.get_channel_info() # -> {'busy': 0, 'endevent': 0, 'queue': None, 'sound': None, 'volume': 1.0}
    ```

- *load_example_sounds(volume=0.5)*

    Load the example sounds provided by the package.

    ```python
    sound = pygameMenu.sound.Sound(...)
    sound.load_example_sounds()
    ```

- *pause()*

    Pause the current channel.

- *set_sound(sound, file, volume, loops, maxtime, fade_ms)*

    Set a sound file to a sound type.

    | Param | Description | Type | Default |
    | :--: | :-- | :--: | :--: |
    | sound | Sound type | str | - |
    | file | Sound file | str | - |
    | volume | Volume of the sound | float | 0.5 |
    | loops | Number of loops of the sound | int | 0 |
    | maxtime | Max playing time of the sound | int | 0 |
    | fade_ms | Fading ms | int | 0 |

    Sounds types are the following:

    | Type | Description |
    | :--: | :-- |
    | SOUND_TYPE_CLICK_MOUSE | Mouse click |
    | SOUND_TYPE_CLOSE_MENU | A menu is closed |
    | SOUND_TYPE_ERROR | Generic error |
    | SOUND_TYPE_EVENT | Generic event |
    | SOUND_TYPE_EVENT_ERROR | Error generated by user |
    | SOUND_TYPE_KEY_ADDITION | User type a key |
    | SOUND_TYPE_KEY_DELETION | User deletes with a key |
    | SOUND_TYPE_OPEN_MENU | A menu is opened |

    ```python
    sound = pygameMenu.sound.Sound()
    sound.set_sound(pygameMenu.sound.SOUND_TYPE_ERROR, None) # Disable a sound
    sound.set_sound(pygameMenu.sound.SOUND_TYPE_OPEN_MENU, 'C:/.../example.ogg')
    ```

- *stop()*

    Stop the current channel.

- *unpause()*

    Unpause the current channel.

### Configuration values

The different configuration values must be loaded from *pygameMenu.locals*.

#### Alignment

- ALIGN_CENTER
- ALIGN_LEFT
- ALIGN_RIGHT

#### Data type

- INPUT_FLOAT
- INPUT_INT
- INPUT_TEXT

#### Shadow position

- POSITION_NORTHWEST
- POSITION_NORTH
- POSITION_NORTHEAST
- POSITION_EAST
- POSITION_SOUTHEAST
- POSITION_SOUTH
- POSITION_SOUTHWEST
- POSITION_WEST

### Using fonts

Also this library has some fonts to use, to load a font run this code:

```python
import pygameMenu

fontdir = pygameMenu.font.FONT_NAME
some_menu = pygameMenu.Menu(surface,
                            font=fontdir,
                            ...
                            )
```

Available embedded fonts (*FONT_NAME*):

- **8BIT**
- **BEBAS**
- **COMIC_NEUE**
- **FRANCHISE**
- **HELVETICA**
- **MUNRO**
- **NEVIS**
- **OPEN_SANS**
- **PT_SERIF**

System fonts can also be used. Available system fonts can be listed using the following command in a python shell:

```python
import pygame
print(pygame.font.get_fonts())
```

## Other configurations

Default parameters of *Menu* and *TextMenu* are stored on the following files:

| File | Description |
| :--: | :-- |
| pygameMenu.config | Configure default parameter of Menu and TextMenu class |
| pygameMenu.controls | Configure default key-events of Menus and widgets |

## Examples

To run the examples simply execute this commands in a terminal:

```bash
py -m pygameMenu.examples.game_selector
py -m pygameMenu.examples.multi_input
py -m pygameMenu.examples.timer_clock
```

Also, examples can be imported as follows:

```python
from pygameMenu.examples.example import main
main()
```

## Author

[Pablo Pizarro R.](https://ppizarror.com) | 2017-2020

### Contributors

Special greetings to:

- [anxuae](https://github.com/anxuae)

## License

This project is licensed under MIT [https://opensource.org/licenses/MIT/](https://opensource.org/licenses/MIT/)

[![Run on Repl.it](https://repl.it/badge/github/ppizarror/pygame-menu)](https://repl.it/github/ppizarror/pygame-menu)