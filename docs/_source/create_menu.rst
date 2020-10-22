
.. module:: pygame_menu.menu

==============
Creating menus
==============

Ready to go deeper into menu usage?

Configuring the menu
--------------------

The :py:class:`pygame_menu.Menu` is the base class to draw the graphical items on
the screen. It offers many parameters to let you adapt the behavior and the visual
aspects of the menu.

The less trivial ones are explained here.

Widgets alignment
^^^^^^^^^^^^^^^^^

By default, the widgets are centered horizontally (``widget_alignment=ALIGN_CENTER``).
All are included in a virtual rectangle positioned at 0 pixel below the title bar and
0 pixel from the left border (``widget_offset=(0, 0)``).

The widget alignment (str) can be changed with one of the following values:

==============================================  ========================
Alignment                                       Description
==============================================  ========================
:py:data:`pygame_menu.locals.ALIGN_LEFT`        Left alignment
:py:data:`pygame_menu.locals.ALIGN_CENTER`      Center alignment
:py:data:`pygame_menu.locals.ALIGN_RIGHT`       Right alignment
==============================================  ========================

In the same way, an offset can be defined for the title using the parameter
``title_offset``.

The content of the menu can be centered vertically after all widgets have
been added by calling the method :py:meth:`pygame_menu.Menu.center_content`:

.. code-block:: python
    :emphasize-lines: 6

    menu = pygame_menu.Menu(...)

    menu.add_text_input(...)
    menu.add_selector(...)
    menu.add_button(...)
    menu.center_content()


.. note:: If the menu size is insufficient to show all of the widgets, horizontal
          and/or vertical scrollbar(s) will appear automatically.

Column and row
^^^^^^^^^^^^^^

By default, the widgets are arranged in one unique column. But using the
``columns`` and ``rows`` parameters, it is possible to arrange them in
a grid.

The defined grid of ``columns`` x ``rows`` cells will be completed with
the widgets (in order of definition) **column by column** starting at the
**top-left** corner of the menu.

On-close callback
^^^^^^^^^^^^^^^^^

A callback can be defined using the ``onclose`` parameter, it will be
called when the menu (end sub-menus) is closing. This parameter can take
one of these two types of values:

 - a python callable object (a function, a method, a class, ...)
   that will be called without any arguments.
 - a specific event of :py:mod:`pygame_menu`. The possible events are
   the following:

   ===========================================  ========================================
   Event                                        Description
   ===========================================  ========================================
   :py:data:`pygame_menu.events.BACK`           Go back to the previously opened menu
   :py:data:`pygame_menu.events.DISABLE_CLOSE`  The menu can not be closed
   :py:data:`pygame_menu.events.EXIT`           Exit the program (not only the menu)
   :py:data:`pygame_menu.events.RESET`          Go back to the first opened menu
   ===========================================  ========================================


Display a menu
--------------

The :ref:`First steps` chapter shows the way to display the menu, this
method lets `pygame-menu` managing the event loop by calling the
:py:meth:`pygame_menu.Menu.mainloop` :

.. code-block:: python
    :emphasize-lines: 6

    def draw_background():
        ...

    mymenu = Menu(...)

    mymenu.mainloop(surface, bgfun=draw_background)

There is a second way that gives more flexibility to the application
because the events loop remains managed outside of the menu. In this
case the application is in charge to update and draw the menu when
it is necessary.

.. code-block:: python
    :emphasize-lines: 15,16,17

    def draw_background():
        ...

    mymenu = Menu(...)

    while True:

        draw_background()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if mymenu.is_enabled():
            mymenu.update(events)
            mymenu.draw(surface)

        pygame.display.update()


.. Document here only the members relative to the menu itself, members
.. for adding widgets are documented in another chapter.

.. autoclass:: pygame_menu.Menu
    :members:
    :exclude-members: add_button, add_color_input, add_image, add_label, add_text_input, add_selector, add_vertical_margin
