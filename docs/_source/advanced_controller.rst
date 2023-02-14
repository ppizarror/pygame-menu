====================
Configure controller
====================

The pygame-menu driver controller is very simple, and can be modified in two
different ways.

First, in ``pygame_menu.controls`` there are different constants to modify each
key to different events, such as apply on a widget, scroll left or right, among
others. If any constant is modified it will apply to the whole library.

   ===============================================   ===========================
   Event                                             Description
   ===============================================   ===========================
   :py:data:`pygame_menu.controls.KEY_APPLY`         Apply on widget
   :py:data:`pygame_menu.controls.KEY_BACK`          Move back on menu or widget
   :py:data:`pygame_menu.controls.KEY_CLOSE_MENU`    Close menu
   :py:data:`pygame_menu.controls.KEY_LEFT`          Move left
   :py:data:`pygame_menu.controls.KEY_MOVE_DOWN`     Move down
   :py:data:`pygame_menu.controls.KEY_MOVE_UP`       Move up
   :py:data:`pygame_menu.controls.KEY_RIGHT`         Move right
   :py:data:`pygame_menu.controls.KEY_TAB`           Apply tab
   ===============================================   ===========================

   Note: See ``pygame_menu.controls`` module for more information.

The following example changes the return key from ``RETURN`` to ``A``:

.. code-block:: python

    import pygame_menu.controls as ctrl
    ctrl.KEY_APPLY = pygame.K_a

    ...
    menu.add.button('button', lambda: print('Clicked!'))

As you might have seen, this procedure to change events is very simple, but limited.
For such reason, pygame-menu provides another way to change the controls, by using
the ``Controller`` object.

This class can be passed to widgets or menu by calling ``object.set_controller(controller)``.
Controller class defines several functions that can be overriden, or you can create
a subclass using inheritance. For example, the following example changes ``apply``
event to keys ``A``, ``B`` or ``C``, and additionally this changes the menu background
color on demand. Methods must return ``True`` if satisfy the event condition.

.. code-block:: python

    from pygame_menu.controls import Controller
    from random import randrange

    # Create a controller
    custom_controller = Controller()

    def btn_apply(event, menu_object):
        applied = event.key in (pygame.K_a, pygame.K_b, pygame.K_c)
        if applied:
            random_color = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
            menu_object.get_scrollarea().update_area_color(random_color)
        return applied

    custom_controller.apply = btn_apply

    ...
    button = menu.add.button('My button', lambda: print('Clicked!'))
    button.set_controller(custom_controller) # Pass new controller to object

.. autoclass:: pygame_menu.controls.Controller
    :members: