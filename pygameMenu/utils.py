import pygame as _pygame


def check_key_pressed_valid(event):
    """
    Checks if the pressed key is valid.

    :param self:
    :param event: Key press event
    :type event: pygame.event.EventType
    :return: True if a key is pressed
    :rtype: bool
    """
    # If the system detects that any key event has been pressed but
    # there's not any key pressed then this method raises a KEYUP
    # flag
    bad_event = not (True in _pygame.key.get_pressed())
    if bad_event:
        if 'test' in event.dict and event.dict['test']:
            return True
        ev = _pygame.event.Event(_pygame.KEYUP, {'key': event.key})
        _pygame.event.post(ev)
    return not bad_event
