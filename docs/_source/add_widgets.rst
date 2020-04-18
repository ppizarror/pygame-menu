
==============
Adding widgets
==============

Add a text
----------

A label is used to display a text. If the text is too large, it
can be wrapped in order to fit the menu size.

**Example:**

.. image:: ../_static/widget_label.png
    :scale: 30%
    :align: center

.. code-block:: python

    HELP = "Press ESC to enable/disable Menu "\
           "Press ENTER to access a Sub-Menu or use an option "\
           "Press UP/DOWN to move through Menu "\
           "Press LEFT/RIGHT to move through Selectors."

    menu = pygame_menu.Menu(...)
    menu.add_label(HELP, max_char=-1, font_size=20)

.. automethod:: pygame_menu.Menu.add_label


Add an image
------------

An image can be displayed on a menu.
The ``scale`` parameter represent the scaling ratio of the image width
and height. When ``scale_smooth=True``, the rendering is better but it
requires more CPU resources.

**Example:**

.. image:: ../_static/widget_image.png
    :scale: 30%
    :align: center

.. code-block:: python

    PATH = os.path.join(os.path.dirname(pygame_menu.__file__),
                        'resources', 'images', 'pygame_menu.png')

    menu = pygame_menu.Menu(...)

    menu.add_image(PATH, angle=10, scale=(0.15, 0.15))
    menu.add_image(PATH, angle=-10, scale=(0.15, 0.15), scale_smooth=True)

.. automethod:: pygame_menu.Menu.add_image


Add a button
------------

A button is a text that fire action when the user trigger it. An action
is linked to a button by defining the `action` parameter with one of the
three values:

 - an other :py:class:`pygame_menu.Menu`, in this case, it will be displayed
   when the button is triggered.
 - a python callable object (a function, a method, a class, ...)
   that will be called with the given arguments.
 - a specific event of :py:mod:`pygame_menu`. The possible events are
   the following:

   ==========================================   ========================================
   Event                                        Description
   ==========================================   ========================================
   :py:data:`pygame_menu.events.BACK`           Go back to previously opened menu
   :py:data:`pygame_menu.events.CLOSE`          Close the menu
   :py:data:`pygame_menu.events.EXIT`           Exit the program (not only the menu)
   :py:data:`pygame_menu.events.RESET`          Go back to first opened menu
   ==========================================   ========================================

**Example:**

.. image:: ../_static/widget_button.png
    :scale: 30%
    :align: center

.. code-block:: python

    def func(name):
        print("Hello world from", name)  # name will be 'foo'

    menu = pygame_menu.Menu(...)

    about_menu = pygame_menu.Menu(...)

    menu.add_button('Exec', func, 'foo',                    # Execute a function
                    align=pygame_menu.locals.ALIGN_LEFT)
    menu.add_button(about_menu.get_title(), about_menu,     # Open a sub-menu
                    shadow=True, shadow_color=(0, 0, 100))
    menu.add_button('Exit', pygame_menu.events.EXIT,         # Link to exit action
                    align=pygame_menu.locals.ALIGN_RIGHT)

.. automethod:: pygame_menu.Menu.add_button


Add a choices list
------------------

A selector gives the possibility choose a value in a predefined list.
An item of a selector is a tuple: the first element is the text
displayed, the others are the arguments passed to the callbacks
``onchange`` and ``onreturn``.

**Example:**

.. image:: ../_static/widget_selector.png
    :scale: 30%
    :align: center

.. code-block:: python

    def change_background_color(value, surface, color):
        name, index = value
        print("Change color to", name)
        if color == (-1, -1, -1):
            # Generate a random color
            color = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
        surface.fill(color)

    menu = pygame_menu.Menu(...)

    menu.add_selector('Current color',
                      # list of (Text, parameters...)
                      [('Default', surface, (128, 0, 128)),
                       ('Black', surface, (0, 0, 0)),
                       ('Blue', surface, (0, 0, 255)),
                       ('Random', surface, (-1, -1, -1))],
                      onchange=change_background_color)

.. automethod:: pygame_menu.Menu.add_selector


Add a text entry
----------------

A text input permits to enter a string using a keyboard. Restriction
on entered characters can be set using ``input_type``, ``maxchar``,
``maxwidth`` and ``valid_chars`` parameters.

**Example:**

.. image:: ../_static/widget_textinput.png
    :scale: 30%
    :align: center

.. code-block:: python

    def check_name(value):
        print('User name:', value)

    menu = pygame_menu.Menu(...)

    menu.add_text_input('First name: ', default='John', onreturn=check_name)
    menu.add_text_input('Last name: ', default='Doe', maxchar=20)
    menu.add_text_input('Password: ', input_type=pygame_menu.locals.INPUT_INT, password=True)

.. automethod:: pygame_menu.Menu.add_text_input


Add a color entry
-----------------

A color input is similar as a text input but with a limited choice of
characters to enter a RGB value of HEX decimal one. There is also a
area to show the current color. By default the RGB integers separator
is a comma (``,``).

**Example:**

.. image:: ../_static/widget_colorinput.png
    :scale: 30%
    :align: center

.. code-block:: python

    def check_color(value):
        print('New color:', value)

    menu = pygame_menu.Menu(...)

    menu.add_color_input('RGB color 1: ', color_type='rgb', default=(255, 0, 255), onreturn=check_color, font_size=18)
    menu.add_color_input('RGB color 2: ', color_type='rgb', input_separator='-', font_size=18)
    menu.add_color_input('HEX color 3: ', color_type='hex', default='#ffaa11', font_size=18)

.. automethod:: pygame_menu.Menu.add_color_input


Add a vertical spacer
---------------------

A vertical spacer can be added between two widgets to have a better
visual rendering of the menu.

**Example:**

.. image:: ../_static/widget_vmargin.png
    :scale: 30%
    :align: center

.. code-block:: python

    menu = pygame_menu.Menu(...)

    menu.add_label('Text #1')
    menu.add_vertical_margin(100)
    menu.add_label('Text #2')

.. automethod:: pygame_menu.Menu.add_vertical_margin
