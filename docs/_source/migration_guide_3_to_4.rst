
==========================
Migration Guide - v3 to v4
==========================

- ``pygame_menu v4`` no longer python 2.7 to 3.5.
- Added ``__all__`` to module, then some usage cases importing with * may fail.
- All locals inner value have changed. If you used the value as-is you'll get an error.
- Menu ``add_image`` method parameter ``scale_smooth`` is now ``True`` by default.
- Menu ``clear`` method now receives ``reset`` argument.
- Menu ``mainloop``, ``update`` and ``draw`` now raises ``RuntimeError`` if it's disabled. This behaviour can be changed though Menu private property ``_runtime_errors``.
- Menu Column/Row positioning has changed, now ``column_max_width`` has a different behaviour. For setting the minimum width of columns use ``column_min_width``. Expect some minor changes to the global layout. Now is much more consistent.
- Menu constructor changed from ``Menu(height, width, title, ...)`` to  ``Menu(title, width, height, ...)``.
- Menu method ``get_width()`` changes to``get_width(inner=False, widget=False)``.
- Moved ``previsualization_width`` colorinput method to ``kwargs``.
- Removed ``column_force_fit_text`` from ``Menu`` constructor.
- Removed ``dummy_function`` from ``pygame_menu.utils``.
- Removed ``events.DISABLE_CLOSE``, use ``None`` or ``events.NONE`` instead.
- Removed ``Widget`` method ``surface_needs_update()``. Now use method ``force_menu_surface_update`` if needed.
- Renamed ``ColorInput`` constants ``TYPE_HEX``, ``TYPE_RGB``, ``HEX_FORMAT_LOWER``, ``HEX_FORMAT_NONE``, and ``HEX_FORMAT_UPPER``, to ``COLORINPUT_*``.
- Renamed ``touchscreen_enabled`` to ``touchscreen`` in ``Menu`` constructor.
- Renamed ``Widget`` method from ``set_selected(selected=True)`` to ``select(status=True, update_menu=False)``.
- Renamed Theme ``menubar_close_button`` to ``title_close_button``.
- Renamed Widget ``_force_menu_surface_update```method to ``force_menu_surface_update``.
- Renamed Widget ``expand_background_inflate_to_selection_effect`` method to ``background_inflate_to_selection_effect``.
- Widget ``selected`` property is now private. Use ``is_selected()`` to check selection status, and ``select(...)`` to modify it.
- Widget ``shadow_offset`` now cannot be ``None``, only ``int`` or ``float`` allowed.
- Widget ``sound`` property is now private. Use ``.get_sound()`` or ``.set_sound()``.
- Widget ``visible`` property is now private. Use ``.is_visible()`` to check visibility status, and ``.show()`` or ``.hide()`` to modify it.
- Widget ``VMargin`` now inherits from ``NoneWidget``.
- Widget properties ``joystick_enabled``, ``mouse_enabled``, ``touchscreen_enabled`` and ``sound`` are now private.
- Widgets now must define only ``_draw``, ``draw()`` is reserved to Widget core class only.