
==========================
Migration Guide - v2 to v3
==========================
    
- Removed from library
    - Renamed library ``pygameMenu`` to ``pygame_menu``
    - Removed all configuration variables from ``pygameMenu.config``.
    - Removed ``TextMenu``, use ``Menu`` and ``add_label()`` method instead
- New Menu behaviour
    - Menu manage the event loop and drawing using ``Menu.mainloop(surface,bgfun,disable_loop=False,fps_limit=0)``
    - User's application manage the event loop, using ``Menu.update(events)` and `Menu.draw(surface)``
- Removed from Menu class
    - ``add_option()``, use ``add_button()`` instead
    - ``set_fps()``, use ``fps_limit`` from ``mainloop()`` instead
    - Constructor parameters:
        - ``bgfun``, now this function is required by ``Menu.mainloop()``
        - ``color_selected``, moved to ``selection_color`` of :py:class:`pygame_menu.themes.Theme`
        - ``dopause``, now user can control this behaviour using ``update()`` or ``mainloop()``
        - ``draw_region_x``, moved to ``widget_offset`` of :py:class:`pygame_menu.themes.Theme`
        - ``draw_region_y``, moved to ``widget_offset`` of :py:class:`pygame_menu.themes.Theme`
        - ``draw_select``, moved to ``widget_selection_effect`` of :py:class:`pygame_menu.themes.Theme`
        - ``font_color``, moved to ``widget_font_color`` of :py:class:`pygame_menu.themes.Theme`
        - ``font_size_title``, moved to ``title_font_size`` of :py:class:`pygame_menu.themes.Theme`
        - ``font_size``, moved to ``widget_font_size`` of :py:class:`pygame_menu.themes.Theme`
        - ``font_title``, moved to ``title_font`` of :py:class:`pygame_menu.themes.Theme`
        - ``font``, moved to ``widget_font`` of :py:class:`pygame_menu.themes.Theme`
        - ``fps``, use ``fps_limit`` from ``mainloop()`` instead
        - ``menu_alpha``, now each color of :py:class:`pygame_menu.themes.Theme` can be defined with opacity
        - ``menu_color_title``, moved to ``title_background_color`` of :py:class:`pygame_menu.themes.Theme`
        - ``menu_color``, moved to ``background_color`` of :py:class:`pygame_menu.themes.Theme`
        - ``menu_height``, use ``height``
        - ``menu_width``, use ``height``
        - ``option_margin``, moved to ``widget_margin`` of :py:class:`pygame_menu.themes.Theme`
        - ``option_shadow_offset``, moved to ``widget_shadow_offset`` of :py:class:`pygame_menu.themes.Theme`
        - ``option_shadow_position``, moved to ``widget_shadow_position`` of :py:class:`pygame_menu.themes.Theme`
        - ``option_shadow``, moved to ``widget_shadow`` of :py:class:`pygame_menu.themes.Theme`
        - ``rect_width``, now change selection effect from :py:class:`pygame_menu.themes.Theme`
        - ``surface``, now pygame surface is only required by ``mainloop()`` and ``update()``
        - ``title_offsetx``, moved to ``title_offset`` of :py:class:`pygame_menu.themes.Theme`
        - ``title_offsety``, moved to ``title_offset`` of :py:class:`pygame_menu.themes.Theme`
        - ``window_width`` and ``window_height`` parameters
- Renamed Menu method parameters
    - ``element_name`` and ``element`` from ``add_button()`` to ``title`` and ``action``
    - ``values`` from ``add_selector()`` to ``items``
    - ``widget_id`` from ``add_button()`` to ``button_id``