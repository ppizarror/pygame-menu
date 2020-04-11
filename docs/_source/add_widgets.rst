
==============
Adding widgets
==============

Label
-----

A label is used to display a text.

.. automethod:: pygameMenu.menu.Menu.add_label

**Example:**

.. code-block:: python

    HELP = "Press ESC to enable/disable Menu \
        Press ENTER to access a Sub-Menu or use an option \
        Press UP/DOWN to move through Menu \
        Press LEFT/RIGHT to move through Selectors."

    menu = pygameMenu.Menu(...)
    menu.add_label(HELP)


Button
------

A button is a text that fire action when the user trigger it.

.. automethod:: pygameMenu.menu.Menu.add_button

**Example:**

.. code-block:: python

    def fun():
        print("Hello world")

    menu = pygameMenu.Menu(...)

    menu.add_button('Simple button', fun, align=pygameMenu.locals.ALIGN_LEFT)
    menu.add_button('Return to Menu', pygameMenu.events.MENU_BACK)

.. code-block:: python

    menu = pygameMenu.Menu(...)

    about_menu = pygameMenu.Menu(...)

    menu.add_button(about_menu.get_title(), about_menu)     # Adds about submenu
    menu.add_button('Exit', pygameMenu.events.MENU_EXIT)    # Adds exit function


Selector
--------

A selector gives the possibility choose a value in a list.

.. automethod:: pygameMenu.menu.Menu.add_selector

**Example:**

.. code-block:: python

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

    menu = pygameMenu.Menu(...)

    menu.add_selector('Change bgcolor',
                      # Values of selector, call to change_color_bg
                      [('Random', (-1, -1, -1)),  # Random color
                      ('Default', (128, 0, 128)),
                      ('Black', (0, 0, 0)),
                      ('Blue', COLOR_BLUE)],
                      onchange=None,
                      onreturn=change_color_bg,
                      write_on_console=True)

Text Input
----------

A text input permits to enter a string using a keyboard.

.. automethod:: pygameMenu.menu.Menu.add_text_input

**Example:**

.. code-block:: python

    def check_name_test(value):
        """
        This function tests the text input widget.
        :param value: The widget value
        :return: None
        """
        print('User name: {0}'.format(value))

    menu = pygameMenu.Menu(...)

    menu.add_text_input('First name: ', default='John', onreturn=check_name_test)
    menu.add_text_input('Last name: ', default='Rambo', maxchar=10)
    menu.add_text_input('Some long text: ', maxwidth=15)


Color Input
-----------

A color input is similar as a text input but with a limited choice of
characters to enter a RGB value of HEX decimal one. There is also a
area to display the current color.

.. automethod:: pygameMenu.menu.Menu.add_color_input

**Example:**

.. code-block:: python

    def check_color_value(value):
        """
        This function tests the color input value.
        :param value: The widget value (tuple)
        :return: None
        """
        print('New color: {0}'.format(color))

    menu = pygameMenu.Menu(...)

    menu.add_color_input('Color RGB: ', color=type='rgb', default=(255, 0, 255), onreturn=check_color_value)
    menu.add_color_input('Empty color in RGB: ', color_type='rgb', input_separator='-')
    menu.add_color_input('Color in Hex: ', color_type='hex', default='#ffaa11')
