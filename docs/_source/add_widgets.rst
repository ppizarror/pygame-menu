
==============
Adding widgets
==============



- *add_button(element_name, element, \*args)*

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
    | font_size | Font size widget (overrides Menu default) | int | Menu *font_size* |
    | option_id | Option identifier | str | "" |

    Check possible alignment in [configuration](https://github.com/ppizarror/pygame-menu#configuration-values).

    Example:

    ```python
    def fun():
        pass

    help_menu = pygameMenu.TextMenu(surface, ...)
    help_menu.add_button('Simple button', fun, align=pygameMenu.locals.ALIGN_LEFT)
    help_menu.add_button('Return to Menu', pygameMenu.events.MENU_BACK)
    ```

    Another example:

    ```python
    menu = pygameMenu.Menu(surface, ...)
    menu.add_button(timer_menu.get_title(), timer_menu)         # Adds timer submenu
    menu.add_button(help_menu.get_title(), help_menu)           # Adds help submenu
    menu.add_button(about_menu.get_title(), about_menu)         # Adds about submenu
    menu.add_button('Exit', pygameMenu.events.MENU_EXIT)        # Adds exit function
    ```

- *add_selector(title, values, selector_id, default, align, font_size, onchange, onreturn, \*\*kwargs)*

    Adds a *selector* to the menu: several options with values and two functions that are executed when the selector is changed left/right (**onchange**) or *Return key* is pressed on the element (**onreturn**).

    | Param | Description | Type | Default |
    | :--: | :-- | :--: | :--: |
    | title | String on menu entry | str | *Required* |
    | values | Value list, list of tuples | list | *Required* |
    | selector_id | Selector identification | str | "" |
    | default | Default index of the displayed option | int | 0 |
    | align | Widget alignment | str | locals.*ALIGN_CENTER* |
    | font_size | Font size widget (overrides Menu default) | int | Menu *font_size* |
    | onchange | Function executed when changing the value of selector | function | None |
    | onreturn | Function executed when pressing return button on selected item | function | None |
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

    timer_menu.add_button('Reset timer', reset_timer)
    timer_menu.add_button('Return to Menu', pygameMenu.events.MENU_BACK)
    timer_menu.add_button('Close Menu', pygameMenu.events.MENU_CLOSE)
    ```

- *add_text_input(title, textinput_id, default, input_type, input_underline, maxchar, maxwidth, align, font_size, enable_copy_paste, enable_selection, password, onchange, onreturn, valid_chars, \*\*kwargs)*

    Adds a *text input* to menu: several options with values and two functions that execute when updating the text in the text entry and pressing the *Return key* on the element.

    | Param | Description | Type | Default |
    | :--: | :-- | :--: | :--: |
    | title | Label string on menu entry | str | *Required* |
    | textinput_id | Text input identificator | str | "" |
    | default | Default value to display | str | "" |
    | input_type | Data type of the input | str | locals.*INPUT_TEST* |
    | input_underline | Char underline of the input | str | "" |
    | maxchar | Maximum length of string, if 0 there's no limit | int | 0 |
    | maxwidth | Maximum size of the text widget, if 0 there's no limit | int | 0 |
    | align | Text input alignment | str | locals.*ALIGN_CENTER* |
    | font_size | Font size widget (overrides Menu default) | int | Menu *font_size* |
    | enable_copy_paste | Enables copy, paste and cut | bool | True |
    | enable_selection | Enables text selection | bool |
    | password | Input is displayed as a password | bool | False |
    | onchange | Function executed when changing the value of text input | function | None |
    | onreturn | Function executed when pressing return button | function | None |
    | valid_chars | List of valid characters, if None all chars are valid | list[str], None |
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

    settings_menu.add_button('Return to main menu', pygameMenu.events.MENU_BACK)
    ```

- *add_color_input(title, color_type, color_id, default, input_separator, input_underline, align, font_size, onchange, onreturn, previsualization_width, \*\*kwargs)*

    Adds a color widget with RGB or Hex format. Includes a preview box that renders the given color.

    | Param | Description | Type | Default |
    | :--: | :-- | :--: | :--: |
    | title | Label string on menu entry | str | *Required* |
    | color_type | Type of the color, can be "rgb" or "hex" | str | *Required* |
    | color_id | Color input identificator | str | "" |
    | default | Default value of the color | str (hex), tuple (r,gb,) | "" |
    | input_separator | Character used to separate channels in RGB format | str | "," |
    | input_underline | Char underline of the input | str | "" |
    | align | Text input alignment | str | locals.*ALIGN_CENTER* |
    | font_size | Font size widget (overrides Menu default) | int | config.*MENU_FONT_SIZE* |
    | onchange | Function executed when changing the value of text input | function | None |
    | onreturn | Function executed when pressing return button | function | None |
    | previsualization_width | Width of the previsualization of the color, scale of the widget height | int,float | 3 |
    | **kwargs | Additional arguments | - | - |

    Check possible alignment or data type in [configuration](https://github.com/ppizarror/pygame-menu#configuration-values).

    Example:

    ```python
    def check_color_value(value):
        """
        This function tests the color input value.
        :param value: The widget value (tuple)
        :return: None
        """
        print('New color: {0}'.format(color))

    settings_menu = pygameMenu.Menu(...)

    settings_menu.add_color_input('Color RGB: ', color=type='rgb', default=(255, 0, 255), onreturn=check_color_value)
    settings_menu.add_color_input('Empty color in RGB: ', color_type='rgb', input_separator='-')
    settings_menu.add_color_input('Color in Hex: ', color_type='hex', default='#ffaa11')
    ```

- *add_line(text)*

    Adds a new line on the **TextMenu** object.

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

    menu_help.add_button('Return to Menu', pygameMenu.events.MENU_BACK)
    ```
