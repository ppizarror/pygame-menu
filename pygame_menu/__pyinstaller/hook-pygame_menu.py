"""
pygame-menu
https://github.com/ppizarror/pygame-menu

PYGAME-MENU HOOK
Used by Pyinstaller.
"""

from pathlib import Path

# noinspection PyProtectedMember
from pygame_menu import __file__ as pygame_menu_main_file

# Get pygame_menu's folder
pygame_menu_folder = Path(pygame_menu_main_file).resolve().parent

# datas is the variable that pyinstaller looks for while processing hooks
datas = []


# A helper to append the relative path of a resource to hook variable - datas
def _append_to_datas(file_path: str, target_folder: str, base_target_folder: Path,
                     relative: bool = True) -> None:
    """
    Add path to datas.

    :param file_path: File path
    :param target_folder: Folder to paste the resources. If empty uses the containing folder of the file as ``base_target_folder+target_folder``
    :param base_target_folder: Base folder of the resource
    :param relative: If ``True`` append ``pygame_menu_folder``
    """
    global datas
    if relative:
        res_path = pygame_menu_folder / file_path
    else:
        res_path = Path(file_path)
    if target_folder == '':
        target_folder = res_path.parent.name
    if res_path.exists():
        datas.append(
            (str(res_path), str(base_target_folder / target_folder))
        )


# Append data
from pygame_menu.font import FONT_EXAMPLES
from pygame_menu.baseimage import IMAGE_EXAMPLES
from pygame_menu.sound import SOUND_EXAMPLES

pygame_menu_resources = Path('pygame_menu') / 'resources'
for f in FONT_EXAMPLES:
    _append_to_datas(f, target_folder='', base_target_folder=pygame_menu_resources)
for f in IMAGE_EXAMPLES:
    _append_to_datas(f, target_folder='', base_target_folder=pygame_menu_resources)
for f in SOUND_EXAMPLES:
    _append_to_datas(f, target_folder='', base_target_folder=pygame_menu_resources)
