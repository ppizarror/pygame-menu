"""
pygame-menu
https://github.com/ppizarror/pygame-menu

PYGAME-MENU HOOK
Used by Pyinstaller.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

import os

# noinspection PyProtectedMember
from pygame_menu import __file__ as pygame_menu_main_file

# Get pygame_menu's folder
pygame_menu_folder = os.path.dirname(os.path.abspath(pygame_menu_main_file))

# datas is the variable that pyinstaller looks for while processing hooks
datas = []


# A helper to append the relative path of a resource to hook variable - datas
def _append_to_datas(file_path: str, target_folder: str, base_target_folder: str = 'pygame_menu',
                     relative: bool = True) -> None:
    """
    Add path to datas.

    :param file_path: File path
    :param target_folder: Folder to paste the resources. If empty uses the containing folder of the file as ``base_target_folder+target_folder``
    :param base_target_folder: Base folder of the resource
    :param relative: If ``True`` append ``pygame_menu_folder``
    :return: None
    """
    global datas
    if relative:
        res_path = os.path.join(pygame_menu_folder, file_path)
    else:
        res_path = file_path
    if target_folder == '':
        target_folder = os.path.basename(os.path.dirname(res_path))
    if os.path.exists(res_path):
        datas.append((res_path, os.path.join(base_target_folder, target_folder)))


# Append data
from pygame_menu.font import FONT_EXAMPLES
from pygame_menu.baseimage import IMAGE_EXAMPLES
from pygame_menu.sound import SOUND_EXAMPLES

pygame_menu_resources = os.path.join('pygame_menu', 'resources')
for f in FONT_EXAMPLES:
    _append_to_datas(f, target_folder='', base_target_folder=pygame_menu_resources)
for f in IMAGE_EXAMPLES:
    _append_to_datas(f, target_folder='', base_target_folder=pygame_menu_resources)
for f in SOUND_EXAMPLES:
    _append_to_datas(f, target_folder='', base_target_folder=pygame_menu_resources)
