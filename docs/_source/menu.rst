
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
    :members: center_vertically, clear, disable, enable, full_reset, get_fps,
              get_input_data, get_position, get_title, get_widget, is_disabled,
              is_enabled, mainloop, set_fps, set_sound, 
