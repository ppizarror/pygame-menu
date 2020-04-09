
==============
Creating menus
==============

TODO: general description

.. code-block:: python

    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    surface = pygame.display.set_mode((400, 600))

    menu = pygameMenu.Menu(surface,
                           pygameMenu.font.FONT_BEBAS,
                           "My first menu")

    while True:

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        menu.mainloop(events)

        # Flip surface
        pygame.display.flip()


.. module:: pygameMenu.menu

.. autoclass:: Menu(...)
    :members:
