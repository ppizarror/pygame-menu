
.. module:: pygameMenu.menu

==============
Creating menus
==============

Ready to go deeper in menu usage?

Configuring the menu
--------------------

The :py:class:`Menu` is the base class to draw the graphical items on
the screen. It offers many parameters to lets you adapt the behavior
and visual aspect of the menu.

The less trivial are explain here.


Execute a menu
--------------

The :ref:`First steps` chapter show the way to execute the menu in the
application which let's `pygame-menu` managing the event loop by calling
the :py:meth:`Menu.mainloop` :

.. code-block:: python
    :emphasize-lines: 6

    def draw_background():
        ...

    mymenu = Menu(...)

    mymenu.mainloop(surface, bgfun=draw_background)

There is a second way that let's more flexibility to the application
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
.. for adding widgets are documented in an other chapter.

.. autoclass:: Menu(surface, menu_height, menu_width, font, title, ...)
    :members:
    :exclude-members: add_button, add_color_input, add_label, add_text_input, add_selector, add_vertical_margin
